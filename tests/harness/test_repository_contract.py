import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
class HarnessContractTests(unittest.TestCase):
    def test_required_docs_exist(self):
        for item in ["AGENTS.md","docs/PRODUCT_REQUIREMENTS.md","docs/ARCHITECTURE.md","docs/ACCEPTANCE_CRITERIA.md","docs/SECURITY_AND_DATA_POLICY.md","docs/SELF_HEALING.md","docs/DEFINITION_OF_DONE.md"]:
            with self.subTest(item=item): self.assertTrue((ROOT/item).is_file())
    def test_self_healing_is_bounded(self):
        text=(ROOT/"docs/SELF_HEALING.md").read_text().lower()
        self.assertIn("three",text)
        self.assertIn("never delete",text)
    def test_platform_policy_is_explicit(self):
        text=(ROOT/"docs/SECURITY_AND_DATA_POLICY.md").read_text().lower()
        self.assertIn("scrape",text); self.assertIn("session cookies",text)
    def test_skills_and_roles_exist(self):
        for item in [".agents/skills/plan-task/SKILL.md",".agents/skills/self-heal/SKILL.md",".agents/agents/planner.md",".agents/agents/reviewer.md"]:
            with self.subTest(item=item): self.assertTrue((ROOT/item).is_file())

    def test_copilot_agent_profiles_exist(self):
        for item in [
            ".github/agents/codeatlas-orchestrator.agent.md",
            ".github/agents/codeatlas-planner.agent.md",
            ".github/agents/codeatlas-fe-test-engineer.agent.md",
            ".github/agents/codeatlas-be-test-engineer.agent.md",
            ".github/agents/codeatlas-test-reviewer.agent.md",
            ".github/agents/codeatlas-fe-implementer.agent.md",
            ".github/agents/codeatlas-be-implementer.agent.md",
            ".github/agents/codeatlas-documentation-engineer.agent.md",
            ".github/agents/codeatlas-independent-reviewer.agent.md",
        ]:
            with self.subTest(item=item):
                self.assertTrue((ROOT / item).is_file())
\nif __name__=="__main__": unittest.main()
