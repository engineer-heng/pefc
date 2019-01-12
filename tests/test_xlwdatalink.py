import unittest
from pefc.xltab import XLWDataLink, XLDataLink
import datetime
import xlwings
import math
import os


class TestXWLDataLink(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.exedir = os.getcwd()
        # Location of file - should be at pefc\tests\data
        os.chdir(os.path.join(os.getcwd(), r'tests\data'))
        print('\nCurrent Directory = {}'.format(os.getcwd()))
        cls.xl_name = r'efcbook.xlsx'
        cls.xl_app = xlwings.App()
        cls.xlwdl = XLWDataLink(cls.xl_app, cls.xl_name)
        cls.xldl = XLDataLink(cls.xl_name)

    @classmethod
    def tearDownClass(cls):
        # restore back executable dir
        os.chdir(cls.exedir)
        # clean up
        cls.xlwdl.close()
        cls.xl_app.quit()

    def test_tab_form(self):
        # test using results from xltab.XLDataLink object
        # remember to specify sheets since it may be changed by other
        # tests
        # some assertions is commented out because of differences
        # in cell handling
        print('\ntab_form Tests')
        # list test
        cell_ls = ['A13', 'B13', 'C13', 'D13', None, 'E13', 'F13', 'G13',
                   'H13', 'I13', 'J13', 'A34:I34']
        self.xlwdl.sheet = 'Sheet1'
        res_ls = self.xlwdl.tab_form(
            cell_ls, opt_date=datetime.date, opt_empty='NA')
        print(res_ls)
        data_ls = self.xldl.tab_form(
            cell_ls, opt_date=datetime.date, opt_empty='NA')
        print(data_ls)
        # self.assertEqual(res_ls, data_ls)
        # cell range test
        self.xlwdl.sheet = 'Sheet5'
        label_ls = self.xlwdl.tab_form('A5:J5')
        self.xldl.sheet = 'Sheet5'
        label_ls2 = self.xldl.tab_form('A5:J5')
        self.assertEqual(label_ls, label_ls2)
        label_ls.append('TestOfNone')
        label_ls.append('TestOfRange')
        cell_ls = ['A12', 'B12', 'C12', 'D12', 'E12', 'F12', 'G12', 'H12',
                   'I12', 'J12', None, 'B6:B23']
        data_dc = dict(zip(label_ls, cell_ls))
        print(data_dc)
        # dict test
        v_dc1 = self.xlwdl.tab_form(data_dc)
        v_dc2 = self.xldl.tab_form(data_dc)
        print(v_dc1)
        print(v_dc2)
        self.assertEqual(v_dc1, v_dc2)
        # string test - single cell value
        value = self.xlwdl.tab_form('A5')
        value2 = self.xldl.tab_form('A5')
        print('Single value = {}'.format(value))
        self.assertEqual(value, value2)
        self.xlwdl.sheet = 'Sheet2'
        self.xldl.sheet = 'Sheet2'
        # 2-D range test
        data_ls = self.xlwdl.tab_form('B4:E34')
        data_ls2 = self.xldl.tab_form('B4:E34')
        print(self.xlwdl.raw_range_value('B4:E34'))
        print(data_ls)
        print(data_ls2)
        # self.assertEqual(data_ls, data_ls2)

    def test_fill_form(self):
        self.xlwdl.sheet = 'Sheet3'  # make sure it is first sheet
        print('\nfill_form Tests')
        # Tuple list test
        tu1 = ('M6', 'N6', 'O6', 'P6', 'Q6', 'R6')
        tu2 = (32.7888, 63, datetime.date(
            2017, 9, 3), math.nan, 'a string', True)
        # [('M6', 32.7888), ('N6', 63), ('O6', datetime.date(2017, 9, 3)),
        # ('P6', nan), ('Q6', 'a string'), ('R6', True)]
        tu_ls = list(zip(tu1, tu2))
        self.xlwdl.fill_form(tu_ls)
        # read back
        tu_res = self.xlwdl.tab_form('M6:R6')
        self.assertEqual(list(tu2), tu_res)
        # tuple test
        self.xlwdl.fill_form(('M5', 'Tuple Test'))
        # dict test
        tab_data = self.xlwdl.tab_form('B4:E34')
        # read and copy data to the next table
        tab_data_dc = {'H4:K34': tab_data, 'M8': 'Dict Test', 'M9': None,
                       'M10': math.nan, 'N9': '<- Blank', 'N10': '<- Blank'}
        self.xlwdl.fill_form(tab_data_dc)
        self.xlwdl.save('test_save.xlsx')
        print('open test_save.xlsx to verify results')

    def test_misc(self):
        print("\nMiscellaneous Tests")
        # print str and repr
        print('str printout  = {}'.format(str(self.xlwdl)))
        print('repr printout = {}'.format(repr(self.xlwdl)))
        # inheritance tests
        print('XL File Name = {}'.format(self.xlwdl.file_name))
        print('XL WS Name   = {}'.format(self.xlwdl.sheet_name))
        print('XL App Object= {}'.format(self.xlwdl.app()))
        print('XL WB Object = {}'.format(self.xlwdl.workbook))
        print('XL WS Object = {}'.format(self.xlwdl.worksheet))
        coord = self.xlwdl.cref_coord('HZ85')
        print('Coordinates of HZ85 = {}'.format(coord))  # 1-based

    def test_xlwdatalink(self):
        """ Just to test XLWDataLink whether with statement works
        """
        xlapp = xlwings.App()
        xlapp.visible = False
        len1 = len2 = 0
        with XLWDataLink(xlapp, self.xl_name, 'Sheet5') as xldl:
            val1 = xldl.tab_form('B1')
            val2 = 'EZDESIGN METRIC SERIES SOCKET HEAD CAP SCREW DATA'
            # test the 'with' statement is working correctly
            self.assertEqual(val1, val2)
            len1 = len(xlwings.books)
            print('No of books = {}'.format(len1))
        len2 = len(xlwings.books)
        print('No of books = {}'.format(len2))
        # check whether the workbook is closed
        self.assertEqual(len1-len2, 1)

        # Close the MS Excel App to free resources
        xlapp.quit()


if __name__ == '__main__':
    unittest.main()
