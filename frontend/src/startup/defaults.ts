import type {
  BerkusRequest,
  CostToDuplicateRequest,
  RiskFactorRequest,
  ScorecardRequest,
  VcMethodRequest,
} from "../api/types";

export const defaultBerkus: BerkusRequest = {
  sound_idea: 400_000,
  prototype: 300_000,
  management_team: 500_000,
  strategic_relationships: 250_000,
  product_rollout: 150_000,
};

export const defaultScorecard: ScorecardRequest = {
  avg_pre_money_valuation: 2_000_000,
  management_team: 1.25,
  size_of_opportunity: 1.5,
  product_technology: 1.0,
  competitive_environment: 1.0,
  marketing_sales: 1.0,
  need_for_funding: 1.0,
  other: 1.0,
};

export const defaultRisk: RiskFactorRequest = {
  avg_pre_money_valuation: 1_500_000,
  management_risk: 250_000,
  stage_of_business: 125_000,
  competition_risk: -250_000,
};

export const defaultCost: CostToDuplicateRequest = {
  research_and_development: 150_000,
  software_development_salaries: 250_000,
  physical_assets_computers: 20_000,
};

export const defaultVc: VcMethodRequest = {
  projected_revenue_at_exit: 50_000_000,
  industry_ps_multiple: 4,
  required_roi_multiple: 20,
  investment_amount: 2_000_000,
};
