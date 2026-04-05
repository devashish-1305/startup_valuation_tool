import { Link } from "react-router-dom";

export function Home() {
  return (
    <div>
      <h1 className="page-title">Startup Valuation &amp; Analysis Tool</h1>
      <p className="page-lead">
        Intrinsic value, ML-based market cap, peer clusters, and five qualitative startup
        models—wired to your FastAPI backend.
      </p>

      <div className="card-grid-2">
        <Link to="/public" className="home-card-link">
          <h2>Public Company Analysis</h2>
          <p className="muted">
            DCF intrinsic value, XGBoost market cap prediction, K-means peer cluster,
            snapshot, and financials.
          </p>
        </Link>
        <Link to="/startup" className="home-card-link">
          <h2>Startup Valuation</h2>
          <p className="muted">
            Berkus, Scorecard, Risk Factor, Cost-to-Duplicate, VC Method, and Run All.
          </p>
        </Link>
      </div>

      <p className="muted" style={{ marginTop: "2.5rem", fontSize: "0.8125rem" }}>
        Financial data available for: AAPL, GOOGL, MSFT, AMZN, TSLA, NVDA, META, NFLX
      </p>
    </div>
  );
}
