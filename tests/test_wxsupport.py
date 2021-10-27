from io import StringIO

import pandas as pd
import wx
from pefc.wxsupport import LongTextInfoBox


def test_longtextinfobox():
    app = wx.App()
    # Read a csv file and display on dialog box
    df = pd.read_csv(r'tests\data\SocketHeadCapScrew.csv')
    with StringIO() as buff:
        df.to_string(buff)
        shcs_table = buff.getvalue()
    with LongTextInfoBox("Preview Socket Head Cap Screw Dimensions",
                         "DataFrame Information",
                         shcs_table) as dlg:
        dlg.ShowModal()
    app.MainLoop()


if __name__ == '__main__':
    test_longtextinfobox()
