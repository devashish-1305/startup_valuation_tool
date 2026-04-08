import { useState } from "react";
import { api } from "../api/client";
import type { FullAnalysisResponse } from "../api/types";
import { PublicCompanyResults } from "./PublicCompanyResults";

const TICKERS = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA", "NVDA", "META", "NFLX"] as const;

export function PublicCompany() {
  const [ticker, setTicker] = useState("AAPL");
  const [growthPct, setGrowthPct] = useState(6);
  const [perpetualPct, setPerpetualPct] = useState(2.5);
  const [waccPct, setWaccPct] = useState(9);
  const [data, setData] = useState<FullAnalysisResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleAnalyze() {
    setLoading(true);
    setError(null);
    try {
      const res = await api.fullAnalysis({
        ticker,
        growth_rate: growthPct / 100,
        perpetual_growth_rate: perpetualPct / 100,
        wacc: waccPct / 100,
      });
      setData(res);
      console.log("[public] analyze", res.ticker);
    } catch (e) {
      setData(null);
      setError(e instanceof Error ? e.message : "Request failed");
    } finally {
      setLoading(false);
    }
  }

  async function handleRecalculate() {
    if (!data) return;
    setLoading(true);
    setError(null);
    try {
      const dcf = await api.dcf({
        ticker,
        growth_rate: growthPct / 100,
        perpetual_growth_rate: perpetualPct / 100,
        wacc: waccPct / 100,
      });
      setData((prev) =>
        prev
          ? {
              ...prev,
              dcf: {
                intrinsic_value_per_share: dcf.intrinsic_value_per_share,
                growth_rate: dcf.growth_rate,
                perpetual_growth_rate: dcf.perpetual_growth_rate,
                wacc: dcf.wacc,
              },
            }
          : prev,
      );
      console.log("[public] dcf recalc", dcf);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Request failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <h1 className="page-title" style={{ fontSize: "1.5rem" }}>
        Public Company Analysis
      </h1>
      <p className="muted" style={{ marginBottom: "1.5rem" }}>
        Run full analysis to load company profile, DCF baseline, ML market-cap estimate,
        and peer cluster. Then adjust assumptions and recalculate only DCF.
      </p>

      {error ? <div className="banner-error">{error}</div> : null}

      <div className="card" style={{ marginBottom: "1.5rem" }}>
        <div style={{ display: "flex", flexWrap: "wrap", gap: "1rem", alignItems: "flex-end" }}>
          <div className="field" style={{ marginBottom: 0, minWidth: "200px" }}>
            <label htmlFor="ticker">Ticker</label>
            <select id="ticker" value={ticker} onChange={(e) => setTicker(e.target.value)}>
              {TICKERS.map((t) => (
                <option key={t} value={t}>
                  {t}
                </option>
              ))}
            </select>
          </div>
          <button
            type="button"
            className="btn btn-primary"
            disabled={loading}
            onClick={handleAnalyze}
          >
            {loading ? "Working…" : "Analyze"}
          </button>
        </div>
      </div>

      {data ? (
        <PublicCompanyResults
          data={data}
          loading={loading}
          growthPct={growthPct}
          setGrowthPct={setGrowthPct}
          perpetualPct={perpetualPct}
          setPerpetualPct={setPerpetualPct}
          waccPct={waccPct}
          setWaccPct={setWaccPct}
          onRecalculate={handleRecalculate}
        />
      ) : (
        <p className="muted">Choose a ticker and click Analyze to load data from the API.</p>
      )}
    </div>
  );
}
