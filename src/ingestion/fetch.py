import httpx
import asyncio
import yaml
import os
from datetime import datetime
from pathlib import Path

CONFIG_PATH = Path("config/corpus.yaml")
RAW_DATA_DIR = Path("data/raw")

async def fetch_url(client: httpx.AsyncClient, scheme: dict):
    url = scheme["url"]
    scheme_id = scheme["id"]
    print(f"Fetching {scheme_id} from {url}...")
    try:
        response = await client.get(url, timeout=20.0)
        response.raise_for_status()
        
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = RAW_DATA_DIR / f"{scheme_id}_{timestamp}.html"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(response.text)
            
        print(f"Saved {scheme_id} to {filename}")
        return filename
    except Exception as e:
        print(f"Error fetching {scheme_id}: {e}")
        return None

async def main():
    if not CONFIG_PATH.exists():
        print(f"Config file not found at {CONFIG_PATH}")
        return
        
    with open(CONFIG_PATH, "r") as f:
        config = yaml.safe_load(f)
        
    schemes = config.get("schemes", [])
    if not schemes:
        print("No schemes found in config.")
        return
        
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
    
    async with httpx.AsyncClient(headers=headers, follow_redirects=True) as client:
        tasks = [fetch_url(client, scheme) for scheme in schemes]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
