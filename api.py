"""
FastAPI backend for the startup valuation tool.
Exposes the same logic as the Streamlit app (SQLite, MongoDB, valuation models, ML).
Run: uvicorn api:app --reload --port 8000
"""

from __future__ import annotations

import json
import os
import sys
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Project root on sys.path (same pattern as app.py)
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

load_dotenv(PROJECT_ROOT / ".env")

from scripts.valuation.berkus_model import calculate_berkus
from scripts.valuation.cost_to_duplicate_model import calculate_cost_to_duplicate
from scripts.valuation.dcf_model import calculate_dcf
from scripts.valuation.risk_factor_model import calculate_risk_factor
from scripts.valuation.scorecard_model import calculate_scorecard
from scripts.valuation.vc_method_model import calculate_vc_method
from utils.query_utils import get_mongo_document, get_sql_data

# --- Constants (aligned with app.py) ---
CLUSTER_DEFINITIONS: dict[int, str] = {
    0: "High-Growth / Volatile Tech (e.g., META, NFLX, NVDA, TSLA)",
    1: "Unique Behemoth - Retail & Cloud (e.g., AMZN)",
    2: "Mega-Cap Tech Giants (e.g., AAPL, GOOGL, MSFT)",
}

ML_FEATURES = ["freeCashFlow", "totalDebt", "cashAndCashEquivalents", "volume"]

REGRESSION_MODEL_PATH = PROJECT_ROOT / "regression_model.joblib"
CLUSTERING_MODEL_PATH = PROJECT_ROOT / "clustering_model.joblib"
SCALER_MODEL_PATH = PROJECT_ROOT / "clustering_scaler.joblib"


# --- ML models (lazy) ---
@lru_cache(maxsize=1)
def _load_ml_bundle() -> tuple[Any, Any, Any] | tuple[None, None, None]:
    try:
        import joblib
    except ImportError:
        return None, None, None
    try:
        reg = joblib.load(REGRESSION_MODEL_PATH)
        cluster = joblib.load(CLUSTERING_MODEL_PATH)
        scaler = joblib.load(SCALER_MODEL_PATH)
        return reg, cluster, scaler
    except FileNotFoundError:
        return None, None, None


def require_ml_models() -> tuple[Any, Any, Any]:
    reg, cluster, scaler = _load_ml_bundle()
    if reg is None or cluster is None or scaler is None:
        raise HTTPException(
            status_code=503,
            detail="ML stack unavailable: install joblib (pip install joblib) and ensure "
            "regression_model.joblib, clustering_model.joblib, and clustering_scaler.joblib "
            "exist in the project root (see scripts/ml_models/train_and_save_models.py).",
        )
    return reg, cluster, scaler


# --- Helpers ---
def normalize_ticker(ticker: str) -> str:
    t = (ticker or "").strip().upper()
    if not t:
        raise HTTPException(status_code=400, detail="Ticker is required.")
    if not t.replace(".", "").isalnum():
        raise HTTPException(
            status_code=400,
            detail="Invalid ticker format. Use letters/numbers (e.g. AAPL, BRK.B).",
        )
    return t


def get_financials_df(ticker: str) -> pd.DataFrame:
    """Load financial time series from SQLite; empty if unknown ticker or missing table."""
    return get_sql_data(ticker)


def require_financials(ticker: str) -> pd.DataFrame:
    df = get_financials_df(ticker)
    if df.empty:
        raise HTTPException(
            status_code=404,
            detail=f"No financial data in SQLite for '{ticker}'. "
            "Use one of the loaded symbols (e.g. AAPL, GOOGL, MSFT, AMZN, TSLA, NVDA, META, NFLX).",
        )
    return df


def dataframe_to_records(df: pd.DataFrame) -> list[dict[str, Any]]:
    """JSON-serializable rows (ISO dates, NaN -> None)."""
    if df.empty:
        return []
    payload = json.loads(df.to_json(orient="records", date_format="iso"))
    return payload


def latest_row(df: pd.DataFrame) -> pd.Series:
    if "date" in df.columns:
        sorted_df = df.sort_values(by="date", ascending=False)
    else:
        sorted_df = df
    return sorted_df.iloc[0]


def company_info_from_sql(ticker: str, df: pd.DataFrame) -> dict[str, Any]:
    row = latest_row(df)
    mongo_doc = get_mongo_document(ticker)
    has_10k = bool(mongo_doc.get("content"))

    out: dict[str, Any] = {
        "ticker": ticker,
        "latest_date": row.get("date"),
        "close": _scalar(row.get("close")),
        "volume": _scalar(row.get("volume")),
        "shares_outstanding": _scalar(row.get("sharesOutstanding")),
        "free_cash_flow": _scalar(row.get("freeCashFlow")),
        "total_debt": _scalar(row.get("totalDebt")),
        "cash_and_cash_equivalents": _scalar(row.get("cashAndCashEquivalents")),
        "sec_filing_10k_available": has_10k,
    }
    if isinstance(out["latest_date"], pd.Timestamp):
        out["latest_date"] = out["latest_date"].isoformat()
    return out


