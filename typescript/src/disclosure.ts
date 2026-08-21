/** Deterministic projection from MARC-Core to MARC-Disclosure. */

import type { MarcCore, MarcDisclosure, SelectedAction } from "./types.js";
import { validateCore, validateDisclosure } from "./validator.js";

export interface ProjectionOptions {
  includeSelectedAction?: boolean;
}

export function projectDisclosure(
  core: MarcCore | Record<string, unknown>,
  answer: string,
  options: ProjectionOptions = {},
): MarcDisclosure {
  const coreResult = validateCore(core);
  if (!coreResult.valid) {
    throw new Error(`invalid MARC-Core record: ${coreResult.errors.join("; ")}`);
  }

  const disclosure: MarcDisclosure = {
    answer,
    confidence_band: core.confidence_band as MarcDisclosure["confidence_band"],
    confidence_target: core.confidence_target as MarcDisclosure["confidence_target"],
    uncertainty_source: core.primary_source as MarcDisclosure["uncertainty_source"],
    recommended_next_step: core.recommended_next_step as string,
  };

  if (options.includeSelectedAction !== false) {
    disclosure.selected_action = core.selected_action as SelectedAction;
  }

  const disclosureResult = validateDisclosure(disclosure);
  if (!disclosureResult.valid) {
    throw new Error(
      `invalid MARC-Disclosure projection: ${disclosureResult.errors.join("; ")}`,
    );
  }
  return disclosure;
}
