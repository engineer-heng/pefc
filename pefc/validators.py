""" This module implements the missing GenericValidator,
    FloatingPointValidator, IntegerValidator and TextValidator from wxpython.
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
from decimal import Decimal
from enum import Enum

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


class GenericValidator(wx.Validator):
    """ This GenericValidator is the base class for FloatingPointValidator,
        IntegerValidator and TextValidator. Derive from this Validator for
        your custom validator by setting dtype and dtype_code attributes.
        For example the IntegerValidator is done by setting:
            dtype = int
            dtype_code = self.ValDtype.INTEGER

        Only need to implement the __init__ and Clone method. For derived
        class, implement the Clone method by just calling super().Clone().
        The GenericValidator will handle the validation.

        Requirements
        ------------
        1. Set style=wx.TE_PROCESS_ENTER in the wx.TextCtrl.
        2. wx.TextCtrl must have the name=field_name of data, e.g. name='price'
           The field name must be present in the App's model data.
           This field name is used by the Validator to access the App's
           model data.
        3. The App's model must implement getvalue and setvalue methods.
           They use the field names to set and get data from the model.
           The model can validate it's own field by implementing
           validate_field_name method and setting the mdlvalidate parameter
           to True. E.g. validate_price('price', new_value) method in the model
           will validate the price field. The Validator will call the method
           based on the field name.

        Changing the Validator's attributes
        -----------------------------------
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
    # Validator's data type enum
    ValDtype = Enum('ValDtype', 'STRING FLOAT INTEGER', module=__name__)

    def __init__(self, mdl, limits: None,
                 mdlvalidate=False, fill=True):
        """ Constructor for GeneratorValidator
            This is a generic validator for a wx.TextCtrl. It is the base
            class of FloatingPointValidator, IntegerValidator, TextValidator
            and DecimalValidator. It provides generic implementation for
            Validate, TransferToWindow, TransferFromWindow methods that can be
            used by the derived classes. It processes the keyboard keys
            according to the ValDtype specified.

            Parameters
            ----------
            mdl: Model's data.

            limits: tuple of (lower_limit, upper_limit), default is None.

            mdlvalidate: bool, default is False. If True, the Validate()
            method will call the model's validate_field_name() to validate
            the field_name's value. Make sure that the model implement
            the validate_field_name method.

            fill: bool, default is True which means it must be filled.
        """
        super().__init__()
        self._model = mdl
        self.minvalue = None if limits is None else min(limits)
        self.maxvalue = None if limits is None else max(limits)
        self.limits = limits
        self._model_validate = mdlvalidate
        self.mustfill = fill

        # dtype and dtype_code must be set by the derived class
        self.dtype = str  # data type, default for GenericValidator is str
        # avoid self.dtype == float or self.dype is float in case of issues.
        # str code = self.ValDtype.STRING, float code = self.ValDtype.FLOAT
        # int code = self.ValDtype.INTEGER
        # dtype_code will determine how the validator process the dtype.
        self.dtype_code = self.ValDtype.STRING  # default for GenericValidator

        self.value = None
        self.na = None  # default NA indicator or by model's NA indicator
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

        # handle NA
        if text == '':
            if self.mustfill is True:
                highlight_error(text_ctrl, "This field is required",
                                "Invalid Input")
                return False
            else:
                highlight_off(text_ctrl)
                return True

        # verify that self.value is the correct dtype
        if self.dtype_code == self.ValDtype.STRING:  # no test for text str
            self.value = text
        else:
            if self.dtype_code == self.ValDtype.FLOAT:
                errormsg = "Please enter valid floating point numbers only"
            elif self.dtype_code == self.ValDtype.INTEGER:
                errormsg = "Please enter valid integer numbers only"
            else:  # unsupported type
                raise TypeError('unsupported type for GenericValidator')
            # safely get the value from control
            try:
                self.value = self.dtype(text)
            except ValueError:  # should not happen unless model data error
                highlight_error(text_ctrl, errormsg,  "Invalid Input")
                self.value = self.na  # model's data NA indicator
                return False
            else:
                highlight_off(text_ctrl)

        # validations section
        # If any tests failed then return result immediately and if pass
        # proceed to the next test to avoid hiding the previous test result.

        # check limits for text is length of text
        if self.limits is not None:
            if self.dtype_code == self.ValDtype.STRING:
                value = len(text)
                errormsg = f'Text length of {value} exceeds these limits'
            else:
                value = self.value
                errormsg = "Input value exceeds these limits"
            if (value < self.minvalue or value > self.maxvalue):
                errormsg = f"{errormsg} ({self.minvalue}, {self.maxvalue})"
                highlight_error(text_ctrl, errormsg, "Invalid Input")
                return False
            else:
                highlight_off(text_ctrl)

        retval = True
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
        # '0' = 48 and '9' = 57
        if (48 <= kcode <= 57) or self.allowedkeys.get(kcode, False):
            pass
        elif kcode == self.decimal_point:  # '.' or ',' internationalization
            if self.dtype_code == self.ValDtype.FLOAT:
                # decimal_point should only appear once
                if text_ctrl.GetValue().rfind(chr(self.decimal_point)) != -1:
                    skip = False
            elif self.dtype_code == self.ValDtype.INTEGER:  # no decimal point
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
            if self.dtype_code != self.ValDtype.STRING:
                skip = False  # for numeric, swallow remaining keys

        if skip is True:
            event.Skip()  # send for default event handling by text ctrl


