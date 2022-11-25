import sys
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from tkinter.messagebox import showinfo
import time


def print_win_dims(parent):
    """ Print tkinter window dimensions like screen, current window sizes,
        window geometry, and requested window sizes for debugging purposes.
    """
    print(f"screen size  = {parent.winfo_screenwidth()} x",
          f"{parent.winfo_screenheight()}")
    print(f"req win size = {parent.winfo_reqwidth()} x",
          f"{parent.winfo_reqheight()}")
    print(f"win size     = {parent.winfo_width()} x",
          f"{parent.winfo_height()}")
    print(f"win geometry = {parent.winfo_geometry()}")


def centered_window_offset(parent, win_width, win_height):
    """ Return the centered screen offset (x, Y) coordinates

        parent: root or a top level window object

        win_width: int, width of window to center

        win_height: int, height of window to center

        Usage
        -----
        >>> win_width = 500
        >>> win_height = 550
        >>> x, y = centered_screen_offset(root, win_width, win_height)
        >>> root.geometry(f"{win_width}x{win_height}+{x}+{y}")
    """
    screen_width = parent.winfo_screenwidth()
    screen_height = parent.winfo_screenheight()
    x = int(screen_width/2 - win_width/2)
    y = int(screen_height/2 - win_height/2)
    return x, y


class BusyInfo(tk.Toplevel):
    """ BusyInfo class is implemented to help inform the user that
        the program is busy. It is a top level window without title bar.

        Usage:
        ------
        >>> import tkinter as tk
        >>> import time
        >>> from pefc.tksupport import BusyInfo
        >>> root = tk.Tk()
        >>> with BusyInfo():
        ...     time.sleep(5)
        >>> root.mainloop()

    """

    def __init__(self,  msg='Please wait, working...', parent=None,
                 win_width=350, win_height=100,
                 bg_color='khaki1', fg_color='black'):
        """ Constructor for the BusyInfo which is a tk.Toplevel window

            parent: root of the application as in root = tk.Tk()

        """
        super().__init__(parent)
        self.title("Busy Info Screen")  # title for debugging only
        self.resizable(False, False)
        self.configure(bg=bg_color)

        if not parent:
            parent = self.master

        x, y = centered_window_offset(parent, win_width, win_height)
        self.geometry(f"{win_width}x{win_height}+{x}+{y}")
        self.overrideredirect(1)  # hide windows title bar
        self.attributes('-topmost', True)

        # Change all window elements to light yellow background
        style = ttk.Style()
        style.configure("BI.TLabel", foreground=fg_color, background=bg_color)
        style.configure("BI.TFrame", foreground=fg_color, background=bg_color)
        main_frame = ttk.Frame(self, style="BI.TFrame")
        # label
        self.label = ttk.Label(main_frame, text=msg, font=("Helvetica", 12),
                               style="BI.TLabel")
        self.label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
        main_frame.pack(expand=True)

        self.grab_set()  # makes this a modal window
        self.update()  # without this it won't show window at all

    # Context Manager implementations

    def __enter__(self):
        return self

    # automatically close() when using 'with' statement
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    # For simplicity implement close() to explicitly close
    # the windows
    def close(self):
        """
        Explicitly close the window.
        Use the 'with' statement instead to avoid forgeting to close it.
        """
        self.destroy()


def busy_info_test():
    with BusyInfo(
        "For multiple lines statement, split using newline.\n"
            "This is the second line.\nThis is the last line."):
        # do something here ...
        time.sleep(5)
        print('First test completed')

    with BusyInfo(parent=root, win_width=200, win_height=75,
                  bg_color='pale green', fg_color='blue'):
        # do something here ...
        time.sleep(5)
        print('Second test completed')


class FuncLauncher(tk.Frame):
    """ Function launcher to debug programs. Avoid using this for python
        exercises because many on-line interpreters don't support tkinter
        module. This Function Launcher is a app not a dialog.
    """

    def __init__(self, parent, button_dict=None, title="Function Launcher",
                 info_txt='Ready', about_msg=None):
        """ Constructor for the FuncLauncher which is a tkinter.Frame.

            parent: tkinter.Frame, parent Frame or main Frame of
            the application.

            button_dict: dict. The format is as follows:
            { button_name1: func_to_call1, button_name2: func_to_call2 ...}

            title: str, window title

            info_txt: str, information to place on the info bar

            about_msg: str, message to display about the app.
        """
        super().__init__(parent)
        self.master.title(title)
        self.master.resizable(False, False)

        self.master.protocol('WM_DELETE_WINDOW', self.btn_cancel)
        self.master.bind('<Return>', self.btn_cancel)  # instead of btn_ok
        self.master.bind('<Escape>', self.btn_cancel)

        # Main screen positioning calc don't work because winfo_reqwidth and
        # winfo_width cannot return the final window size even at the end. Use
        # self.master.eval('tk::PlaceWindow . center') at end instead.

        # Launcher Menu Bar
        launcher_menubar = tk.Menu(self.master)
        if about_msg:
            self.about_msg = about_msg
        else:
            self.about_msg = (
                'Function Launcher from\n' +
                'Python Engineering Foundation Class (PEFC) 2022')
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

        # info bar
        self.info_txt = tk.StringVar(value=info_txt)
        self.tk_info_label = ttk.Label(self, textvariable=self.info_txt,
                                       relief=tk.GROOVE)
        self.tk_info_label.pack(side=tk.BOTTOM, anchor=tk.W,
                                fill='x', expand=True)

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

        # This method works and must be at end of method after pack
        self.master.eval('tk::PlaceWindow . center')  # run tcl/tk command

        self.save_old_terminal()
        sys.stdout = TextRedirector(self.text, "stdout")
        sys.stderr = TextRedirector(self.text, "stderr")
        sys.stdin = TextRedirector(self.text, "stdin")

    def help_about(self):
        showinfo(title='About This App', message=self.about_msg)

    def set_info_txt(self, new_txt):
        print("See Info bar below for changes")
        self.info_txt.set(new_txt)

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
    # app.msg = "This is a great test"


def info_bar_test():
    app.set_info_txt("Status is updated!!")


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
        self.listbox.config(takefocus=0)
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
                   "Single Choice Dialog Test": singlechoicedialog_test,
                   "BusyInfo Test": busy_info_test,
                   "Info Bar Test": info_bar_test}
    app = FuncLauncher(root, button_dict)  # main frame
    root.mainloop()
