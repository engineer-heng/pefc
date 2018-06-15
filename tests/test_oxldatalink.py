import datetime
import math
import os
import unittest

from xltab import OXLDataLink, XLDataLink


class TestOXLDataLink(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.exedir = os.getcwd()
        # Location of file - should be at pefc\tests\data
        os.chdir(os.path.join(cls.exedir, r'tests\data'))
        print('\nCurrent Directory = {}'.format(os.getcwd()))
        xl_name = r'efcbook.xlsx'
        # Both OXLDataLink and XLDataLink are tested with results
        # compared to each other
        cls.oxldl = OXLDataLink(xl_name)
        cls.xldl = XLDataLink(xl_name)

    @classmethod
    def tearDownClass(cls):
        # restore back executable dir
        os.chdir(cls.exedir)

    def test_tab_form(self):
        # test using results from xltab.XLDataLink object
        self.oxldl.sheet = 0  # make sure it is first sheet
        print('\ntab_form Tests')
        # list test
        cell_ls = ['A13', 'B13', 'C13', 'D13', None, 'E13',
                   'F13', 'G13', 'H13', 'I13', 'J13', 'A34:I34']
        res_ls = self.oxldl.tab_form(
            cell_ls, opt_date=datetime.date, opt_empty='NA')
        print(res_ls)
        data_ls = self.xldl.tab_form(
            cell_ls, opt_date=datetime.date, opt_empty='NA')
        print(data_ls)
        self.assertEqual(res_ls, data_ls)
        # cell range test
        self.oxldl.sheet = 'Sheet5'
        label_ls = self.oxldl.tab_form('A5:J5')
        self.xldl.sheet = 'Sheet5'
        label_ls2 = self.xldl.tab_form('A5:J5')
        self.assertEqual(label_ls, label_ls2)
        label_ls.append('TestOfNone')
        label_ls.append('TestOfRange')
        cell_ls = ['A12', 'B12', 'C12', 'D12', 'E12', 'F12',
                   'G12', 'H12', 'I12', 'J12', None, 'B6:B23']
        data_dc = dict(zip(label_ls, cell_ls))
        print(data_dc)
        # dict test
        v_dc1 = self.oxldl.tab_form(data_dc)
        v_dc2 = self.xldl.tab_form(data_dc)
        print(v_dc1)
        print(v_dc2)
        self.assertEqual(v_dc1, v_dc2)
        # string test - single cell value
        value = self.oxldl.tab_form('A5')
        value2 = self.xldl.tab_form('A5')
        print('Single value = {}'.format(value))
        self.assertEqual(value, value2)
        print('\nRow and Column values test')
        row_vals1 = self.oxldl.row_values(13)
        print(row_vals1)
        row_vals2 = self.xldl.row_values(13)
        print(row_vals2)
        self.assertEqual(row_vals1, row_vals2)
        col_vals1 = self.oxldl.col_values('B')
        print(col_vals1)
        col_vals2 = self.xldl.col_values('B')
        print(col_vals2)
        self.assertEqual(col_vals1, col_vals2)
        print('\n 2-D Range Test')
        self.oxldl.sheet = 'Sheet2'
        self.xldl.sheet = 'Sheet2'
        # 2-D range test
        data_ls = self.oxldl.tab_form('B4:E34')
        data_ls2 = self.xldl.tab_form('B4:E34')
        print(self.oxldl.raw_range_value('B4:E34'))
        print(data_ls)
        print(data_ls2)
        self.assertEqual(data_ls, data_ls2)

    def test_fill_form(self):
        self.oxldl.sheet = 'Sheet3'  # make sure it is first sheet
        print('\nfill_form Tests')
        # Tuple list test
        tu1 = ('M6', 'N6', 'O6', 'P6', 'Q6', 'R6')
        tu2 = (32.7888, 63, datetime.date(
            2017, 9, 3), math.nan, 'a string', True)
        # [('M6', 32.7888), ('N6', 63), ('O6', datetime.date(2017, 9, 3)),
        # ('P6', nan), ('Q6', 'a string'), ('R6', True)]
        tu_ls = list(zip(tu1, tu2))
        self.oxldl.fill_form(tu_ls)
        # read back
        tu_res = self.oxldl.tab_form('M6:R6')
        self.assertEqual(list(tu2), tu_res)
        # tuple test
        self.oxldl.fill_form(('M5', 'Tuple Test'))
        # dict test
        tab_data = self.oxldl.tab_form('B4:E34')
        # read and copy data to the next table
        tab_data_dc = {'H4:K34': tab_data, 'M8': 'Dict Test', 'M9': None,
                       'M10': math.nan, 'N9': '<- Blank', 'N10': '<- Blank'}
        self.oxldl.fill_form(tab_data_dc)
        self.oxldl.save('test_save.xlsx')
        print('open test_save.xlsx to verify results')

    def test_misc(self):
        print("\nMiscellaneous Tests")
        # print str and repr
        print('str printout  = {}'.format(str(self.oxldl)))
        print('repr printout = {}'.format(repr(self.oxldl)))
        # inheritance tests
        print('XL File Name = {}'.format(self.oxldl.file_name))
        print('XL WS Name   = {}'.format(self.oxldl.sheet_name))
        print('XL WB Object = {}'.format(self.oxldl.workbook))
        print('XL WS Object = {}'.format(self.oxldl.worksheet))
        print('Coordinates of HZ85 = {}'.format(
            self.oxldl.cref_coord('HZ85')))  # 1-based


if __name__ == '__main__':
    unittest.main()
