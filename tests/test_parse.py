import pytest
import os
import tempfile
import json
from pathlib import Path
from bs4 import BeautifulSoup
from src.ingestion.parse import extract_sections, extract_metrics, process_file

def test_extract_sections_empty_elements():
    html_content = """
    <h2>Expense Ratio</h2>
    <p>0.5% per annum</p>
    <h2>Exit Load</h2>
    <div></div>
    <p></p>
    <h2>Fund Management</h2>
    <div>John Doe manages this fund</div>
    """
    soup = BeautifulSoup(html_content, "html.parser")
    sections = extract_sections(soup)
    
    assert "expense_ratio" in sections
    assert sections["expense_ratio"] == "0.5% per annum"
    
    # Exit load is empty, shouldn't be populated or should just be an empty string/missing
    # Actually if it's empty, extract_sections might store an empty string, but it won't crash
    if "exit_load" in sections:
        assert sections["exit_load"] == ""

    assert "fund_management" in sections
    assert sections["fund_management"] == "John Doe manages this fund"

def test_extract_metrics_fallback():
    html_content = """
    <div>
        <div>Expense Ratio</div>
        <div class="value">1.2%</div>
    </div>
    """
    soup = BeautifulSoup(html_content, "html.parser")
    metrics = extract_metrics(soup)
    
    assert metrics.get("Expense ratio") == "1.2%"

def test_process_file(monkeypatch):
    # Mock PROCESSED_DATA_DIR
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        monkeypatch.setattr("src.ingestion.parse.PROCESSED_DATA_DIR", tmp_path)
        
        # Create dummy HTML file
        raw_file = tmp_path / "hdfc-dummy_123.html"
        raw_file.write_text("<h2>Overview</h2><p>This is a dummy fund.</p>")
        
        data = process_file(raw_file)
        
        assert data["scheme_id"] == "hdfc-dummy"
        assert "overview" in data["sections"]
        assert data["sections"]["overview"] == "This is a dummy fund."
        
        # Check that it saved the json
        saved_file = tmp_path / "hdfc-dummy.json"
        assert saved_file.exists()
        saved_data = json.loads(saved_file.read_text())
        assert saved_data["scheme_id"] == "hdfc-dummy"

def test_main(monkeypatch):
    from src.ingestion.parse import main
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        monkeypatch.setattr("src.ingestion.parse.RAW_DATA_DIR", tmp_path)
        monkeypatch.setattr("src.ingestion.parse.PROCESSED_DATA_DIR", tmp_path / "processed")
        
        # Test empty
        main()
        
        # Test with files
        f1 = tmp_path / "hdfc-test_100.html"
        f1.write_text("<h2>Test</h2>")
        main()
        
        # Processed should exist
        assert (tmp_path / "processed" / "hdfc-test.json").exists()
