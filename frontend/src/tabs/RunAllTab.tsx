import { useState } from "react";
import { api } from "../api/client";
import { useStartupModels } from "../context/StartupModelsContext";
import type { BerkusRequest, ScorecardRequest, StartupAllResponse } from "../api/types";
import { formatUsd } from "../utils/format";

const berkusLabels: Record<keyof BerkusRequest, string> = {
  sound_idea: "Sound idea ($)",
  prototype: "Prototype ($)",
  management_team: "Management team ($)",
  strategic_relationships: "Strategic relationships ($)",
  product_rollout: "Product rollout ($)",
};

const scoreRows: [keyof ScorecardRequest, string][] = [
  ["management_team", "Management"],
  ["size_of_opportunity", "Size"],
  ["product_technology", "Product"],
  ["competitive_environment", "Competition"],
  ["marketing_sales", "Marketing"],
  ["need_for_funding", "Funding need"],
  ["other", "Other"],
];

export function RunAllTab() {
  const { berkus, setBerkus, scorecard, setScorecard, risk, setRisk, cost, setCost, vc, setVc, loading, runAsync } =
    useStartupModels();
  const [out, setOut] = useState<StartupAllResponse | null>(null);
  const berkusKeys = Object.keys(berkus) as (keyof BerkusRequest)[];

  async function handleSubmit() {
    await runAsync(async () => {
      const r = await api.startupAll({
        berkus,
        scorecard,
        risk_factor: risk,
        cost_to_duplicate: cost,
        vc_method: vc,
      });
      setOut(r);
      console.log("[run all] done", r);
    });
  }

  return (
    <div className="card">
      <p className="muted" style={{ marginTop: 0 }}>
        One POST to <code>/api/startup/all</code> with the fields below.
      </p>
      <h3 className="section-title">Berkus</h3>
      {berkusKeys.map((k) => (
        <div className="field" key={k}>
          <label htmlFor={`all-${String(k)}`}>{berkusLabels[k]}</label>
          <input
            id={`all-${String(k)}`}
            type="number"
            value={berkus[k]}
            onChange={(e) => setBerkus({ ...berkus, [k]: Number(e.target.value) })}
          />
        </div>
      ))}

      <h3 className="section-title">Scorecard</h3>
      <div className="field">
        <label htmlFor="all-avg-sc">Average pre-money ($)</label>
        <input
          id="all-avg-sc"
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
      {scoreRows.map(([key, label]) => (
        <div className="field" key={key}>
          <label htmlFor={`all-sc-${key}`}>{label}</label>
          <input
            id={`all-sc-${key}`}
            type="number"
            min={0.5}
            max={1.5}
            step={0.05}
            value={scorecard[key]}
            onChange={(e) => setScorecard({ ...scorecard, [key]: Number(e.target.value) })}
          />
        </div>
      ))}

      <h3 className="section-title">Risk factor</h3>
      <div className="field">
        <label htmlFor="all-avg-r">Average pre-money ($)</label>
        <input
          id="all-avg-r"
          type="number"
          value={risk.avg_pre_money_valuation}
          onChange={(e) => setRisk({ ...risk, avg_pre_money_valuation: Number(e.target.value) })}
        />
      </div>
      <div className="field">
        <label>Management / stage / competition ($)</label>
        <div className="grid-3">
          <input
            type="number"
            value={risk.management_risk}
            onChange={(e) => setRisk({ ...risk, management_risk: Number(e.target.value) })}
          />
          <input
            type="number"
            value={risk.stage_of_business}
            onChange={(e) => setRisk({ ...risk, stage_of_business: Number(e.target.value) })}
          />
          <input
            type="number"
            value={risk.competition_risk}
            onChange={(e) => setRisk({ ...risk, competition_risk: Number(e.target.value) })}
          />
        </div>
      </div>

      <h3 className="section-title">Cost to duplicate</h3>
      <div className="field">
        <label>R&amp;D / Dev / Assets ($)</label>
        <div className="grid-3">
          <input
            type="number"
            value={cost.research_and_development}
            onChange={(e) =>
              setCost({ ...cost, research_and_development: Number(e.target.value) })
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
              setCost({ ...cost, physical_assets_computers: Number(e.target.value) })
            }
          />
        </div>
      </div>

      <h3 className="section-title">VC method</h3>
      <div className="field">
        <label>Revenue / P:S / ROI / Investment</label>
        <div className="grid-2">
          <input
            type="number"
            value={vc.projected_revenue_at_exit}
            onChange={(e) =>
              setVc({ ...vc, projected_revenue_at_exit: Number(e.target.value) })
            }
          />
          <input
            type="number"
            value={vc.industry_ps_multiple}
            onChange={(e) => setVc({ ...vc, industry_ps_multiple: Number(e.target.value) })}
          />
          <input
            type="number"
            value={vc.required_roi_multiple}
            onChange={(e) => setVc({ ...vc, required_roi_multiple: Number(e.target.value) })}
          />
          <input
            type="number"
            value={vc.investment_amount}
            onChange={(e) => setVc({ ...vc, investment_amount: Number(e.target.value) })}
          />
        </div>
      </div>

      <button
        type="button"
        className="btn btn-primary"
        style={{ marginTop: "1rem" }}
        disabled={loading}
        onClick={handleSubmit}
      >
        {loading ? "…" : "Run all"}
      </button>
      {out ? (
        <div className="run-all-grid" style={{ marginTop: "1.5rem" }}>
          <div className="card pad-sm">
            <div className="muted overline">Berkus</div>
            <div className="result-big size-md">{formatUsd(out.berkus)}</div>
          </div>
          <div className="card pad-sm">
            <div className="muted overline">Scorecard</div>
            <div className="result-big size-md">{formatUsd(out.scorecard)}</div>
          </div>
          <div className="card pad-sm">
            <div className="muted overline">Risk factor</div>
            <div className="result-big size-md">{formatUsd(out.risk_factor)}</div>
          </div>
          <div className="card pad-sm">
            <div className="muted overline">Cost to duplicate</div>
            <div className="result-big size-md">{formatUsd(out.cost_to_duplicate)}</div>
          </div>
          <div className="card pad-sm">
            <div className="muted overline">VC method</div>
            <dl className="kv tight">
              <dt>Exit</dt>
              <dd>{formatUsd(out.vc_method.exit_value)}</dd>
              <dt>Post-money</dt>
              <dd>{formatUsd(out.vc_method.post_money_valuation)}</dd>
              <dt>Pre-money</dt>
              <dd>{formatUsd(out.vc_method.pre_money_valuation)}</dd>
            </dl>
          </div>
        </div>
      ) : null}
    </div>
  );
}
