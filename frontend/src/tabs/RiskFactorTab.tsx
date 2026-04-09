import { useState } from "react";
import { api } from "../api/client";
import { useStartupModels } from "../context/StartupModelsContext";
import { formatUsd } from "../utils/format";

export function RiskFactorTab() {
  const { risk, setRisk, loading, runAsync } = useStartupModels();
  const [out, setOut] = useState<number | null>(null);

  async function handleSubmit() {
    await runAsync(async () => {
      const r = await api.startupRiskFactor(risk);
      setOut(r.valuation);
      console.log("[risk] valuation", r.valuation);
    });
  }

  return (
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
          onChange={(e) => setRisk({ ...risk, management_risk: Number(e.target.value) })}
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
      <button type="button" className="btn btn-primary" disabled={loading} onClick={handleSubmit}>
        {loading ? "…" : "Calculate"}
      </button>
      {out != null ? (
        <div style={{ marginTop: "1.25rem" }}>
          <div className="muted" style={{ fontSize: "0.8125rem", fontWeight: 600 }}>
            Risk factor valuation
          </div>
          <div className="result-big">{formatUsd(out)}</div>
        </div>
      ) : null}
    </div>
  );
}
