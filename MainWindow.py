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
        calcrow = 1
        for i in fieldwidget_list:
            try:
                calcrow += i.current_row_span
            except Exception: #Sometimes, we will encounter a str in fieldwidget_list...
                calcrow += 0 
        print(f"bottom bar row len {calcrow}")
        return calcrow
    
    def reapply_bottom_menu(self):
        """Recalculates the position the menu at the bottom should be at and reapplies it."""
        calcrow = self.calc_row_len()
        self.bottom_menu_bar.grid_forget()
        self.bottom_menu_bar.grid(row=calcrow, column=0)


    def process(self, widget = None):
        #FIXME break this into its own class and such
        """Process all the inputs and create the focus block.\n
           Format: (no children) 
           tag_str = key_str\n

           (children)\n
           tag_str = {\n
           \t child_tag_str = {
           \t repeat this process
           \t}
           
           }
        """
        output = ""
        for parent in fieldwidget_list:
            # TODO: check all child blocks
            output += f"{parent.tag_str.get()} = " # add the tag

            if not parent.childlist == None:
                output += "{\n"
                output += self.process_child_block(parent)
                output += "}\n"
            else:
                output += parent.user_input_str.get() + "\n"
        
        print(output)

    
    def process_child_block(self, widget: FieldWidget, prev_tab_level: int | None = 1):
        """Processes a child block, ergo, manages the tab level and investigates
           all of its child blocks and so on until there are no more
        """
        output = ""
        tab_level = prev_tab_level
        newline = "\n"
        tab = "\t"
        #output += "{\n"
        for child in widget.childlist:
            output += tab * tab_level + f"{child.tag_str.get()} = "
            if not child.childlist == None:
                output += "{\n"
                output += self.process_child_block(child, tab_level + 1)
                output += "\n" + tab * tab_level + "}\n"
            else: 
                output += child.user_input_str.get() + "\n"                

        #print (f"\n\nCHILDBLOCK OUTPUT: {output}\n\n")
        return output
        
        




    def do_things(self):
        
        self.grid(row=0, column=0)


        # Add the default options
        """
        for i in range(len(TagOptions.default_focus_options.keys())):
            tag = TagOptions.default_focus_tags[i]
            fieldwidget_list.append(FieldWidget(self, self.childcontroller, row=i, col=0, default_tagoption=tag))
        """

        self.bottom_menu_bar = BottomMenuBar(parent=self, controller=self.childcontroller)
        self.bottom_menu_bar.grid(row=len(fieldwidget_list), column=0)

        # add the parent of the entire block
        fieldwidget_list.append(FieldWidget(self, self.childcontroller, 0, 0, template='focus', default_tagoption='focus', disabled_buttons=FWIDG_DEL))
        self.reapply_bottom_menu()
        # Add in the bottom bar options (wrap in their own class)
        # Add new button
        

        #self.root.mainloop()

if __name__ == "__main__":
    """Testing this class."""
    root = Tk()
    window = MainWindow(root)
    fieldwidget_list.append(FieldWidget(window, window.childcontroller, row=6, col=0, template='character', default_tagoption='character'))
    window.reapply_bottom_menu()
    window.mainloop()