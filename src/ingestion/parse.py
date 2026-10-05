import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

RAW_DATA_DIR = Path("data/raw")
PROCESSED_DATA_DIR = Path("data/processed")

def clean_html(soup: BeautifulSoup):
    for element in soup(["nav", "footer", "script", "style", "noscript", "svg", "iframe", "header"]):
        element.extract()
    return soup

def extract_next_data(soup: BeautifulSoup) -> dict:
    """Extract structured server-side data from Next.js __NEXT_DATA__ script tag if available."""
    script_elem = soup.find("script", id="__NEXT_DATA__")
    if not script_elem or not script_elem.string:
        return {}
    try:
        data = json.loads(script_elem.string)
        return data.get("props", {}).get("pageProps", {}).get("mfServerSideData", {})
    except Exception as e:
        print(f"Warning: Failed to parse __NEXT_DATA__: {e}")
        return {}

def extract_metrics(soup: BeautifulSoup, mf_data: dict = None) -> dict:
    metrics = {}
    labels = ["NAV", "Min. for SIP", "Fund size (AUM)", "Expense ratio", "Rating"]
    
    for label in labels:
        label_elem = soup.find(string=re.compile(label, re.IGNORECASE))
        if label_elem and label_elem.parent:
            # 1. Try to find the parent container structure
            parent_div = label_elem.parent.find_parent("div", class_=re.compile("fundDetails_gap4", re.I))
            if parent_div:
                value_div = parent_div.find("div", class_=re.compile("bodyXLargeHeavy", re.I))
                if value_div:
                    metrics[label] = value_div.get_text(strip=True)
                    continue
                    
            # 2. Fallback: try next sibling or next element
            next_sibling = label_elem.parent.find_next_sibling()
            if next_sibling:
                metrics[label] = next_sibling.get_text(strip=True)
                continue
                
            # 3. Fallback: looking for text in next elements
            next_elem = label_elem.parent.find_next()
            if next_elem:
                metrics[label] = next_elem.get_text(strip=True)

    # Augment/fill from Next.js server side data if available
    if mf_data:
        if mf_data.get("nav") and not metrics.get("NAV"):
            date_str = f" as of {mf_data['nav_date']}" if mf_data.get("nav_date") else ""
            metrics["NAV"] = f"₹{mf_data['nav']}{date_str}"
        if mf_data.get("min_sip_investment") and not metrics.get("Min. for SIP"):
            metrics["Min. for SIP"] = f"₹{mf_data['min_sip_investment']}"
        if mf_data.get("expense_ratio") and not metrics.get("Expense ratio"):
            metrics["Expense ratio"] = f"{mf_data['expense_ratio']}%"
        if mf_data.get("groww_rating") and not metrics.get("Rating"):
            metrics["Rating"] = str(mf_data["groww_rating"])
        if mf_data.get("benchmark") or mf_data.get("benchmark_name"):
            metrics["Benchmark"] = mf_data.get("benchmark_name") or mf_data.get("benchmark")
        
        # Additional key metrics
        risk = mf_data.get("risk") or (mf_data.get("return_stats", [{}])[0].get("risk") if mf_data.get("return_stats") else None)
        if risk:
            metrics["Riskometer"] = risk
        if mf_data.get("exit_load"):
            metrics["Exit Load"] = mf_data.get("exit_load")
        if mf_data.get("amc"):
            metrics["Fund House"] = mf_data.get("amc")

    return metrics

def extract_sections(soup: BeautifulSoup, mf_data: dict = None, scheme_name: str = "") -> dict:
    sections = {}
    
    section_mappings = {
        "expense_ratio": ["Expense Ratio", "Expense", "Charges"],
        "exit_load": ["Exit Load"],
        "minimum_investment": ["Minimum Investment", "Investment details", "SIP"],
        "benchmark": ["Benchmark", "Index"],
        "fund_management": ["Fund Management", "Fund Managers", "Fund manager"],
        "investment_objective": ["Investment Objective", "Objective", "Strategy"],
        "fund_house": ["Fund House", "About AMC", "AMC details", "About HDFC"],
        "overview": ["Overview", "About this fund", "About"]
    }
    
    headings = soup.find_all(['h2', 'h3', 'h4'])
    
    for heading in headings:
        heading_text = heading.get_text(strip=True)
        matched_section = None
        
        for key, possible_texts in section_mappings.items():
            for text in possible_texts:
                if text.lower() in heading_text.lower():
                    matched_section = key
                    break
            if matched_section:
                break
                
        if matched_section:
            # Collect all siblings until the next heading
            content = []
            curr = heading.find_next_sibling()
            while curr and curr.name not in ['h1', 'h2', 'h3', 'h4']:
                # Clean up text by separating with space
                text = curr.get_text(separator=" ", strip=True)
                if text:
                    content.append(text)
                curr = curr.find_next_sibling()
                
            sections[matched_section] = "\n".join(content).strip()

    # Fill missing or sparse sections with high-fidelity server data
    if mf_data:
        fund_title = mf_data.get("fund_name") or mf_data.get("scheme_name") or scheme_name
        bench_name = mf_data.get("benchmark_name") or mf_data.get("benchmark") or ""
        bench_code = mf_data.get("benchmark") or ""
        bench_display = f"{bench_name} ({bench_code})" if (bench_name and bench_code and bench_name != bench_code) else (bench_name or bench_code)
        
        if bench_display and not sections.get("benchmark"):
            sections["benchmark"] = f"The benchmark index for {fund_title} is {bench_display}."

        risk = mf_data.get("risk") or (mf_data.get("return_stats", [{}])[0].get("risk") if mf_data.get("return_stats") else "Very High")
        if risk and not sections.get("riskometer"):
            sections["riskometer"] = f"The riskometer classification for {fund_title} is {risk}. It carries a {risk} risk profile as per regulatory risk-o-meter guidelines."

        exp_ratio = mf_data.get("expense_ratio")
        if exp_ratio and not sections.get("expense_ratio"):
            sections["expense_ratio"] = f"The expense ratio for {fund_title} (Direct Plan) is {exp_ratio}%."

        exit_load_val = mf_data.get("exit_load")
        if exit_load_val and (not sections.get("exit_load") or len(sections.get("exit_load", "")) < 10):
            sections["exit_load"] = exit_load_val

        min_sip = mf_data.get("min_sip_investment", 100)
        min_lump = mf_data.get("min_investment_amount", 100)
        if not sections.get("minimum_investment") or len(sections.get("minimum_investment", "")) < 10:
            sections["minimum_investment"] = f"Minimum SIP investment: ₹{min_sip}. Minimum lump sum (1st investment): ₹{min_lump}."

        category = mf_data.get("sub_category") or mf_data.get("category", "Mutual Fund")
        amc_name = mf_data.get("amc", "HDFC Mutual Fund")
        if not sections.get("overview") or len(sections.get("overview", "")) < 10:
            sections["overview"] = f"{fund_title} is an open-ended {category} scheme managed by {amc_name}. The benchmark index is {bench_display}."

        if not sections.get("fund_house") or len(sections.get("fund_house", "")) < 10:
            sections["fund_house"] = f"HDFC Mutual Fund is managed by HDFC Asset Management Company (AMC) Limited, one of India's largest and most trusted mutual fund houses."

    return sections

