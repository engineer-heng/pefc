""" A demostration of MVC concepts using a panel for Data Entry.
    This is a simple implementation of the MVC inspired by
    Stefano Borini.
    It avoids the use of wxpython MVC's recommended PyPubSub package.
"""
import math
import wx
from pefc.genericmodels import DictModel
from pefc.validators import (TextValidator, FloatingPointValidator,
                             IntegerValidator, BooleanValidator)


class DemoModel(DictModel):
    """ This is the 'Model', the business logic layer.
        The Model's responsibilites is to notify
        the listeners of the change in data so that they are all in sync.
        All implementations of the biz logic should be done here if
        it is related to this data model.
        The Model's biz logic can be tested independently without any
        views, controllers and registered listeners help.
    """

    def __init__(self, model_dict):
        # inherits from DictModel
        super().__init__(model_dict)

    def calc_new_total_price(self, new_qty):
        """ Calculate new total_price as per biz logic.
        """
        # Implementations as per Model's biz logic to ensure correctness.
        # Note here that the Model calculates price not the Controller!
        # All biz logic no matter how simple is managed by the Model
        # This is just a simple example in real situation it may complicated.
        return new_qty * self.getvalue('unit_price')


class DemoController:
    """ This is the 'Controller', the Application logic layer.
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

    def get_text_validator(self):
        """ Controller returns the TextValidator with text length limits
            and pass its reponsibilities to the validator
        """
        # self._model may also supply the limits
        return TextValidator(self._model, (0, 20))

    def get_msg_validator(self):
        """ Controller returns the TexttValidator with text length limits
            and pass its reponsibilities to the validator
        """
        # self._model may also supply the limits
        return TextValidator(self._model, (0, 20), fill=False)

    def get_floating_point_validator(self):
        """ Controller returns the FloatingPointValidator with data
            value limits and pass its reponsibilities to the validator
        """
        # self._model may also supply the limits
        return FloatingPointValidator(self._model, (0.0, 300.0))

    def get_integer_validator(self):
        """ Controller returns the IntegerValidator with data value limits
            and pass its reponsibilities to the validator
        """
        # self._model may also supply the limits
        return IntegerValidator(self._model, (-50, 150))

    def update_model(self):
        """ Controller's task is to update the model data on those
            fields that are NOT handled by the validators.
            This method is normally called by the ID_OK button.
        """
        # Data validation already done by the View's control
        self._model.setvalue(self._view.spcl_qty.GetName(),
                             self._view.spcl_qty.GetValue())

        new_total_price = float(self._view.tc_total_price.GetValue())
        self._model.setvalue(self._view.tc_total_price.GetName(),
                             new_total_price)


class DemoView(wx.Panel):
    """ This is the 'View', the Presentation logic layer.
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
        gbs = wx.GridBagSizer(hgap=5, vgap=5)
        heading = "PANEL DEMO"
        self.st_heading = wx.StaticText(self, label=heading)
        font = wx.Font(wx.FontInfo(12).Bold().Underlined())
        self.st_heading.SetFont(font)
        gbs.Add(self.st_heading, pos=(ipo, 0))
        ipo += 1
        st = wx.StaticText(self, label="Show information: ")
        gbs.Add(st, pos=(ipo, 0))
        self.tc_info = wx.TextCtrl(self, style=wx.TE_READONLY, size=(200, -1),
                                   name='info')
        # no validator so use the model to init the info value
        self._model.register('info', self.tc_info)
        gbs.Add(self.tc_info, pos=(ipo, 1))
        ipo += 1
        # the edit control - one line version for text data
        st = wx.StaticText(self, label="Text Data :")
        gbs.Add(st, pos=(ipo, 0))
        self.tc_txt_data = wx.TextCtrl(
            self, value="", size=(200, -1),
            style=wx.TE_PROCESS_ENTER,  # get tab and CR
            validator=self._controller.get_text_validator(),
            name='text_data')
        gbs.Add(self.tc_txt_data, pos=(ipo, 1))
        self.Bind(wx.EVT_TEXT, self.evt_text, self.tc_txt_data)
        ipo += 1
        # floating point tests
        st = wx.StaticText(self, label="Floating Point Data :")
        gbs.Add(st, pos=(ipo, 0))
        self.tc_float_data = wx.TextCtrl(
            self, value='', size=(200, -1),
            style=wx.TE_PROCESS_ENTER,  # get tab and CR
            validator=self._controller.get_floating_point_validator(),
            name='float_data')
        gbs.Add(self.tc_float_data, pos=(ipo, 1))
        self.Bind(wx.EVT_TEXT, self.evt_text, self.tc_float_data)
        ipo += 1
        # integer data tests
        st = wx.StaticText(self, label="Integer Data :")
        gbs.Add(st, pos=(ipo, 0))
        self.tc_int_data = wx.TextCtrl(
            self, value='', size=(200, -1),
            style=wx.TE_PROCESS_ENTER,  # get tab and CR
            validator=self._controller.get_integer_validator(),
            name='int_data')
        gbs.Add(self.tc_int_data, pos=(ipo, 1))
        self.Bind(wx.EVT_TEXT, self.evt_text, self.tc_int_data)
        ipo += 1
        # the combobox Control
        self.answer_ls = ['Fantastic!', 'I love it!', 'Ok only', 'Can do',
                          'So so only', 'Too complicated']
        st = wx.StaticText(self, label="How did you like this test?")
        gbs.Add(st, pos=(ipo, 0))
        self.cb_survey = wx.ComboBox(
            self,
            size=(120, -1), choices=self.answer_ls,
            style=wx.TE_PROCESS_ENTER | wx.CB_DROPDOWN,  # get tab and CR
            validator=self._controller.get_text_validator(),
            name='test_survey')
        gbs.Add(self.cb_survey, pos=(ipo, 1))
        self.Bind(wx.EVT_COMBOBOX, self.evt_combo_box, self.cb_survey)
        self.Bind(wx.EVT_TEXT, self.evt_text, self.cb_survey)
        ipo += 1
        # Checkbox
        self.chb_option = wx.CheckBox(
            self,
            label="Want special edition option?",
            style=wx.CHK_3STATE | wx.CHK_ALLOW_3RD_STATE_FOR_USER,
            validator=BooleanValidator(self._model),
            name='option')
        gbs.Add(self.chb_option, pos=(ipo, 0), span=(1, 2),
                flag=wx.BOTTOM, border=5)
        self.Bind(wx.EVT_CHECKBOX, self.evt_check_box, self.chb_option)
        ipo += 1
        # Radio Box demo
        radio_ls = ['None', 'Ok!', 'Not Ok!']
        self.rb_msg = wx.RadioBox(
            self, label="Choose Text Message:", choices=radio_ls,
            majorDimension=3, style=wx.RA_SPECIFY_COLS)
        gbs.Add(self.rb_msg, pos=(ipo, 0))
        self.Bind(wx.EVT_RADIOBOX, self.evt_radio_box, self.rb_msg)
        self.tc_text_msg = wx.TextCtrl(
            self,
            style=wx.TE_READONLY | wx.TE_CENTER,
            validator=self._controller.get_msg_validator(),
            name='text_message')
        font = wx.Font(wx.FontInfo(16).Bold())
        self.tc_text_msg.SetFont(font)
        gbs.Add(
            self.tc_text_msg, pos=(ipo, 1),
            flag=wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL)
        # add a spacer to the sizer
        ipo += 1
        gbs.Add((10, 10), pos=(ipo, 1))  # spacer for demo purposes
        ipo += 1
        # FlexGridSizer and data fields sync demo
        # quantity and total price work in tandem with qty
        fgs = wx.FlexGridSizer(3, 2, 10, 10)
        # unit price
        st_upr = wx.StaticText(self, label="Unit price: ")
        self.tc_unit_price = wx.TextCtrl(self, style=wx.TE_READONLY,
                                         size=(75, -1), name='unit_price')
        # no validator so use model to init unit_price. unit_price not editable
        self._model.register('unit_price', self.tc_unit_price)

        # quantity and total_price are managed by the model because
        # SpinCtrl don't allow any validator. Both are also related.
        # quantity
        st_qty = wx.StaticText(self, label="Quantity: ")
        self.spcl_qty = wx.SpinCtrl(
            self, size=(50, -1),
            style=wx.TE_PROCESS_ENTER,
            name='quantity')
        self.Bind(wx.EVT_SPINCTRL, self.spcl_qty_updated, self.spcl_qty)
        self.Bind(wx.EVT_TEXT_ENTER, self.spcl_qty_updated, self.spcl_qty)
        # total price
        st_tpr = wx.StaticText(self, label="Total price: ")
        self.tc_total_price = wx.TextCtrl(self,
                                          style=wx.TE_READONLY,
                                          size=(75, -1), name='total_price')
        # Register and init values from Model
        # Must register in order of ctrl creation
        # total_price is sync with quantity during registration
        # total_price in model is ignored in case of errors in model data
        self._model.register('quantity', self.spcl_qty)

        # arrange ctrls in correct order
        fgs.AddMany([(st_upr), (self.tc_unit_price, 1, wx.EXPAND),
                     (st_qty), (self.spcl_qty, 1, wx.EXPAND),
                     (st_tpr), (self.tc_total_price, 1, wx.EXPAND)
                     ])
        # add as part of gb
        gbs.Add(fgs, pos=(ipo, 0))

        # ListCtrl
        self.list_ctrl = wx.ListCtrl(
            self, size=(-1, 100),
            style=wx.LC_REPORT | wx.LC_HRULES
        )
        self.list_ctrl.InsertColumn(0, 'Stock No', width=70)
        self.list_ctrl.InsertColumn(1, 'List Price', width=70)
        self.list_ctrl.InsertColumn(2, 'Stock Qty', width=70)

        items = self._model.getvalue('price_list').items()
        idx = 0
        for key, data in items:
            index = self.list_ctrl.InsertItem(idx, data[0])
            self.list_ctrl.SetItem(index, 1, data[1])
            self.list_ctrl.SetItem(index, 2, data[2])
            self.list_ctrl.SetItemData(index, key)
            idx += 1
        # add as part of gb
        gbs.Add(self.list_ctrl, pos=(ipo, 1))

        # A multiline TextCtrl demo to display model data and other info
        self.tc_display = wx.TextCtrl(
            self, size=(300, 400),
            style=wx.TE_MULTILINE | wx.TE_READONLY)
        # StaticBoxSizer demo
        vsbs_display = wx.StaticBoxSizer(wx.VERTICAL, self, 'Display')
        vsbs_display.Add(self.tc_display, 0, wx.ALL, 5)

        hbs1 = wx.BoxSizer(wx.HORIZONTAL)
        hbs1.Add(gbs, 0, wx.ALL, 5)
        hbs1.Add(vsbs_display)

        # A buttons row demo
        hbs2 = wx.BoxSizer(wx.HORIZONTAL)

        # Use standard button IDs for validators to work correctly
        bu_okay = wx.Button(self, wx.ID_OK)
        self.Bind(wx.EVT_BUTTON, self.on_okay, bu_okay)
        bu_cancel = wx.Button(self, wx.ID_CANCEL)
        self.Bind(wx.EVT_BUTTON, self.on_cancel, bu_cancel)

        # only for standard buttons e.g. ID_OK and ID_CANCEL
        bus = wx.StdDialogButtonSizer()  # for look and feel
        bus.AddButton(bu_okay)
        bus.AddButton(bu_cancel)
        bus.Realize()

        # non-standard buttons
        bu_update = wx.Button(self, label='Update')
        bu_clr_display = wx.Button(self, label='Clear Display')
        bu_info = wx.Button(self, label="Show Model Info")
        self.Bind(wx.EVT_BUTTON, self.on_update, bu_update)
        self.Bind(wx.EVT_BUTTON, self.on_clr_display, bu_clr_display)
        self.Bind(wx.EVT_BUTTON, self.on_info, bu_info)
        hbs2.Add(bus)
        hbs2.Add(10, -1, 0)  # add spacer in-between
        hbs2.Add(bu_update, 0, wx.CENTER, 5)
        hbs2.Add(10, -1, 0)
        hbs2.Add(bu_clr_display, 0, wx.CENTER, 5)
        hbs2.Add(10, -1, 0)
        hbs2.Add(bu_info, 0, wx.CENTER, 5)

        vbs_main = wx.BoxSizer(wx.VERTICAL)
        vbs_main.Add(hbs1, 0, wx.ALL, 5)  # grid bag and logger
        vbs_main.Add(hbs2, 0, wx.CENTER, 5)  # buttons
        vbs_main.Add((10, 5))  # add spacer after button row
        self.SetSizerAndFit(vbs_main)

        # init the validators' controls
        self.TransferDataToWindow()  # use this instead of InitDialog

    def notify(self, ltr):
        """ The View's job is to update its displayed data from the model and
            to make sure the data is displayed in the correct format.
            Should have no involvement from the Controller and
            the Model's biz logic.

            listener: Specify the listener that is being notified.
        """
        # Make sure the listener is already created before any method call!
        # Follow the order of listener creation in __init__ method.
        # init values managed by model
        if ltr is self.tc_info:
            ltr.SetLabel(self._model.getvalue(ltr.GetName()))
        elif ltr is self.tc_unit_price:
            val = self._model.getstrvalue(ltr.GetName(), '{:.2f}')
            ltr.SetLabel(val)
        elif ltr is self.spcl_qty:
            new_qty = self._model.getvalue(ltr.GetName())
            if new_qty is None or (isinstance(new_qty, float) and
                                   math.isnan(new_qty)):
                new_qty = 0
            ltr.SetValue(new_qty)
            self.sync_total_price(new_qty)

    def evt_radio_box(self, event):
        # process text_msg
        val = event.GetString()
        self.tc_display.AppendText(f'EvtRadioBox: {val}\n')
        # self._controller.change_msg(val)
        if val == 'None':
            self.tc_text_msg.SetValue('')
        elif val == 'Not Ok!':
            self.tc_text_msg.SetValue(val)
            self.tc_text_msg.SetForegroundColour('red')
        else:
            self.tc_text_msg.SetValue(val)
            self.tc_text_msg.SetForegroundColour('forest green')
        # background defaults to white value is updated
        self.tc_text_msg.SetBackgroundColour(self.menu_color)

    def evt_combo_box(self, event):
        self.tc_display.AppendText(
            f'EvtComboBox: {event.GetString()}\n')

    def spcl_qty_updated(self, event):
        # Get quantity and calculates total price
        new_qty = self.spcl_qty.GetValue()
        self.tc_display.AppendText(f'EvtSpinCtrl: {new_qty}\n')
        self.sync_total_price(new_qty)

    def sync_total_price(self, new_qty):
        # get new total_price from model
        new_total_price = self._model.calc_new_total_price(new_qty)
        # show to user
        self.tc_total_price.SetValue(f'{new_total_price:.2f}')

    def on_okay(self, event):
        # Update data to model for ctrls managed by model and will never
        # be handled automatically by the DialogBox unlike validators
        self._controller.update_model()  # both quantity and total_price

        # This is done automatically for dialog box but for panel need to DIY.
        # Updates all validators' control
        if self.Validate() and self.TransferDataFromWindow():
            self.GetParent().Close(True)

    def on_update(self, event):
        # Update data to model for ctrls managed by model
        self._controller.update_model()

        # Update data to model for all validators' control
        if self.Validate():
            self.TransferDataFromWindow()
        # fix background color change in text_msg
        self.tc_text_msg.SetBackgroundColour(self.menu_color)

    def on_cancel(self, event):
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
                      'text_data': 'Enter text here',
                      'float_data': math.nan,
                      'int_data': 15,
                      'test_survey': None,
                      'option': None,
                      'text_message': None,  # need sync with rb
                      'unit_price': 8.00,
                      'quantity': math.nan,
                      'total_price': math.nan,
                      'price_list': {0: ('ZS001', '8.00', '100'),
                                     1: ('ZS002', '10.50', '150'),
                                     2: ('ZS003', '12.50', '50')
                                     }
                      }
        # Init the Model which in a real app has databases and biz logic in it.
        model = DemoModel(model_dict)
        frame = MainWindow(None, model, "Practical MVC Demo")
        # frame.InitDialog()
        frame.Show()

        app.MainLoop()
        print(model.fields_report())

    except Exception:
        traceback.print_exc()
