import sys
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText


class FuncLauncher(tk.Frame):
    """ Function launcher to debug programs. Avoid using this for python
        exercises because many on-line interpreters don't support tkinter
        module.
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
        self.button_dc = button_dict

        self.master.protocol('WM_DELETE_WINDOW', self.btn_cancel)
        self.master.bind('<Return>', self.btn_cancel)  # instead of btn_ok
        self.master.bind('<Escape>', self.btn_cancel)

        # main screen position
        x = (self.master.winfo_screenwidth() // 2 -
             self.master.winfo_reqwidth()) // 2
        y = (self.master.winfo_screenheight() // 2 -
             self.master.winfo_reqheight()) // 2
        self.master.geometry(f"+{x}+{y}")

        self.master.config(menu=tk.Menu(self.master))
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

    def btn_ok(self, event=None):
        print("*** Test all functions ***")
        for func in self.func_list:
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


if __name__ == '__main__':
    root = tk.Tk()
    # dict of button name and function to call
    button_dict = {"Function Test": func_test}
    app = FuncLauncher(root, button_dict)
    app.mainloop()
