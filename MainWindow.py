"""The main window controller for hoi4 tools."""
from FieldWidget import *
from tkinter import *
from BottomMenuBar import *
from WidgetOperationController import *

fieldwidget_list = []

class MainWindow(ttk.Frame):
    from tkinter import ttk

    def __init__(self, root: Tk):
        self.root = root # Passes the Tk object to this object

        super().__init__(self.root, padding=5)
        self.childcontroller = WidgetOperationController(self, fieldwidget_list, self)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.do_things()
    
    def calc_row_len(self):
        """Calculates the row the bottom menu should be in."""
        calcrow = 0
        for i in fieldwidget_list:
            calcrow += i.current_row_span
        print(f"bottom bar row len {calcrow}")
        return calcrow
    
    def reapply_bottom_menu(self):
        """Recalculates the position the menu at the bottom should be at and reapplies it."""
        calcrow = self.calc_row_len()
        self.bottom_menu_bar.grid_forget()
        self.bottom_menu_bar.grid(row=calcrow, column=0)


    def process(self):
        """ Process all the inputs and create the focus block. """
        output = ""
        for i in fieldwidget_list:
            output += f"{i.tag_str.get()} = {{ {i.user_input_str.get()} }}\n"
        
        print(output)

    def do_things(self):
        
        self.grid(row=0, column=0)


        # Add the default options
        for i in range(5):
            fieldwidget_list.append(FieldWidget(self, self.childcontroller, i, 0))

        # Add in the bottom bar options (wrap in their own class)
        # Add new button
        self.bottom_menu_bar = BottomMenuBar(parent=self, controller=self.childcontroller)
        self.bottom_menu_bar.grid(row=len(fieldwidget_list), column=0)

        self.root.mainloop()