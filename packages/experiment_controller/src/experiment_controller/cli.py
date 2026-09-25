from __future__ import annotations
import hashlib, json
from datetime import UTC, datetime
from pathlib import Path
from frontend_ai_contracts import TaskDefinition
from spec_generator import LoadedCondition, load_condition

def _task(root: Path, task_id: str) -> tuple[Path, TaskDefinition]:
    task_dir = root / "tasks" / task_id
    definition = TaskDefinition.model_validate_json((task_dir / "task.json").read_text(encoding="utf-8"))
    return task_dir, definition

def validate_project(root: Path) -> None:
    task_dir, definition = _task(root, "task-001")
    loaded = {name: load_condition(task_dir, name) for name in "ABC"}
    sets = {name: set(item.files) for name, item in loaded.items()}
    if not sets["A"] < sets["B"] < sets["C"]:
        raise ValueError("conditions must be strict supersets: A < B < C")
    print(f"Validated {definition.id}: " + ", ".join(f"{name}={len(item.files)} artifacts" for name, item in loaded.items()))

def _mock_generate(condition: LoadedCondition, workspace: Path) -> dict[str, object]:
    workspace.mkdir(parents=True)
    html = ("<!doctype html><html><head><meta charset='utf-8'><title>MVP probe</title></head>"
            "<body><main><h1>Experiment pipeline probe</h1>"
            f"<p data-condition='{condition.manifest.condition}'>Condition {condition.manifest.condition}</p>"
            "</main></body></html>")
    (workspace / "index.html").write_text(html, encoding="utf-8")
    return {"mode": "mock", "visible_artifacts": sorted(condition.files), "workspace_sha256": hashlib.sha256(html.encode()).hexdigest()}

def _evaluate(workspace: Path) -> dict[str, object]:
    html = (workspace / "index.html").read_text(encoding="utf-8").lower()
    checks = {"has_document": "<!doctype html>" in html, "has_main_landmark": "<main" in html, "declares_charset": "charset=" in html}
    return {"evaluator": "mvp-static-smoke", "checks": checks, "passed": all(checks.values())}

def _snapshot(run_dir: Path, condition: LoadedCondition) -> None:
    for relative_name, content in condition.files.items():
        destination = run_dir / "input" / relative_name
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(content)

def run_dry_run(root: Path, task_id: str, conditions: list[str]) -> None:
    task_dir, definition = _task(root, task_id)
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%S.%fZ")
    experiment_dir = root / "runs" / f"dry-run-{stamp}"
    experiment_dir.mkdir(parents=True)
    for index, name in enumerate(conditions, start=1):
        loaded = load_condition(task_dir, name)
        run_dir = experiment_dir / f"{index:02d}-{name}"
        _snapshot(run_dir, loaded)
        generation = _mock_generate(loaded, run_dir / "workspace")
        evaluation = _evaluate(run_dir / "workspace")
        manifest = {"schema_version": 1, "experiment_mode": "mock-dry-run", "research_data": False,
                    "task_id": definition.id, "condition": name, "input_sha256": loaded.digest,
                    "created_at": datetime.now(UTC).isoformat(), "generation": generation}
        (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        (run_dir / "evaluation.json").write_text(json.dumps(evaluation, indent=2), encoding="utf-8")
        print(f"{name}: {'PASS' if evaluation['passed'] else 'FAIL'} -> {run_dir}")
    print(f"Dry-run complete: {experiment_dir}")