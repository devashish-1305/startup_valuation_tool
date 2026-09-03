# Startup Valuation & Analysis Tool

Full-stack valuation app: public-company DCF + ML peer clustering, and early-stage startup methods (Berkus, Scorecard, Risk Factor, Cost-to-Duplicate, VC Method).

## Quick start (interview demo)

### 1. Backend (FastAPI)

```bash
cd /path/to/startup_valuation_tool
source venv/bin/activate   # or: ./venv/bin/python
uvicorn api:app --reload --port 8000
```

Health check: http://127.0.0.1:8000/api/health

### 2. Frontend (React + Vite)

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000 (Vite proxies `/api` → port 8000).

### 3. Refresh data (without Airflow UI)

```bash
./scripts/run_pipeline.sh
```

This fetches FMP + yFinance + SEC, cleans, merges, and loads `financials.db`.

## Data pipeline notes

- Airflow DAG: `airflow/dags/data_pipeline_dag.py` (paths resolve from the project root automatically).
- FMP uses the **stable** API (`/stable/...`) — legacy `/api/v3/...` endpoints are blocked for new keys.
- Tickers: AAPL, GOOGL, MSFT, AMZN, TSLA, NVDA, META, NFLX.

## Stack

Python, FastAPI, React, TypeScript, Vite, Apache Airflow, SQLite, MongoDB, Scikit-learn, XGBoost.
