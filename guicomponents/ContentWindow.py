"""Contains definitions for the possible content panes.\n
   Ex. WidgetWindow, MainMenuWindow, 

"""
from tkinter import *
#from WidgetOperationController import *
from FieldWidget import FieldWidget
# from guicomponents.BottomMenuBar import BottomMenuBar
# from guicomponents.guicontroller import *
# from guicomponents.ComponentSetupScripts import *
from tkinter import ttk
# from guicomponents.tooltipcontroller import TooltipController
from Tooltip import *

fieldwidget_list = []

class WidgetWindow(ttk.Frame):
    """Frame holding FieldWidgets."""
    size = ('300x300')
    def __init__(self, master, controller = None):
        import ComponentSetupScripts
        super().__init__(master=master)

        self.grid(row=0, column=0, ipadx=50, ipady=100)

        self.childlist = []
        self.tooltiplist = []
        
        self.childcontroller = WidgetWindowController(parentwindow=self)
        ComponentSetupScripts.configure_row_col(self)
        ComponentSetupScripts.configure_row_col(self.master)

        # Tooltip handling
        self.current_tooltip = None
    
    def move_all_down(self, widget: FieldWidget, num_rows: int):
        """Moves all widgets below widget down by num_rows."""
        target_index = self.childlist.index(widget) + 1
        if target_index < len(self.childlist - 1):
            for widg in self.childlist[target_index:]:
                widg.change_position(change_y=num_rows)

    ##INTERFACE##

    def insert_widget(self, widget: FieldWidget, coords: tuple[int], insert_below: FieldWidget):
        """Insert a widget below insert_below."""
        widget.update_layout(coords=coords)
        self.move_all_down(insert_below, 1)
    
    def add_widget(self, widget: FieldWidget):
        """Add a FieldWidget to the bottom of the frame."""

    def get_childlist(self):
        return self.children
    
    def display_tooltip(self, hover_window, text, *args):
        """Display a tooltip on the screen."""
        self.current_tooltip = Tooltip(target_window=self, hover_window=hover_window, text=text)
        return self.current_tooltip
    
