import json
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.config import COURSE_SELECTION_PATH, PLAN_PATH, SUMMARY_PATH
from src.pipeline import run_pipeline


class PipelineTestCase(unittest.TestCase):
    def test_pipeline_generates_artifacts(self):
        summary = run_pipeline()
        self.assertTrue(COURSE_SELECTION_PATH.exists())
        self.assertTrue(PLAN_PATH.exists())
        self.assertTrue(SUMMARY_PATH.exists())
        self.assertEqual(summary["selected_courses"], 6)
        plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
        self.assertEqual(len(plan["weekly_plan"]), 6)


if __name__ == "__main__":
    unittest.main()

