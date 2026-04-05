import { useState } from "react";
import { api } from "../api/client";
import type {
  BerkusRequest,
  CostToDuplicateRequest,
  RiskFactorRequest,
  ScorecardRequest,
  StartupAllResponse,
  VcMethodRequest,
} from "../api/types";
import { formatUsd } from "../utils/format";

type Tab = "berkus" | "scorecard" | "risk" | "cost" | "vc" | "all";

const defaultBerkus: BerkusRequest = {
  sound_idea: 400_000,
  prototype: 300_000,
  management_team: 500_000,
  strategic_relationships: 250_000,
  product_rollout: 150_000,
};

const defaultScorecard: ScorecardRequest = {
  avg_pre_money_valuation: 2_000_000,
  management_team: 1.25,
  size_of_opportunity: 1.5,
  product_technology: 1.0,
  competitive_environment: 1.0,
  marketing_sales: 1.0,
  need_for_funding: 1.0,
  other: 1.0,
};

const defaultRisk: RiskFactorRequest = {
  avg_pre_money_valuation: 1_500_000,
  management_risk: 250_000,
  stage_of_business: 125_000,
  competition_risk: -250_000,
};

const defaultCost: CostToDuplicateRequest = {
  research_and_development: 150_000,
  software_development_salaries: 250_000,
  physical_assets_computers: 20_000,
};

const defaultVc: VcMethodRequest = {
  projected_revenue_at_exit: 50_000_000,
  industry_ps_multiple: 4,
  required_roi_multiple: 20,
  investment_amount: 2_000_000,
};

