import os
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()
USER_EMAIL = os.getenv("USER_EMAIL", "your-email@example.com")

# SEC EDGAR base URL
SEC_BASE_URL = "https://www.sec.gov"
EDGAR_SEARCH_URL = "https://www.sec.gov/cgi-bin/browse-edgar"
SAVE_DIR = "data_sources/raw/sec_edgar"

# User agent required by SEC
HEADERS = {
    'User-Agent': f'Academic Research {USER_EMAIL}',
    'Accept-Encoding': 'gzip, deflate',
    'Host': 'www.sec.gov'
}

# CIK mapping for our companies
SYMBOL_TO_CIK = {
    "META": "0001326801",
    "AMZN": "0001018724", 
    "TSLA": "0001318605",
    "MSFT": "0000789019",
    "AAPL": "0000320193",
    "NVDA": "0001045810",
    "GOOGL": "0001652044",
    "NFLX": "0001065280"
}

def fetch_sec_edgar_data(symbol):
    """Fetch latest 10-K filing for a symbol"""
    
    # Create directory
    symbol_dir = os.path.join(SAVE_DIR, symbol)
    os.makedirs(symbol_dir, exist_ok=True)
    
    # Check if already exists
    filename = f"{symbol_dir}/{symbol}_10k_latest.txt"
    if os.path.exists(filename):
        print(f" Skipping SEC EDGAR: {filename} already exists")
        return
    
    print(f" Fetching SEC EDGAR data for {symbol}...")
    
    # Get CIK
    cik = SYMBOL_TO_CIK.get(symbol)
    if not cik:
        print(f" No CIK found for {symbol}")
        return
    
    try:
        # Step 1: Get list of 10-K filings
        cik_no_zeros = cik.lstrip('0')
        params = {
            'action': 'getcompany',
            'CIK': cik_no_zeros,
            'type': '10-K',
            'count': '1',
            'output': 'atom'
        }
        
        response = requests.get(EDGAR_SEARCH_URL, params=params, headers=HEADERS)
        response.raise_for_status()
        
        # Parse XML to get filing URL
        soup = BeautifulSoup(response.content, 'xml')
        filing_href = soup.find('filing-href')
        
        if not filing_href:
            print(f" No 10-K found for {symbol}")
            return
        
        filing_url = filing_href.text
        print(f"   Found filing: {filing_url}")
        
        # Step 2: Get the filing page
        time.sleep(0.5)  # Be nice to SEC
        response = requests.get(filing_url, headers=HEADERS)
        response.raise_for_status()
        
        # Find the main document link
        soup = BeautifulSoup(response.text, 'html.parser')
        doc_table = soup.find('table', class_='tableFile')
        
        doc_url = None
        for row in doc_table.find_all('tr')[1:]:
            cells = row.find_all('td')
            if len(cells) >= 4 and '10-K' in cells[3].text:
                link = cells[2].find('a')
                if link and '.htm' in link.text:
                    doc_url = f"{SEC_BASE_URL}{link['href']}"
                    break
        
        if not doc_url:
            print(f" Could not find 10-K document")
            return
        
        # Step 3: Get the actual 10-K content
        time.sleep(0.5)
        response = requests.get(doc_url, headers=HEADERS)
        response.raise_for_status()
        
        # Extract text content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove scripts and styles
        for element in soup(['script', 'style']):
            element.decompose()
        
        # Get text
        text_content = soup.get_text()
        
        # Basic cleaning
        text_content = re.sub(r'\s+', ' ', text_content)
        text_content = text_content.strip()
        
        # Save the full 10-K text
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(text_content)
        
        print(f"   SEC EDGAR data saved to {filename}")
        
        # Save metadata
        metadata = {
            'symbol': symbol,
            'cik': cik,
            'filing_url': filing_url,
            'document_url': doc_url,
            'extraction_date': datetime.now().isoformat()
        }
        
        metadata_file = f"{symbol_dir}/{symbol}_metadata.csv"
        pd.DataFrame([metadata]).to_csv(metadata_file, index=False)
        
    except Exception as e:
        print(f" Error fetching SEC data for {symbol}: {e}")
        raise

if __name__ == "__main__":
    # Test with one symbol
    fetch_sec_edgar_data("AAPL")