class FloatingPointValidator(GenericValidator):

    def __init__(self, mdl, limits: None,
                 mdlvalidate=False, fill=True):
        """ Constructor for FloatPointValidator
            This is a floating point validator for a wx.TextCtrl.
            Currently only fixed format is supported on input, i.e.
            scientific format with mantissa and exponent are not supported.

            Parameters
            ----------
            mdl: Model's data.

            limits: tuple of float values, (lower_limit, upper_limit).
            default is None.

            mdlvalidate: bool, default is False. If True, the Validate()
            method will call the model's validate_field_name() to validate
            the field_name's value. Make sure that the model implement
            the validate_field_name method.

            fill: bool, default is True which means it must be filled.
         """
        super().__init__(mdl, limits, mdlvalidate, fill)
        self.dtype = float  # override Generic Validator's default value
        self.dtype_code = self.ValDtype.FLOAT

    def Clone(self):
        return super().Clone()


class IntegerValidator(GenericValidator):

    def __init__(self, mdl, limits: None,
                 mdlvalidate=False, fill=True):
        """ Constructor for IntegerValidator
            This is a integer validator for a wx.TextCtrl.

            Parameters
            ----------
            mdl: Model's data.

            limits: tuple of int values, (lower_limit, upper_limit)
            default is None.

            mdlvalidate: bool, default is False. If True, the Validate()
            method will call the model's validate_field_name() to validate
            the field_name's value. Make sure that the model implement
            the validate_field_name method.

            fill: bool, default is True which means it must be filled.
         """
        super().__init__(mdl, limits, mdlvalidate, fill)
        self.dtype = int  # override Generic Validator's default value
        self.dtype_code = self.ValDtype.INTEGER

    def Clone(self):
        return super().Clone()


# Currently the TextValidator is same as GenericValidator
class TextValidator(GenericValidator):
    """ Constructor for TextValidator
        This is a text validator for a wx.TextCtrl.
        Regular expression pattern should be implemented by the
        model's validate_field_name method.

        Parameters
        ----------
        mdl: Model's data.

        limits: tuple of text's lengths, (lower_limit, upper_limit)
        default is None. lower_limit=0 means allow blank input

        mdlvalidate: bool, default is False. If True, the Validate()
        method will call the model's validate_field_name() to validate
        the field_name's value. Make sure that the model implement
        the validate_field_name method.

        fill: bool, default is True which means it must be filled.
    """

    def __init__(self, mdl, limits: None,
                 mdlvalidate=False, fill=True):
        super().__init__(mdl, limits, mdlvalidate, fill)
        self.dtype = str  # override Generic Validator's default value
        self.dtype_code = self.ValDtype.STRING
        if self.minvalue < 0:
            self.minvalue = 0  # no negative len of text

    def Clone(self):
        return super().Clone()


class DecimalValidator(GenericValidator):
    """ Constructor for DecimalValidator
        This is a decimal validator for a wx.TextCtrl.
        Currently only fixed format is supported on input, i.e.
        scientific format with mantissa and exponent are not supported.

        Parameters
        ----------
        mdl: Model's data.

        limits: tuple of text's lengths, (lower_limit, upper_limit)
            default is None.

        mdlvalidate: bool, default is False. If True, the Validate()
        method will call the model's validate_field_name() to validate
        the field_name's value. Make sure that the model implement
        the validate_field_name method.

        fill: bool, default is True which means it must be filled.
    """

    def __init__(self, mdl, limits: None,
                 mdlvalidate=False, fill=True):
        super().__init__(mdl, limits, mdlvalidate, fill)
        self.dtype = Decimal  # override Generic Validator's default value
        self.dtype_code = self.ValDtype.FLOAT

    def Clone(self):
        return super().Clone()


