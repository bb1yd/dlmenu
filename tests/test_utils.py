import datetime
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import utils  # noqa: E402


class UtilsTest(unittest.TestCase):
    def test_width_counts_cjk_as_two(self):
        self.assertEqual(utils.width("米饭"), 4)
        self.assertEqual(utils.width("rice"), 4)

    def test_allergen_filters(self):
        self.assertEqual(utils.parse_allergen_filters(["花生", "shrimp", "3"]), {23, 32, 3})
        self.assertEqual(utils.parse_allergen_filters(["花生,虾"]), {23, 32})

    def test_school_alias(self):
        self.assertEqual(utils.resolve_school("primary"), "小学")
        self.assertEqual(utils.resolve_school("中学"), "中学")

    def test_week_for_fetches_weeks_once(self):
        orig_list, orig_probe = utils.list_weeks, utils.probe_week
        self.addCleanup(setattr, utils, "list_weeks", orig_list)
        self.addCleanup(setattr, utils, "probe_week", orig_probe)
        calls = []
        sample = [{"id": 149, "start": datetime.date(2026, 11, 9), "end": datetime.date(2026, 11, 15)}]
        probed = {"id": 150, "start": datetime.date(2026, 11, 16), "end": datetime.date(2026, 11, 22)}

        def fake_list():
            calls.append("list")
            return sample

        def fake_probe(date, weeks=None):
            calls.append(("probe", weeks))
            return probed

        utils.list_weeks = fake_list
        utils.probe_week = fake_probe
        self.assertEqual(utils.week_for(datetime.date(2026, 11, 18)), probed)
        self.assertEqual(calls, ["list", ("probe", sample)])


if __name__ == "__main__":
    unittest.main()
