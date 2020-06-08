""" This module implements the missing FloatingPointValidator,
    IntegerValidator and TextValidator from wxpython.
    Once wxpython implements the missing validators then recommend to
    use their standard validators if it meets your requirements.

    These validators here are used for client-side form validation.
    The client-side data here is stored in the App's model data.
    Only the App's model data is updated by the validators.
    It is the App's responsibility to submit the validated model data to
    the server.

    Client-side validation is an initial check and an important feature of
    good user experience; by catching invalid data on the client-side,
    the user can fix it straight away. If it is caught by the server and then
    rejected, it will cause a noticeable delay.
"""
import math
import wx
from pefc.genericmodels import DictModel, ValidationResult


def highlight_error(ctrl, errormsg, mbtitle):
    ctrl.SetBackgroundColour("pink")
    ctrl.SetFocus()
    ctrl.Refresh()
    wx.MessageBox(errormsg, mbtitle, wx.OK | wx.ICON_ERROR)


def highlight_off(ctrl):
    ctrl.SetBackgroundColour(
        wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
    ctrl.Refresh()


def handle_na(ctrl, value, fill, errormsg, mbtitle):
    if value == '':
        if fill is True:
            highlight_error(ctrl, errormsg, mbtitle)
            retval = False
        else:
            highlight_off(ctrl)
            retval = True
    else:
        retval = 'no NA'
    return retval


def get_verified_value(ctrl, text, dtype, errormsg, mbtitle):
    try:
        retval = dtype(text)
    except ValueError:  # should not happen unless model data error
        highlight_error(ctrl, errormsg, mbtitle)
        retval = None
    else:
        highlight_off(ctrl)
    return retval


def check_limits(ctrl, value, minvalue, maxvalue,
                 errormsg="Input value exceed these limits",
                 mbtitle="Invalid Input"):
    if (value < minvalue or value > maxvalue):
        errormsg = f"{errormsg} ({minvalue}, {maxvalue})"
        highlight_error(ctrl, errormsg, mbtitle)
        return False
    else:
        highlight_off(ctrl)
        return True


class FloatingPointValidator(wx.Validator):
    """ Validator for entering float values within the high and low limits.
        This is a floating point validator for a wx.TextCtrl.
        Currently only fixed format is supported on input,
        i.e. scientific format with mantissa and exponent is not supported.

        Requirements
        ------------
        1. Set style=wx.TE_PROCESS_ENTER in the wx.TextCtrl.
        2. wx.TextCtrl must have the name=field_name of data, e.g. name='price'
           The field name must be present in the App's model data.
           This field name is used by the Validator to access the App's
           model data.
        3. The App's model must implement getstrvalue and setvalue methods
           They use the field names to set and get data from the model.

        Changing the Validator's attributes
        -------------------------------
        Because of cloning the, validator's attributes can only be
        changed through TextCtrl.GetValidator().
        For example TextCtrl.GetValidator().mustfill = False

        MVC
        ---
        A validator mediates between a class of control(View),
        and application data(Model) which makes it also a Controller.
        It is able set and get the Model's data by their field names.
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

    def __init__(self, mdl, limits: tuple = (-100.0, 100.0),
                 mdlvalidate=False, fill=True):
        """ Constructor for FloatValidator

            Parameters
            ----------
              mdl: Model's data.
              limits: tuple of float values, (lower limit, upper limit)
                default (-100.0, 100.0)
              fill: bool, default is True which means it must be filled.
        """
        super().__init__()
        self._model = mdl
        self.minvalue = None if limits is None else min(limits)
        self.maxvalue = None if limits is None else max(limits)
        self.limits = limits
        self._model_validate = mdlvalidate
        self.mustfill = fill
        self.dtype = float  # data type
        self.value = None
        self.na = None  # NA indicator used by model's data
        # Events sent to txtctrl processed by this validator
        self.Bind(wx.EVT_CHAR, self.on_char)

    # MUST implement Clone()
    def Clone(self):
        return self.__class__(self._model, self.limits, self._model_validate,
                              self.mustfill)

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

        res = handle_na(text_ctrl, text, self.mustfill,
                        "This field is required", "Invalid Input")
        if res != 'no NA':
            return res

        self.value = get_verified_value(
            text_ctrl, text, self.dtype,
            "Please enter valid floating point numbers only",
            "Invalid Input")

        if self.value is None:
            self.value = self.na  # model's data NA indicator
            return False

        # validations section
        # If any tests failed then return result immediately and if pass
        # proceed to the next test to avoid hiding the previous test result.
        retval = False
        if self.limits is not None:
            retval = check_limits(text_ctrl, self.value,
                                  self.minvalue, self.maxvalue)
            if retval is False:
                return retval

        if self._model_validate is True:
            fldname = text_ctrl.GetName()
            # call the model's validate function
            vres = self._model.validate(fldname, self.value)
            if vres.result is None or vres.result is False:
                highlight_error(text_ctrl, vres.errormsg, vres.title)
                retval = False
            else:
                highlight_off(text_ctrl)
                retval = True

        return retval

    def TransferToWindow(self):
        text_ctrl = self.GetWindow()  # correct protocol
        # init original value in case of cancel or mustfill = False
        self.value = self._model.getvalue(text_ctrl.GetName())
        if self.value is None:  # NA indicator is None
            val = ''
            self.na = self.value  # store the model's data NA indicator
        elif isinstance(self.value, float) and math.isnan(self.value):
            val = ''  # NA indicator is math.nan
            self.na = self.value
        else:
            val = f'{self.value}'
        # no validation to show error to user, final value is validated anyway
        text_ctrl.SetValue(val)
        return True

    def TransferFromWindow(self):
        text_ctrl = self.GetWindow()  # correct protocol
        if self.Validate(text_ctrl.GetParent()) is True:
            if text_ctrl.GetValue() == '':
                # use back the model's NA indicator to avoid problems
                self._model.setvalue(text_ctrl.GetName(), self.na)
            else:
                self._model.setvalue(text_ctrl.GetName(), self.value)
            return True
        else:
            return False

    def on_char(self, event):
        # process key char to prevent non-numeric entry
        kcode = event.GetKeyCode()
        text_ctrl = event.GetEventObject()
        skip = True
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
                skip = False
        elif kcode == 45:  # '-' = 45, not needed is  '+' = 43
            if text_ctrl.GetInsertionPoint() != 0:  # allow '-' at pos 0 only
                skip = False
        elif kcode == 13:  # 13=CR for style=wx.TE_PROCESS_ENTER
            self.Validate(text_ctrl.GetParent())  # OK button update value
            skip = False  # prevent double processing
        elif kcode == 9:  # 9=TAB for style=wx.TE_PROCESS_ENTER
            self.Validate(text_ctrl.GetParent())  # OK button update value
        else:  # 44 comma or 46 dot, 32 space and other keys swallowed up
            skip = False

        if skip is True:
            event.Skip()  # send for default event handling by text ctrl


class IntegerValidator(wx.Validator):
    """ Validator for entering integer values within the high and low limits.
        This is a integer validator for a wx.TextCtrl.

        Requirements
        ------------
        1. Set style=wx.TE_PROCESS_ENTER in the wx.TextCtrl.
        2. wx.TextCtrl must have the name=field_name of data, e.g. name='price'
           The field name must be present in the App's model data.
           This field name is used by the Validator to access the App's
           model data.
        3. The App's model must implement getstrvalue and setvalue methods
           They use the field names to set and get data from the model.

        Changing the Validator's attributes
        -------------------------------
        Because of cloning, the validator's attributes can only be
        changed through TextCtrl.GetValidator().
        For example TextCtrl.GetValidator().mustfill = False

        MVC
        ---
        A validator mediates between a class of control(View),
        and application data(Model) which makes it also a Controller.
        It is able set and get the Model's data by their field names.
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

    def __init__(self, mdl, limits: tuple = (-100, 100), fill=True):
        """ Constructor for IntegerValidator

            Parameters
            ----------
              mdl: Model's data. Model must implement getstrvalue and setvalue.
              lowlim: lower limit of float value
              upperlim: upper limit of float value
        """
        super().__init__()
        self._model = mdl
        self.minvalue = min(limits)
        self.maxvalue = max(limits)
        self.limits = limits
        self.mustfill = fill
        self.value = None
        # Events sent to txtctrl processed by this validator
        self.Bind(wx.EVT_CHAR, self.on_char)

    # MUST implement Clone()
    def Clone(self):
        return self.__class__(self._model, self.limits, self.mustfill)

    def Validate(self, parent):
        """ Check that the input is numeric and is within the limits specified
        """
        # correct protocol to get the validator's associated control.
        text_ctrl = self.GetWindow()
        text = text_ctrl.GetValue()

        if text == '':
            if self.mustfill is True:
                highlight_error(text_ctrl, "This field is required",
                                "Invalid Input")
                return False
            else:
                return True

        try:
            self.value = int(text)
        except ValueError:  # should not happen unless model data error
            highlight_error(text_ctrl,
                            "Please enter valid integer numbers only",
                            "Invalid Input")
            return False
        else:
            return check_limits(text_ctrl, self.value,
                                self.minvalue, self.maxvalue)

    def TransferToWindow(self):
        text_ctrl = self.GetWindow()  # correct protocol
        # init original value
        self.value = self._model.getvalue(text_ctrl.GetName())
        val = '' if self.value is None or math.isnan(
            self.value) else f'{self.value}'
        # no validation if error is from user, final value is validated
        text_ctrl.SetValue(val)
        return True

    def TransferFromWindow(self):
        text_ctrl = self.GetWindow()  # correct protocol
        if self.Validate(text_ctrl.GetParent()) is True:
            self._model.setvalue(text_ctrl.GetName(), self.value)
            return True
        else:
            return False

    def on_char(self, event):
        # process key char to prevent non-numeric entry
        kcode = event.GetKeyCode()
        text_ctrl = event.GetEventObject()
        skip = True
        # print(kcode)  # for debugging
        # '0' = 48 and '9' = 57,
        if (48 <= kcode <= 57) or self.allowedkeys.get(kcode, False):
            pass
        elif kcode == 45:  # '-' = 45, not needed is  '+' = 43
            if text_ctrl.GetInsertionPoint() != 0:  # allow '-' at pos 0 only
                skip = False
        elif kcode == 13:  # 13=CR for style=wx.TE_PROCESS_ENTER
            self.Validate(text_ctrl.GetParent())  # OK button update value
            skip = False  # prevent double processing
        elif kcode == 9:  # 9=TAB for style=wx.TE_PROCESS_ENTER
            self.Validate(text_ctrl.GetParent())  # OK button update value
        else:  # 44 comma or 46 dot, 32 space and other keys swallowed up
            skip = False

        if skip is True:
            event.Skip()  # send for default event handling by text ctrl


class TextValidator(wx.Validator):
    """ Validator for entering text.
        This is a text validator for a wx.TextCtrl.

        Requirements
        ------------
        1. Set style=wx.TE_PROCESS_ENTER in the wx.TextCtrl.
        2. wx.TextCtrl must have the name=field_name of data, e.g. name='price'
           The field name must be present in the App's model data.
           This field name is used by the Validator to access the App's
           model data.
        3. The App's model must implement getstrvalue and setvalue methods
           They use the field names to set and get data from the model.

        Changing the Validator's attributes
        -------------------------------
        Because of cloning the, validator's attributes can only be
        changed through TextCtrl.GetValidator().
        For example TextCtrl.GetValidator().mustfill = False

        MVC
        ---
        A validator mediates between a class of control(View),
        and application data(Model) which makes it also a Controller.
        It is able set and get the Model's data by their field names.
        The App's Controller should delegate its responsibility to this
        validator and set its limits.
    """
    # NOTE: Use vfunc instead of pattern (regular expression)

    def __init__(self, mdl, limits: tuple = (-100, 100), vfunc=None):
        """ Constructor for TextValidator

            Parameters
            ----------
            mdl: Model's data.

            limits: tuple of int values, (min len limit, max len limit)
                default (0, 25)

            vfunc: validate function name. Default is None. i.e. no validation.

        """
        super().__init__()
        self._model = mdl
        self.minlength = min(limits)
        self.maxlength = max(limits)
        self.limits = limits
        self.required = True  # required to be filled.
        self._vfunc = vfunc
        self.value = None
        # Events sent to txtctrl processed by this validator
        self.Bind(wx.EVT_CHAR, self.on_char)

    # MUST implement Clone()
    def Clone(self):
        return self.__class__(self._model, self.limits, self._vfunc)

    def Validate(self, parent):
        """ Check that the input is numeric and is within the limits specified
        """
        # correct protocol to get the validator's associated control.
        text_ctrl = self.GetWindow()
        text = text_ctrl.GetValue()

        try:
            self.value = int(text)
        except ValueError:  # should not happen unless model data error
            text_ctrl.SetBackgroundColour("pink")
            text_ctrl.SetFocus()
            text_ctrl.Refresh()
            wx.MessageBox("Please enter valid integer numbers only",
                          "Invalid Input",
                          wx.OK | wx.ICON_ERROR)
            return False
        else:  # control string lengths
            if (len(self.value) < self.minlength or
                    len(self.value) > self.maxlength):
                text_ctrl.SetBackgroundColour("pink")
                text_ctrl.SetFocus()
                text_ctrl.Refresh()
                wx.MessageBox(
                    "Text length exceed these limits ({}, {})".format(
                        self.minlength, self.maxlength),
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
        # init original value
        self.value = self._model.getvalue(text_ctrl.GetName())
        val = '' if self.value is None or math.isnan(
            self.value) else f'{self.value}'
        # no validation if error is from user, final value is validated
        text_ctrl.SetValue(val)
        return True

    def TransferFromWindow(self):
        text_ctrl = self.GetWindow()  # correct protocol
        if self.Validate(text_ctrl.GetParent()) is True:
            self._model.setvalue(text_ctrl.GetName(), self.value)
            return True
        else:
            return False

    def on_char(self, event):
        # process key char to prevent non-numeric entry
        kcode = event.GetKeyCode()
        text_ctrl = event.GetEventObject()
        skip = True
        # print(kcode)  # for debugging
        # '0' = 48 and '9' = 57,
        if (48 <= kcode <= 57) or self.allowedkeys.get(kcode, False):
            pass
        elif kcode == 45:  # '-' = 45, not needed is  '+' = 43
            if text_ctrl.GetInsertionPoint() != 0:  # allow '-' at pos 0 only
                skip = False
        elif kcode == 13:  # 13=CR for style=wx.TE_PROCESS_ENTER
            self.Validate(text_ctrl.GetParent())  # OK button update value
            skip = False  # prevent double processing
        elif kcode == 9:  # 9=TAB for style=wx.TE_PROCESS_ENTER
            self.Validate(text_ctrl.GetParent())  # OK button update value
        else:  # 44 comma or 46 dot, 32 space and other keys swallowed up
            skip = False

        if skip is True:
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
            st_heading = wx.StaticText(self, label=heading)
            font = wx.Font(wx.FontInfo(12).Bold().Underlined())
            st_heading.SetFont(font)

            # Create the text controls and set the validators
            # Tab sequence are in order of creation
            # floating point tests
            st_fv = wx.StaticText(self, label="Float value(fv):")
            tc_float_data = wx.TextCtrl(
                self, value='', size=(100, -1),
                style=wx.TE_PROCESS_ENTER,  # get tab and CR
                validator=FloatingPointValidator(
                    self._model, (-50.0, 150.0)),
                name='float_value')
            # integer data tests
            st_iv = wx.StaticText(self, label="Integer value(iv):")
            tc_int_data = wx.TextCtrl(
                self, value='', size=(100, -1),
                style=wx.TE_PROCESS_ENTER,  # get tab and CR
                validator=IntegerValidator(self._model, (-100, 100)),
                name='int_value')
            tc_float_data.GetValidator().mustfill = False  # mustfill test
            # model validator test
            st_constraint = wx.StaticText(self, label="Constraint value:")
            tc_constraint = wx.TextCtrl(
                self, value='', size=(100, -1),
                style=wx.TE_PROCESS_ENTER,  # get tab and CR
                validator=FloatingPointValidator(
                    self._model, None, True),
                name='constraint')

            fgs = wx.FlexGridSizer(3, 3, 5, 5)
            fgs.Add(st_fv, 0, wx.ALIGN_RIGHT)
            fgs.Add(tc_float_data, 0, wx.EXPAND)
            fgs.Add(wx.StaticText(self, label="limits (-50.0, 150.0)"),
                    0, wx.EXPAND)
            fgs.Add(st_iv, 0, wx.ALIGN_RIGHT)
            fgs.Add(tc_int_data, 0, wx.EXPAND)
            fgs.Add(wx.StaticText(self, label="limits (-100, 100)"),
                    0, wx.EXPAND)
            # test on model's validate_* func
            fgs.Add(st_constraint, 0, wx.ALIGN_RIGHT)
            fgs.Add(tc_constraint, 0, wx.EXPAND)
            fgs.Add(wx.StaticText(self, label="valid values are -3, 5, 10"),
                    0, wx.EXPAND)

            # Use standard button IDs for validators to work correctly
            bu_okay = wx.Button(self, wx.ID_OK)
            bu_okay.SetDefault()
            bu_cancel = wx.Button(self, wx.ID_CANCEL)
            # non-standard buttons
            # bu_show_fields = wx.Button(self, wx.ID_ANY, 'Show Fields')
            # self.Bind(wx.EVT_BUTTON, self.show_fields, bu_show_fields)
            # only for standard buttons e.g. ID_OK and ID_CANCEL
            bus = wx.StdDialogButtonSizer()  # for look and feel
            bus.AddButton(bu_okay)
            bus.AddButton(bu_cancel)
            bus.Realize()

            # Layout with sizers
            vbs_main = wx.BoxSizer(wx.VERTICAL)
            vbs_main.Add(st_heading)
            vbs_main.Add((10, 10))
            vbs_main.Add(fgs)
            vbs_main.Add((10, 10))
            # vbs_main.Add(bu_show_fields)
            # vbs_main.Add((10, 10))
            vbs_main.Add(bus)

            self.SetSizerAndFit(vbs_main)
            self.CenterOnScreen()

        def show_fields(self, event):
            print(self._model.fields_report())

    class AppModel(DictModel):
        def __init__(self, model_dict):
            # inherits from DictModel
            super().__init__(model_dict)

        def validate_constraint(self, field_name, new_value):
            # test validate using the model's validate_* function
            if (math.isclose(new_value, 5.0) or math.isclose(new_value, 10.0)
                    or math.isclose(new_value, -3.0)):
                return ValidationResult(True)
            else:
                return ValidationResult(
                    False, 'Value must be -3, 5 or 10', 'Input Error')

    # run the demos
    app = wx.App(False)
    mydict = {"float_value": math.nan, "int_value": None,
              "constraint": None}
    # create the App's model
    mymodel = AppModel(mydict)

    with CheckValidatorsDialog(None, mymodel,
                               title='Validators Test') as dlg:
        if dlg.ShowModal() == wx.ID_OK:
            print("Congragulations! Data Entry done correctly.")
        else:
            print('Data Entry Dialog cancelled!')

    app.MainLoop()
    print(mymodel.fields_report())
