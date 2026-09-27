"""
Honest evaluation of the XGBoost market-cap model.

Compares three validation schemes and a naive baseline:
  1. Random 80/20 split (what regression_model.py does)  -> leaks: the same
     company's near-identical rows land in both train and test.
  2. Time-based split (train on first 80% of dates, test on the last 20%).
  3. Leave-one-company-out (can the model value a company it has never seen?).
  4. Naive baseline: each company's last market cap in the training window.

Place at scripts/ml_models/evaluate_regression.py and run from the project root:
    python scripts/ml_models/evaluate_regression.py
"""
import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_percentage_error as mape, r2_score
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor

DB = Path(__file__).resolve().parents[2] / "financials.db"
FEATURES = ["freeCashFlow", "totalDebt", "cashAndCashEquivalents", "volume"]


def load() -> pd.DataFrame:
    with sqlite3.connect(DB) as conn:
        tables = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")]
        df = pd.concat(
            [pd.read_sql(f"SELECT * FROM '{t}'", conn).assign(symbol=t) for t in tables],
            ignore_index=True,
        )
    df["date"] = pd.to_datetime(df["date"])
    df["marketCap"] = df["close"] * df["sharesOutstanding"]
    df = df.dropna(subset=FEATURES + ["marketCap"])
    return df[df["marketCap"] > 0]


def model() -> XGBRegressor:
    return XGBRegressor(objective="reg:squarederror", n_estimators=100,
                        learning_rate=0.1, max_depth=3, random_state=42)


def report(name, y, p):
    print(f"{name:<32} R2 = {r2_score(y, p):6.3f}   MAPE = {mape(y, p):7.1%}")


def main():
    d = load()
    n_fund = d.groupby("symbol")[FEATURES[:3]].nunique().max().max()
    print(f"{len(d):,} daily rows, {d['symbol'].nunique()} companies, "
          f"~{n_fund} distinct fundamental snapshots per company "
          f"({d['date'].min():%Y-%m} to {d['date'].max():%Y-%m})\n")

    # 1. Random split (original approach)
    Xtr, Xte, ytr, yte = train_test_split(d[FEATURES], d["marketCap"], test_size=0.2, random_state=42)
    report("Random split (leaky)", yte, model().fit(Xtr, ytr).predict(Xte))

    # 2. Time split + 4. naive baseline on the same test window
    cut = d["date"].quantile(0.8)
    tr, te = d[d["date"] <= cut], d[d["date"] > cut]
    report("Time split (last 20% of dates)", te["marketCap"], model().fit(tr[FEATURES], tr["marketCap"]).predict(te[FEATURES]))
    last = tr.sort_values("date").groupby("symbol")["marketCap"].last()
    report("Naive last-value baseline", te["marketCap"], te["symbol"].map(last))

    # 3. Leave-one-company-out
    errs = []
    for s in sorted(d["symbol"].unique()):
        tr, te = d[d["symbol"] != s], d[d["symbol"] == s]
        errs.append(mape(te["marketCap"], model().fit(tr[FEATURES], tr["marketCap"]).predict(te[FEATURES])))
    print(f"{'Leave-one-company-out':<32} mean MAPE = {np.mean(errs):7.1%}")


if __name__ == "__main__":
    main()
