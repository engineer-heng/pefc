""" Support wx GUI
"""
import wx


class LongTextInfoBox(wx.Dialog):
    """ Display Long Text in a dialog box. Use mainly to display
        pandas Dataframe with many columns for reviewing data.
        To view the data correctly, the text font is in monospaced.
    """

    def __init__(self, message, caption, content="", tsize=(750, 380),
                 parent=None):
        """ Constructor

            Display Long Text in monospaced font using a dialog box.
            Mainly use for displaying pandas DataFrame for review.

            message: str, show a message on top of the table display

            caption: str, dialog box title.

            content: str, content to be displayed.

            Example for a pandas DataFrame
            -------------------------------
            >>> # Create or get data for the pandas DataFrame df.
            >>> with io.StringIO() as buff:
            >>>     df.to_string(buff)
            >>>     content = buff.getvalue()
            >>> with LongTextInfoBox("Check data", "DataFrame Information",
            >>>                      content) as dlg:
            >>>     dlg.ShowModal()
        """
        super().__init__(parent, id=wx.ID_ANY, title=caption)

        # Add a bitmap on the left side.
        bmp = wx.ArtProvider.GetBitmap(wx.ART_INFORMATION)
        self.staticbmp = wx.StaticBitmap(self, bitmap=bmp)

        # Show message at top of table
        self.st_msg = wx.StaticText(self, label=message, size=(380, -1))
        font = wx.Font(wx.FontInfo(12).Bold())
        self.st_msg.SetFont(font)
        hbs1 = wx.BoxSizer(wx.HORIZONTAL)
        hbs1.Add(self.staticbmp, 0, wx.ALIGN_CENTER_VERTICAL, 5)
        hbs1.Add((10, 5))
        hbs1.Add(self.st_msg, 0, wx.ALIGN_CENTER_VERTICAL, 5)

        # A multiline TextCtrl to display pandas DataFrames
        self.tc_display = wx.TextCtrl(
            self, size=tsize,  # size of tabular display
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL)
        # monospaced font
        display_font = wx.Font(wx.FontInfo(10).Family(wx.FONTFAMILY_MODERN))
        self.tc_display.SetFont(display_font)
        self.append_content(content)

        # only for standard buttons e.g. ID_OK and ID_CANCEL
        bus = wx.StdDialogButtonSizer()  # for look and feel
        # Use standard button IDs for validators to work correctly
        bu_okay = wx.Button(self, wx.ID_OK)
        bus.AddButton(bu_okay)
        bus.Realize()

        vbs_main = wx.BoxSizer(wx.VERTICAL)
        vbs_main.Add(hbs1, 0, wx.ALL, 5)
        vbs_main.Add(self.tc_display, 0, wx.ALL, 5)  # display
        vbs_main.Add(bus, 0, wx.ALIGN_RIGHT, 5)  # buttons
        vbs_main.Add((10, 5))  # add spacer after button row
        self.SetSizerAndFit(vbs_main)

    def append_content(self, content):
        self.tc_display.AppendText(content)
        self.Fit()

    def clear_content(self):
        self.tc_display.Clear()
