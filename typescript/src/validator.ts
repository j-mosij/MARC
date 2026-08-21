/** Deterministic validation with MUST errors and SHOULD warnings. */

import {
  confidenceBands,
  confidenceTargets,
  remediabilities,
  selectedActions,
  uncertaintySources,
  type ValidationResult,
} from "./types.js";

const coreRequired = [
  "marc_version",
  "pre_capability",
  "uncertainty",
  "primary_source",
  "remediability",
  "selected_action",
  "confidence_band",
  "confidence_target",
  "recommended_next_step",
] as const;

const coreFields = new Set<string>([
  ...coreRequired,
  "decision_id",
  "parent_decision_id",
  "iteration",
  "max_iterations",
  "calibration_profile",
  "secondary_source",
  "post_answer_confidence",
]);

const disclosureRequired = [
  "answer",
  "confidence_band",
  "confidence_target",
  "uncertainty_source",
  "recommended_next_step",
] as const;

const disclosureFields = new Set<string>([
  ...disclosureRequired,
  "selected_action",
]);

const actionRemediability: Readonly<Record<string, string>> = {
  CLARIFY: "user_clarification",
  RETRIEVE: "retrieval",
  TOOL: "tool",
  ESCALATE: "human",
  ABSTAIN: "none",
};

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function isNumber(value: unknown): value is number {
  return typeof value === "number" && Number.isFinite(value);
}

function validateNumber(
  record: Record<string, unknown>,
  field: string,
  errors: string[],
  nullable = false,
): void {
  if (!(field in record)) return;
  const value = record[field];
  if (value === null && nullable) return;
  if (!isNumber(value)) {
    errors.push(`${field} must be a finite number`);
  } else if (value < 0.0 || value > 1.0) {
    errors.push(`${field} must be between 0.0 and 1.0`);
  }
}

function validateEnum(
  record: Record<string, unknown>,
  field: string,
  values: readonly string[],
  errors: string[],
): void {
  if (field in record && !values.includes(record[field] as string)) {
    errors.push(`${field} must be one of ${values.join(", ")}`);
  }
}

function validateString(
  record: Record<string, unknown>,
  field: string,
  errors: string[],
  maximum?: number,
  nullable = false,
): void {
  if (!(field in record)) return;
  const value = record[field];
  if (value === null && nullable) return;
  if (typeof value !== "string") {
    errors.push(`${field} must be a string`);
    return;
  }
  const length = Array.from(value).length;
  if (length === 0) {
    errors.push(`${field} must not be empty`);
  } else if (maximum !== undefined && length > maximum) {
    errors.push(`${field} must be at most ${maximum} characters`);
  }
}

function validateInteger(
  record: Record<string, unknown>,
  field: string,
  errors: string[],
): void {
  if (!(field in record)) return;
  const value = record[field];
  if (typeof value !== "number" || !Number.isInteger(value)) {
    errors.push(`${field} must be an integer`);
  } else if (value < 0) {
    errors.push(`${field} must be greater than or equal to 0`);
  }
}

function validateUnknownFields(
  record: Record<string, unknown>,
  allowed: ReadonlySet<string>,
  errors: string[],
): void {
  for (const field of Object.keys(record).sort()) {
    if (!allowed.has(field) && !field.startsWith("x_")) {
      errors.push(`unknown field: ${field}`);
    }
  }
}

export function validateCore(record: unknown): ValidationResult {
  if (!isRecord(record)) {
    return { valid: false, errors: ["record must be an object"], warnings: [] };
  }

  const errors: string[] = [];
  const warnings: string[] = [];

  for (const field of coreRequired) {
    if (!(field in record)) errors.push(`${field} is required`);
  }

  if ("marc_version" in record && record.marc_version !== "1.0") {
    errors.push('marc_version must equal "1.0"');
  }

  validateString(record, "decision_id", errors, 128);
  validateString(record, "parent_decision_id", errors, 128, true);
  validateInteger(record, "iteration", errors);
  validateInteger(record, "max_iterations", errors);
  validateString(record, "calibration_profile", errors, 128);
  validateNumber(record, "pre_capability", errors);

  if ("uncertainty" in record) {
    const uncertainty = record.uncertainty;
    if (!isRecord(uncertainty)) {
      errors.push("uncertainty must be an object");
    } else {
      for (const source of uncertaintySources) {
        const qualified = `uncertainty.${source}`;
        if (!(source in uncertainty)) {
          errors.push(`${qualified} is required`);
        } else {
          const value = uncertainty[source];
          if (!isNumber(value)) {
            errors.push(`${qualified} must be a finite number`);
          } else if (value < 0.0 || value > 1.0) {
            errors.push(`${qualified} must be between 0.0 and 1.0`);
          }
        }
      }
      for (const field of Object.keys(uncertainty).sort()) {
        if (!uncertaintySources.includes(field as (typeof uncertaintySources)[number])) {
          errors.push(`unknown uncertainty field: ${field}`);
        }
      }
    }
  }

  validateEnum(record, "primary_source", uncertaintySources, errors);
  if (record.secondary_source !== null) {
    validateEnum(record, "secondary_source", uncertaintySources, errors);
  }
  validateEnum(record, "remediability", remediabilities, errors);
  validateEnum(record, "selected_action", selectedActions, errors);
  validateNumber(record, "post_answer_confidence", errors, true);
  validateEnum(record, "confidence_band", confidenceBands, errors);
  validateEnum(record, "confidence_target", confidenceTargets, errors);
  validateString(record, "recommended_next_step", errors, 280);
  validateUnknownFields(record, coreFields, errors);

  const action = record.selected_action;
  if (action === "ANSWER") {
    if (record.post_answer_confidence === null || record.post_answer_confidence === undefined) {
      errors.push("post_answer_confidence must be non-null for ANSWER");
    }
    if (record.confidence_target !== "answer") {
      errors.push('confidence_target must be "answer" for ANSWER');
    }
  }

  const expectedRemediability =
    typeof action === "string" ? actionRemediability[action] : undefined;
  const remediability = record.remediability;
  if (
    expectedRemediability !== undefined &&
    typeof remediability === "string" &&
    remediabilities.includes(remediability as (typeof remediabilities)[number]) &&
    remediability !== expectedRemediability
  ) {
    warnings.push(
      `remediability should be "${expectedRemediability}" for ${String(action)}`,
    );
  }

  return { valid: errors.length === 0, errors, warnings };
}

export function validateDisclosure(record: unknown): ValidationResult {
  if (!isRecord(record)) {
    return { valid: false, errors: ["record must be an object"], warnings: [] };
  }

  const errors: string[] = [];
  for (const field of disclosureRequired) {
    if (!(field in record)) errors.push(`${field} is required`);
  }

  validateString(record, "answer", errors);
  validateEnum(record, "confidence_band", confidenceBands, errors);
  validateEnum(record, "confidence_target", confidenceTargets, errors);
  validateEnum(record, "uncertainty_source", uncertaintySources, errors);
  validateString(record, "recommended_next_step", errors, 280);
  validateEnum(record, "selected_action", selectedActions, errors);
  validateUnknownFields(record, disclosureFields, errors);

  return { valid: errors.length === 0, errors, warnings: [] };
}
