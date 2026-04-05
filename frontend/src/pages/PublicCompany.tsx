import { useState } from "react";
import { api } from "../api/client";
import type { FullAnalysisResponse } from "../api/types";
import { formatInt, formatUsd, formatUsdPerShare } from "../utils/format";

const TICKERS = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA", "NVDA", "META", "NFLX"] as const;

export function PublicCompany() {
  const [ticker, setTicker] = useState<string>("AAPL");
  const [growthPct, setGrowthPct] = useState(6);
  const [perpetualPct, setPerpetualPct] = useState(2.5);
  const [waccPct, setWaccPct] = useState(9);
  const [data, setData] = useState<FullAnalysisResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const ratesBody = () => ({
    growth_rate: growthPct / 100,
    perpetual_growth_rate: perpetualPct / 100,
    wacc: waccPct / 100,
  });

  async function runAnalyze() {
    setLoading(true);
    setError(null);
    try {
      const res = await api.fullAnalysis({
        ticker,
        ...ratesBody(),
      });
      setData(res);
    } catch (e) {
      setData(null);
      setError(e instanceof Error ? e.message : "Request failed");
    } finally {
      setLoading(false);
    }
  }

  async function runRecalculate() {
    if (!data) return;
    setLoading(true);
    setError(null);
    try {
      const dcf = await api.dcf({ ticker, ...ratesBody() });
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
    } catch (e) {
      setError(e instanceof Error ? e.message : "Request failed");
    } finally {
      setLoading(false);
    }
  }

  const rows = data?.financials.rows ?? [];
  const displayRows = [...rows]
    .sort((a, b) => String(b.date ?? "").localeCompare(String(a.date ?? "")))
    .slice(0, 12);

  return (
    <div>
      <h1 className="page-title" style={{ fontSize: "1.5rem" }}>
        Public Company Analysis
      </h1>
      <p className="muted" style={{ marginBottom: "1.5rem" }}>
        Uses <code>POST /api/full-analysis</code> for the full run and{" "}
        <code>POST /api/dcf</code> for Recalculate.
      </p>

      {error ? <div className="banner-error">{error}</div> : null}

      <div className="card" style={{ marginBottom: "1.5rem" }}>
        <div style={{ display: "flex", flexWrap: "wrap", gap: "1rem", alignItems: "flex-end" }}>
          <div className="field" style={{ marginBottom: 0, minWidth: "200px" }}>
            <label htmlFor="ticker">Ticker</label>
            <select
              id="ticker"
              value={ticker}
              onChange={(e) => setTicker(e.target.value)}
            >
              {TICKERS.map((t) => (
                <option key={t} value={t}>
                  {t}
                </option>
              ))}
            </select>
          </div>
          <button type="button" className="btn btn-primary" disabled={loading} onClick={runAnalyze}>
            {loading ? "Working…" : "Analyze"}
          </button>
        </div>
      </div>

      {data ? (
        <>
          <h2 className="section-title">Results</h2>
          <div className="metric-row" style={{ marginBottom: "1.5rem" }}>
            <div className="card metric-card">
              <h3>Intrinsic value (DCF)</h3>
              <div className="value">{formatUsdPerShare(data.dcf.intrinsic_value_per_share)}</div>
              <div className="sub">per share</div>
            </div>
            <div className="card metric-card">
              <h3>Predicted market cap (ML)</h3>
              <div className="value">{formatUsd(data.ml.predicted_market_cap)}</div>
              <div className="sub">XGBoost regression</div>
            </div>
            <div className="card metric-card">
              <h3>Peer cluster</h3>
              <div className="value" style={{ fontSize: "1.15rem" }}>
                <span className="pill">Cluster {data.ml.cluster}</span>
              </div>
              <div className="sub">{data.ml.peer_group_description}</div>
            </div>
          </div>

          <div className="card" style={{ marginBottom: "1.5rem" }}>
            <h2 className="section-title">Company snapshot</h2>
            <dl className="kv">
              <dt>Latest date</dt>
              <dd>{data.company.latest_date ?? "—"}</dd>
              <dt>Close</dt>
              <dd>{formatUsdPerShare(data.company.close)}</dd>
              <dt>Volume</dt>
              <dd>{formatInt(data.company.volume)}</dd>
              <dt>Shares outstanding</dt>
              <dd>{formatInt(data.company.shares_outstanding)}</dd>
              <dt>Free cash flow</dt>
              <dd>{formatUsd(data.company.free_cash_flow)}</dd>
              <dt>Total debt</dt>
              <dd>{formatUsd(data.company.total_debt)}</dd>
              <dt>Cash &amp; equivalents</dt>
              <dd>{formatUsd(data.company.cash_and_cash_equivalents)}</dd>
              <dt>SEC 10-K text available</dt>
              <dd>{data.company.sec_filing_10k_available ? "Yes" : "No"}</dd>
            </dl>
          </div>

          <div className="card" style={{ marginBottom: "1.5rem" }}>
            <h2 className="section-title">DCF assumptions</h2>
            <p className="muted" style={{ marginTop: 0 }}>
              Percentages are converted to decimals for the API (e.g. 6% → 0.06).
            </p>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "1rem" }}>
              <div className="field" style={{ marginBottom: 0 }}>
                <label htmlFor="g">5-year growth (%)</label>
                <input
                  id="g"
                  type="number"
                  step={0.1}
                  value={growthPct}
                  onChange={(e) => setGrowthPct(Number(e.target.value))}
                />
              </div>
              <div className="field" style={{ marginBottom: 0 }}>
                <label htmlFor="p">Perpetual growth (%)</label>
                <input
                  id="p"
                  type="number"
                  step={0.1}
                  value={perpetualPct}
                  onChange={(e) => setPerpetualPct(Number(e.target.value))}
                />
              </div>
              <div className="field" style={{ marginBottom: 0 }}>
                <label htmlFor="w">WACC / discount (%)</label>
                <input
                  id="w"
                  type="number"
                  step={0.1}
                  value={waccPct}
                  onChange={(e) => setWaccPct(Number(e.target.value))}
                />
              </div>
            </div>
            <button
              type="button"
              className="btn btn-secondary"
              style={{ marginTop: "1rem" }}
              disabled={loading}
              onClick={runRecalculate}
            >
              Recalculate DCF
            </button>
          </div>

          <div className="card">
            <h2 className="section-title">Financials</h2>
            <div className="table-wrap">
              <table className="data">
                <thead>
                  <tr>
                    <th>Date</th>
                    <th>Close</th>
                    <th>Volume</th>
                    <th>Shares out.</th>
                    <th>Free cash flow</th>
                  </tr>
                </thead>
                <tbody>
                  {displayRows.map((r, i) => (
                    <tr key={`${r.date}-${i}`}>
                      <td>{r.date ?? "—"}</td>
                      <td>{formatUsdPerShare(r.close ?? null)}</td>
                      <td>{formatInt(r.volume ?? null)}</td>
                      <td>{formatInt(r.sharesOutstanding ?? null)}</td>
                      <td>{formatUsd(r.freeCashFlow ?? null)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </>
      ) : (
        <p className="muted">Choose a ticker and click Analyze to load data from the API.</p>
      )}
    </div>
  );
}
