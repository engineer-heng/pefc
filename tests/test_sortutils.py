import unittest
from pefc.sortutils import AlphaNum, sort_by_month


class TestSortUtils(unittest.TestCase):

    def test_alphanum(self):

        test_strings = ["1000X Radonius Maximus", "10X Radonius",
                        "200X Radonius", "20X Radonius",
                        "20X Radonius Prime", "30X Radonius", "40X Radonius",
                        "Allegia 50 Clasteron", "Allegia 500 Clasteron",
                        "Allegia 51 Clasteron", "Allegia 51B Clasteron",
                        "Allegia 52 Clasteron", "Allegia 60 Clasteron",
                        "Alpha 100", "Alpha 2", "Alpha 200", "Alpha 2A",
                        "Alpha 2A-8000", "Alpha 2A-900", "Callisto Morphamax",
                        "Callisto Morphamax 500", "Callisto Morphamax 5000",
                        "Callisto Morphamax 600", "Callisto Morphamax 700",
                        "Callisto Morphamax 7000",
                        "Callisto Morphamax 7000 SE",
                        "Callisto Morphamax 7000 SE2",
                        "QRS-60 Intrinsia Machine",
                        "QRS-60F Intrinsia Machine",
                        "QRS-62 Intrinsia Machine",
                        "QRS-62F Intrinsia Machine",
                        "Xiph Xlater 10000", "Xiph Xlater 2000",
                        "Xiph Xlater 300", "Xiph Xlater 40", "Xiph Xlater 5",
                        "Xiph Xlater 50", "Xiph Xlater 500",
                        "Xiph Xlater 5000", "Xiph Xlater 58"]

        test_strings.sort(key=AlphaNum)
        ans = ['10X Radonius', '20X Radonius', '20X Radonius Prime',
               '30X Radonius', '40X Radonius',
               '200X Radonius', '1000X Radonius Maximus',
               'Allegia 50 Clasteron', 'Allegia 51 Clasteron',
               'Allegia 51B Clasteron', 'Allegia 52 Clasteron',
               'Allegia 60 Clasteron', 'Allegia 500 Clasteron', 'Alpha 2',
               'Alpha 2A', 'Alpha 2A-900', 'Alpha 2A-8000', 'Alpha 100',
               'Alpha 200', 'Callisto Morphamax', 'Callisto Morphamax 500',
               'Callisto Morphamax 600', 'Callisto Morphamax 700',
               'Callisto Morphamax 5000', 'Callisto Morphamax 7000',
               'Callisto Morphamax 7000 SE', 'Callisto Morphamax 7000 SE2',
               'QRS-60 Intrinsia Machine', 'QRS-60F Intrinsia Machine',
               'QRS-62 Intrinsia Machine', 'QRS-62F Intrinsia Machine',
               'Xiph Xlater 5', 'Xiph Xlater 40', 'Xiph Xlater 50',
               'Xiph Xlater 58', 'Xiph Xlater 300', 'Xiph Xlater 500',
               'Xiph Xlater 2000', 'Xiph Xlater 5000', 'Xiph Xlater 10000']
        print(test_strings)
        self.assertEqual(test_strings, ans)

    def test_sort_by_month(self):

        res = ['APR 16.xls', ' FEB 16.xls', 'JAN 16.xls', 'NOV  16.xls',
               'OCT 16.xls', 'MAY 16.xls', 'JUL 16.xls', 'AUG-16.xls',
               'MAR_16.xls', 'SEP 16.xls',
               'JUN 16.xls', 'DEC 16.xls', 'test_no_month.xls']
        res = sort_by_month(res)
        ans = ['JAN 16.xls', ' FEB 16.xls', 'MAR_16.xls', 'APR 16.xls',
               'MAY 16.xls', 'JUN 16.xls', 'JUL 16.xls', 'AUG-16.xls',
               'SEP 16.xls', 'OCT 16.xls', 'NOV  16.xls', 'DEC 16.xls',
               'test_no_month.xls']
        print(res)
        self.assertEqual(res, ans)


if __name__ == '__main__':
    unittest.main()
