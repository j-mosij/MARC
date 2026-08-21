/** Typed data model for MARC 1.0 as specified by draft-c4tz-marc-02. */

export const uncertaintySources = [
  "ambiguity",
  "missing_evidence",
  "capability_limit",
  "evidence_conflict",
  "safety",
] as const;

export const remediabilities = [
  "user_clarification",
  "retrieval",
  "tool",
  "human",
  "none",
] as const;

export const selectedActions = [
  "ANSWER",
  "CLARIFY",
  "RETRIEVE",
  "TOOL",
  "DELIBERATE",
  "ABSTAIN",
  "ESCALATE",
] as const;

export const confidenceBands = ["low", "medium", "high"] as const;

export const confidenceTargets = [
  "answer",
  "direct_answer_suitability",
  "action_suitability",
] as const;

export type UncertaintySource = (typeof uncertaintySources)[number];
export type Remediability = (typeof remediabilities)[number];
export type SelectedAction = (typeof selectedActions)[number];
export type ConfidenceBand = (typeof confidenceBands)[number];
export type ConfidenceTarget = (typeof confidenceTargets)[number];

export interface Uncertainty {
  ambiguity: number;
  missing_evidence: number;
  capability_limit: number;
  evidence_conflict: number;
  safety: number;
}

export interface MarcCore {
  marc_version: "1.0";
  decision_id?: string;
  parent_decision_id?: string | null;
  iteration?: number;
  max_iterations?: number;
  calibration_profile?: string;
  pre_capability: number;
  uncertainty: Uncertainty;
  primary_source: UncertaintySource;
  secondary_source?: UncertaintySource | null;
  remediability: Remediability;
  selected_action: SelectedAction;
  post_answer_confidence?: number | null;
  confidence_band: ConfidenceBand;
  confidence_target: ConfidenceTarget;
  recommended_next_step: string;
  [extension: `x_${string}`]: unknown;
}

export interface MarcDisclosure {
  answer: string;
  confidence_band: ConfidenceBand;
  confidence_target: ConfidenceTarget;
  uncertainty_source: UncertaintySource;
  recommended_next_step: string;
  selected_action?: SelectedAction;
  [extension: `x_${string}`]: unknown;
}

export interface ValidationResult {
  valid: boolean;
  errors: string[];
  warnings: string[];
}