class WidgetWindowController():
    """Controller for WidgetWindow."""
    def __init__(self, parentwindow: WidgetWindow):
        self.parentwindow = parentwindow

        self.control_list = parentwindow.childlist
        self.tooltip_list = parentwindow.tooltiplist

        # Handle tooltips
        self.tooltip_creation_delay = 1000 #ms FIXME constant this
        self.current_tooltip: Tooltip = None
        self.requested_tooltip = None
        self.still_wants_tooltip = True


    def _insert_in_childlist(self, widget, index):
        """Inserts Widget into the childlist at index.\n
           index: must be within the bounds of childlist
        """

        self.control_list.insert(index, widget)

    def _append_to_childlist(self, widget):
        """Appends widget to the end of childlist."""
        self.control_list.append(widget)
    

    def _fetch_parent_fieldwidgets(self):
        """Puts all the FieldWidgets in the parent's child list into this controller's control list."""
        self.control_list = [i for i in self.parentwindow.children.items() if isinstance(i, FieldWidget)]
    
    def _find_last_child(self, target: FieldWidget):
        """Finds the last child of target and returns it, or returns target if it has no children."""
        # The last child will be the last widget in control_list with an indentation of target.indentation + 1
        # followed by a widget with indentation == target.indendation
        target_index = self.control_list.index(target)
        last_child = None

        for i in self.control_list[target_index + 1:]:
            if i.indentation >= target.indentation + 1:
                last_child = i
            elif i.indentation <= target.indentation:
                break
        
        if last_child != None:
            return last_child
        else:
            return target
    
    def _add_new_fieldwidget(self, target: FieldWidget, template = None, is_child = False):
        """Adds a new fieldwidget below all the children of target.
           template: the template (defined in FieldWidgetTemplates.py) to apply to the new FieldWidget.
        """
        # Find the row we will place new FieldWidget in.
        placement_row = self._find_last_child(target).grid_info()['row'] + 1
        placement_column = target.indentation

        if is_child:
            placement_column += 1

        self.parentwindow.insert_widget(widget=FieldWidget(master=self.parentwindow), coords=(placement_row, placement_column), insert_below=target)

    def _add_new_child_widget(self, target: FieldWidget, template = None):
       """Adds a new widget that is a child of the target.
          FIXME template should default to the childof_parent template
       """
       self._add_new_fieldwidget(target=target, template=template, is_child=True)

    def _destroy_tooltip(self, tooltip: Tooltip):
        """"""
        self.tooltip_list.remove(tooltip)
        tooltip.destroy()
    
    def _make_tooltip(self, hover_window, *args):
        """Tell WidgetWindow to display a tooltip on top of the widget being hovered over."""
        if self.still_wants_tooltip:
            self.tooltip_list.append(self.parentwindow.display_tooltip(hover_window=hover_window, text='example tooltip'))
        

    ##INTERFACE##
    def update_control_list(self):
        """Updates the list of FieldWidgets this controller is controlling."""
        self.control_list = self._fetch_parent_fieldwidgets()

    def on_event_fieldwidget_hover(self, *args):
        """Queue a tooltip for display after tooltip_creation_delay milliseconds."""
        print('hovering')
        if self.parentwindow.current_tooltip == None: #Only queue a new tooltip if there is not one on screen already
            self.still_wants_tooltip = True
            self.requested_tooltip = args[0].widget.after(self.tooltip_creation_delay, self._make_tooltip, args[0].widget) # Wait a second before creating the tooltip.
            print(args[0].widget)
            print(self.requested_tooltip)
    
    def on_event_fieldwidget_leave(self, *args):
        """Cancel queued Tooltips and destroy existing tooltips, if any."""
        print('left fieldwidget')
        self.still_wants_tooltip = False

        for tooltip in self.tooltip_list[:]:
            self._destroy_tooltip(tooltip)

        args[0].widget.after_cancel(self.requested_tooltip)

        self.parentwindow.current_tooltip = None # Finally, set current_tooltip to None

    def on_event_fieldwidget_up(self, *args):
        """Swaps a FieldWidget and all of its children with the FieldWidget above it."""
        pass

    def on_event_fieldwidget_down(self, *args):
        """Swaps a FieldWidget and all of its children with the FieldWidget below it."""
        pass

    def on_event_fieldwidget_add_child(self, *args):
        """Creates a new FieldWidget below all children of the target."""
        pass

    def on_event_fieldwidget_delete(self, *args):
        """Deletes a FieldWidget and all its children."""
        pass




    
if __name__ == "__main__":
    """Testing this module."""
    root = Tk()
    root.minsize(width=300, height=300)
    ww1 = WidgetWindow(root)
    ww1.grid(row=0, column=0)
    fw1 = FieldWidget(master=ww1, start_pos=(0,0), tagoptions_list=['test', 'test2'], disabled_elements=['input'], padding=5)

    root.mainloop()


# class oldWidgetWindow(ttk.Frame):
#     size = ('1000x400')
#     def __init__(self, parent):
#         self.root = parent # Passes the parent object to this object

#         super().__init__(self.root, padding=5)
#         self.childcontroller = WidgetOperationController(self, fieldwidget_list, self, tooltipcontroller=TooltipController(self.root))

#         # FIXME set these configurations in their own file
#         self.root.columnconfigure(0, weight=1)
#         self.root.rowconfigure(0, weight=1)
#         self.columnconfigure(0, weight=1)
#         self.rowconfigure(0, weight=1)

#         self.do_things()
    
#     def calc_row_len(self):
#         """Calculates the row the bottom menu should be in."""
#         calcrow = 1
#         for i in fieldwidget_list:
#             try:
#                 calcrow += i.current_row_span
#             except Exception: #Sometimes, we will encounter a str in fieldwidget_list...
#                 calcrow += 0 
#         print(f"bottom bar row len {calcrow}")
#         return calcrow
    
#     def reapply_bottom_menu(self):
#         pass
#         """Recalculates the position the menu at the bottom should be at and reapplies it."""
#         """
#         calcrow = self.calc_row_len()
#         self.bottom_menu_bar.grid_forget()
#         self.bottom_menu_bar.grid(row=calcrow, column=0)
#         """


#     def process(self, widget = None):
#         #FIXME break this into its own class and such
#         """Process all the inputs and create the focus block.\n
#            Format: (no children) 
#            tag_str = key_str\n