def create_general_faq_file():
    """Generates standard general FAQs for non-scheme queries (ELSS lock-in, statements, etc.)"""
    general_data = {
        "scheme_id": "general",
        "metrics": {},
        "sections": {
            "elss_lock_in": (
                "Equity Linked Savings Scheme (ELSS) mutual funds have a mandatory statutory lock-in period of 3 years "
                "from the date of unit allotment under Section 80C of the Income Tax Act. During this 3-year lock-in period, "
                "investments cannot be redeemed, switched, or withdrawn. For SIP investments in an ELSS fund, each monthly "
                "installment has its own individual 3-year lock-in period calculated from its respective allotment date."
            ),
            "download_statements": (
                "To download your HDFC Mutual Fund account statement or capital gains tax statement:\n"
                "1. Official Website: Visit the HDFC Mutual Fund portal (hdfcfund.com) and log in to the Investor Services section using your PAN or Folio number.\n"
                "2. RTA Consolidated Account Statement (CAS): Request an instant mailback statement through CAMS (camsonline.com) or KFintech using your registered email and PAN.\n"
                "3. Investment App: In the Groww app or web portal, go to Profile > Reports > Mutual Fund Statements or Capital Gains Report to download your statement directly."
            ),
            "taxation_rules": (
                "For Equity Mutual Funds in India: Long-Term Capital Gains (LTCG) on equity investments held for more than 12 months "
                "are taxed at 12.5% on gains exceeding ₹1.25 lakh in a financial year. Short-Term Capital Gains (STCG) on equity investments "
                "held for 12 months or less are taxed at 20%."
            )
        }
    }
    general_file = PROCESSED_DATA_DIR / "general.json"
    with open(general_file, "w", encoding="utf-8") as f:
        json.dump(general_data, f, indent=2, ensure_ascii=False)
    print(f"Generated general FAQs file -> {general_file.name}")

def process_file(filepath: Path):
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()
        
    soup = BeautifulSoup(html, "html.parser")
    
    # 1. Extract Next.js server-side JSON BEFORE stripping <script> tags
    mf_data = extract_next_data(soup)
    
    # 2. Clean HTML elements
    soup = clean_html(soup)
    
    scheme_id = filepath.stem.split("_")[0]
    scheme_name = scheme_id.replace("-", " ").title()
    
    metrics = extract_metrics(soup, mf_data)
    sections = extract_sections(soup, mf_data, scheme_name)
    
    data = {
        "scheme_id": scheme_id,
        "metrics": metrics,
        "sections": sections
    }
    
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    out_file = PROCESSED_DATA_DIR / f"{scheme_id}.json"
    
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
    print(f"Parsed {filepath.name} -> {out_file.name}")
    return data

def main():
    if not RAW_DATA_DIR.exists():
        print(f"Raw data directory {RAW_DATA_DIR} does not exist.")
        return
        
    files = list(RAW_DATA_DIR.glob("*.html"))
    if not files:
        print("No HTML files found to parse.")
        return
        
    # Group by scheme_id to only parse the latest
    latest_files = {}
    for f in files:
        parts = f.stem.rsplit("_", 1)
        if len(parts) == 2:
            scheme_id, timestamp = parts
            if scheme_id not in latest_files or timestamp > latest_files[scheme_id].stem.rsplit("_", 1)[1]:
                latest_files[scheme_id] = f
                
    for scheme_id, filepath in latest_files.items():
        process_file(filepath)

    # Also generate general FAQs file
    create_general_faq_file()

if __name__ == "__main__":
    main()
