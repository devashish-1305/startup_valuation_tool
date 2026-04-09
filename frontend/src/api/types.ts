export type CompanyInfo = {
  ticker: string;
  latest_date?: string | null;
  close: number | null;
  volume: number | null;
  shares_outstanding: number | null;
  free_cash_flow: number | null;
  total_debt: number | null;
  cash_and_cash_equivalents: number | null;
  sec_filing_10k_available: boolean;
};

export type FinancialRow = {
  date?: string;
  close?: number | null;
  volume?: number | null;
  sharesOutstanding?: number | null;
  freeCashFlow?: number | null;
  totalDebt?: number | null;
  cashAndCashEquivalents?: number | null;
  symbol?: string | null;
};

export type FullAnalysisResponse = {
  ticker: string;
  company: CompanyInfo;
  financials: { ticker: string; rows: FinancialRow[] };
  dcf: {
    intrinsic_value_per_share: number;
    growth_rate: number;
    perpetual_growth_rate: number;
    wacc: number;
  };
  ml: {
    predicted_market_cap: number;
    cluster: number;
    peer_group_description: string;
  };
  startup_valuations: {
    berkus: number;
    scorecard: number;
    risk_factor: number;
    cost_to_duplicate: number;
    vc_method: {
      exit_value: number;
      post_money_valuation: number;
      pre_money_valuation: number;
    };
  };
};

export type DcfRequest = {
  ticker: string;
  growth_rate: number;
  perpetual_growth_rate: number;
  wacc: number;
};

export type BerkusRequest = {
  sound_idea: number;
  prototype: number;
  management_team: number;
  strategic_relationships: number;
  product_rollout: number;
};

export type ScorecardRequest = {
  avg_pre_money_valuation: number;
  management_team: number;
  size_of_opportunity: number;
  product_technology: number;
  competitive_environment: number;
  marketing_sales: number;
  need_for_funding: number;
  other: number;
};

export type RiskFactorRequest = {
  avg_pre_money_valuation: number;
  management_risk: number;
  stage_of_business: number;
  competition_risk: number;
};

export type CostToDuplicateRequest = {
  research_and_development: number;
  software_development_salaries: number;
  physical_assets_computers: number;
};

export type VcMethodRequest = {
  projected_revenue_at_exit: number;
  industry_ps_multiple: number;
  required_roi_multiple: number;
  investment_amount: number;
};

export type FullAnalysisRequest = {
  ticker: string;
  growth_rate: number;
  perpetual_growth_rate: number;
  wacc: number;
  berkus?: BerkusRequest;
  scorecard?: ScorecardRequest;
  risk_factor?: RiskFactorRequest;
  cost_to_duplicate?: CostToDuplicateRequest;
  vc_method?: VcMethodRequest;
};

export type StartupAllRequest = {
  berkus: BerkusRequest;
  scorecard: ScorecardRequest;
  risk_factor: RiskFactorRequest;
  cost_to_duplicate: CostToDuplicateRequest;
  vc_method: VcMethodRequest;
};

export type StartupAllResponse = {
  berkus: number;
  scorecard: number;
  risk_factor: number;
  cost_to_duplicate: number;
  vc_method: {
    exit_value: number;
    post_money_valuation: number;
    pre_money_valuation: number;
  };
};
