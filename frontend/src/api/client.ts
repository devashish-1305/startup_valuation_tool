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

async function parseError(res: Response): Promise<string> {
  try {
    const j = (await res.json()) as { detail?: string | Array<{ msg?: string }> };
    if (typeof j.detail === "string") return j.detail;
    if (Array.isArray(j.detail)) return j.detail.map((d) => d.msg ?? "").join("; ");
  } catch {
    /* ignore */
  }
  return res.statusText || `HTTP ${res.status}`;
}

async function req<T>(
  path: string,
  init?: RequestInit,
): Promise<T> {
  const url = `${base()}${path}`;
  const res = await fetch(url, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
  });
  if (!res.ok) throw new Error(await parseError(res));
  if (res.status === 204) return undefined as T;
  return res.json() as Promise<T>;
}

export const api = {
  health: () => req<{ status: string }>("/api/health"),

  fullAnalysis: (body: FullAnalysisRequest) =>
    req<FullAnalysisResponse>("/api/full-analysis", {
      method: "POST",
      body: JSON.stringify(body),
    }),

  dcf: (body: DcfRequest) =>
    req<{
      ticker: string;
      intrinsic_value_per_share: number;
      growth_rate: number;
      perpetual_growth_rate: number;
      wacc: number;
    }>("/api/dcf", { method: "POST", body: JSON.stringify(body) }),

  startupBerkus: (body: BerkusRequest) =>
    req<{ valuation: number }>("/api/startup/berkus", {
      method: "POST",
      body: JSON.stringify(body),
    }),

  startupScorecard: (body: ScorecardRequest) =>
    req<{ valuation: number }>("/api/startup/scorecard", {
      method: "POST",
      body: JSON.stringify(body),
    }),

  startupRiskFactor: (body: RiskFactorRequest) =>
    req<{ valuation: number }>("/api/startup/risk-factor", {
      method: "POST",
      body: JSON.stringify(body),
    }),

  startupCostToDuplicate: (body: CostToDuplicateRequest) =>
    req<{ valuation: number }>("/api/startup/cost-to-duplicate", {
      method: "POST",
      body: JSON.stringify(body),
    }),

  startupVcMethod: (body: VcMethodRequest) =>
    req<{
      exit_value: number;
      post_money_valuation: number;
      pre_money_valuation: number;
    }>("/api/startup/vc-method", { method: "POST", body: JSON.stringify(body) }),

  startupAll: (body: StartupAllRequest) =>
    req<StartupAllResponse>("/api/startup/all", {
      method: "POST",
      body: JSON.stringify(body),
    }),
};
