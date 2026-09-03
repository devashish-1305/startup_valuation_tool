#!/bin/bash
# Refresh financial data without needing the Airflow UI.
# Usage (from project root): ./scripts/run_pipeline.sh
set -euo pipefail
cd "$(dirname "$0")/.."

PYTHON="./venv/bin/python"
if [ ! -x "$PYTHON" ]; then
  PYTHON="python3"
fi

echo "=== 1/6 Fetch raw data ==="
"$PYTHON" scripts/fetching/fetch_all_raw.py

echo "=== 2/6 Clean FMP ==="
"$PYTHON" scripts/cleaning/clean_fmp.py

echo "=== 3/6 Clean SEC ==="
"$PYTHON" scripts/cleaning/clean_sec.py

echo "=== 4/6 Clean yFinance ==="
"$PYTHON" scripts/cleaning/clean_yfinance.py

echo "=== 5/6 Merge ==="
"$PYTHON" scripts/integration/merge_company_data.py

echo "=== 6/6 Load SQLite ==="
"$PYTHON" scripts/integration/db_push.py

echo "✅ Pipeline complete. financials.db is ready."
