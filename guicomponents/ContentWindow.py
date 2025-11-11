"""Contains definitions for the possible content panes.\n
   Ex. WidgetWindow, MainMenuWindow, 

"""
from tkinter import *
from WidgetOperationController import *
from guicomponents.FieldWidget import FieldWidget
from guicomponents.BottomMenuBar import BottomMenuBar
from guicomponents.guicontroller import *
from guicomponents.ComponentSetupScripts import *
from tkinter import ttk
from guicomponents.tooltipcontroller import TooltipController

fieldwidget_list = []

class WidgetWindow(ttk.Frame):
    size = ('1000x400')
    def __init__(self, parent):
        self.root = parent # Passes the parent object to this object

        super().__init__(self.root, padding=5)
        self.childcontroller = WidgetOperationController(self, fieldwidget_list, self, tooltipcontroller=TooltipController(self.root))

        # FIXME set these configurations in their own file
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
        pass
        """Recalculates the position the menu at the bottom should be at and reapplies it."""
        """
        calcrow = self.calc_row_len()
        self.bottom_menu_bar.grid_forget()
        self.bottom_menu_bar.grid(row=calcrow, column=0)
        """


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

        # FIXME The Bottom menu bar cannot be a part of WidgetWindow
        # Re-enabling it for this build
        self.bottom_menu_bar = BottomMenuBar(parent=self, controller=self.childcontroller)
        self.bottom_menu_bar.grid(row=100, column=0) # FIXME remove this once top menu is done

        # add the parent of the entire block
        fieldwidget_list.append(FieldWidget(self, self.childcontroller, 0, 0, valid_tagoptions=FWIDG_FOCUS_BLOCK, template=FWIDG_FOCUS_BLOCK, default_tagoption=FWIDG_FOCUS_BLOCK, disabled_elements=(FWIDG_DEL, FWIDG_TAG_SELECT, FWIDG_KEY_ENTRY)))
        self.reapply_bottom_menu()
        # Add in the bottom bar options (wrap in their own class)
        # Add new button
        

        #self.root.mainloop()

class SettingsPane(ttk.Frame):
    """The settings menu for the program.
    
    """

class MainMenuOptions(ttk.Frame):
    """The tool launching options that will go within the MainMenuPane."""
    NUM_LAUNCHABLE_TOOLS = 1
    def __init__(self, parent, controller: guicontroller):
        """ 
           parent: MainWindow object\n
           controller: guicontroller object this is registered to.
        """
        super().__init__(master=parent, padding=5)
        configure_row_col(self)
        
        # Create the list of available tools to launch
        self.focus_launch_button = ttk.Button(master=self, text='Focus Creator', padding=5, command=controller.open_focus_pane) #command = 
        self.focus_launch_button.grid(row=0, column=0, ipadx=5, ipady=5)


class MainMenuPane(ttk.Frame):
    """The main menu for the program. Contains tool selection and settings.
    
    """
    def __init__(self, parent):
        """Creates and aligns the main menu elements.\n
           parent: the MainWindow this is a part of.
           controller: the guicontroller object this is registered to.
        """
        super().__init__(master=parent, padding=5)
        self.controller: guicontroller = parent.master.guicontroller
        configure_row_col(self)

        # Set up the components of this window
        # Main menu options
        MainMenuOptions(parent=self, controller=self.controller).grid(row=0, column=0, rowspan=MainMenuOptions.NUM_LAUNCHABLE_TOOLS) #FIXME rowspan = NUM_LAUNCHABLE_TOOLS

        # Settings button (launches settings window)

if __name__ == "__main__":
    """Testing this module."""
    root = Tk()
    MainMenuPane(parent=root).grid(row=0, column=0)