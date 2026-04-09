import { useState } from "react";
import { api } from "../api/client";
import { useStartupModels } from "../context/StartupModelsContext";
import { formatUsd } from "../utils/format";

type VcOut = {
  exit_value: number;
  post_money_valuation: number;
  pre_money_valuation: number;
};

export function VCMethodTab() {
  const { vc, setVc, loading, runAsync } = useStartupModels();
  const [out, setOut] = useState<VcOut | null>(null);

  async function handleSubmit() {
    await runAsync(async () => {
      const r = await api.startupVcMethod(vc);
      setOut(r);
      console.log("[vc] exit/pre/post", r.exit_value, r.pre_money_valuation);
    });
  }

  return (
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
      <button type="button" className="btn btn-primary" disabled={loading} onClick={handleSubmit}>
        {loading ? "…" : "Calculate"}
      </button>
      {out ? (
        <div style={{ marginTop: "1.25rem" }}>
          <dl className="kv">
            <dt>Exit value</dt>
            <dd>{formatUsd(out.exit_value)}</dd>
            <dt>Post-money valuation</dt>
            <dd>{formatUsd(out.post_money_valuation)}</dd>
            <dt>Pre-money valuation</dt>
            <dd>{formatUsd(out.pre_money_valuation)}</dd>
          </dl>
        </div>
      ) : null}
    </div>
  );
}