class BoolValidator(wx.Validator):
    """ This is BoolValidator for a wx.CheckBox. It can handle both the
        default 2 state check box and 3 state check box.
        The following style can be used for a 3 state check box.
            style=wx.wx.CHK_3STATE | wx.CHK_ALLOW_3RD_STATE_FOR_USER

        Requirements
        ------------
        1. wx.CheckBox must have the name=field_name of data,
           e.g. name='status'.
           The field name must be present in the App's model data.
           This field name is used by the Validator to access the App's
           model data.
        2. The App's model must implement getvalue and setvalue methods.
           They use the field names to set and get data from the model.
           The model can validate it's own field by implementing
           validate_field_name method and setting the mdlvalidate parameter
           to True. E.g. validate_status('status', new_value) method in
           the model will validate the status field. The Validator will
           call the method based on the field name.

    """

    def __init__(self, mdl, limit=None, mdlvalidate=False, fill=True):
        """ Constructor for BoolValidator
            This is a validator for a wx.CheckBox.

            fill: bool, Only valid for 3 State CheckBox.
                default is True which means the state must be True or False.
        """
        super().__init__()

        self._model = mdl
        self.limit = None
        self._model_validate = mdlvalidate
        self.mustfill = fill
        # self.dtype and self.dtype_code not required
        self.value = None
        self.na = None  # default NA indicator or by model's NA indicator

    # MUST implement Clone()

    def Clone(self):
        return self.__class__(self._model, self.limit, self._model_validate,
                              self.mustfill)

    def Validate(self, parent):
        # correct protocol to get the validator's associated control.
        # self.text_ctrl in Validator cause NoneType obj
        check_box = self.GetWindow()
        if check_box.Is3State() is True:
            state = check_box.Get3StateValue()

            # handle NA and mustfill
            if state == wx.CHK_UNDETERMINED:
                # use back the model's NA indicator to avoid problems
                self.value = self.na
                if self.mustfill is True:
                    highlight_error(
                        check_box, "This field must be True or False",
                        "Invalid Input")
                    return False
                else:
                    highlight_off(check_box)
            elif state == wx.CHK_CHECKED:
                self.value = True
            else:
                # wx.CHK_UNCHECKED
                self.value = False
        else:
            self.value = check_box.GetValue()

        retval = True
        if self._model_validate is True:
            fldname = check_box.GetName()
            # call the model's validate function
            vres = self._model.validate(fldname, self.value)
            if vres.result is None or vres.result is False:
                highlight_error(check_box, vres.errormsg, vres.title)
                retval = False
            else:
                highlight_off(check_box)
                retval = True

        return retval

        return True

    def TransferToWindow(self):
        check_box = self.GetWindow()  # correct protocol
        # init original value in case of cancel or mustfill = False
        self.value = self._model.getvalue(check_box.GetName())
        if check_box.Is3State() is True:
            if self.value is None:  # NA indicator is None
                val = wx.CHK_UNDETERMINED
                self.na = self.value  # store the model's data NA indicator
            elif isinstance(self.value, float) and math.isnan(self.value):
                val = wx.CHK_UNDETERMINED  # NA indicator is math.nan
                self.na = self.value
            else:
                val = bool(self.value)
                if self.value is True:
                    val = wx.CHK_CHECKED
                else:
                    val = wx.CHK_UNCHECKED
            check_box.Set3StateValue(val)
        else:  # 2State checkbox
            if self.value is None:  # NA indicator is None
                val = False  # interpret NA as False
                self.na = self.value  # store the model's data NA indicator
            elif isinstance(self.value, float) and math.isnan(self.value):
                # NA indicator is math.nan
                val = False  # interpret NA as False
                self.na = self.value
            else:
                val = bool(self.value)
            check_box.SetValue(val)
        return True

    def TransferFromWindow(self):
        check_box = self.GetWindow()  # correct protocol
        if self.Validate(check_box.GetParent()) is True:
            self._model.setvalue(check_box.GetName(), self.value)
            return True
        else:
            return False


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
            st_fv = wx.StaticText(self, label="Float value:")
            tc_float_data = wx.TextCtrl(
                self, value='', size=(70, -1),
                style=wx.TE_PROCESS_ENTER,  # get tab and CR
                validator=FloatingPointValidator(
                    self._model, (-50.0, 150.0)),
                name='float_value')
            tc_float_data.GetValidator().mustfill = False  # mustfill test
            # integer data tests
            st_iv = wx.StaticText(self, label="Integer value:")
            tc_int_data = wx.TextCtrl(
                self, value='', size=(70, -1),
                style=wx.TE_PROCESS_ENTER,  # get tab and CR
                validator=IntegerValidator(self._model, (-100, 100)),
                name='int_value')
            # text data tests
            st_text = wx.StaticText(self, label="Text Data:")
            tc_text_data = wx.TextCtrl(
                self, value="",
                style=wx.TE_PROCESS_ENTER,  # get tab and CR
                validator=TextValidator(self._model, (0, 16)),
                name='text_value')
            # model validator test
            st_constraint = wx.StaticText(self, label="Constrained value:")
            tc_constraint = wx.TextCtrl(
                self, value='', size=(70, -1),
                style=wx.TE_PROCESS_ENTER,  # get tab and CR
                validator=FloatingPointValidator(
                    self._model, None, True),
                name='constrained_value')
            # decimal validator test
            st_decimal_value = wx.StaticText(self, label="Decimal value:")
            tc_decimal_value = wx.TextCtrl(
                self, value='', size=(70, -1),
                style=wx.TE_PROCESS_ENTER,  # get tab and CR
                validator=DecimalValidator(
                    self._model, (-1000, 1000)),
                name='decimal_value')
            # bool validator test
            st_status = wx.StaticText(self, label="Boolean Status:")
            cb_status1 = wx.CheckBox(
                self, label='1',
                style=wx.CHK_3STATE | wx.CHK_ALLOW_3RD_STATE_FOR_USER,
                validator=BoolValidator(
                    self._model),
                name='status1')
            cb_status2 = wx.CheckBox(
                self, label='2',
                style=wx.CHK_3STATE | wx.CHK_ALLOW_3RD_STATE_FOR_USER,
                validator=BoolValidator(
                    self._model,
                    fill=False),
                name='status2')
            cb_status3 = wx.CheckBox(
                self, label='3',
                validator=BoolValidator(
                    self._model),
                name='status3')
            hbs = wx.BoxSizer(wx.HORIZONTAL)
            hbs.Add(cb_status1, 0, wx.ALL, 5)
            hbs.Add(cb_status2, 0, wx.ALL, 5)
            hbs.Add(cb_status3, 0, wx.ALL, 5)

            fgs = wx.FlexGridSizer(6, 3, 5, 5)
            # floating point validation test
            fgs.Add(st_fv, 0, wx.ALIGN_RIGHT)
            fgs.Add(tc_float_data, 0, wx.EXPAND)
            fgs.Add(wx.StaticText(self, label="limits (-50.0, 150.0)"),
                    0, wx.EXPAND)
            # integer validation test
            fgs.Add(st_iv, 0, wx.ALIGN_RIGHT)
            fgs.Add(tc_int_data, 0, wx.EXPAND)
            fgs.Add(wx.StaticText(self, label="limits (-100, 100)"),
                    0, wx.EXPAND)
            # text validation test
            fgs.Add(st_text, 0, wx.ALIGN_RIGHT)
            fgs.Add(tc_text_data, 0, wx.EXPAND)
            fgs.Add(wx.StaticText(self, label="limits (0, 16)"),
                    0, wx.EXPAND)
            # floating point validation test using model's validate_* func
            fgs.Add(st_constraint, 0, wx.ALIGN_RIGHT)
            fgs.Add(tc_constraint, 0, wx.EXPAND)
            fgs.Add(wx.StaticText(self, label="valid values are -3, 5, 10"),
                    0, wx.EXPAND)
            # Decimal validation test
            fgs.Add(st_decimal_value, 0, wx.ALIGN_RIGHT)
            fgs.Add(tc_decimal_value, 0, wx.EXPAND)
            fgs.Add(wx.StaticText(self, label="limits (-1000, 1000)"),
                    0, wx.EXPAND)
            # bool validation test
            fgs.Add(st_status, 0, wx.ALIGN_RIGHT)
            fgs.Add(hbs, 0, wx.EXPAND)
            fgs.Add(wx.StaticText(self, label="Either True or False"),
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
            vbs_main.Add(wx.StaticLine(self), 0, wx.EXPAND | wx.ALL, 5)
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

        def validate_constrained_value(self, field_name, new_value):
            # test validate using the model's validate_* function
            if (math.isclose(new_value, 5.0) or math.isclose(new_value, 10.0)
                    or math.isclose(new_value, -3.0)):
                return ValidationResult(True)
            else:
                return ValidationResult(
                    False, 'Value must be -3, 5 or 10', 'Input Error')

    import traceback

    try:
        # run the demos
        app = wx.App(False)
        mydict = {"float_value": math.nan, "int_value": None,
                  "text_value": '', "constrained_value": None,
                  "decimal_value": Decimal('1'),
                  "status1": None, "status2": None, "status3": None}
        # create the App's model
        mymodel = AppModel(mydict)

        with CheckValidatorsDialog(None, mymodel,
                                   title='Validators Test') as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                print("Congragulations! Data Entry done correctly.")
            else:
                print('Data Entry Dialog cancelled!')

        app.MainLoop()
        print(mymodel.fields_report())  # must be after MainLoop()
        # decimal division tests
        dv = mymodel.getvalue('decimal_value')
        print('decimal value division by 3 =', dv/Decimal(3.0))

    except Exception:
        traceback.print_exc()
