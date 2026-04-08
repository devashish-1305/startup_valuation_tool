import type { FullAnalysisResponse } from "../api/types";
import { formatInt, formatUsd, formatUsdPerShare } from "../utils/format";
import { PublicCompanyFinancials } from "./PublicCompanyFinancials";

type Props = {
  data: FullAnalysisResponse;
  loading: boolean;
  growthPct: number;
  setGrowthPct: (n: number) => void;
  perpetualPct: number;
  setPerpetualPct: (n: number) => void;
  waccPct: number;
  setWaccPct: (n: number) => void;
  onRecalculate: () => void;
};

export function PublicCompanyResults({
  data,
  loading,
  growthPct,
  setGrowthPct,
  perpetualPct,
  setPerpetualPct,
  waccPct,
  setWaccPct,
  onRecalculate,
}: Props) {
  return (
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
            <label htmlFor="growthPct">5-year growth (%)</label>
            <input
              id="growthPct"
              type="number"
              step={0.1}
              value={growthPct}
              onChange={(e) => setGrowthPct(Number(e.target.value))}
            />
          </div>
          <div className="field" style={{ marginBottom: 0 }}>
            <label htmlFor="perpetualPct">Perpetual growth (%)</label>
            <input
              id="perpetualPct"
              type="number"
              step={0.1}
              value={perpetualPct}
              onChange={(e) => setPerpetualPct(Number(e.target.value))}
            />
          </div>
          <div className="field" style={{ marginBottom: 0 }}>
            <label htmlFor="waccPct">WACC / discount (%)</label>
            <input
              id="waccPct"
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
          onClick={onRecalculate}
        >
          Recalculate DCF
        </button>
      </div>

      <PublicCompanyFinancials rows={data.financials.rows} />
    </>
  );
}