export function StartupValuation() {
  const [tab, setTab] = useState<Tab>("berkus");
  const [berkus, setBerkus] = useState(defaultBerkus);
  const [scorecard, setScorecard] = useState(defaultScorecard);
  const [risk, setRisk] = useState(defaultRisk);
  const [cost, setCost] = useState(defaultCost);
  const [vc, setVc] = useState(defaultVc);

  const [berkusVal, setBerkusVal] = useState<number | null>(null);
  const [scoreVal, setScoreVal] = useState<number | null>(null);
  const [riskVal, setRiskVal] = useState<number | null>(null);
  const [costVal, setCostVal] = useState<number | null>(null);
  const [vcVal, setVcVal] = useState<{
    exit_value: number;
    post_money_valuation: number;
    pre_money_valuation: number;
  } | null>(null);
  const [allVal, setAllVal] = useState<StartupAllResponse | null>(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function wrap(fn: () => Promise<void>) {
    setLoading(true);
    setError(null);
    try {
      await fn();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Request failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <h1 className="page-title" style={{ fontSize: "1.5rem" }}>
        Startup Valuation
      </h1>
      <p className="muted" style={{ marginBottom: "1.25rem" }}>
        Forms map to <code>POST /api/startup/*</code> and <code>/api/startup/all</code>.
      </p>

      {error ? <div className="banner-error">{error}</div> : null}

      <div className="tabs">
        {(
          [
            ["berkus", "Berkus"],
            ["scorecard", "Scorecard"],
            ["risk", "Risk Factor"],
            ["cost", "Cost to Duplicate"],
            ["vc", "VC Method"],
            ["all", "Run All"],
          ] as const
        ).map(([id, label]) => (
          <button
            key={id}
            type="button"
            className={tab === id ? "active" : ""}
            onClick={() => setTab(id)}
          >
            {label}
          </button>
        ))}
      </div>

      {tab === "berkus" && (
        <div className="card">
          <p className="muted" style={{ marginTop: 0 }}>
            Each factor $0–$500,000; total valuation is the sum (Berkus method).
          </p>
          {(Object.keys(berkus) as (keyof BerkusRequest)[]).map((key) => (
            <div className="field" key={key}>
              <label htmlFor={key}>{labelBerkus(key)}</label>
              <input
                id={key}
                type="number"
                min={0}
                max={500_000}
                step={1000}
                value={berkus[key]}
                onChange={(e) =>
                  setBerkus({ ...berkus, [key]: Number(e.target.value) })
                }
              />
            </div>
          ))}
          <button
            type="button"
            className="btn btn-primary"
            disabled={loading}
            onClick={() =>
              wrap(async () => {
                const r = await api.startupBerkus(berkus);
                setBerkusVal(r.valuation);
              })
            }
          >
            {loading ? "…" : "Calculate"}
          </button>
          {berkusVal != null ? (
            <div style={{ marginTop: "1.25rem" }}>
              <div className="muted" style={{ fontSize: "0.8125rem", fontWeight: 600 }}>
                Berkus valuation
              </div>
              <div className="result-big">{formatUsd(berkusVal)}</div>
            </div>
          ) : null}
        </div>
      )}

      {tab === "scorecard" && (
        <div className="card">
          <div className="field">
            <label htmlFor="avg-sc">Average pre-money ($)</label>
            <input
              id="avg-sc"
              type="number"
              min={1}
              step={100_000}
              value={scorecard.avg_pre_money_valuation}
              onChange={(e) =>
                setScorecard({
                  ...scorecard,
                  avg_pre_money_valuation: Number(e.target.value),
                })
              }
            />
          </div>
          {( [
            ["management_team", "Management team"],
            ["size_of_opportunity", "Size of opportunity"],
            ["product_technology", "Product / technology"],
            ["competitive_environment", "Competitive environment"],
            ["marketing_sales", "Marketing / sales"],
            ["need_for_funding", "Need for funding"],
            ["other", "Other"],
          ] as const).map(([key, lab]) => (
            <div className="field" key={key}>
              <label htmlFor={key}>{lab} (0.5–1.5)</label>
              <input
                id={key}
                type="number"
                min={0.5}
                max={1.5}
                step={0.05}
                value={scorecard[key]}
                onChange={(e) =>
                  setScorecard({ ...scorecard, [key]: Number(e.target.value) })
                }
              />
            </div>
          ))}
          <button
            type="button"
            className="btn btn-primary"
            disabled={loading}
            onClick={() =>
              wrap(async () => {
                const r = await api.startupScorecard(scorecard);
                setScoreVal(r.valuation);
              })
            }
          >
            {loading ? "…" : "Calculate"}
          </button>
          {scoreVal != null ? (
            <div style={{ marginTop: "1.25rem" }}>
              <div className="muted" style={{ fontSize: "0.8125rem", fontWeight: 600 }}>
                Scorecard valuation
              </div>
              <div className="result-big">{formatUsd(scoreVal)}</div>
            </div>
          ) : null}
        </div>
      )}

      {tab === "risk" && (
        <div className="card">
          <div className="field">
            <label htmlFor="avg-r">Average pre-money ($)</label>
            <input
              id="avg-r"
              type="number"
              min={1}
              step={100_000}
              value={risk.avg_pre_money_valuation}
              onChange={(e) =>
                setRisk({ ...risk, avg_pre_money_valuation: Number(e.target.value) })
              }
            />
          </div>
          <div className="field">
            <label htmlFor="mr">Management risk adj. ($)</label>
            <input
              id="mr"
              type="number"
              step={25_000}
              value={risk.management_risk}
              onChange={(e) =>
                setRisk({ ...risk, management_risk: Number(e.target.value) })
              }
            />
          </div>
          <div className="field">
            <label htmlFor="sb">Stage of business adj. ($)</label>
            <input
              id="sb"
              type="number"
              step={25_000}
              value={risk.stage_of_business}
              onChange={(e) =>
                setRisk({ ...risk, stage_of_business: Number(e.target.value) })
              }
            />
          </div>
          <div className="field">
            <label htmlFor="cr">Competition risk adj. ($)</label>
            <input
              id="cr"
              type="number"
              step={25_000}
              value={risk.competition_risk}
              onChange={(e) =>
                setRisk({ ...risk, competition_risk: Number(e.target.value) })
              }
            />
          </div>
          <button
            type="button"
            className="btn btn-primary"
            disabled={loading}
            onClick={() =>
              wrap(async () => {
                const r = await api.startupRiskFactor(risk);
                setRiskVal(r.valuation);
              })
            }
          >
            {loading ? "…" : "Calculate"}
          </button>
          {riskVal != null ? (
            <div style={{ marginTop: "1.25rem" }}>
              <div className="muted" style={{ fontSize: "0.8125rem", fontWeight: 600 }}>
                Risk factor valuation
              </div>
              <div className="result-big">{formatUsd(riskVal)}</div>
            </div>
          ) : null}
        </div>
      )}

      {tab === "cost" && (
        <div className="card">
          <div className="field">
            <label htmlFor="rd">R&amp;D ($)</label>
            <input
              id="rd"
              type="number"
              min={0}
              step={5000}
              value={cost.research_and_development}
              onChange={(e) =>
                setCost({ ...cost, research_and_development: Number(e.target.value) })
              }
            />
          </div>
          <div className="field">
            <label htmlFor="dev">Dev salaries ($)</label>
            <input
              id="dev"
              type="number"
              min={0}
              step={5000}
              value={cost.software_development_salaries}
              onChange={(e) =>
                setCost({
                  ...cost,
                  software_development_salaries: Number(e.target.value),
                })
              }
            />
          </div>
          <div className="field">
            <label htmlFor="phys">Physical assets ($)</label>
            <input
              id="phys"
              type="number"
              min={0}
              step={1000}
              value={cost.physical_assets_computers}
              onChange={(e) =>
                setCost({
                  ...cost,
                  physical_assets_computers: Number(e.target.value),
                })
              }
            />
          </div>
          <button
            type="button"
            className="btn btn-primary"
            disabled={loading}
            onClick={() =>
              wrap(async () => {
                const r = await api.startupCostToDuplicate(cost);
                setCostVal(r.valuation);
              })
            }
          >
            {loading ? "…" : "Calculate"}
          </button>
          {costVal != null ? (
            <div style={{ marginTop: "1.25rem" }}>
              <div className="muted" style={{ fontSize: "0.8125rem", fontWeight: 600 }}>
                Cost to duplicate
              </div>
              <div className="result-big">{formatUsd(costVal)}</div>
            </div>
          ) : null}
        </div>
      )}

      {tab === "vc" && (
        <div className="card">
          <div className="field">
            <label htmlFor="rev">Projected revenue at exit ($)</label>
            <input
              id="rev"
              type="number"
              min={1}
              step={1_000_000}
              value={vc.projected_revenue_at_exit}
              onChange={(e) =>
                setVc({ ...vc, projected_revenue_at_exit: Number(e.target.value) })
              }
            />
          </div>
          <div className="field">
            <label htmlFor="ps">Industry P/S multiple</label>
            <input
              id="ps"
              type="number"
              min={0.1}
              step={0.5}
              value={vc.industry_ps_multiple}
              onChange={(e) =>
                setVc({ ...vc, industry_ps_multiple: Number(e.target.value) })
              }
            />
          </div>
          <div className="field">
            <label htmlFor="roi">Required ROI (multiple)</label>
            <input
              id="roi"
              type="number"
              min={0.1}
              step={1}
              value={vc.required_roi_multiple}
              onChange={(e) =>
                setVc({ ...vc, required_roi_multiple: Number(e.target.value) })
              }
            />
          </div>
          <div className="field">
            <label htmlFor="inv">Investment amount ($)</label>
            <input
              id="inv"
              type="number"
              min={0}
              step={100_000}
              value={vc.investment_amount}
              onChange={(e) =>
                setVc({ ...vc, investment_amount: Number(e.target.value) })
              }
            />
          </div>
          <button
            type="button"
            className="btn btn-primary"
            disabled={loading}
            onClick={() =>
              wrap(async () => {
                const r = await api.startupVcMethod(vc);
                setVcVal(r);
              })
            }
          >
            {loading ? "…" : "Calculate"}
          </button>
          {vcVal ? (
            <div style={{ marginTop: "1.25rem" }}>
              <dl className="kv">
                <dt>Exit value</dt>
                <dd>{formatUsd(vcVal.exit_value)}</dd>
                <dt>Post-money valuation</dt>
                <dd>{formatUsd(vcVal.post_money_valuation)}</dd>
                <dt>Pre-money valuation</dt>
                <dd>{formatUsd(vcVal.pre_money_valuation)}</dd>
              </dl>
            </div>
          ) : null}
        </div>
      )}

      {tab === "all" && (
        <div className="card">
          <p className="muted" style={{ marginTop: 0 }}>
            Single request to <code>POST /api/startup/all</code> using the values below.
          </p>
          <h3 className="section-title">Berkus</h3>
          {(Object.keys(berkus) as (keyof BerkusRequest)[]).map((key) => (
            <div className="field" key={key}>
              <label htmlFor={`all-${key}`}>{labelBerkus(key)}</label>
              <input
                id={`all-${key}`}
                type="number"
                value={berkus[key]}
                onChange={(e) =>
                  setBerkus({ ...berkus, [key]: Number(e.target.value) })
                }
              />
            </div>
          ))}
          <h3 className="section-title">Scorecard</h3>
          <div className="field">
            <label>Average pre-money ($)</label>
            <input
              type="number"
              value={scorecard.avg_pre_money_valuation}
              onChange={(e) =>
                setScorecard({
                  ...scorecard,
                  avg_pre_money_valuation: Number(e.target.value),
                })
              }
            />
          </div>
          {( [
            ["management_team", "Management"],
            ["size_of_opportunity", "Size"],
            ["product_technology", "Product"],
            ["competitive_environment", "Competition"],
            ["marketing_sales", "Marketing"],
            ["need_for_funding", "Funding need"],
            ["other", "Other"],
          ] as const).map(([key, lab]) => (
            <div className="field" key={key}>
              <label>{lab}</label>
              <input
                type="number"
                min={0.5}
                max={1.5}
                step={0.05}
                value={scorecard[key]}
                onChange={(e) =>
                  setScorecard({ ...scorecard, [key]: Number(e.target.value) })
                }
              />
            </div>
          ))}
          <h3 className="section-title">Risk factor</h3>
          <div className="field">
            <label>Average pre-money ($)</label>
            <input
              type="number"
              value={risk.avg_pre_money_valuation}
              onChange={(e) =>
                setRisk({
                  ...risk,
                  avg_pre_money_valuation: Number(e.target.value),
                })
              }
            />
          </div>
          <div className="field">
            <label>Management / stage / competition ($)</label>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: "0.5rem" }}>
              <input
                type="number"
                value={risk.management_risk}
                onChange={(e) =>
                  setRisk({ ...risk, management_risk: Number(e.target.value) })
                }
              />
              <input
                type="number"
                value={risk.stage_of_business}
                onChange={(e) =>
                  setRisk({ ...risk, stage_of_business: Number(e.target.value) })
                }
              />
              <input
                type="number"
                value={risk.competition_risk}
                onChange={(e) =>
                  setRisk({ ...risk, competition_risk: Number(e.target.value) })
                }
              />
            </div>
          </div>
          <h3 className="section-title">Cost to duplicate</h3>
          <div className="field">
            <label>R&amp;D / Dev / Assets ($)</label>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: "0.5rem" }}>
              <input
                type="number"
                value={cost.research_and_development}
                onChange={(e) =>
                  setCost({
                    ...cost,
                    research_and_development: Number(e.target.value),
                  })
                }
              />
              <input
                type="number"
                value={cost.software_development_salaries}
                onChange={(e) =>
                  setCost({
                    ...cost,
                    software_development_salaries: Number(e.target.value),
                  })
                }
              />
              <input
                type="number"
                value={cost.physical_assets_computers}
                onChange={(e) =>
                  setCost({
                    ...cost,
                    physical_assets_computers: Number(e.target.value),
                  })
                }
              />
            </div>
          </div>
          <h3 className="section-title">VC method</h3>
          <div className="field">
            <label>Revenue / P:S / ROI / Investment</label>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "0.5rem" }}>
              <input
                type="number"
                value={vc.projected_revenue_at_exit}
                onChange={(e) =>
                  setVc({
                    ...vc,
                    projected_revenue_at_exit: Number(e.target.value),
                  })
                }
              />
              <input
                type="number"
                value={vc.industry_ps_multiple}
                onChange={(e) =>
                  setVc({
                    ...vc,
                    industry_ps_multiple: Number(e.target.value),
                  })
                }
              />
              <input
                type="number"
                value={vc.required_roi_multiple}
                onChange={(e) =>
                  setVc({
                    ...vc,
                    required_roi_multiple: Number(e.target.value),
                  })
                }
              />
              <input
                type="number"
                value={vc.investment_amount}
                onChange={(e) =>
                  setVc({ ...vc, investment_amount: Number(e.target.value) })
                }
              />
            </div>
          </div>

          <button
            type="button"
            className="btn btn-primary"
            disabled={loading}
            onClick={() =>
              wrap(async () => {
                const r = await api.startupAll({
                  berkus,
                  scorecard,
                  risk_factor: risk,
                  cost_to_duplicate: cost,
                  vc_method: vc,
                });
                setAllVal(r);
              })
            }
          >
            {loading ? "…" : "Run all"}
          </button>

          {allVal ? (
            <div style={{ marginTop: "1.5rem", display: "grid", gap: "1rem" }}>
              <div className="card" style={{ padding: "1rem" }}>
                <div className="muted" style={{ fontSize: "0.75rem", fontWeight: 600 }}>
                  Berkus
                </div>
                <div className="result-big" style={{ fontSize: "1.35rem" }}>
                  {formatUsd(allVal.berkus)}
                </div>
              </div>
              <div className="card" style={{ padding: "1rem" }}>
                <div className="muted" style={{ fontSize: "0.75rem", fontWeight: 600 }}>
                  Scorecard
                </div>
                <div className="result-big" style={{ fontSize: "1.35rem" }}>
                  {formatUsd(allVal.scorecard)}
                </div>
              </div>
              <div className="card" style={{ padding: "1rem" }}>
                <div className="muted" style={{ fontSize: "0.75rem", fontWeight: 600 }}>
                  Risk factor
                </div>
                <div className="result-big" style={{ fontSize: "1.35rem" }}>
                  {formatUsd(allVal.risk_factor)}
                </div>
              </div>
              <div className="card" style={{ padding: "1rem" }}>
                <div className="muted" style={{ fontSize: "0.75rem", fontWeight: 600 }}>
                  Cost to duplicate
                </div>
                <div className="result-big" style={{ fontSize: "1.35rem" }}>
                  {formatUsd(allVal.cost_to_duplicate)}
                </div>
              </div>
              <div className="card" style={{ padding: "1rem" }}>
                <div className="muted" style={{ fontSize: "0.75rem", fontWeight: 600 }}>
                  VC method
                </div>
                <dl className="kv" style={{ margin: "0.5rem 0 0" }}>
                  <dt>Exit</dt>
                  <dd>{formatUsd(allVal.vc_method.exit_value)}</dd>
                  <dt>Post-money</dt>
                  <dd>{formatUsd(allVal.vc_method.post_money_valuation)}</dd>
                  <dt>Pre-money</dt>
                  <dd>{formatUsd(allVal.vc_method.pre_money_valuation)}</dd>
                </dl>
              </div>
            </div>
          ) : null}
        </div>
      )}
    </div>
  );
}

function labelBerkus(key: keyof BerkusRequest): string {
  const labels: Record<keyof BerkusRequest, string> = {
    sound_idea: "Sound idea ($)",
    prototype: "Prototype ($)",
    management_team: "Quality management team ($)",
    strategic_relationships: "Strategic relationships ($)",
    product_rollout: "Product rollout ($)",
  };
  return labels[key];
}
