import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for package in ("contracts", "spec_generator", "experiment_controller"):
    sys.path.insert(0, str(ROOT / "packages" / package / "src"))

from frontend_ai_contracts import UIContract
from spec_generator import load_condition

TASK = ROOT / "tasks" / "task-001"

class MvpTests(unittest.TestCase):
    def test_conditions_are_strictly_nested(self):
        artifacts = {name: set(load_condition(TASK, name).files) for name in "ABC"}
        self.assertLess(artifacts["A"], artifacts["B"])
        self.assertLess(artifacts["B"], artifacts["C"])

    def test_input_digest_is_deterministic(self):
        self.assertEqual(load_condition(TASK, "C").digest, load_condition(TASK, "C").digest)

    def test_ui_contract_rejects_unknown_navigation_target(self):
        with self.assertRaises(ValueError):
            UIContract.model_validate({
                "version": "1.0",
                "screens": [{
                    "id": "home", "route": "/", "purpose": "home",
                    "states": [{"name": "ready", "trigger": "load", "expected_ui": "home"}],
                    "navigates_to": ["missing"]
                }]
            })

if __name__ == "__main__":
    unittest.main()