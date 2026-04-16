import { useState } from "react";
import { api } from "../api/client";
import { useStartupModels } from "../context/StartupModelsContext";
import type { BerkusRequest } from "../api/types";
import { formatUsd } from "../utils/format";

const berkusLabels: Record<keyof BerkusRequest, string> = {
  sound_idea: "Sound idea ($)",
  prototype: "Prototype ($)",
  management_team: "Management team ($)",
  strategic_relationships: "Strategic relationships ($)",
  product_rollout: "Product rollout ($)",
};

export function BerkusTab() {
  const { berkus, setBerkus, loading, runAsync } = useStartupModels();
  const [out, setOut] = useState<number | null>(null);

  const keys = Object.keys(berkus) as (keyof BerkusRequest)[];

  async function handleSubmit() {
    await runAsync(async () => {
      const r = await api.startupBerkus(berkus);
      setOut(r.valuation);
      console.log("[berkus] valuation", r.valuation);
    });
  }

  return (
    <div className="card">
      <p className="muted" style={{ marginTop: 0 }}>
        Each factor $0–$500,000; total is the sum (Berkus method).
      </p>
      {keys.map((k) => (
        <div className="field" key={k}>
          <label htmlFor={k}>{berkusLabels[k]}</label>
          <input
            id={k}
            type="number"
            min={0}
            max={500_000}
            step={1000}
            value={berkus[k]}
            onChange={(e) => setBerkus({ ...berkus, [k]: Number(e.target.value) })}
          />
        </div>
      ))}
      <button type="button" className="btn btn-primary" disabled={loading} onClick={handleSubmit}>
        {loading ? "…" : "Calculate"}
      </button>
      {out != null ? (
        <div style={{ marginTop: "1.25rem" }}>
          <div className="muted" style={{ fontSize: "0.8125rem", fontWeight: 600 }}>
            Berkus valuation
          </div>
          <div className="result-big">{formatUsd(out)}</div>
        </div>
      ) : null}
    </div>
  );
}


