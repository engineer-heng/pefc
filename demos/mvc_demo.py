""" A demostration of MVC concepts using a panel for Data Entry.
    This is a simple implementation of the MVC inspired by
    Stefano Borini.
    It avoids the use of wxpython MVC's recommended PyPubSub package.
"""
import wx
from pefc.genericmodels import DictModel
from pefc.validators import FloatValidator


class DemoModel(DictModel):
    """ This is the 'Model'. The Model's responsibilites is to notify
        the listeners of the change in data so that they are all in sync.
        All implementations of the biz logic should be done here if
        it is related to this data model.
        The Model's biz logic can be tested independently without any
        views, controllers and registered listeners help.
    """

    def __init__(self, model_dict):
        # inherits from DictModel
        super().__init__(model_dict)

    # Implementations to Model's biz logic and to update databases
    def update_price(self):
        """ Update price biz logic
        """
        new_total_price = self.getvalue('quantity') * self.getvalue(
            'unit_price')
        self.setvalue('total_price', new_total_price)


class DemoController:
    """ This is the 'Controller'.
        The User triggers an event through the View which acts
        on the event and calls the appropriate Controller.
        The Controller then calls the Model's methods to update data
        through its biz logic.
        For procedural programming style a Controller can be used to interact
        with the Model to execute its biz logic without any View.
    """

    def __init__(self, model, view):
        """ Links the Model and the View to this Controller.
        """
        self._model = model
        self._view = view

    def change_msg(self, msg):
        """ Updates the RadioBox's text message change

            msg: str, message selected by User
        """
        if msg == 'None':
            self._model.setvalue(self._view.rb_msg.GetName(), None)
        else:
            self._model.setvalue(self._view.rb_msg.GetName(), msg)

    def get_floating_point_validator(self):
        """ Controller returns the FloatValidator with data value limits
            and pass its reponsibilities to the validator
        """
        # self._model can also supply the limits
        return FloatValidator(self._model, 0.0, 300.0)

    def qty_updated(self):
        """ Controller's task for quantity spin control
        """
        # Data validation should be done by the View's control not here.
        # Any sync between controls is done here.
        # quantity managed by spin control ui
        # sync ctrl new value with model value
        self._model.setvalue(self._view.spic_qty.GetName(),
                             self._view.spic_qty.GetValue())
        # Note here that the Model updates price not the Controller!
        # All biz logic no matter how simple is managed by the Model
        self._model.update_price()


