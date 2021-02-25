import unittest
from models37 import *
from datetime import date, datetime


class TestParse(unittest.TestCase):
    _data = [
        (False, TypeError), (True, TypeError),
        (-1, TypeError), (0, TypeError), (1, TypeError),
        ("-1", TypeError), ("0", TypeError), ("1", TypeError),
        ("-1.", TypeError), ("0.", TypeError), ("1.", TypeError),
        ("-1.0", TypeError), ("0.0", TypeError), ("1.0", TypeError),
        ("-.5", TypeError), (".5", TypeError), ("-1.5", TypeError), ("1.5", TypeError),
        ("inf", TypeError), ("-inf", TypeError),
        ("True", TypeError), ("False", TypeError),
        ("", TypeError), ("x", TypeError), ("abcd", TypeError),
        ("2021-02-23T09:34:26.976720", TypeError),
        ("2021-02-23", TypeError),
        (datetime(2021, 2, 23, 9, 34, 26, 976720), TypeError),
        (date(2021, 2, 23), TypeError),
    ]

    def test_to_bool(self):
        parse = Parse.to_bool
        data = [
            (False, False), (True, True),
            (-1, True), (0, False), (1, True),
            ("-1", TypeError), ("0", TypeError), ("1", TypeError),
            ("-1.", TypeError), ("0.", TypeError), ("1.", TypeError),
            ("-1.0", TypeError), ("0.0", TypeError), ("1.0", TypeError),
            ("-.5", TypeError), (".5", TypeError), ("-1.5", TypeError), ("1.5", TypeError),
            ("inf", TypeError), ("-inf", TypeError),
            ("True", True), ("False", False),
            ("", TypeError), ("x", TypeError), ("abcd", TypeError),
            ("2021-02-23T09:34:26.976720", TypeError),
            ("2021-02-23", TypeError),
            (datetime(2021, 2, 23, 9, 34, 26, 976720), TypeError),
            (date(2021, 2, 23), TypeError),
        ]

        for value, result in data:
            if result is TypeError:
                self.assertRaises(result, parse, value)
            else:
                self.assertEqual(result, parse(value))

    def test_to_int(self):
        parse = Parse.to_int
        data = [
            (False, 0), (True, 1),
            (-1, -1), (0, 0), (1, 1),
            ("-1", -1), ("0", 0), ("1", 1),
            ("-1.", -1), ("0.", 0), ("1.", 1),
            ("-1.0", -1), ("0.0", 0), ("1.0", 1),
            ("-.5", TypeError), (".5", TypeError), ("-1.5", TypeError), ("1.5", TypeError),
            ("inf", TypeError), ("-inf", TypeError),
            ("True", TypeError), ("False", TypeError),
            ("", TypeError), ("x", TypeError), ("abcd", TypeError),
            ("2021-02-23T09:34:26.976720", TypeError),
            ("2021-02-23", TypeError),
            (datetime(2021, 2, 23, 9, 34, 26, 976720), TypeError),
            (date(2021, 2, 23), TypeError),
        ]

        for value, result in data:
            if result is TypeError:
                self.assertRaises(result, parse, value)
            else:
                self.assertEqual(result, parse(value))

    def test_to_float(self):
        parse = Parse.to_float
        data = [
            (False, 0.0), (True, 1.0),
            (-1, -1.0), (0, 0.0), (1, 1.0),
            ("-1", -1.0), ("0", 0.0), ("1", 1.0),
            ("-1.", -1.0), ("0.", 0.0), ("1.", 1.0),
            ("-1.0", -1.0), ("0.0", 0.0), ("1.0", 1.0),
            ("-.5", -0.5), (".5", 0.5), ("-1.5", -1.5), ("1.5", 1.5),
            ("inf", float("inf")), ("-inf", float("-inf")),
            ("True", TypeError), ("False", TypeError),
            ("", TypeError), ("x", TypeError), ("abcd", TypeError),
        ]

        for value, result in data:
            if result is TypeError:
                self.assertRaises(result, parse, value)
            else:
                self.assertEqual(result, parse(value))

    def test_to_str(self):
        parse = Parse.to_str
        data = [
            (False, "False"), (True, "True"),
            (-1, "-1"), (0, "0"), (1, "1"),
            ("-1", "-1"), ("0", "0"), ("1", "1"),
            ("-1.", "-1."), ("0.", "0."), ("1.", "1."),
            ("-1.0", "-1.0"), ("0.0", "0.0"), ("1.0", "1.0"),
            ("-.5", "-.5"), (".5", ".5"), ("-1.5", "-1.5"), ("1.5", "1.5"),
            ("inf", "inf"), ("-inf", "-inf"),
            ("True", "True"), ("False", "False"),
            ("", ""), ("x", "x"), ("abcd", "abcd"),
            ("2021-02-23T09:34:26.976720", "2021-02-23T09:34:26.976720"),
            ("2021-02-23", "2021-02-23"),
            (datetime(2021, 2, 23, 9, 34, 26, 976720), "2021-02-23T09:34:26.976720"),
            (date(2021, 2, 23), "2021-02-23"),
        ]

        for value, result in data:
            if result is TypeError:
                self.assertRaises(result, parse, value)
            else:
                self.assertEqual(result, parse(value))

    def test_to_date(self):
        parse = Parse.to_date
        data = [
            (False, TypeError), (True, TypeError),
            (-1, TypeError), (0, TypeError), (1, TypeError),
            ("-1", TypeError), ("0", TypeError), ("1", TypeError),
            ("-1.", TypeError), ("0.", TypeError), ("1.", TypeError),
            ("-1.0", TypeError), ("0.0", TypeError), ("1.0", TypeError),
            ("-.5", TypeError), (".5", TypeError), ("-1.5", TypeError), ("1.5", TypeError),
            ("inf", TypeError), ("-inf", TypeError),
            ("True", TypeError), ("False", TypeError),
            ("", TypeError), ("x", TypeError), ("abcd", TypeError),
            ("2021-02-23T09:34:26.976720", date(2021, 2, 23)),
            ("2021-02-23", date(2021, 2, 23)),
            (datetime(2021, 2, 23, 9, 34, 26, 976720), date(2021, 2, 23)),
            (date(2021, 2, 23), date(2021, 2, 23)),
        ]

        for value, result in data:
            if result is TypeError:
                self.assertRaises(result, parse, value)
            else:
                self.assertEqual(result, parse(value))

    def test_to_datetime(self):
        parse = Parse.to_datetime
        data = [
            (False, TypeError), (True, TypeError),
            (-1, TypeError), (0, TypeError), (1, TypeError),
            ("-1", TypeError), ("0", TypeError), ("1", TypeError),
            ("-1.", TypeError), ("0.", TypeError), ("1.", TypeError),
            ("-1.0", TypeError), ("0.0", TypeError), ("1.0", TypeError),
            ("-.5", TypeError), (".5", TypeError), ("-1.5", TypeError), ("1.5", TypeError),
            ("inf", TypeError), ("-inf", TypeError),
            ("True", TypeError), ("False", TypeError),
            ("", TypeError), ("x", TypeError), ("abcd", TypeError),
            ("2021-02-23T09:34:26.976720", datetime(2021, 2, 23, 9, 34, 26, 976720)),
            ("2021-02-23", datetime(2021, 2, 23, 0, 0, 0)),
            (datetime(2021, 2, 23, 9, 34, 26, 976720), datetime(2021, 2, 23, 9, 34, 26, 976720)),
            (date(2021, 2, 23), datetime(2021, 2, 23, 0, 0, 0)),
        ]

        for value, result in data:
            if result is TypeError:
                self.assertRaises(result, parse, value)
            else:
                self.assertEqual(result, parse(value))


class TestModel(unittest.TestCase):
    def test_001(self):
        """
            Verify that we can access the model by it's name
        """

        class A(Model):
            pass

        self.assertIs(ModelHandler.models.get("A"), A)

        ModelHandler.models.remove(A)

    def test_002(self):
        """
            Verify that we can overwrite a model by creating a new one with the same name
        """

        class B(Model):
            pass

        old_B = B

        class B(Model):
            pass

        self.assertIs(ModelHandler.models.get("B"), B)
        self.assertIsNot(ModelHandler.models.get("B"), old_B)
        self.assertNotIn(old_B, ModelHandler.models)

        ModelHandler.models.remove(B)

    def test_003(self):
        """
            Verify that we can't overwrite the Model class
        """
        try:
            exec("class Model(Model):\n\tpass")

            raise Exception
        except ModelOverwriteError:
            pass


if __name__ == '__main__':
    unittest.main()
