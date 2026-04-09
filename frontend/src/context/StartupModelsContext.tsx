import {
  createContext,
  useContext,
  useState,
  type ReactNode,
} from "react";
import type {
  BerkusRequest,
  CostToDuplicateRequest,
  RiskFactorRequest,
  ScorecardRequest,
  VcMethodRequest,
} from "../api/types";
import {
  defaultBerkus,
  defaultCost,
  defaultRisk,
  defaultScorecard,
  defaultVc,
} from "../startup/defaults";

type StartupModelsValue = {
  berkus: BerkusRequest;
  setBerkus: (next: BerkusRequest) => void;
  scorecard: ScorecardRequest;
  setScorecard: (next: ScorecardRequest) => void;
  risk: RiskFactorRequest;
  setRisk: (next: RiskFactorRequest) => void;
  cost: CostToDuplicateRequest;
  setCost: (next: CostToDuplicateRequest) => void;
  vc: VcMethodRequest;
  setVc: (next: VcMethodRequest) => void;
  loading: boolean;
  error: string | null;
  runAsync: (fn: () => Promise<void>) => Promise<void>;
};

const StartupModelsContext = createContext<StartupModelsValue | null>(null);

export function StartupModelsProvider({ children }: { children: ReactNode }) {
  const [berkus, setBerkus] = useState(defaultBerkus);
  const [scorecard, setScorecard] = useState(defaultScorecard);
  const [risk, setRisk] = useState(defaultRisk);
  const [cost, setCost] = useState(defaultCost);
  const [vc, setVc] = useState(defaultVc);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function runAsync(fn: () => Promise<void>) {
    setLoading(true);
    setError(null);
    try {
      await fn();
    } catch (e) {
      const msg = e instanceof Error ? e.message : "Request failed";
      setError(msg);
      console.log("[startup] request error", msg);
    } finally {
      setLoading(false);
    }
  }

  const value: StartupModelsValue = {
    berkus,
    setBerkus,
    scorecard,
    setScorecard,
    risk,
    setRisk,
    cost,
    setCost,
    vc,
    setVc,
    loading,
    error,
    runAsync,
  };

  return (
    <StartupModelsContext.Provider value={value}>{children}</StartupModelsContext.Provider>
  );
}

export function useStartupModels() {
  const ctx = useContext(StartupModelsContext);
  if (!ctx) {
    throw new Error("useStartupModels must be used inside StartupModelsProvider");
  }
  return ctx;
}
