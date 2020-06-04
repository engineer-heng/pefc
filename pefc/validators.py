""" This module implements the missing IntegerValidator
    and FloatingPointValidator from wxpython.
    Once wxpython implements the missing validators then recommend to
    use their standard validators.
"""
import math
import wx
from pefc.genericmodels import DictModel


class FloatValidator(wx.Validator):
    """ Validator for entering float values within the high and low limits.
        This is a floating point validator for a wx.TextCtrl.
        Currently only fixed format is supported on input,
        i.e. scientific format with mantissa and exponent is not supported.

        Require to set style=wx.TE_PROCESS_ENTER in the wx.TextCtrl.

        MVC
        ---
        A validator mediates between a class of control(View),
        and application data(Model) which makes it also a Controller.
        It is able get and set the Model's data.
        The App's Controller should delegate its responsibility to this
        validator and set its limits.
    """
    # ASCII key codes which do not change
    decimal_point = 46  # default is 46 ('.'), EU is 44 (',')
    allowedkeys = {
        3: True, 22: True, 24: True,  # 3=CTRL-C, 22=CTRL-V, 24=CTRL-X
        8: True, 127: True,  # 8=BS, 127=DEL, no need for 322=Ins
        312: True, 313: True,  # 312=End, 313=Home
        314: True, 315: True, 316: True, 317: True  # arrow keys
    }

    def __init__(self, mdl, lowlim: float = 0.0, upperlim: float = 100.0):
        """ Constructor for FloatValidator

            Parameters
            ----------
              mdl: Model's data. Model must implement getstrvalue and setvalue.
              lowlim: lower limit of float value
              upperlim: upper limit of float value
        """
        super().__init__()
        self._model = mdl
        self.lower_limit = lowlim
        self.upper_limit = upperlim
        self.fvalue = math.nan
        # Events sent to txtctrl processed by this validator
        self.Bind(wx.EVT_CHAR, self.on_char)

    # MUST implement Clone()
    def Clone(self):
        return self.__class__(self._model, self.lower_limit, self.upper_limit)

    def Validate(self, parent):
        """ Check that the input is numeric and is within the limits specified
        """
        # use the text_ctrl's parent if you want to get the data from other
        # widgets in the dialog/panel if that's important, or you can
        # ignore the argument altogether.

        # correct protocol to get the validator's associated control.
        # self.text_ctrl in Validator cause NoneType obj
        text_ctrl = self.GetWindow()
        text = text_ctrl.GetValue()

        try:
            self.fvalue = float(text)
        except ValueError:  # should not happen unless model data error
            text_ctrl.SetBackgroundColour("pink")
            text_ctrl.SetFocus()
            text_ctrl.Refresh()
            wx.MessageBox("Please enter valid floating point numbers only",
                          "Invalid Input",
                          wx.OK | wx.ICON_ERROR)
            return False
        else:
            if (self.fvalue < self.lower_limit or
                    self.fvalue > self.upper_limit):
                text_ctrl.SetBackgroundColour("pink")
                text_ctrl.SetFocus()
                text_ctrl.Refresh()
                wx.MessageBox(
                    "Input value exceed these limits ({}, {})".format(
                        self.lower_limit, self.upper_limit),
                    "Invalid Input",
                    wx.OK | wx.ICON_ERROR)
                return False
            else:
                text_ctrl.SetBackgroundColour(
                    wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
                text_ctrl.Refresh()
                return True

    def TransferToWindow(self):
        text_ctrl = self.GetWindow()  # correct protocol
        # no validation if error is from user, final value is validated
        text_ctrl.SetValue(
            self._model.getstrvalue(text_ctrl.GetName(), '{}'))
        return True

    def TransferFromWindow(self):
        text_ctrl = self.GetWindow()  # correct protocol
        if self.Validate(text_ctrl.GetParent()) is True:
            self._model.setvalue(text_ctrl.GetName(), self.fvalue)
            return True
        else:
            return False

    def on_char(self, event):
        # process key char to prevent non-numeric entry
        kcode = event.GetKeyCode()
        text_ctrl = event.GetEventObject()
        # print(kcode)  # for debugging
        # NOTE: Update data on CR, tab or change of focus is incorrect
        # because if cancelled cannot undo changes especially in forms.
        # Better to add an 'update' button.
        # '0' = 48 and '9' = 57,
        if (48 <= kcode <= 57) or self.allowedkeys.get(kcode, False):
            pass
        elif kcode == self.decimal_point:  # '.' or ',' internationalization
            # decimal_point should only appear once
            if text_ctrl.GetValue().rfind(chr(self.decimal_point)) != -1:
                return
        elif kcode == 45:  # '-' = 45, not needed is  '+' = 43
            if text_ctrl.GetInsertionPoint() != 0:  # allow '-' at pos 0 only
                return
        elif kcode == 13:  # 13=CR for style=wx.TE_PROCESS_ENTER
            self.Validate(text_ctrl.GetParent())  # OK button update value
            return  # prevent double processing
        elif kcode == 9:  # 9=TAB for style=wx.TE_PROCESS_ENTER
            self.Validate(text_ctrl.GetParent())  # OK button update value
        else:  # 44 comma or 46 dot, 32 space and other keys swallowed up
            return
        event.Skip()  # send for default event handling by text ctrl


class IntegerValidator(wx.Validator):
    """ Validator for entering integer values within the high and low limits.
        This is a integer validator for a wx.TextCtrl.

        Require to set style=wx.TE_PROCESS_ENTER in the wx.TextCtrl.

        MVC
        ---
        A validator mediates between a class of control(View),
        and application data(Model) which makes it also a Controller.
        It is able get and set the Model's data.
        The App's Controller should delegate its responsibility to this
        validator and set its limits.
    """
    # ASCII key codes which do not change
    decimal_point = 46  # default is 46 ('.'), EU is 44 (',')
    allowedkeys = {
        3: True, 22: True, 24: True,  # 3=CTRL-C, 22=CTRL-V, 24=CTRL-X
        8: True, 127: True,  # 8=BS, 127=DEL, no need for 322=Ins
        312: True, 313: True,  # 312=End, 313=Home
        314: True, 315: True, 316: True, 317: True  # arrow keys
    }

    def __init__(self, mdl, lowlim: int = 0, upperlim: int = 100):
        """ Constructor for IntegerValidator

            Parameters
            ----------
              mdl: Model's data. Model must implement getstrvalue and setvalue.
              lowlim: lower limit of float value
              upperlim: upper limit of float value
        """
        super().__init__()
        self._model = mdl
        self.lower_limit = lowlim
        self.upper_limit = upperlim
        self.ivalue = math.nan
        # Events sent to txtctrl processed by this validator
        self.Bind(wx.EVT_CHAR, self.on_char)

    # MUST implement Clone()
    def Clone(self):
        return self.__class__(self._model, self.lower_limit, self.upper_limit)

    def Validate(self, parent):
        """ Check that the input is numeric and is within the limits specified
        """
        # use the text_ctrl's parent if you want to get the data from other
        # widgets in the dialog/panel if that's important, or you can
        # ignore the argument altogether.

        # correct protocol to get the validator's associated control.
        text_ctrl = self.GetWindow()
        text = text_ctrl.GetValue()

        try:
            self.ivalue = int(text)
        except ValueError:  # should not happen unless model data error
            text_ctrl.SetBackgroundColour("pink")
            text_ctrl.SetFocus()
            text_ctrl.Refresh()
            wx.MessageBox("Please enter valid integer numbers only",
                          "Invalid Input",
                          wx.OK | wx.ICON_ERROR)
            return False
        else:
            if (self.ivalue < self.lower_limit or
                    self.ivalue > self.upper_limit):
                text_ctrl.SetBackgroundColour("pink")
                text_ctrl.SetFocus()
                text_ctrl.Refresh()
                wx.MessageBox(
                    "Input value exceed these limits ({}, {})".format(
                        self.lower_limit, self.upper_limit),
                    "Invalid Input",
                    wx.OK | wx.ICON_ERROR)
                return False
            else:
                text_ctrl.SetBackgroundColour(
                    wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
                text_ctrl.Refresh()
                return True

    def TransferToWindow(self):
        text_ctrl = self.GetWindow()  # correct protocol
        # no validation if error is from user, final value is validated
        text_ctrl.SetValue(
            self._model.getstrvalue(text_ctrl.GetName(), '{}'))
        return True

    def TransferFromWindow(self):
        text_ctrl = self.GetWindow()  # correct protocol
        if self.Validate(text_ctrl.GetParent()) is True:
            self._model.setvalue(text_ctrl.GetName(), self.ivalue)
            return True
        else:
            return False

    def on_char(self, event):
        # process key char to prevent non-numeric entry
        kcode = event.GetKeyCode()
        text_ctrl = event.GetEventObject()
        # print(kcode)  # for debugging
        # '0' = 48 and '9' = 57,
        if (48 <= kcode <= 57) or self.allowedkeys.get(kcode, False):
            pass
        elif kcode == 45:  # '-' = 45, not needed is  '+' = 43
            if text_ctrl.GetInsertionPoint() != 0:  # allow '-' at pos 0 only
                return
        elif kcode == 13:  # 13=CR for style=wx.TE_PROCESS_ENTER
            self.Validate(text_ctrl.GetParent())  # OK button update value
            return  # prevent double processing
        elif kcode == 9:  # 9=TAB for style=wx.TE_PROCESS_ENTER
            self.Validate(text_ctrl.GetParent())  # OK button update value
        else:  # 44 comma or 46 dot, 32 space and other keys swallowed up
            return
        event.Skip()  # send for default event handling by text ctrl


if __name__ == '__main__':

    class CheckValidatorsDialog(wx.Dialog):
        """ For a Dialog box, the Window.TransferDataToWindow() and
            Window.TransferDataFromWindow() are called automatically.
            The model data fields are initialized and updated by the Dialog
            Box. If it is Panel/Wizard they have to be explicitly called in
            your code. See mvc_demo.py for a sample code on how it is done.
        """

        def __init__(self, parent, mdl, *args, **kwargs):
            super().__init__(parent, *args, **kwargs)
            self._model = mdl

            heading = "DIALOG BOX DEMO"
            stxt_heading = wx.StaticText(self, label=heading)
            font = wx.Font(wx.FontInfo(12).Bold().Underlined())
            stxt_heading.SetFont(font)

            # Create the text controls and set the validators
            # floating point tests
            stxt_fv = wx.StaticText(self, label="Float value(fv):")
            tc_float_data = wx.TextCtrl(
                self, value='', size=(100, -1),
                style=wx.TE_PROCESS_ENTER,  # get tab and CR
                validator=FloatValidator(self._model, -50.0, 150.0),
                name='float_value')
            # integer data tests
            stxt_iv = wx.StaticText(self, label="Integer value(iv):")
            tc_int_data = wx.TextCtrl(
                self, value='', size=(100, -1),
                style=wx.TE_PROCESS_ENTER,  # get tab and CR
                validator=IntegerValidator(self._model, -100, 100),
                name='int_value')

            fgs = wx.FlexGridSizer(2, 3, 5, 5)
            fgs.Add(stxt_fv, 0, wx.ALIGN_RIGHT)
            fgs.Add(tc_float_data, 0, wx.EXPAND)
            fgs.Add(wx.StaticText(self, label="limits (-50.0, 150.0)"),
                    0, wx.EXPAND)
            fgs.Add(stxt_iv, 0, wx.ALIGN_RIGHT)
            fgs.Add(tc_int_data, 0, wx.EXPAND)
            fgs.Add(wx.StaticText(self, label="limits (-100, 100)"),
                    0, wx.EXPAND)

            # Use standard button IDs for validators to work correctly
            btn_okay = wx.Button(self, wx.ID_OK)
            btn_okay.SetDefault()
            btn_cancel = wx.Button(self, wx.ID_CANCEL)
            # non-standard buttons
            # btn_show_fields = wx.Button(self, wx.ID_ANY, 'Show Fields')
            # self.Bind(wx.EVT_BUTTON, self.show_fields, btn_show_fields)
            # only for standard buttons e.g. ID_OK and ID_CANCEL
            btn_sizer = wx.StdDialogButtonSizer()  # for look and feel
            btn_sizer.AddButton(btn_okay)
            btn_sizer.AddButton(btn_cancel)
            btn_sizer.Realize()

            # Layout with sizers
            vbs_main = wx.BoxSizer(wx.VERTICAL)
            vbs_main.Add(stxt_heading)
            vbs_main.Add((10, 10))
            vbs_main.Add(fgs)
            vbs_main.Add((10, 10))
            # vbs_main.Add(btn_show_fields)
            # vbs_main.Add((10, 10))
            vbs_main.Add(btn_sizer)

            self.SetSizerAndFit(vbs_main)
            self.CenterOnScreen()

        def show_fields(self, event):
            print(self._model.fields_report())

    # run the demos
    app = wx.App(False)

    mydict = {"float_value": None, "int_value": None}
    mymodel = DictModel(mydict)

    with CheckValidatorsDialog(None, mymodel,
                               title='Validators Test') as dlg:
        if dlg.ShowModal() == wx.ID_OK:
            print("Congragulations! Data Entry done correctly.")
        else:
            print('Data Entry Dialog cancelled!')

    app.MainLoop()
    print(mymodel.fields_report())
