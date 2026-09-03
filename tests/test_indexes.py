import unittest

from scripts.rebuild_indexes import build


class IndexTests(unittest.TestCase):
    def test_catalog_covers_structured_records(self):
        catalog, relations, search = build()
        self.assertGreater(len(catalog), 0)
        self.assertEqual({x["id"] for x in catalog}, {x["id"] for x in search})

    def test_relations_point_to_existing_ids(self):
        catalog, relations, _ = build()
        ids = {x["id"] for x in catalog}
        for rel in relations:
            self.assertIn(rel["from"], ids)
            self.assertIn(rel["to"], ids)


if __name__ == "__main__":
    unittest.main()
