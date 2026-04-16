import type {
  BerkusRequest,
  CostToDuplicateRequest,
  DcfRequest,
  FullAnalysisRequest,
  FullAnalysisResponse,
  RiskFactorRequest,
  ScorecardRequest,
  StartupAllRequest,
  StartupAllResponse,
  VcMethodRequest,
} from "./types";

const base = () => import.meta.env.VITE_API_BASE_URL ?? "";

type FastApiErrorBody = { detail?: string | Array<{ msg?: string }> };

async function readErrorMessage(res: Response): Promise<string> {
  try {
    const j = (await res.json()) as FastApiErrorBody;
    if (typeof j.detail === "string") return j.detail;
    if (Array.isArray(j.detail)) return j.detail.map((d) => d.msg ?? "").join("; ");
  } catch {
    void 0;
  }
  return res.statusText || `HTTP ${res.status}`;
}
async function postJson(path: string, body: object): Promise<unknown> {
  const url = `${base()}${path}`;
  try {
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    if (!res.ok) {
      const msg = await readErrorMessage(res);
      console.log("[api] POST failed", path, res.status, msg);
      throw new Error(msg);
    }
    if (res.status === 204) return undefined;
    return await res.json();
  } catch (e) {
    if (e instanceof Error) throw e;
    throw new Error(String(e));
  }
}

export async function fullAnalysis(body: FullAnalysisRequest): Promise<FullAnalysisResponse> {
  const data = await postJson("/api/full-analysis", body);
  return data as FullAnalysisResponse;
}

export async function dcf(body: DcfRequest) {
  const data = await postJson("/api/dcf", body);
  return data as {
    ticker: string;
    intrinsic_value_per_share: number;
    growth_rate: number;
    perpetual_growth_rate: number;
    wacc: number;
  };
}

export async function startupBerkus(body: BerkusRequest) {
  const data = await postJson("/api/startup/berkus", body);
  return data as { valuation: number };
}

export async function startupScorecard(body: ScorecardRequest) {
  const data = await postJson("/api/startup/scorecard", body);
  return data as { valuation: number };
}

export async function startupRiskFactor(body: RiskFactorRequest) {
  const data = await postJson("/api/startup/risk-factor", body);
  return data as { valuation: number };
}

export async function startupCostToDuplicate(body: CostToDuplicateRequest) {
  const data = await postJson("/api/startup/cost-to-duplicate", body);
  return data as { valuation: number };
}

export async function startupVcMethod(body: VcMethodRequest) {
  const data = await postJson("/api/startup/vc-method", body);
  return data as {
    exit_value: number;
    post_money_valuation: number;
    pre_money_valuation: number;
  };
}

export async function startupAll(body: StartupAllRequest): Promise<StartupAllResponse> {
  const data = await postJson("/api/startup/all", body);
  return data as StartupAllResponse;
}

export async function health(): Promise<{ status: string }> {
  const url = `${base()}/api/health`;
  try {
    const res = await fetch(url);
    if (!res.ok) {
      const msg = await readErrorMessage(res);
      console.log("[api] GET failed", "/api/health", res.status, msg);
      throw new Error(msg);
    }
    return (await res.json()) as { status: string };
  } catch (e) {
    if (e instanceof Error) throw e;
    throw new Error(String(e));
  }
}

export const api = {
  fullAnalysis,
  dcf,
  startupBerkus,
  startupScorecard,
  startupRiskFactor,
  startupCostToDuplicate,
  startupVcMethod,
  startupAll,
  health,
};