def _scalar(v: Any) -> Any:
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return None
    if isinstance(v, (np.floating, np.integer)):
        return float(v) if isinstance(v, np.floating) else int(v)
    return v


def predict_market_cap_and_cluster(df: pd.DataFrame) -> tuple[float, int, str]:
    reg, cluster_model, scaler = require_ml_models()
    latest = latest_row(df)
    missing = [f for f in ML_FEATURES if f not in latest.index or pd.isna(latest.get(f))]
    if missing:
        raise HTTPException(
            status_code=422,
            detail=f"Missing or NaN ML features for this ticker: {missing}.",
        )
    X = pd.DataFrame([latest[ML_FEATURES].tolist()], columns=ML_FEATURES)
    predicted_mcap = float(reg.predict(X)[0])
    scaled = scaler.transform(X)
    cluster_id = int(cluster_model.predict(scaled)[0])
    description = CLUSTER_DEFINITIONS.get(
        cluster_id,
        f"Cluster {cluster_id}",
    )
    return predicted_mcap, cluster_id, description


def run_dcf_or_fail(
    ticker: str,
    growth_rate: float,
    perpetual_growth_rate: float,
    wacc: float,
) -> float:
    if wacc <= perpetual_growth_rate:
        raise HTTPException(
            status_code=422,
            detail="WACC must be greater than perpetual growth rate for a stable terminal value.",
        )
    value = calculate_dcf(ticker, growth_rate, perpetual_growth_rate, wacc)
    if value <= 0:
        raise HTTPException(
            status_code=422,
            detail="Could not compute a positive intrinsic value. Check FCF, shares outstanding, "
            "and assumptions (growth, WACC).",
        )
    return float(value)


# --- Pydantic models ---
class DcfRequest(BaseModel):
    ticker: str
    growth_rate: float = Field(..., description="FCF growth rate for years 1–5 (e.g. 0.06 for 6%)")
    perpetual_growth_rate: float = Field(..., description="Terminal perpetual growth (e.g. 0.025)")
    wacc: float = Field(..., description="Discount rate / WACC (e.g. 0.09)")


class BerkusRequest(BaseModel):
    sound_idea: float = Field(400_000, ge=0, le=500_000)
    prototype: float = Field(300_000, ge=0, le=500_000)
    management_team: float = Field(500_000, ge=0, le=500_000)
    strategic_relationships: float = Field(250_000, ge=0, le=500_000)
    product_rollout: float = Field(150_000, ge=0, le=500_000)


def _default_scorecard_factors(
    management_team: float,
    size_of_opportunity: float,
    product_technology: float,
    competitive_environment: float,
    marketing_sales: float,
    need_for_funding: float,
    other: float,
) -> dict:
    return {
        "management_team": (0.30, management_team),
        "size_of_opportunity": (0.25, size_of_opportunity),
        "product_technology": (0.15, product_technology),
        "competitive_environment": (0.10, competitive_environment),
        "marketing_sales": (0.10, marketing_sales),
        "need_for_funding": (0.05, need_for_funding),
        "other": (0.05, other),
    }


class ScorecardRequest(BaseModel):
    avg_pre_money_valuation: float = Field(2_000_000, gt=0)
    management_team: float = Field(1.25, ge=0.5, le=1.5)
    size_of_opportunity: float = Field(1.50, ge=0.5, le=1.5)
    product_technology: float = Field(1.0, ge=0.5, le=1.5)
    competitive_environment: float = Field(1.0, ge=0.5, le=1.5)
    marketing_sales: float = Field(1.0, ge=0.5, le=1.5)
    need_for_funding: float = Field(1.0, ge=0.5, le=1.5)
    other: float = Field(1.0, ge=0.5, le=1.5)


class RiskFactorRequest(BaseModel):
    avg_pre_money_valuation: float = Field(1_500_000, gt=0)
    management_risk: float = Field(250_000)
    stage_of_business: float = Field(125_000)
    competition_risk: float = Field(-250_000)


class CostToDuplicateRequest(BaseModel):
    research_and_development: float = Field(150_000, ge=0)
    software_development_salaries: float = Field(250_000, ge=0)
    physical_assets_computers: float = Field(20_000, ge=0)


class VcMethodRequest(BaseModel):
    projected_revenue_at_exit: float = Field(50_000_000, gt=0)
    industry_ps_multiple: float = Field(4.0, gt=0)
    required_roi_multiple: float = Field(20.0, gt=0)
    investment_amount: float = Field(2_000_000, ge=0)


