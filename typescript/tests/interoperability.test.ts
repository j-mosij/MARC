import { spawnSync } from "node:child_process";
import { readFileSync } from "node:fs";
import { delimiter, join } from "node:path";
import { describe, expect, test } from "vitest";

import { validateCore } from "../src/validator.js";
import type { ValidationResult } from "../src/types.js";

interface Vector {
  name: string;
  record: unknown;
  expected_valid: boolean;
  expected_errors: string[];
  expected_warnings: string[];
}

interface NamedResult extends ValidationResult {
  name: string;
}

const root = process.cwd();
const vectors = JSON.parse(
  readFileSync(join(root, "interoperability", "vectors.json"), "utf8"),
) as Vector[];
const expected = JSON.parse(
  readFileSync(join(root, "interoperability", "expected-results.json"), "utf8"),
) as NamedResult[];

function typescriptResults(): NamedResult[] {
  return vectors.map((vector) => ({ name: vector.name, ...validateCore(vector.record) }));
}

function pythonResults(): NamedResult[] {
  const program = [
    "import json",
    "from pathlib import Path",
    "from marc import validate_core",
    "vectors = json.loads(Path('interoperability/vectors.json').read_text(encoding='utf-8'))",
    "results = [dict(name=v['name'], **validate_core(v['record']).as_dict()) for v in vectors]",
    "print(json.dumps(results))",
  ].join("; ");
  const pythonPath = [join(root, "python"), process.env.PYTHONPATH]
    .filter((value): value is string => Boolean(value))
    .join(delimiter);
  const result = spawnSync(process.env.PYTHON ?? "python3", ["-c", program], {
    cwd: root,
    encoding: "utf8",
    env: { ...process.env, PYTHONPATH: pythonPath },
  });
  if (result.status !== 0) {
    throw new Error(`Python interoperability runner failed: ${result.stderr}`);
  }
  return JSON.parse(result.stdout) as NamedResult[];
}

describe("common interoperability vectors", () => {
  test("TypeScript matches each vector's declared result", () => {
    for (const vector of vectors) {
      expect(validateCore(vector.record), vector.name).toEqual({
        valid: vector.expected_valid,
        errors: vector.expected_errors,
        warnings: vector.expected_warnings,
      });
    }
  });

  test("TypeScript matches the canonical result set", () => {
    expect(typescriptResults()).toEqual(expected);
  });

  test("Python and TypeScript results agree exactly", () => {
    expect(typescriptResults()).toEqual(pythonResults());
  });
});