class DemoView(wx.Panel):
    """ This is the 'View'.
        Here a single Panel control that can be used to manage all or
        some of the controls on the Panel.
        Each control should have the name parameter set to the database field
        name e.g. a customer name control should have name='customer_name'
        so that ctrl.GetName() will return the field name. This will make
        refactoring the field names a lot easier. It will fail to work
        if name parameter is not set to the field name.
        Methods related to an event trigger should have prefix evt_*
        to differentiate event handling methods with update action methods.
        However events that trigger another dialog/frame the
        recommended prefix is on_*
    """

    def __init__(self, parent, model):
        super(DemoView, self).__init__(parent)

        self._parent = parent
        self._model = model
        # Sets the Controller for the View
        self._controller = DemoController(self._model, self)
        # Use for restoring background of non-editable TextCtrl
        self.menu_color = wx.SystemSettings.GetColour(wx.SYS_COLOUR_MENU)

        # Sizers demos
        ipo = 0  # Using ipo makes it easier to add rows
        gb_sizer = wx.GridBagSizer(hgap=5, vgap=5)
        heading = "DEMO VIEW"
        self.stxt_heading = wx.StaticText(self, label=heading)
        font = wx.Font(wx.FontInfo(12).Bold().Underlined())
        self.stxt_heading.SetFont(font)
        gb_sizer.Add(self.stxt_heading, pos=(ipo, 0))
        ipo += 1
        stxt = wx.StaticText(self, label="Show information: ")
        gb_sizer.Add(stxt, pos=(ipo, 0))
        self.tc_info = wx.TextCtrl(self, style=wx.TE_READONLY,
                                   size=(200, -1), name='info')
        self._model.register('info', self.tc_info)
        gb_sizer.Add(self.tc_info, pos=(ipo, 1))
        ipo += 1
        # the edit control - one line version for text data
        stxt = wx.StaticText(self, label="Text Data :")
        gb_sizer.Add(stxt, pos=(ipo, 0))
        self.tc_txt_data = wx.TextCtrl(
            self, value="Enter text data here", size=(200, -1))
        gb_sizer.Add(self.tc_txt_data, pos=(ipo, 1))
        self.Bind(wx.EVT_TEXT, self.evt_text, self.tc_txt_data)
        ipo += 1
        # floating point tests
        stxt = wx.StaticText(self, label="Floating Point Data :")
        gb_sizer.Add(stxt, pos=(ipo, 0))
        self.tc_float_data = wx.TextCtrl(
            self, value='', size=(200, -1),
            style=wx.TE_PROCESS_ENTER,  # get tab and CR
            validator=self._controller.get_floating_point_validator(),
            # validator=FloatValidator(self._model, 0.0, 300.0),
            name='float_data')
        gb_sizer.Add(self.tc_float_data, pos=(ipo, 1))
        self.Bind(wx.EVT_TEXT, self.evt_text, self.tc_float_data)
        # self.Bind(wx.EVT_TEXT_ENTER, self.float_updated, self.tc_float_data)
        ipo += 1
        # the combobox Control
        self.answer_ls = ['Fantastic!', 'I love it!', 'Ok only', 'Can do',
                          'So so only', 'Too complicated']
        stxt = wx.StaticText(self, label="How did you like this test?")
        gb_sizer.Add(stxt, pos=(ipo, 0))
        self.cb_survey = wx.ComboBox(self, size=(
            120, -1), choices=self.answer_ls, style=wx.CB_DROPDOWN)
        gb_sizer.Add(self.cb_survey, pos=(ipo, 1))
        self.Bind(wx.EVT_COMBOBOX, self.evt_combo_box, self.cb_survey)
        self.Bind(wx.EVT_TEXT, self.evt_text, self.cb_survey)
        ipo += 1
        # Checkbox
        self.chb_query = wx.CheckBox(
            self,
            label="Do you want more complex tests in the future?")
        gb_sizer.Add(self.chb_query, pos=(ipo, 0), span=(1, 2),
                     flag=wx.BOTTOM, border=5)
        self.Bind(wx.EVT_CHECKBOX, self.evt_check_box, self.chb_query)
        ipo += 1
        # Radio Box demo
        radio_ls = ['None', 'Ok!', 'Not Ok!']
        self.rb_msg = wx.RadioBox(
            self, label="Choose Text Message:", choices=radio_ls,
            majorDimension=3, style=wx.RA_SPECIFY_COLS, name='message')
        gb_sizer.Add(self.rb_msg, pos=(ipo, 0))
        self.Bind(wx.EVT_RADIOBOX, self.evt_radio_box, self.rb_msg)
        self.tc_text_msg = wx.TextCtrl(
            self,
            style=wx.TE_READONLY | wx.TE_CENTER)
        font = wx.Font(wx.FontInfo(16).Bold())
        self.tc_text_msg.SetFont(font)
        gb_sizer.Add(
            self.tc_text_msg, pos=(ipo, 1),
            flag=wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL)
        self._model.register('message', self.rb_msg)

        # add a spacer to the sizer
        ipo += 1
        gb_sizer.Add((10, 10), pos=(ipo, 1))  # spacer for demo purposes
        ipo += 1
        # FlexGridSizer and data fields sync demo
        # quantity and total price work in tandem with qty
        fg_sizer = wx.FlexGridSizer(3, 2, 10, 10)
        # unit price
        stxt_upr = wx.StaticText(self, label="Unit price: ")
        self.tc_unit_price = wx.TextCtrl(self, style=wx.TE_READONLY,
                                         size=(100, -1), name='unit_price')
        # quantity
        stxt_qty = wx.StaticText(self, label="Quantity: ")
        self.spic_qty = wx.SpinCtrl(self, size=(75, -1),
                                    style=wx.TE_PROCESS_ENTER,
                                    name='quantity')
        self.Bind(wx.EVT_SPINCTRL, self.spic_qty_updated, self.spic_qty)
        self.Bind(wx.EVT_TEXT_ENTER, self.spic_qty_updated, self.spic_qty)
        # total price
        stxt_tpr = wx.StaticText(self, label="Total price: ")
        self.tc_total_price = wx.TextCtrl(self, style=wx.TE_READONLY,
                                          size=(100, -1), name='total_price')
        # Register and init values from Model
        self._model.register('unit_price', self.tc_unit_price)
        self._model.register('quantity', self.spic_qty)
        self._model.register('total_price', self.tc_total_price)
        # Make sure qty and total price are in sync
        self._controller.qty_updated()
        fg_sizer.AddMany([(stxt_upr), (self.tc_unit_price, 1, wx.EXPAND),
                          (stxt_qty), (self.spic_qty, 1, wx.EXPAND),
                          (stxt_tpr), (self.tc_total_price, 1, wx.EXPAND)
                          ])
        # add as part of gb
        gb_sizer.Add(fg_sizer, pos=(ipo, 0))

        # A multiline TextCtrl demo to display model data and other info
        self.tc_display = wx.TextCtrl(
            self, size=(300, 400),
            style=wx.TE_MULTILINE | wx.TE_READONLY)
        # StaticBoxSizer demo
        vsb_sizer_display = wx.StaticBoxSizer(wx.VERTICAL, self, 'Display')
        vsb_sizer_display.Add(self.tc_display, 0, wx.ALL, 5)

        hb_sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        hb_sizer1.Add(gb_sizer, 0, wx.ALL, 5)
        hb_sizer1.Add(vsb_sizer_display)

        # A buttons row demo
        hb_sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        btn_okay = wx.Button(self, wx.ID_OK)  # Use standard button ID
        btn_okay.SetDefault()
        btn_close = wx.Button(self, label='Close')
        btn_clr_display = wx.Button(self, label='Clear Display')
        btn_info = wx.Button(self, label="Show Model Info")
        self.Bind(wx.EVT_BUTTON, self.on_okay, btn_okay)
        self.Bind(wx.EVT_BUTTON, self.on_close, btn_close)
        self.Bind(wx.EVT_BUTTON, self.on_clr_display, btn_clr_display)
        self.Bind(wx.EVT_BUTTON, self.on_info, btn_info)
        hb_sizer2.Add(btn_okay)
        hb_sizer2.Add(10, -1, 0)  # add spacer in-between
        hb_sizer2.Add(btn_close)
        hb_sizer2.Add(10, -1, 0)  # add spacer in-between
        hb_sizer2.Add(btn_clr_display)
        hb_sizer2.Add(10, -1, 0)  # add spacer in-between
        hb_sizer2.Add(btn_info)

        vb_sizer_main = wx.BoxSizer(wx.VERTICAL)
        vb_sizer_main.Add(hb_sizer1, 0, wx.ALL, 5)  # grid bag and logger
        vb_sizer_main.Add(hb_sizer2, 0, wx.CENTER, 5)  # buttons
        vb_sizer_main.Add((10, 5))  # add spacer after button row
        self.SetSizerAndFit(vb_sizer_main)

        # init the validators' controls
        self.TransferDataToWindow()  # use this directly instead of InitDialog

    def notify(self, ltr):
        """ The View's job is to update its displayed data from the model and
            to make sure the data is displayed in the correct format.
            Should have no involvement from the Controller and
            the Model's biz logic. Initialization should not be done here.

            listener: Specify the listener that is being notified.
        """
        # Make sure the listener is already created before any method call!
        # Follow the order of listener creation in __init__ method.
        if ltr is self.tc_info:
            ltr.SetLabel(self._model.getvalue(ltr.GetName()))
        elif ltr is self.rb_msg:
            val = self._model.getstrvalue(ltr.GetName())
            # background defaults to white when foreground is set
            self.tc_text_msg.SetBackgroundColour(self.menu_color)
            if val == 'Not Ok!':
                self.tc_text_msg.SetForegroundColour('red')
            else:
                self.tc_text_msg.SetForegroundColour('forest green')
            self.tc_text_msg.SetValue(val)
        elif ltr is self.tc_unit_price:
            val = self._model.getstrvalue(ltr.GetName(), '{:.2f}')
            ltr.SetLabel(val)
        elif ltr is self.spic_qty:
            ltr.SetValue(self._model.getvalue(ltr.GetName()))
        elif ltr is self.tc_total_price:
            val = self._model.getstrvalue(ltr.GetName(), '{:.2f}')
            ltr.SetLabel(val)

    def evt_radio_box(self, event):
        val = event.GetString()
        self.tc_display.AppendText(f'EvtRadioBox: {val}\n')
        self._controller.change_msg(val)

    def evt_combo_box(self, event):
        self.tc_display.AppendText(
            f'EvtComboBox: {event.GetString()}\n')

    def spic_qty_updated(self, event):
        # Updates both quantity and total price
        self.tc_display.AppendText(
            f'EvtSpinCtrl: {self.spic_qty.GetValue()}\n')
        self._controller.qty_updated()

    def on_okay(self, event):
        # transfer data from validators' control
        self.TransferDataFromWindow()

    def on_close(self, event):
        self.GetParent().Close(True)

    def on_clr_display(self, event):
        self.tc_display.Clear()

    def on_info(self, event):
        self.tc_display.AppendText(self._model.model_report())

    def evt_text(self, event):
        self.tc_display.AppendText(f'EvtText: {event.GetString()}\n')

    def evt_check_box(self, event):
        self.tc_display.AppendText(f'EvtCheckBox: {event.IsChecked()}\n')


