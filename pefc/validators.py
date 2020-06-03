""" This module implements the missing IntegerValidator
    and FloatingPointValidator from wxpython.
    Once wxpython implements the missing validators then recommend to
    use their standard validators.
"""
import math
import wx


class FloatValidator(wx.Validator):
    """ Validator for entering float values with high and low limits.
        This is a floating point validator for a wx.TextCtrl.
        Currently only fixed format is supported on input,
        i.e. scientific format with mantissa and exponent is not supported.

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
        except ValueError:
            text_ctrl.SetBackgroundColour("pink")
            text_ctrl.SetFocus()
            text_ctrl.Refresh()
            wx.MessageBox("Please enter valid floating point numbers only",
                          "Invalid Input",
                          wx.OK | wx.ICON_ERROR)
            return False
        else:
            if self.fvalue < self.lower_limit or \
                    self.fvalue > self.upper_limit:
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
        # no validation if error is from developer
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
        print(kcode)  # for debugging
        # TODO: Add change of focus
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
        elif kcode == 13 or kcode == 9:  # 13=CR and 9=TAB
            self.TransferFromWindow()
        else:  # 44 comma or 46 dot, 32 space and other keys swallowed up
            return
        event.Skip()  # send for default event handling by text ctrl
