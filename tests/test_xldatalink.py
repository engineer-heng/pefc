import datetime
import math
import os
import unittest

from xltab import XLDataLink


class TestXLDataLink(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.exedir = os.getcwd()
        # Location of file - should be at pefc\tests\data
        os.chdir(os.path.join(os.getcwd(), r'tests\data'))
        print('\nCurrent Directory = {}'.format(os.getcwd()))
        xl_name = r'efcbook.xlsx'
        cls.xldl = XLDataLink(xl_name, 1)

    @classmethod
    def tearDownClass(cls):
        # restore back executable dir
        os.chdir(cls.exedir)

    def test_funcs(self):
        print('\nClass Method Tests')
        res = XLDataLink.cref_coord('A1')
        print(res)
        self.assertEqual(res, (0, 0))
        res = XLDataLink.cref_coord('Sheet1!A10')
        print(res)
        self.assertEqual(res, (9, 0))
        res = XLDataLink.cref_num_index('Sheet1!A10')
        print(res)
        self.assertEqual(res, 8)
        res = XLDataLink.cref_coord('B100')
        print(res)
        self.assertEqual(res, (99, 1))
        res = XLDataLink.cref_coord('Sheet1!$Z$35')
        print(res)
        self.assertEqual(res, (34, 25))
        res = XLDataLink.cref_coord('zzzz1000')
        print(res)
        self.assertEqual(res, (999, 475253))
        res = XLDataLink.cref_coord('iv525')  # R525C256 = (524, 255) 0-based
        print(res)
        self.assertEqual(res, (524, 255))
        res = XLDataLink.cref_column_no('CD78')
        print(res)
        self.assertEqual(res, 81)
        res = XLDataLink.cref_row_no('CD78')
        print(res)
        self.assertEqual(res, 77)

    def test_sheet_name(self):
        print('\nSheet Name')
        res = self.xldl.sheet_name()
        print(res)
        self.assertEqual(res, 'Sheet2')

    def test_range_value(self):
        print('\nRange Values')
        res = self.xldl.range_value('B4:E34', ndim=2, empty='NA')
        rge = [[90.2, 113.8, 111.8, 104.4], [105.6, 98.8, 109.3, 113.5],
               [104.0, 84.5, 98.9, 97.0], [112.4, 86.2, 85.5, 106.5],
               [96.6, 'a string', 112.9, 96.8], [91.7, 101.3, 107.1, 101.2],
               [112.0, 97.9, 109.0, 95.2], [91.8, 98.0, 98.1, 79.2],
               [94.9, 87.1, datetime.date(2014, 9, 24), 112.7],
               [101.1, 104.0, 101.1, 102.7], [100.6, 83.3, 96.6, 88.5],
               [80.5, 95.0, 98.3, 113.6], [89.2, 93.9, 98.5, 106.7],
               [True, 96.8, 106.2, 90.0], [74.2, 104.3, 111.2, 108.7],
               [100.8, 106.0, 101.5, 108.8], [96.7, 101.3, 101.3, 95.1],
               [105.1, 92.0, 92.5, 95.0], [104.5, 94.5, 91.3, 82.7],
               [110.1, 110.7, 104.0, 115.6], ['NA', 'NA', 'NA', 'NA'],
               [116.9, 86.3, 96.4, 99.3], ['NA', 91.4, 96.5, 109.2],
               [112.2, 110.5, 98.3, 109.2], [88.8, 105.9, 63.0, 76.0],
               [98.6, 93.5, 106.2, 92.8], [99.1, 99.6, 83.6, 106.5],
               [90.5, math.nan, 82.6, 86.0], [106.7, 107.9, 109.9, 108.8],
               [87.4, 95.0, 108.5, 96.7], [112.7, 78.4, 112.8, math.nan]]
        print(res)
        self.assertEqual(res, rge)
        print('\nRange Single Dimension')
        res = self.xldl.range_value('B4:E34', ndim=1)
        rge = [90.2, 113.8, 111.8, 104.4, 105.6, 98.8, 109.3, 113.5, 104.0,
               84.5, 98.9, 97.0, 112.4, 86.2, 85.5, 106.5, 96.6, 'a string',
               112.9, 96.8, 91.7, 101.3, 107.1, 101.2, 112.0, 97.9, 109.0,
               95.2, 91.8, 98.0, 98.1, 79.2, 94.9, 87.1,
               datetime.date(2014, 9, 24), 112.7, 101.1, 104.0, 101.1, 102.7,
               100.6, 83.3, 96.6, 88.5, 80.5, 95.0, 98.3, 113.6, 89.2, 93.9,
               98.5, 106.7, True, 96.8, 106.2, 90.0, 74.2, 104.3, 111.2,
               108.7, 100.8, 106.0, 101.5, 108.8, 96.7, 101.3, 101.3,
               95.1, 105.1, 92.0, 92.5, 95.0, 104.5, 94.5, 91.3, 82.7,
               110.1, 110.7, 104.0, 115.6, math.nan, math.nan, math.nan,
               math.nan, 116.9, 86.3, 96.4, 99.3, math.nan, 91.4, 96.5,
               109.2, 112.2, 110.5, 98.3, 109.2, 88.8, 105.9, 63.0, 76.0,
               98.6, 93.5, 106.2, 92.8, 99.1, 99.6, 83.6, 106.5, 90.5,
               math.nan, 82.6, 86.0, 106.7, 107.9, 109.9, 108.8, 87.4,
               95.0, 108.5, 96.7, 112.7, 78.4, 112.8, math.nan]
        print(res)
        self.assertEqual(res, rge)

    def test_raw_range_value(self):
        print('\nRaw Range Values')
        res = self.xldl.raw_range_value('B4:E34')
        rge = [[90.2, 113.8, 111.8, 104.4], [105.6, 98.8, 109.3, 113.5],
               [104.0, 84.5, 98.9, 97.0], [112.4, 86.2, 85.5, 106.5],
               [96.6, 'a string', 112.9, 96.8], [91.7, 101.3, 107.1, 101.2],
               [112.0, 97.9, 109.0, 95.2], [91.8, 98.0, 98.1, 79.2],
               [94.9, 87.1, 41906.94993055556, 112.7],
               [101.1, 104.0, 101.1, 102.7],
               [100.6, 83.3, 96.6, 88.5], [80.5, 95.0, 98.3, 113.6],
               [89.2, 93.9, 98.5, 106.7], [1, 96.8, 106.2, 90.0],
               [74.2, 104.3, 111.2, 108.7], [100.8, 106.0, 101.5, 108.8],
               [96.7, 101.3, 101.3, 95.1], [105.1, 92.0, 92.5, 95.0],
               [104.5, 94.5, 91.3, 82.7], [110.1, 110.7, 104.0, 115.6],
               ['', '', '', ''], [116.9, 86.3, 96.4, 99.3],
               ['', 91.4, 96.5, 109.2], [112.2, 110.5, 98.3, 109.2],
               [88.8, 105.9, 63.0, 76.0], [98.6, 93.5, 106.2, 92.8],
               [99.1, 99.6, 83.6, 106.5], [90.5, 15, 82.6, 86.0],
               [106.7, 107.9, 109.9, 108.8], [87.4, 95.0, 108.5, 96.7],
               [112.7, 78.4, 112.8, 7]]
        print(res)
        self.assertEqual(res, rge)

    def test_cell_value(self):
        print('\nCell Value')
        res = self.xldl.cell_value(2, 1)
        print(res)
        self.assertEqual(res, 'X1')

    def test_cell_range_value(self):
        print('\nCell Range Value')
        res = self.xldl.cell_range_value(52, 1, 60, 1)
        rge = [74.2, 100.8, 96.7, 105.1, 104.5, 110.1, 116.9, 78.9, 112.2]
        print(res)
        self.assertEqual(res, rge)

    def test_get_cell_ref(self):
        print('\nget_cell_ref test')
        oval = XLDataLink.cref_coord('Sheet1!A10')
        print(oval)
        res = XLDataLink.get_cell_ref(*oval)
        print(res)
        self.assertEqual(res, 'A10')
        res = XLDataLink.get_cell_ref(*oval, True, True)
        print(res)
        self.assertEqual(res, '$A$10')
        oval = XLDataLink.cref_coord('iv525')  # R525C256 = (524, 255) 0-based
        print(oval)
        res = XLDataLink.get_cell_ref(*oval)
        print(res)
        self.assertEqual(res, 'IV525')
        oval = XLDataLink.cref_coord('ADZ2800')
        print(oval)
        res = XLDataLink.get_cell_ref(*oval)
        print(res)
        self.assertEqual(res, 'ADZ2800')
        oval = XLDataLink.cref_coord('zzzz1000')
        print(oval)
        res = XLDataLink.get_cell_ref(*oval)
        print(res)
        self.assertEqual(res, 'ZZZZ1000')

    def test_cref_abs(self):
        print('\nis_cref_row_abs and is_cref_col_abs tests')
        self.assertEqual(XLDataLink.is_cref_row_abs('Sheet5!$C$10'), True)
        self.assertEqual(XLDataLink.is_cref_row_abs('Sheet5!$C10'), False)
        self.assertEqual(XLDataLink.is_cref_row_abs('Z$15'), True)
        self.assertEqual(XLDataLink.is_cref_row_abs('$C11'), False)
        self.assertEqual(XLDataLink.is_cref_col_abs('Sheet5!$C10'), True)
        self.assertEqual(XLDataLink.is_cref_col_abs('Sheet5!C$10'), False)
        self.assertEqual(XLDataLink.is_cref_col_abs('$C11'), True)
        self.assertEqual(XLDataLink.is_cref_col_abs('Z15'), False)

    def test_misc(self):
        print("\nMiscellaneous Tests")
        # print str and repr
        print('str printout  = {}'.format(str(self.xldl)))
        print('repr printout = {}'.format(repr(self.xldl)))
        # inheritance tests
        print('XL File Name = {}'.format(self.xldl.file_name()))
        print('XL WS Name   = {}'.format(self.xldl.sheet_name()))
        print('XL WB Object = {}'.format(self.xldl.workbook()))
        print('XL WS Object = {}'.format(self.xldl.worksheet()))

        print('Error cell value')
        cerr = self.xldl.raw_range_value('E34')
        print('Error Value = {}'.format(cerr))

        print('\nTest for using workbook and sheet outside the class')
        curr_sht_name = self.xldl.sheet_name()
        self.xldl.sheet = 'Sheet5'
        sht = self.xldl.worksheet()
        col_ls = sht.col_values(1)
        print(col_ls)
        self.xldl.sheet = curr_sht_name  # reset to previous sheet


if __name__ == '__main__':
    unittest.main()
