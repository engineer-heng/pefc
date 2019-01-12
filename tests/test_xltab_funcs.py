"""
Unittest for xltab functions
"""
import unittest
import os

import xlwings as xw

from pefc.xltab import XLWDataLink, convert_xls


class TestXlTabFuncs(unittest.TestCase):
    """
    xltab function tests
    """
    @staticmethod
    def test_funcs():
        """
        Test convert_xls function
        """
        print('xltab function Tests')
        print('convert_xls tests')
        # Location of file - should be at pefc\tests\data
        cwd = os.getcwd()
        src_dir = os.path.join(
            cwd,
            r'tests\data\ProblemWorksheets\OriginalWorksheets')
        dest_dir = os.path.join(
            cwd,
            r'tests\data\ProblemWorksheets\FixedWorksheets')
        print('\nSource Directory = {}'.format(src_dir))
        print('\nDestination Directory = {}'.format(dest_dir))

        # TODO: Change manual testing and add assertions
        # convert_xls(src_dir, dest_dir)  # alerts if VBA, 51
        convert_xls(src_dir, dest_dir, -4143)
        # convert_xls(src_dir, dest_dir, 6)  # data loss
        # convert_xls(src_dir, dest_dir, 44)  # extra files
        # convert_xls(src_dir, dest_dir, 50)  # no alerts
        # convert_xls(src_dir, dest_dir, 52)  # no alerts
        # convert_xls(src_dir, dest_dir, 56)  # no alerts
        # All the above successfully tested. Some with alerts.
        # If have VBA use 52 to convert all to xlsm
        # The above alerts were silent when xl.DisplayAlerts = False
        # were added before SaveAS


if __name__ == '__main__':
    unittest.main()
