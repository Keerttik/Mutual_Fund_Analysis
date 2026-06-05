import json
import re
from pathlib import Path
# pyrefly: ignore [missing-import]
from bs4 import BeautifulSoup

RAW_DATA_DIR = Path("data/raw")
PROCESSED_DATA_DIR = Path("data/processed")

def clean_html(soup: BeautifulSoup):
    for element in soup(["nav", "footer", "script", "style", "noscript", "svg", "iframe", "header"]):
        element.extract()
    return soup

def extract_metrics(soup: BeautifulSoup) -> dict:
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

    return metrics

def extract_sections(soup: BeautifulSoup) -> dict:
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
            
    return sections

def process_file(filepath: Path):
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()
        
    soup = BeautifulSoup(html, "html.parser")
    soup = clean_html(soup)
    
    scheme_id = filepath.stem.split("_")[0]
    
    metrics = extract_metrics(soup)
    sections = extract_sections(soup)
    
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

if __name__ == "__main__":
    main()
