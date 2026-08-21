"""Command-line interface for validating MARC JSON records."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence

from .validator import ValidationResult, validate_core, validate_disclosure


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="marc", description="Validate MARC JSON")
    subparsers = parser.add_subparsers(dest="command", required=True)
    validate = subparsers.add_parser("validate", help="validate a JSON record")
    validate.add_argument("path", type=Path, help="path to a MARC JSON object")
    validate.add_argument(
        "--profile",
        choices=("auto", "core", "disclosure"),
        default="auto",
        help="record profile (default: infer from fields)",
    )
    validate.add_argument(
        "--json", action="store_true", help="emit the structured validation result"
    )
    return parser


def _load(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _validate(record: object, profile: str) -> ValidationResult:
    if profile == "core":
        return validate_core(record)
    if profile == "disclosure":
        return validate_disclosure(record)
    if isinstance(record, dict) and "marc_version" not in record and "answer" in record:
        return validate_disclosure(record)
    return validate_core(record)


def _print_human(result: ValidationResult) -> None:
    print("VALID" if result.valid else "INVALID")
    if result.errors:
        for error in result.errors:
            print(f"- {error}")
    if result.warnings:
        print("WARNINGS")
        for warning in result.warnings:
            print(f"- {warning}")


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI and return a process exit status."""

    args = _parser().parse_args(argv)
    try:
        record = _load(args.path)
    except (OSError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2

    result = _validate(record, args.profile)
    if args.json:
        print(json.dumps(result.as_dict(), indent=2))
    else:
        _print_human(result)
    return 0 if result.valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
