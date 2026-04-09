import { useState } from "react";
import { api } from "../api/client";
import { useStartupModels } from "../context/StartupModelsContext";
import type { ScorecardRequest } from "../api/types";
import { formatUsd } from "../utils/format";

const rows: [keyof ScorecardRequest, string][] = [
  ["management_team", "Management team"],
  ["size_of_opportunity", "Size of opportunity"],
  ["product_technology", "Product / technology"],
  ["competitive_environment", "Competitive environment"],
  ["marketing_sales", "Marketing / sales"],
  ["need_for_funding", "Need for funding"],
  ["other", "Other"],
];

export function ScorecardTab() {
  const { scorecard, setScorecard, loading, runAsync } = useStartupModels();
  const [out, setOut] = useState<number | null>(null);

  async function handleSubmit() {
    await runAsync(async () => {
      const r = await api.startupScorecard(scorecard);
      setOut(r.valuation);
      console.log("[scorecard] valuation", r.valuation);
    });
  }

  return (
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
            setScorecard({ ...scorecard, avg_pre_money_valuation: Number(e.target.value) })
          }
        />
      </div>
      {rows.map(([key, lab]) => (
        <div className="field" key={key}>
          <label htmlFor={key}>
            {lab} (0.5–1.5)
          </label>
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
      <button type="button" className="btn btn-primary" disabled={loading} onClick={handleSubmit}>
        {loading ? "…" : "Calculate"}
      </button>
      {out != null ? (
        <div style={{ marginTop: "1.25rem" }}>
          <div className="muted" style={{ fontSize: "0.8125rem", fontWeight: 600 }}>
            Scorecard valuation
          </div>
          <div className="result-big">{formatUsd(out)}</div>
        </div>
      ) : null}
    </div>
  );
}