class MainWindow(wx.Frame):
    def __init__(self, parent, model, title, *args, **kwargs):
        super().__init__(parent, title=title, *args, **kwargs)

        # A StatusBar in the bottom of the window
        self.mwstatus_bar = self.CreateStatusBar()
        self.mwstatus_bar.SetStatusText('Try all the controls. Enjoy!')

        # Setting up the menu.
        filemenu = wx.Menu()

        # wx.ID_ABOUT and wx.ID_EXIT are standard ids provided by wxWidgets.
        menu_about = filemenu.Append(
            wx.ID_ABOUT, "&About", " Test Model-View-Comtroller")
        menu_exit = filemenu.Append(
            wx.ID_EXIT, "E&xit", " Terminate the program")

        # Creating the menubar.
        menu_bar = wx.MenuBar()
        # Adding the "filemenu" to the MenuBar
        menu_bar.Append(filemenu, "&MVC")
        self.SetMenuBar(menu_bar)  # Adding the MenuBar to the Frame content.

        # Set events.
        self.Bind(wx.EVT_MENU, self.on_about, menu_about)
        self.Bind(wx.EVT_MENU, self.on_exit, menu_exit)

        # Create MVC DemoView Panel
        # Panel below must be created after status and menu bar creation
        DemoView(self, model)
        self.Fit()
        self.Centre()

    def on_about(self, event):
        # A message dialog box with an OK button.
        # wx.OK is a standard ID in wxWidgets.
        dlg = wx.MessageDialog(self, "Demo to test MVC Concepts",
                               "About MVC Tests", wx.OK)
        dlg.ShowModal()  # Show it
        dlg.Destroy()  # finally destroy it when finished.

    def on_exit(self, event):
        self.Close(True)  # Close the frame.


if __name__ == '__main__':
    import traceback

    try:
        app = wx.App(False)
        # MVC Tests
        model_dict = {'info': 'MVC Demo using wxpython',
                      'text_data': None,
                      'float_data': 11.8,
                      'test_survey': False,
                      'message': None,
                      'unit_price': 8.00,
                      'quantity': 1,
                      'total_price': 0.0
                      }
        # Init the Model which in a real app has databases and biz logic in it.
        model = DemoModel(model_dict)
        frame = MainWindow(None, model, "Practical MVC Demo")
        # frame.InitDialog()
        frame.Show()

        app.MainLoop()

    except Exception:
        traceback.print_exc()