class FullAnalysisRequest(BaseModel):
    ticker: str
    growth_rate: float
    perpetual_growth_rate: float
    wacc: float
    berkus: BerkusRequest = Field(default_factory=BerkusRequest)
    scorecard: ScorecardRequest = Field(default_factory=ScorecardRequest)
    risk_factor: RiskFactorRequest = Field(default_factory=RiskFactorRequest)
    cost_to_duplicate: CostToDuplicateRequest = Field(default_factory=CostToDuplicateRequest)
    vc_method: VcMethodRequest = Field(default_factory=VcMethodRequest)


class StartupAllRequest(BaseModel):
    berkus: BerkusRequest = Field(default_factory=BerkusRequest)
    scorecard: ScorecardRequest = Field(default_factory=ScorecardRequest)
    risk_factor: RiskFactorRequest = Field(default_factory=RiskFactorRequest)
    cost_to_duplicate: CostToDuplicateRequest = Field(default_factory=CostToDuplicateRequest)
    vc_method: VcMethodRequest = Field(default_factory=VcMethodRequest)


# --- App ---
app = FastAPI(title="Startup Valuation API", version="1.0.0")

_cors_origins = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:3000,http://127.0.0.1:3000",
).split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in _cors_origins if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/company/{ticker}")
def get_company(ticker: str) -> dict[str, Any]:
    t = normalize_ticker(ticker)
    df = require_financials(t)
    return company_info_from_sql(t, df)


@app.get("/api/financials/{ticker}")
def get_financials(ticker: str) -> dict[str, Any]:
    t = normalize_ticker(ticker)
    df = require_financials(t)
    return {"ticker": t, "rows": dataframe_to_records(df)}


@app.post("/api/dcf")
def post_dcf(body: DcfRequest) -> dict[str, Any]:
    t = normalize_ticker(body.ticker)
    require_financials(t)
    intrinsic = run_dcf_or_fail(
        t,
        body.growth_rate,
        body.perpetual_growth_rate,
        body.wacc,
    )
    return {
        "ticker": t,
        "intrinsic_value_per_share": intrinsic,
        "growth_rate": body.growth_rate,
        "perpetual_growth_rate": body.perpetual_growth_rate,
        "wacc": body.wacc,
    }


@app.get("/api/ml-predict/{ticker}")
def ml_predict(ticker: str) -> dict[str, Any]:
    t = normalize_ticker(ticker)
    df = require_financials(t)
    mcap, _, _ = predict_market_cap_and_cluster(df)
    return {"ticker": t, "predicted_market_cap": mcap}


@app.get("/api/peer-group/{ticker}")
def peer_group(ticker: str) -> dict[str, Any]:
    t = normalize_ticker(ticker)
    df = require_financials(t)
    _, cluster_id, description = predict_market_cap_and_cluster(df)
    return {
        "ticker": t,
        "cluster": cluster_id,
        "peer_group_description": description,
    }


@app.post("/api/full-analysis")
def full_analysis(body: FullAnalysisRequest) -> dict[str, Any]:
    t = normalize_ticker(body.ticker)
    df = require_financials(t)

    intrinsic = run_dcf_or_fail(
        t,
        body.growth_rate,
        body.perpetual_growth_rate,
        body.wacc,
    )
    predicted_mcap, cluster_id, peer_desc = predict_market_cap_and_cluster(df)

    b = body.berkus
    berkus_val = calculate_berkus(
        {
            "sound_idea": b.sound_idea,
            "prototype": b.prototype,
            "management_team": b.management_team,
            "strategic_relationships": b.strategic_relationships,
            "product_rollout": b.product_rollout,
        }
    )

    sc = body.scorecard
    scorecard_val = calculate_scorecard(
        sc.avg_pre_money_valuation,
        _default_scorecard_factors(
            sc.management_team,
            sc.size_of_opportunity,
            sc.product_technology,
            sc.competitive_environment,
            sc.marketing_sales,
            sc.need_for_funding,
            sc.other,
        ),
    )

    rf = body.risk_factor
    risk_val = calculate_risk_factor(
        rf.avg_pre_money_valuation,
        {
            "management_risk": rf.management_risk,
            "stage_of_business": rf.stage_of_business,
            "competition_risk": rf.competition_risk,
        },
    )

    c = body.cost_to_duplicate
    cost_val = calculate_cost_to_duplicate(
        {
            "research_and_development": c.research_and_development,
            "software_development_salaries": c.software_development_salaries,
            "physical_assets_computers": c.physical_assets_computers,
        }
    )

    vc = body.vc_method
    vc_out = calculate_vc_method(
        vc.projected_revenue_at_exit,
        vc.industry_ps_multiple,
        vc.required_roi_multiple,
        vc.investment_amount,
    )

    return {
        "ticker": t,
        "company": company_info_from_sql(t, df),
        "financials": {"ticker": t, "rows": dataframe_to_records(df)},
        "dcf": {
            "intrinsic_value_per_share": intrinsic,
            "growth_rate": body.growth_rate,
            "perpetual_growth_rate": body.perpetual_growth_rate,
            "wacc": body.wacc,
        },
        "ml": {
            "predicted_market_cap": predicted_mcap,
            "cluster": cluster_id,
            "peer_group_description": peer_desc,
        },
        "startup_valuations": {
            "berkus": berkus_val,
            "scorecard": scorecard_val,
            "risk_factor": risk_val,
            "cost_to_duplicate": cost_val,
            "vc_method": vc_out,
        },
    }


