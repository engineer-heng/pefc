""" This module implements the missing IntegerValidator
    and FloatingPointValidator from wxpython.
    Once wxpython implements the missing validators then recommend to
    use their standard validators.
"""
import wx
# Reference
# https://www.pythonstudio.us/wxpython/how-do-i-use-a-validator-to-ensure-correct-data.html


class FloatValidator(wx.Validator):
    """ Validator for entering float values with high and low limits
    """

    def __init__(self, mdl, lowlim=0.0, upperlim=10000.0,):
        super().__init__()
        self._model = mdl
        self.lower_limit = lowlim
        self.upper_limit = upperlim
        self.value = ''

    # MUST implement Clone()
    def Clone(self):
        return FloatValidator(self._model, self.lower_limit, self.upper_limit)

    def outside_limits(self):
        if self.value < self.lower_limit or self.value > self.upper_limit:
            return True
        return False

    def Validate(self, parent):
        """ Check that the input is numeric and is within the limits specified
        """
        # Usually for a TextCtrl
        text_ctrl = self.GetWindow()
        text = text_ctrl.GetValue()

        try:
            self.value = float(text)
        except ValueError:
            wx.MessageBox("Please enter valid floating point numbers only",
                          "Invalid Input",
                          wx.OK | wx.ICON_ERROR)
            text_ctrl.SetValue('')
            return False
        else:
            if self.outside_limits():
                wx.MessageBox(
                    "Input value exceed these limits ({}, {})".format(
                        self.lower_limit, self.upper_limit),
                    "Invalid Input",
                    wx.OK | wx.ICON_ERROR)
            text_ctrl.SetValue('')
            return False
        return True

    def TransferToWindow(self):
        text_ctrl = self.GetWindow()
        text_ctrl.SetValue(
            self._model.getstrvalue(text_ctrl.GetName(), '{}'))
        return True

    def TransferFromWindow(self):
        text_ctrl = self.GetWindow()
        try:
            val = float(text_ctrl.GetValue())
        except ValueError:
            wx.MessageBox("Please enter valid floating point numbers only",
                          "Invalid Input",
                          wx.OK | wx.ICON_ERROR)
            text_ctrl.SetValue('')
            return False
        self._model.setvalue(text_ctrl.GetName(), val)
        return True
