import sys
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from tkinter.messagebox import showinfo


class FuncLauncher(tk.Frame):
    """ Function launcher to debug programs. Avoid using this for python
        exercises because many on-line interpreters don't support tkinter
        module. This Function Launcher is a app not a dialog.
    """

    def __init__(self, parent, button_dict=None):
        """ Constructor for the FuncLauncher which is a tkinter.Frame.

            parent: tkinter.Frame, parent Frame or main Frame of
            the application.

            dict_list: dict. The format is as follows:
            { button_name1: func_to_call1, button_name2: func_to_call2 ...}
        """
        super().__init__(parent)
        self.master.title("Function Launcher")
        self.master.resizable(False, False)

        self.master.protocol('WM_DELETE_WINDOW', self.btn_cancel)
        self.master.bind('<Return>', self.btn_cancel)  # instead of btn_ok
        self.master.bind('<Escape>', self.btn_cancel)

        # main screen position
        x = (self.master.winfo_screenwidth() // 2 -
             self.master.winfo_reqwidth()) // 2
        y = (self.master.winfo_screenheight() // 2 -
             self.master.winfo_reqheight()) // 2
        self.master.geometry(f"+{x}+{y}")

        # Launcher Menu Bar
        launcher_menubar = tk.Menu(self.master)
        # create the Help menu
        help_menu = tk.Menu(launcher_menubar, tearoff=0)
        help_menu.add_command(label='About', command=self.help_about)
        # add the Help menu to the menubar
        launcher_menubar.add_cascade(label="Help", menu=help_menu)

        self.master.config(menu=launcher_menubar)
        self.button_dc = button_dict

        top_frame = ttk.Frame(self)
        top_frame.pack(side=tk.TOP)
        if self.button_dc:
            button_list_frame = ttk.LabelFrame(top_frame,
                                               text="Functions to launch")
            button_list_frame.pack(padx=15, pady=(0, 20), side=tk.LEFT,
                                   fill=tk.BOTH)
            for btn_name, func in self.button_dc.items():
                ttk.Button(button_list_frame, text=btn_name,
                           command=decorator_function(func)).pack(
                               padx=2, pady=2, fill=tk.X)
        # results display
        results_frame = ttk.LabelFrame(top_frame, text="Results")
        results_frame.pack(padx=15, pady=(0, 20), side=tk.LEFT)
        self.text = ScrolledText(results_frame, wrap=None)
        self.text.config(width=100, height=30)
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # command buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(padx=15, pady=(0, 15), side=tk.BOTTOM)

        ttk.Button(button_frame, text="Clear Results",
                   command=self.btn_clear_results).pack(padx=3, side=tk.LEFT)
        ttk.Button(button_frame, text="Results to Terminal",
                   command=self.btn_restore_terminal).pack(padx=3,
                                                           side=tk.LEFT)
        ttk.Button(button_frame, text='Cancel', default=tk.ACTIVE,
                   command=self.btn_cancel).pack(padx=3, side=tk.LEFT)
        # repurpose btn_ok to run all functions
        ttk.Button(button_frame, text='Run All',
                   command=self.btn_ok).pack(padx=3, side=tk.LEFT)

        self.pack()

        self.save_old_terminal()
        sys.stdout = TextRedirector(self.text, "stdout")
        sys.stderr = TextRedirector(self.text, "stderr")
        sys.stdin = TextRedirector(self.text, "stdin")

    def help_about(self):
        msg = ('Function Launcher from\n' +
               'Python Engineering Foundation Class (PEFC) 2022')
        showinfo(title='Information', message=msg)

    def btn_ok(self, event=None):  # repurpose btn_ok to run all functions
        print("*** Test all functions ***")
        for func in self.button_dc.values():
            decorator_function(func)()

    def btn_cancel(self, event=None):
        self.master.destroy()

    def btn_restore_terminal(self, event=None):
        self.restore_old_terminal()

    def btn_clear_results(self, event=None):
        self.text.config(state=tk.NORMAL)
        # first index "1.0" -> "<line>.<char>" means line 1 at char 0
        # line start from 1, char start from 0
        self.text.delete("1.0", tk.END)
        self.text.config(state=tk.DISABLED)

    def save_old_terminal(self):
        self.old_stdout = sys.stdout
        self.old_stderr = sys.stderr
        self.old_stdin = sys.stdin

    def restore_old_terminal(self):
        """ In case the redirected output causes problem to restore
            back the output to computer terminal
        """
        print("*** Results redirected to Computer Terminal ***")
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr
        sys.stdin = self.old_stdin


def decorator_function(original_function):  # function as parameter
    def wrapper_function():  # function inside function
        print(f'* Run {original_function.__name__} *')
        return original_function()
    return wrapper_function


class TextRedirector(object):
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, str):
        self.widget.configure(state=tk.NORMAL)
        self.widget.insert(tk.END, str, (self.tag,))
        self.widget.configure(state=tk.DISABLED)


def func_test():
    print("Func Test ran")


