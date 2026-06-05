import json
from unittest.mock import patch, mock_open, MagicMock
from src.ingestion.chunk import chunk_data

@patch("src.ingestion.chunk.PROCESSED_DATA_DIR")
def test_chunk_data(mock_dir):
    # Setup mock files
    mock_file = MagicMock()
    mock_file.name = "hdfc-small-cap.json"
    mock_dir.glob.return_value = [mock_file]
    
    mock_json = {
        "scheme_id": "hdfc-small-cap",
        "metrics": {"Expense ratio": "0.5%"},
        "sections": {
            "fund_management": "Manager A handles this fund. " * 50
        }
    }
    
    # Mock file read and write
    m_open = mock_open(read_data=json.dumps(mock_json))
    with patch("builtins.open", m_open):
        with patch("json.dump") as mock_dump:
            chunk_data()
            
            # Verify json dump was called
            assert mock_dump.called
            
            # Extract arguments passed to json.dump
            dump_args = mock_dump.call_args[0]
            chunks = dump_args[0]
            
            # Check length of chunks (1 metrics + multiple for fund_management)
            assert len(chunks) > 1
            
            # Verify metadata
            for chunk in chunks:
                assert "metadata" in chunk
                assert "scheme_id" in chunk["metadata"]
                assert chunk["metadata"]["scheme_id"] == "hdfc-small-cap"
                assert chunk["page_content"] != ""