@app.post("/api/startup/berkus")
def startup_berkus(body: BerkusRequest) -> dict[str, float]:
    scores = {
        "sound_idea": body.sound_idea,
        "prototype": body.prototype,
        "management_team": body.management_team,
        "strategic_relationships": body.strategic_relationships,
        "product_rollout": body.product_rollout,
    }
    return {"valuation": calculate_berkus(scores)}


@app.post("/api/startup/scorecard")
def startup_scorecard(body: ScorecardRequest) -> dict[str, float]:
    factors = _default_scorecard_factors(
        body.management_team,
        body.size_of_opportunity,
        body.product_technology,
        body.competitive_environment,
        body.marketing_sales,
        body.need_for_funding,
        body.other,
    )
    return {"valuation": calculate_scorecard(body.avg_pre_money_valuation, factors)}


@app.post("/api/startup/risk-factor")
def startup_risk_factor(body: RiskFactorRequest) -> dict[str, float]:
    risk_scores = {
        "management_risk": body.management_risk,
        "stage_of_business": body.stage_of_business,
        "competition_risk": body.competition_risk,
    }
    return {"valuation": calculate_risk_factor(body.avg_pre_money_valuation, risk_scores)}


@app.post("/api/startup/cost-to-duplicate")
def startup_cost_to_duplicate(body: CostToDuplicateRequest) -> dict[str, float]:
    costs = {
        "research_and_development": body.research_and_development,
        "software_development_salaries": body.software_development_salaries,
        "physical_assets_computers": body.physical_assets_computers,
    }
    return {"valuation": calculate_cost_to_duplicate(costs)}


@app.post("/api/startup/vc-method")
def startup_vc_method(body: VcMethodRequest) -> dict[str, float]:
    out = calculate_vc_method(
        body.projected_revenue_at_exit,
        body.industry_ps_multiple,
        body.required_roi_multiple,
        body.investment_amount,
    )
    return {
        "exit_value": out["exit_value"],
        "post_money_valuation": out["post_money_valuation"],
        "pre_money_valuation": out["pre_money_valuation"],
    }


@app.post("/api/startup/all")
def startup_all(body: StartupAllRequest) -> dict[str, Any]:
    b = body.berkus
    berkus_val = calculate_berkus(
        {
            "sound_idea": b.sound_idea,
            "prototype": b.prototype,
            "management_team": b.management_team,
            "strategic_relationships": b.strategic_relationships,
            "product_rollout": b.product_rollout,
        }
    )

    sc = body.scorecard
    scorecard_val = calculate_scorecard(
        sc.avg_pre_money_valuation,
        _default_scorecard_factors(
            sc.management_team,
            sc.size_of_opportunity,
            sc.product_technology,
            sc.competitive_environment,
            sc.marketing_sales,
            sc.need_for_funding,
            sc.other,
        ),
    )

    rf = body.risk_factor
    risk_val = calculate_risk_factor(
        rf.avg_pre_money_valuation,
        {
            "management_risk": rf.management_risk,
            "stage_of_business": rf.stage_of_business,
            "competition_risk": rf.competition_risk,
        },
    )

    c = body.cost_to_duplicate
    cost_val = calculate_cost_to_duplicate(
        {
            "research_and_development": c.research_and_development,
            "software_development_salaries": c.software_development_salaries,
            "physical_assets_computers": c.physical_assets_computers,
        }
    )

    vc = body.vc_method
    vc_out = calculate_vc_method(
        vc.projected_revenue_at_exit,
        vc.industry_ps_multiple,
        vc.required_roi_multiple,
        vc.investment_amount,
    )

    return {
        "berkus": berkus_val,
        "scorecard": scorecard_val,
        "risk_factor": risk_val,
        "cost_to_duplicate": cost_val,
        "vc_method": vc_out,
    }
