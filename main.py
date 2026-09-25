from __future__ import annotations
import argparse, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
for package in ("contracts", "spec_generator", "experiment_controller"):
    sys.path.insert(0, str(ROOT / "packages" / package / "src"))
from experiment_controller.cli import run_dry_run, validate_project

def main() -> int:
    parser = argparse.ArgumentParser(description="Frontend specification experiment MVP")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("validate")
    dry_run = commands.add_parser("dry-run")
    dry_run.add_argument("--task", default="task-001")
    dry_run.add_argument("--conditions", nargs="+", choices=("A", "B", "C"), default=["A", "B", "C"])
    args = parser.parse_args()
    validate_project(ROOT) if args.command == "validate" else run_dry_run(ROOT, args.task, args.conditions)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())