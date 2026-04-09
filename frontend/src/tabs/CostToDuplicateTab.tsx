import { useState } from "react";
import { api } from "../api/client";
import { useStartupModels } from "../context/StartupModelsContext";
import { formatUsd } from "../utils/format";

export function CostToDuplicateTab() {
  const { cost, setCost, loading, runAsync } = useStartupModels();
  const [out, setOut] = useState<number | null>(null);

  async function handleSubmit() {
    await runAsync(async () => {
      const r = await api.startupCostToDuplicate(cost);
      setOut(r.valuation);
      console.log("[cost] valuation", r.valuation);
    });
  }

  return (
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
            setCost({ ...cost, software_development_salaries: Number(e.target.value) })
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
            setCost({ ...cost, physical_assets_computers: Number(e.target.value) })
          }
        />
      </div>
      <button type="button" className="btn btn-primary" disabled={loading} onClick={handleSubmit}>
        {loading ? "…" : "Calculate"}
      </button>
      {out != null ? (
        <div style={{ marginTop: "1.25rem" }}>
          <div className="muted" style={{ fontSize: "0.8125rem", fontWeight: 600 }}>
            Cost to duplicate
          </div>
          <div className="result-big">{formatUsd(out)}</div>
        </div>
      ) : null}
    </div>
  );
}