class SingleChoiceDialog(tk.Toplevel):
    def __init__(self, parent=None, message='Select one of the following:',
                 title='Single Choice Dialog',
                 choice_list=['default list', 'put your own list here'],
                 box_height=10, box_width=50):
        """  Contructor for SingleChoiceDialog

            parent: tkinter.Frame, parent Frame or main Frame of
            the application.

            message: str, message label to inform user to pick one
            item on the list

            title: str, dialog box's window title

            choice_list: list, list of items to be picked.

                items = ['Red', 'Blue', 'Yellow', 'Green'] or

                items = [1, 2, 3] or

                items = [(1, 'fish'), (2, 'boat'), (3, 'hut')]


        """
        super().__init__(parent)

        self.title(title)
        self.resizable(False, False)
        # intercept close button
        self.protocol('WM_DELETE_WINDOW', self.btn_cancel)
        self.bind('<Return>', self.btn_ok)
        self.bind('<Escape>', self.btn_cancel)

        x = (self.winfo_screenwidth() -
             self.winfo_reqwidth()) // 2
        y = (self.winfo_screenheight() -
             self.winfo_reqheight()) // 3
        self.geometry(f"+{x}+{y}")

        dialog_frame = ttk.Frame(self)
        dialog_frame.pack(padx=20, pady=5)
        ttk.Label(dialog_frame, text=message).pack()

        # list box
        lstbox_frame = ttk.Frame(self)
        lstbox_frame.pack()
        scrollbar = ttk.Scrollbar(lstbox_frame)
        scrollbar.pack(padx=(0, 15), side=tk.RIGHT, fill=tk.BOTH)
        lst_len = len(choice_list)
        if lst_len > box_height:
            lbox_height = box_height
        elif lst_len < 3:
            lbox_height = 3  # improve the matching scrollbar to list box
        else:
            lbox_height = lst_len
        list_items = tk.StringVar(self, value=choice_list)
        self.listbox = tk.Listbox(lstbox_frame, height=lbox_height,
                                  width=box_width, listvariable=list_items)

        self.listbox.pack(padx=(15, 0))
        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)
        self.listbox.selection_set(0)  # set selection at 0 index by default
        self.listbox.focus_set()  # put focus on list box

        # Binding double click with left mouse
        # button with go function
        self.listbox.bind('<Double-1>', self.go)

        ttk.Separator(self, orient=tk.HORIZONTAL).pack(
            padx=15, pady=10, fill=tk.X)

        button_frame = ttk.Frame(self)
        button_frame.pack(padx=15, anchor='e')

        ttk.Button(button_frame, text='OK', default=tk.ACTIVE,
                   command=self.btn_ok).pack(side=tk.RIGHT)

        ttk.Button(button_frame, text='Cancel',
                   command=self.btn_cancel).pack(padx=3, side=tk.RIGHT)

        # init
        self.selected = None

        self.transient(parent)   # dialog window is related to main
        self.wait_visibility()  # can't grab until window appears, so we wait
        self.grab_set()        # ensure all input goes to our window

    def btn_ok(self, event=None):
        cs = self.listbox.curselection()
        self.selected = self.listbox.get(cs)
        self.dismiss()

    def btn_cancel(self, event=None):
        self.selected = None
        self.dismiss()

    def go(self, event=None):  # handle double click
        cs = self.listbox.curselection()
        self.selected = self.listbox.get(cs)
        self.dismiss()

    def show(self):
        self.wait_window()  # block until window  is destroyed
        return self.selected

    def dismiss(self):
        self.grab_release()
        self.destroy()


def ask_singlechoicedialog_item(
        parent=None, message='Select one of the following:',
        title='Single Choice Dialog',
        choice_list=['default list', 'put your own list here'],
        box_height=10, box_width=50):
    """ Returns a single item selected from the choice list.

        parent: tkinter.Frame, parent Frame or main Frame of
        the application.

        message: str, message label to inform user to pick one
        item on the list

        title: str, dialog box's window title

        choice_list: list, list of items to be picked e.g. ['right', 'left']

        height: int, List box height. Default is 10 text characters high.

        width: int, List box weight. Default is 50 text characters long.

        Usage
        -----
        >>> items = ['Red', 'Blue', 'Yellow', 'Green']
        >>> item = ask_singlechoicedialog_item(root, choice_list=items)
        >>> print(f"Item chosen is {item} and type is {type(item)}")
        >>> Item chosen is Blue and type is <class 'str'>
        >>>
        >>> items = [1, 2, 3, 4, 5]
        >>> item = ask_singlechoicedialog_item(root, choice_list=items)
        >>> print(f"Item chosen is {item} and type is {type(item)}")
        >>> Item chosen is 3 and type is <class 'int'>
        >>>
        >>> items = [(1, 'fish'), (2, 'boat'), (3, 'hut')]
        >>> item = ask_singlechoicedialog_item(root, choice_list=items)
        >>> print(f"Item chosen is {item} and type is {type(item)}")
        >>> Item chosen is (1, 'fish') and type is <class 'tuple'>


    """
    dlg_result = SingleChoiceDialog(parent, message, title, choice_list,
                                    box_height, box_width).show()
    return dlg_result


def singlechoicedialog_test():
    items = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight',
             'nine', 'ten', 'eleven', 'twelve']
    # root is from the caller's mainloop
    item = ask_singlechoicedialog_item(root, choice_list=items, box_height=8)
    print(f"Item chosen is {item} and type is {type(item)}")


if __name__ == '__main__':
    root = tk.Tk()
    # dict of button name and function to call
    button_dict = {"Function Test": func_test,
                   "Single Choice Dialog Test": singlechoicedialog_test}
    FuncLauncher(root, button_dict)
    root.mainloop()
