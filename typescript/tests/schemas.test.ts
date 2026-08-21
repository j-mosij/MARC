import { readFileSync, readdirSync } from "node:fs";
import { join } from "node:path";
import Ajv2020 from "ajv/dist/2020.js";
import { describe, expect, test } from "vitest";

const root = process.cwd();

function load(path: string): unknown {
  return JSON.parse(readFileSync(path, "utf8"));
}

describe("JSON Schemas", () => {
  const ajv = new Ajv2020({ allErrors: true, strict: true });
  const core = ajv.compile(load(join(root, "schemas", "marc-core.schema.json")));
  const disclosure = ajv.compile(
    load(join(root, "schemas", "marc-disclosure.schema.json")),
  );

  test("compile as JSON Schema 2020-12", () => {
    expect(core).toBeTypeOf("function");
    expect(disclosure).toBeTypeOf("function");
  });

  test("core schema accepts every positive example", () => {
    const directory = join(root, "examples", "valid");
    for (const filename of readdirSync(directory).sort()) {
      expect(core(load(join(directory, filename))), filename).toBe(true);
    }
  });

  test("core schema rejects every negative example", () => {
    const directory = join(root, "examples", "invalid");
    for (const filename of readdirSync(directory).sort()) {
      expect(core(load(join(directory, filename))), filename).toBe(false);
    }
  });

  test("disclosure schema accepts the projected shape", () => {
    expect(
      disclosure({
        answer: "The result is available.",
        confidence_band: "high",
        confidence_target: "answer",
        uncertainty_source: "missing_evidence",
        recommended_next_step: "review the supporting evidence",
        selected_action: "ANSWER",
      }),
    ).toBe(true);
  });
});
