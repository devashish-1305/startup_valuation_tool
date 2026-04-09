import { useState } from "react";
import { StartupModelsProvider, useStartupModels } from "../context/StartupModelsContext";
import { BerkusTab } from "../tabs/BerkusTab";
import { CostToDuplicateTab } from "../tabs/CostToDuplicateTab";
import { RiskFactorTab } from "../tabs/RiskFactorTab";
import { RunAllTab } from "../tabs/RunAllTab";
import { ScorecardTab } from "../tabs/ScorecardTab";
import { VCMethodTab } from "../tabs/VCMethodTab";

type TabId = "berkus" | "scorecard" | "risk" | "cost" | "vc" | "all";

const tabs: [TabId, string][] = [
  ["berkus", "Berkus"],
  ["scorecard", "Scorecard"],
  ["risk", "Risk Factor"],
  ["cost", "Cost to Duplicate"],
  ["vc", "VC Method"],
  ["all", "Run All"],
];

function StartupValuationInner() {
  const [tab, setTab] = useState<TabId>("berkus");
  const { error } = useStartupModels();

  return (
    <div>
      <h1 className="page-title" style={{ fontSize: "1.5rem" }}>
        Startup Valuation
      </h1>
      <p className="muted" style={{ marginBottom: "1.25rem" }}>
        POST endpoints under <code>/api/startup</code> and <code>/api/startup/all</code>.
      </p>
      {error ? <div className="banner-error">{error}</div> : null}
      <div className="tabs">
        {tabs.map(([id, label]) => (
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
      {tab === "berkus" ? <BerkusTab /> : null}
      {tab === "scorecard" ? <ScorecardTab /> : null}
      {tab === "risk" ? <RiskFactorTab /> : null}
      {tab === "cost" ? <CostToDuplicateTab /> : null}
      {tab === "vc" ? <VCMethodTab /> : null}
      {tab === "all" ? <RunAllTab /> : null}
    </div>
  );
}

export function StartupValuation() {
  return (
    <StartupModelsProvider>
      <StartupValuationInner />
    </StartupModelsProvider>
  );
}
