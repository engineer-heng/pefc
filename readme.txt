Removed rsixsigma.py and test_rsixsigma to ..\code discards\
More reliable to run R instead of through rpy2 because of app crashes
Takes a lot of time to fix issues.
Better to gain expertise to use python own graphical library to do some basic charts.
For complicated charts use R directly.

Temporary put some docstrings here for later use
"""
        This method extracts data from an MS Excel workbook by specifying the cell references.
        If cell errors need to be analyzed then use raw_range_value method. Use OXLDataLink
        or XLDataLink for data extraction however if the following error are encountered
        'xlrd.biffh.XLRDError: Workbook is encrypted' MS Excel 95 protected file issue then use
        XLWDatalink. XLWDatalink uses xlwings library to extract data from an MS Excel workbook.
        xlwings library makes use of the MS Excel App installed on the computer therefore
        additional steps are required. XLWDatalink xlwdl.close() is need to conserve memory and to
        manage the MS Excel App.

        Usage:
        # Store the current directory
        cwd = os.getcwd()
        # Location of directory to process
        xl_dir = 'C:\\YourFolder'
        os.chdir(location)
        print("Processing files from %s directory" % xl_dir)
        re_test = re.compile("T\\d.*\\.xls", re.IGNORECASE)  # regex if needed
        fnames = os.listdir(location)
        fnames = [f for f in fnames if re.match(re_test, f)]
        fnames.sort(key=AlphaNum)  # if sorting is required

        # The following steps are ONLY for XLWDataLink Class
        xlapp = xlwings.App()  # open MS Excel App. Only do this once to avoid consuming memory.
        xlapp.visible = False  # hide app unless you want to see it in action

        # For all classes
        # Put this section in a for loop for multiple file processing
        for xl_name in fnames:
            # For XLDatalink class use xldl = XLDataLink(xl_name)
            # For OXLDataLink class use xldl = OXLDataLink(xl_name)
            xldl = XLWDataLink(xlapp, xl_name)  # default first sheet
            # data from various cells
            # Note: If a range value is specified in a cell reference it will return a
            # single dimension list
            # Can use None as a placeholder to insert other data into the record
            cell_ls = ['A12', 'B15', 'C20', 'D23', None, 'E23', 'F30', 'G33', 'H33', 'I78', 'J88']
            data_ls = xldl.tab_form(cell_ls)  # process the default first sheet
            # range data
            # Note: This will return a two dimensional list
            xldl.sheet = 'Sheet5'  # multiple sheets can be processed
            data_ls = xldl.tab_form('A2:I36')
            # dict data
            # Note: If a range value is specified in a cell reference it will return a
            # single dimension list
            xldl.sheet = 'Sheet2'
            cref_dc = {'Name': 'B12', 'Age': 'B15', 'Height': 'C20'}
            values_dc = xldl.tab_form(cref_dc)
            # return value is {'Name': 'John Doe', 'Age': 33.0, 'Height': 168.0}
            # single value
            xldl.sheet = 'Sheet3'
            value = xldl.tab_form('A2')

        # The following steps are ONLY XLWDataLink Class
            # close this workbook to save resources and prepare to get data from next workbook
            xldl.close()
        # close the MS Excel instance without affecting other running instances.
        xlapp.quit()  # For XLWDataLink only

        # For all classes
        # Optional - restore the previous directory to avoid confusing the user
        os.chdir(cwd)

        e.g. 2017-01-01 Default is datetime.date
        opt_empty: Return this specified value if cell is blank, empty or error.
        Default is math.nan
        return: a single value, list of values or dict of values depending on cell_refs parameter
        """