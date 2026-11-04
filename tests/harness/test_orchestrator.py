import importlib.util
import shlex
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

SCRIPT = Path(__file__).resolve().parents[2] / "tools" / "orchestrate.py"
SPEC = importlib.util.spec_from_file_location("codeatlas_orchestrate", SCRIPT)
ORCH = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ORCH)


class OrchestratorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        ORCH.ARTIFACTS = Path(self.temp.name)
        self.feature = "sample-feature"
        self.folder = ORCH.feature_dir(self.feature)

    def test_rejects_unsafe_feature_slug(self):
        with self.assertRaises(ValueError):
            ORCH.feature_dir("../outside")

    def test_start_creates_plan_state(self):
        result = ORCH.cmd_start(SimpleNamespace(feature=self.feature))
        self.assertEqual(result, 0)
        self.assertEqual(ORCH.load_state(self.folder)["phase"], "plan")

    def test_cannot_advance_without_plan_artifacts(self):
        ORCH.cmd_start(SimpleNamespace(feature=self.feature))
        result = ORCH.cmd_advance(SimpleNamespace(feature=self.feature))
        self.assertEqual(result, 2)
        self.assertEqual(ORCH.load_state(self.folder)["phase"], "plan")

    def test_full_gated_workflow(self):
        ORCH.cmd_start(SimpleNamespace(feature=self.feature))
        for name in ORCH.REQUIRED["plan"]:
            (self.folder / name).write_text("approved plan evidence\n", encoding="utf-8")
        self.assertEqual(ORCH.cmd_advance(SimpleNamespace(feature=self.feature)), 0)

        for name in ORCH.REQUIRED["tests"]:
            (self.folder / name).write_text("test evidence\n", encoding="utf-8")
        self.assertEqual(ORCH.cmd_advance(SimpleNamespace(feature=self.feature)), 0)

        (self.folder / "test-review-report.md").write_text("Status: APPROVED\nAll tests trace to criteria.\n", encoding="utf-8")
        self.assertEqual(ORCH.cmd_advance(SimpleNamespace(feature=self.feature)), 0)
        self.assertEqual(ORCH.load_state(self.folder)["phase"], "red")

        marker = self.folder / "implemented.flag"
        code = f"from pathlib import Path; raise SystemExit(0 if Path({str(marker)!r}).exists() else 1)"
        command = f"{shlex.quote(sys.executable)} -c {shlex.quote(code)}"
        red_args = SimpleNamespace(feature=self.feature, frontend_cmd=command, backend_cmd=command)
        self.assertEqual(ORCH.cmd_verify_red(red_args), 0)
        self.assertEqual(ORCH.load_state(self.folder)["phase"], "implement")

        (self.folder / "frontend-implementation-report.md").write_text("FE implementation evidence\n", encoding="utf-8")
        (self.folder / "backend-implementation-report.md").write_text("BE implementation evidence\n", encoding="utf-8")
        self.assertEqual(ORCH.cmd_advance(SimpleNamespace(feature=self.feature)), 0)
        self.assertEqual(ORCH.load_state(self.folder)["phase"], "green")

        self.assertEqual(ORCH.cmd_verify_green(SimpleNamespace(feature=self.feature)), 2)
        marker.write_text("implemented", encoding="utf-8")
        self.assertEqual(ORCH.cmd_verify_green(SimpleNamespace(feature=self.feature)), 0)
        self.assertEqual(ORCH.load_state(self.folder)["phase"], "refactor")

        (self.folder / "refactor-report.md").write_text("Refactor evidence\n", encoding="utf-8")
        self.assertEqual(ORCH.cmd_advance(SimpleNamespace(feature=self.feature)), 0)
        (self.folder / "documentation-report.md").write_text("Docs evidence\n", encoding="utf-8")
        self.assertEqual(ORCH.cmd_advance(SimpleNamespace(feature=self.feature)), 0)

        (self.folder / "review-report.md").write_text("Status: APPROVED\nNo blocking findings.\n", encoding="utf-8")
        self.assertEqual(ORCH.cmd_advance(SimpleNamespace(feature=self.feature)), 0)
        (self.folder / "final-verification.md").write_text("Status: PASS\nChecks passed.\n", encoding="utf-8")
        self.assertEqual(ORCH.cmd_advance(SimpleNamespace(feature=self.feature)), 0)
        self.assertEqual(ORCH.load_state(self.folder)["phase"], "complete")


if __name__ == "__main__":
    unittest.main()
