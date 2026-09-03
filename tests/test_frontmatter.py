import unittest

from scripts.common import ROOT, load_records


class FrontmatterTests(unittest.TestCase):
    def test_structured_records_have_unique_ids(self):
        records = load_records()
        ids = [r["data"].get("id") for r in records]
        self.assertGreater(len(ids), 0)
        self.assertEqual(len(ids), len(set(ids)))

    def test_decision_trace_is_summarized_not_private_cot(self):
        trace = ROOT / "reflections/2026/09/TRACE-2026-000001-v2-architecture.md"
        record = next(r for r in load_records() if r["file"] == trace)
        self.assertIn(record["data"]["reasoning_visibility"], {"summarized", "exposed", "unavailable"})


if __name__ == "__main__":
    unittest.main()