#            (children)\n
#            tag_str = {\n
#            \t child_tag_str = {
#            \t repeat this process
#            \t}
           
#            }
#         """
#         output = ""
#         for parent in fieldwidget_list:
#             # TODO: check all child blocks
#             output += f"{parent.tag_str.get()} = " # add the tag

#             if not parent.childlist == None:
#                 output += "{\n"
#                 output += self.process_child_block(parent)
#                 output += "}\n"
#             else:
#                 output += parent.user_input_str.get() + "\n"
        
#         print(output)

    
#     def process_child_block(self, widget: FieldWidget, prev_tab_level: int | None = 1):
#         """Processes a child block, ergo, manages the tab level and investigates
#            all of its child blocks and so on until there are no more
#         """
#         output = ""
#         tab_level = prev_tab_level
#         newline = "\n"
#         tab = "\t"
#         #output += "{\n"
#         for child in widget.childlist:
#             output += tab * tab_level + f"{child.tag_str.get()} = "
#             if not child.childlist == None:
#                 output += "{\n"
#                 output += self.process_child_block(child, tab_level + 1)
#                 output += "\n" + tab * tab_level + "}\n"
#             else: 
#                 output += child.user_input_str.get() + "\n"                

#         #print (f"\n\nCHILDBLOCK OUTPUT: {output}\n\n")
#         return output

#     def do_things(self):
        
#         self.grid(row=0, column=0)


#         # Add the default options
#         """
#         for i in range(len(TagOptions.default_focus_options.keys())):
#             tag = TagOptions.default_focus_tags[i]
#             fieldwidget_list.append(FieldWidget(self, self.childcontroller, row=i, col=0, default_tagoption=tag))
#         """

#         # FIXME The Bottom menu bar cannot be a part of WidgetWindow
#         # Re-enabling it for this build
#         self.bottom_menu_bar = BottomMenuBar(parent=self, controller=self.childcontroller)
#         self.bottom_menu_bar.grid(row=100, column=0) # FIXME remove this once top menu is done

#         # add the parent of the entire block
#         fieldwidget_list.append(FieldWidget(self, self.childcontroller, 0, 0, valid_tagoptions=FWIDG_FOCUS_BLOCK, template=FWIDG_FOCUS_BLOCK, default_tagoption=FWIDG_FOCUS_BLOCK, disabled_elements=(FWIDG_DEL, FWIDG_TAG_SELECT, FWIDG_KEY_ENTRY)))
#         self.reapply_bottom_menu()
#         # Add in the bottom bar options (wrap in their own class)
#         # Add new button
        

#         #self.root.mainloop()

# class SettingsPane(ttk.Frame):
#     """The settings menu for the program.
    
#     """

# class MainMenuOptions(ttk.Frame):
#     """The tool launching options that will go within the MainMenuPane."""
#     NUM_LAUNCHABLE_TOOLS = 1
#     def __init__(self, parent, controller: guicontroller):
#         """ 
#            parent: MainWindow object\n
#            controller: guicontroller object this is registered to.
#         """
#         super().__init__(master=parent, padding=5)
#         configure_row_col(self)
        
#         # Create the list of available tools to launch
#         self.focus_launch_button = ttk.Button(master=self, text='Focus Creator', padding=5, command=controller.open_focus_pane) #command = 
#         self.focus_launch_button.grid(row=0, column=0, ipadx=5, ipady=5)


# class MainMenuPane(ttk.Frame):
#     """The main menu for the program. Contains tool selection and settings.
    
#     """
#     def __init__(self, parent):
#         """Creates and aligns the main menu elements.\n
#            parent: the MainWindow this is a part of.
#            controller: the guicontroller object this is registered to.
#         """
#         super().__init__(master=parent, padding=5)
#         self.controller: guicontroller = parent.master.guicontroller
#         configure_row_col(self)

#         # Set up the components of this window
#         # Main menu options
#         MainMenuOptions(parent=self, controller=self.controller).grid(row=0, column=0, rowspan=MainMenuOptions.NUM_LAUNCHABLE_TOOLS) #FIXME rowspan = NUM_LAUNCHABLE_TOOLS

#         # Settings button (launches settings window)

