from __future__ import annotations
import hashlib, json
from dataclasses import dataclass
from pathlib import Path
from frontend_ai_contracts import ConditionManifest, UIContract, UserStory

@dataclass(frozen=True)
class LoadedCondition:
    manifest: ConditionManifest
    files: dict[str, bytes]

    @property
    def digest(self) -> str:
        digest = hashlib.sha256()
        for name, content in sorted(self.files.items()):
            digest.update(name.encode())
            digest.update(b"\0")
            digest.update(content)
        return digest.hexdigest()

def load_condition(task_dir: Path, condition: str) -> LoadedCondition:
    manifest_path = task_dir / "conditions" / condition / "input-manifest.json"
    manifest = ConditionManifest.model_validate_json(manifest_path.read_text(encoding="utf-8"))
    files: dict[str, bytes] = {}
    for relative_name in manifest.artifacts:
        path = task_dir / relative_name
        if not path.is_file():
            raise FileNotFoundError(f"manifest references missing artifact: {path}")
        files[relative_name] = path.read_bytes()
    if "conditions/B/user-stories.json" in files:
        for story in json.loads(files["conditions/B/user-stories.json"]):
            UserStory.model_validate(story)
    if "conditions/C/ui-contract.json" in files:
        UIContract.model_validate_json(files["conditions/C/ui-contract.json"])
    return LoadedCondition(manifest=manifest, files=files)