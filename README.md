# Startup Valuation & Analysis Tool

**Repo:** https://github.com/devashish-1305/startup_valuation_tool

Full-stack valuation app for:

- **Public companies** — DCF intrinsic value, XGBoost market-cap prediction, K-Means peer clusters, financials table  
- **Startups** — Berkus, Scorecard, Risk Factor, Cost-to-Duplicate, VC Method, and Run All  

> There is **no separate live web URL**. Opening the GitHub link shows the code. To use the tool, clone and run backend + frontend locally (steps below). Sample data is already in `financials.db`.

## Clone

```bash
git clone https://github.com/devashish-1305/startup_valuation_tool.git
cd startup_valuation_tool
```

## Run the app (someone else's laptop)

### 1. Backend (FastAPI) — terminal 1

```bash
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn api:app --reload --port 8000
```

Check: http://127.0.0.1:8000/api/health → `{"status":"ok"}`

### 2. Frontend (React) — terminal 2

```bash
cd frontend
npm install
npm run dev
```

Open: **http://localhost:3000**

Vite proxies `/api` → `http://127.0.0.1:8000`.

## Optional: refresh market data

Needs a `.env` in the project root:

```bash
FMP_API_KEY=your_key
SEC_EDGAR_EMAIL=your_email@example.com
MONGO_URI=            # optional; app works without Mongo
```

Then:

```bash
chmod +x scripts/run_pipeline.sh
./scripts/run_pipeline.sh
```

## Tickers included

`AAPL`, `GOOGL`, `MSFT`, `AMZN`, `TSLA`, `NVDA`, `META`, `NFLX`

## Stack

Python · FastAPI · React · TypeScript · Vite · Apache Airflow · SQLite · MongoDB · Scikit-learn · XGBoost
