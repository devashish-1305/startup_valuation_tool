from sec_edgar_downloader import Downloader
import os

def download_10k(ticker, limit=1):
    """
    Downloads the latest 10-K filings from SEC EDGAR for a given ticker.
    """
    save_dir = "sec_filings"
    downloader = Downloader(save_dir)
    
    print(f"Downloading {limit} 10-K filings for {ticker}...")
    downloader.get("10-K", ticker, amount=limit)

    filing_path = os.path.join(save_dir, ticker, "10-K")
    downloaded_files = [os.path.join(filing_path, f) for f in os.listdir(filing_path)]
    
    return downloaded_files

# Quick local test
if __name__ == "__main__":
    files = download_10k("AAPL", limit=1)
    print(f"Downloaded files:\n{files}")
