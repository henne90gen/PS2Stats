import unittest
from helper import *


class TestClasses(unittest.TestCase):
    def test_remove_duplicate_separators(self):
        self.assertEqual(remove_duplicate_separators("a||abc|||ab||||abcd", "|"), "a|abc|ab|abcd")
        self.assertEqual(remove_duplicate_separators("a||abc|||ab||||", "|"), "a|abc|ab|")
        self.assertEqual(remove_duplicate_separators("||abc|||ab||||abcd", "|"), "|abc|ab|abcd")

    def test_string_to_dict(self):
        self.assertEqual(string_to_dict("abc|123"), {"abc": "123"})
        self.assertEqual(string_to_dict("abc|123|cde|2g4"), {"abc": "123", "cde": "2g4"})
        self.assertEqual(string_to_dict("abc|123|"), {"abc": "123"})

    def test_time_to_mins(self):
        self.assertEqual(time_to_mins("1d"), 24 * 60)
        self.assertEqual(time_to_mins("1h"), 60)
        self.assertEqual(time_to_mins("5d15h"), (24 * 5 + 15) * 60)
        self.assertEqual(time_to_mins("13d1h"), (24 * 13 + 1) * 60)

    def test_dict_string_to_number(self):
        self.assertEqual(dict_string_to_number({"abc": "123"}), {"abc": 123})
        self.assertEqual(dict_string_to_number({"abc": "123_"}), {"abc": 123})
        self.assertEqual(dict_string_to_number({"abc": "123%"}), {"abc": 123})
        self.assertEqual(dict_string_to_number({"abc": "12.3%"}), {"abc": 12.3})
        self.assertEqual(dict_string_to_number({"abc": "1,123"}), {"abc": 1123})
        self.assertEqual(dict_string_to_number({"abc": "12.3"}), {"abc": 12.3})

    def test_remove_duplicates(self):
        self.assertEqual(remove_duplicates(["hello", "hello", "goodbye"]), ["hello", "goodbye"])
        self.assertEqual(remove_duplicates(["hello", "hello", "goodbye", "hello"]), ["hello", "goodbye"])
        self.assertEqual(remove_duplicates(["hello", "hello"]), ["hello"])

    def test_sort_rows(self):
        self.assertEqual(sort_rows([["Name"], ["b"], ["a"], ["Avg"]], 1, 2), [["Name"], ["a"], ["b"], ["Avg"]])
        self.assertEqual(sort_rows([["Name"], ["Swooshed"], ["halospud"], ["Bilowan"], ["Avg"]], 1, 3),
                         [["Name"], ["Bilowan"], ["halospud"], ["Swooshed"], ["Avg"]])

    def test_get_month_data(self):
        get_month_data("HenneGamer")
