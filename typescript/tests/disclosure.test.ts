import { readFileSync } from "node:fs";
import { join } from "node:path";
import { describe, expect, test } from "vitest";

import { projectDisclosure } from "../src/disclosure.js";
import { validateDisclosure } from "../src/validator.js";

const answerRecord = JSON.parse(
  readFileSync(join(process.cwd(), "examples", "valid", "answer.json"), "utf8"),
) as Record<string, unknown>;

describe("MARC-Disclosure", () => {
  test("projects deterministic public fields without numeric scores", () => {
    const disclosure = projectDisclosure(
      answerRecord,
      "The documented behavior is supported.",
    );
    expect(disclosure).toEqual({
      answer: "The documented behavior is supported.",
      confidence_band: "high",
      confidence_target: "answer",
      uncertainty_source: "missing_evidence",
      recommended_next_step: "review the cited sources",
      selected_action: "ANSWER",
    });
    expect(validateDisclosure(disclosure).valid).toBe(true);
    expect(disclosure).not.toHaveProperty("pre_capability");
    expect(disclosure).not.toHaveProperty("post_answer_confidence");
    expect(disclosure).not.toHaveProperty("uncertainty");
  });

  test("can omit the optional selected action", () => {
    const disclosure = projectDisclosure(answerRecord, "A concise answer.", {
      includeSelectedAction: false,
    });
    expect(disclosure).not.toHaveProperty("selected_action");
    expect(validateDisclosure(disclosure).valid).toBe(true);
  });

  test("rejects an invalid source record", () => {
    expect(() =>
      projectDisclosure({ ...answerRecord, primary_source: "none" }, "An answer"),
    ).toThrow("invalid MARC-Core record");
  });
});
