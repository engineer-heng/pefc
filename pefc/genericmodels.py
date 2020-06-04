# Python Engineering Foundation Class Library (pefc)
# genericmodels Library, originated date: 2020-01-07
# Copyright(C) 2020 Heng Swee Ngee
#
# Released under the MIT License - https://opensource.org/licenses/MIT
#

""" Generic Models for MVC Implementations.
    It is based on a listener model. The model is generic and it can
    be used for any GUI API like wxpython, tkinter etc.
    However each version must be customized to the GUI package because of the
    GetParent() and GetName() function call.
    DictModel that store data in a dictionary.
"""

# TODO: DbaseModel that store data in a database using SQLAlchemy


class DictModel:
    """ This is the 'Model'. The Model's responsibilites is to notify
        the listeners of the change in data so that they are all in sync.
        All implementations of the biz logic should be done here if
        it is related to this data model.
        The Model's biz logic can be tested independently without any
        views, controllers and registered listeners' help.
        This version is for wxpython.
    """

    def __init__(self, model_dict):
        # Temporary store data in a dict and when confirmed update the
        # app's database through the app's Model
        self._mdl_dc = model_dict
        # idea here is to use a dict to store listeners_set for a field name
        # e.g. {field_name: listeners_set, ...}
        # Those field_names not in listeners_dc means it does not have
        # any listeners registered. Listeners are contained in a set to avoid
        # any duplicates. Only valid field_names are stored in dict.
        self._listeners_dc = {}

    def register(self, field_name, listener):
        """ Register the control as a listener and initialize
            the listener's data views with the Model's data

            field_name: str, name of your field in the database record

            listener: GUI controls
        """
        try:
            self._listeners_dc[field_name].add(listener)
        except KeyError:
            # verify field name is valid in dbase
            if field_name in self._mdl_dc.keys():
                self._listeners_dc[field_name] = set()  # init set listeners
                self._listeners_dc[field_name].add(listener)
            else:  # provide message and continue
                print("Model register KeyError: '{}' does not exist".format(
                      field_name))

        # Sends message to the registered listener to init value.
        # Allows the flexibility of whether the listener or
        # its parent handles the notification. Parent is usually a Panel
        # containing many controls that it manages.
        # Here LBYL is better than EAFP because AttributeError is very common
        # which can occur inside the notify method and be unidentified.
        if hasattr(listener, 'notify'):
            listener.notify()
        elif hasattr(listener.GetParent(), 'notify'):  # allow one panel only
            listener.GetParent().notify(listener)
        else:
            msg = "{}::{}'s Parent {} don't have notify()".format(
                type(listener),
                listener.GetName(),
                type(listener.GetParent()))
            print(msg)

    def unregister(self, field_name, listener):
        """ Unregister the control as a listener

            field_name: str, name of field in database record

            listener: GUI controls
        """
        try:
            self._listeners_dc[field_name].discard(listener)
        except Exception:  # print message and continue
            # verify field name is valid in dbase
            if field_name in self._mdl_dc.keys():  # actually no listeners
                return
            print(f"Model unregister KeyError: '{field_name}' does not exist")

    def getvalue(self, field_name, default=None):
        """ Get the value from the Model

            field_name: str, name of field in database record

            default: default value if value is None or math.nan
        """
        try:
            value = self._mdl_dc[field_name]
        except KeyError:  # print message and continue
            print(f"Model get_value KeyError: '{field_name}' does not exist")
            value = None
        else:
            if default is not None:
                if value is None:  # cannot add math.isnan(value)
                    value = default

        return value

    def getstrvalue(self, field_name, str_fmt=None):
        """ Get the value from the Model and convert it into
            a formatted string using the str_fmt parameter.
            This is a helper function for GUI Text Controls which
            expects the data in a formmated string for display.

            field_name: str, name of field in database record

            str_fmt: str, string format e.g. '{:.2%}' or '{:8.6f}'
            Default is None. if value is a str then no need
            to specify str_fmt.

            return: formatted str value of field or '' if value is None.
        """
        val = self.getvalue(field_name)
        if val is None:
            val = ''
        else:
            if str_fmt is not None:
                val = str_fmt.format(val)
        return val

    def setvalue(self, field_name, new_value):
        """ Sets value and notifies all listeners of the change

            field_name: str, name of field in database record

            new_value: new value of field
        """
        # Don't allow accidental creation of a new field name with new value
        # since the model dict may be mapped to a database record
        if field_name in self._mdl_dc.keys():
            self._mdl_dc[field_name] = new_value
        else:
            print(f"Model set_value KeyError: '{field_name}' does not exist")
        self._notify_listeners(field_name)

    def _notify_listeners(self, field_name):
        """ Notifies the listeners of the field name to take action
            on the change.
            Whether they do or not is NOT the Model's responsibility.

            field_name: str, name of field in database record
        """
        try:
            listeners = self._listeners_dc[field_name]
        except KeyError:  # print message and continue
            # verify field name is valid in dbase
            if field_name in self._mdl_dc.keys():  # actually no listeners
                return
            print(f"Notification KeyError: '{field_name}' does not exist")
        else:
            if len(listeners) == 0:
                return
            for ltr in listeners:
                if hasattr(ltr, 'notify'):
                    ltr.notify()
                elif hasattr(ltr.GetParent(), 'notify'):
                    ltr.GetParent().notify(ltr)
                else:
                    msg = "{}::{}'s Parent {} don't have notify()".format(
                        type(ltr),
                        ltr.GetName(),
                        type(ltr.GetParent()))
                    print(msg)

    def model_report(self):
        """ Returns model data and listeners in str report format
            for debugging purposes.
        """
        rep1 = self.fields_report()
        rep2 = self.listeners_report()

        return rep1 + rep2

    def fields_report(self):
        ls = ["MODEL DATA FIELDS REPORT\n"]
        for k, v in self._mdl_dc.items():
            ls.append("{} = {}\n".format(k, v))
        return "".join(ls)

    def listeners_report(self):
        ls = ["MODEL LISTENERS REPORT\n"]
        for k, v in self._listeners_dc.items():
            # build a new str set for reporting/debugging purposes
            # listener_class::listener_field_name=>listener_parent_class
            vs = set()
            for ltr in v:
                if hasattr(ltr, 'notify'):
                    rs = '{}::{}'.format(type(ltr), ltr.GetName())
                elif hasattr(ltr.GetParent(), 'notify'):
                    rs = '{}::{} <= {}'.format(type(ltr),
                                               ltr.GetName(),
                                               type(ltr.GetParent()))
                else:  # no notify method
                    rs = '{}::{} <= <No notify method!>'.format(type(ltr),
                                                                ltr.GetName())
                vs.add(rs)
            ls.append("{} <= {}\n".format(k, vs))
        return "".join(ls)
