import { readFileSync, readdirSync } from "node:fs";
import { join } from "node:path";
import { describe, expect, test } from "vitest";

import { validateCore } from "../src/validator.js";

const root = process.cwd();

function load(path: string): unknown {
  return JSON.parse(readFileSync(path, "utf8"));
}

describe("validateCore", () => {
  test("accepts every positive example without warnings", () => {
    const directory = join(root, "examples", "valid");
    for (const filename of readdirSync(directory).sort()) {
      const result = validateCore(load(join(directory, filename)));
      expect(result, filename).toEqual({ valid: true, errors: [], warnings: [] });
    }
  });

  test("rejects every negative example", () => {
    const directory = join(root, "examples", "invalid");
    for (const filename of readdirSync(directory).sort()) {
      const result = validateCore(load(join(directory, filename)));
      expect(result.valid, filename).toBe(false);
      expect(result.errors.length, filename).toBeGreaterThan(0);
    }
  });

  test("reports SHOULD mismatches as warnings", () => {
    const record = load(join(root, "examples", "valid", "retrieve.json")) as Record<
      string,
      unknown
    >;
    record.remediability = "none";
    expect(validateCore(record)).toEqual({
      valid: true,
      errors: [],
      warnings: ['remediability should be "retrieval" for RETRIEVE'],
    });
  });

  test("does not require uncertainty scores to sum to one", () => {
    const record = load(join(root, "examples", "valid", "clarify.json")) as {
      uncertainty: Record<string, number>;
    };
    const total = Object.values(record.uncertainty).reduce((sum, value) => sum + value, 0);
    expect(total).toBeGreaterThan(1);
    expect(validateCore(record).valid).toBe(true);
  });

  test("accepts x_ extensions and rejects unknown standard fields", () => {
    const record = load(join(root, "examples", "valid", "answer.json")) as Record<
      string,
      unknown
    >;
    record.x_deployment_trace = { opaque: true };
    expect(validateCore(record).valid).toBe(true);
    record.future_field = true;
    expect(validateCore(record).errors).toContain("unknown field: future_field");
  });
});
