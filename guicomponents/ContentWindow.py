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
from guiconfig import *

fieldwidget_list = []

class WidgetWindow(ttk.Frame):
    """Frame holding FieldWidgets."""
    size = ('300x300')
    def __init__(self, master, controller = None):
        import ComponentSetupScripts
        super().__init__(master=master)

        self.grid(row=0, column=0, sticky=(N, E, W, S))

        self.childlist = [] # Childlist will eventually be a 2D array of indentation levels
        self.tooltiplist = []

        
        
        self.childcontroller = WidgetWindowController(parentwindow=self)
        ComponentSetupScripts.configure_row_col(self)
        ComponentSetupScripts.configure_row_col(self.master)

        # Tooltip handling
        self.current_tooltip = None
    
    def _move_all_down(self, widget: FieldWidget, num_rows: int):
        """Moves all widgets below widget down by num_rows."""
        target_index = self.childlist.index(widget) + 1
        if target_index <= len(self.childlist) - 1:
            for widg in self.childlist[target_index:]:
                widg.change_position(change_y=num_rows)

    def _get_relative_row(self, widget: FieldWidget):
        """Get the row of a FieldWidget relative to its parent."""
        widget_row = widget.grid_info()['row']
        print(f"FIXME: finish _get_relative_row")

    ##INTERFACE##

    def insert_widget(self, widget: FieldWidget, coords: tuple[int], insert_below: FieldWidget):
        """Insert a widget below insert_below.
           indent_level: the level of indentation to give this FieldWidget.
        """
        widget.update_layout(coords=coords, columnspan=4, sticky=(N,E), padx=(widget.indentation * PIXEL_PER_INDENT, 0))
        if not insert_below == None:
            self._move_all_down(insert_below, 1)

    def get_childlist(self):
        return self.children
    
    def display_tooltip(self, hover_window, text, *args):
        """Display a tooltip on the screen."""
        # must be displayed on self.master so it doesn't get clipped by size of WidgetWindow
        self.current_tooltip = Tooltip(target_window=self.master, hover_window=hover_window, text=text)
        return self.current_tooltip
    
    def move_widget_up(self, widget: FieldWidget, num_rows: int = 0):
        """Move a FieldWidget and its children up by num_rows."""
        widget.change_position(change_y= -1 *num_rows)

        if widget in self.childcontroller.child_dict.keys():
            # Because children of children are in the first parent's list,
            # need to make sure it only moves them once.
            for widg in self.childcontroller.child_dict[widget]:
                widg.change_position(change_y = -1 * num_rows)
    
    def move_widget_down(self, widget: FieldWidget, num_rows: int = 0):
        """Move a FieldWidget and its children in this Frame down by num_rows."""
        widget.change_position(change_y=num_rows)
        
        if widget in self.childcontroller.child_dict.keys():
            for widg in self.childcontroller.child_dict[widget]:
                widg.change_position(change_y = num_rows)
    
   
    
class WidgetWindowController():
    """Controller for WidgetWindow."""
    REMOVE = -1
    ADD = 1
    SORT = 0

    def __init__(self, parentwindow: WidgetWindow):
        self.parentwindow = parentwindow

        self.control_list = parentwindow.childlist
        self.tooltip_list = parentwindow.tooltiplist
        self.indentation_dict = {} # List of indentation levels str(num) : [widgets in level]
        self.child_dict = {} # List of children of widgets in control_list

        # Handle tooltips
        self.tooltip_creation_delay = 1000 #ms FIXME constant this
        self.current_tooltip: Tooltip = None
        self.requested_tooltip = None
        self.prev_tooltip_requester = None
        self.still_wants_tooltip = True


    def _insert_in_childlist(self, widget, index):
        """Inserts Widget into the childlist at index.\n
           index: must be within the bounds of childlist
        """

        self.control_list.insert(index, widget)

    def _append_to_childlist(self, widget):
        """Appends widget to the end of childlist."""
        self.control_list.append(widget)
    
    def _has_children(self, widget: FieldWidget):
        """Returns a boolean True/False depending on whether widget has children."""
        if widget in self.child_dict.keys():
            return True
        else:
            return False

    def _get_last_child(self, target: FieldWidget):
        """Finds the last child of target and returns it, or returns target if it has no children."""
        if self._has_children(target):
            return self.child_dict[target][-1]
        else:
            return target
        
    def _get_first_child(self, target: FieldWidget):
        """Finds the first child of target and returns it, or returns target if it has no children."""
        if self._has_children(target):
            return self.child_dict[target][0]
        else:
            return target
        
    def _get_parent(self, target: FieldWidget):
        """Gets the parent of a FieldWidget and returns it, or the FieldWidget itself if no parent is found."""
        if target.get_parent() == None:
            return target
        else:
            return target.get_parent()
                
    def _get_rowspan(self, target: FieldWidget):
        """Returns int number of rows occupied by target and all its children."""
        if self._has_children(target):
            return len(self.child_dict[target]) + 1
        else:
            return 1
    
    def _add_new_fieldwidget(self, target: FieldWidget = None, template = None, parent: FieldWidget = None):
        """Adds a new fieldwidget below all the children of target.
           template: the template (defined in FieldWidgetTemplates.py) to apply to the new FieldWidget.
        """
        placement_column = 0
        indent_level = 0
        # Find the row we will place new FieldWidget in.
        if not target == None:
            placement_row = self._get_last_child(target).grid_info()['row'] + 1
            indent_level = target.indentation
            
            if not parent == None:
                indent_level += 1
        else:
            placement_row = len(self.control_list)
            #print(placement_row)
        
        new_widget = FieldWidget(master=self.parentwindow, indentation=indent_level, parent=parent)

        self.parentwindow.insert_widget(widget=new_widget, coords=(placement_column, placement_row), insert_below=self._get_last_child(target))
        self._update_lists(self.ADD, new_widget)

    def _add_new_child_widget(self, target: FieldWidget, template = None):
       """Adds a new widget that is a child of the target.
          FIXME template should default to the childof_parent template
       """
       self._add_new_fieldwidget(target=target, template=template, parent=target)

    def _destroy_tooltip(self, tooltip: Tooltip):
        """"""
        self.tooltip_list.remove(tooltip)
        tooltip.destroy()
    
    def _make_tooltip(self, hover_window, *args):
        """Tell WidgetWindow to display a tooltip on top of the widget being hovered over."""
        if self.still_wants_tooltip:
            self.tooltip_list.append(self.parentwindow.display_tooltip(hover_window=hover_window, text='example tooltip'))
            #self.requested_tooltip = None
    
    def _insert_in_fwidg_childlist(self, parent: FieldWidget, widget: FieldWidget):
        """Inserts widget into the appropriate place in its parent childlist."""
        if parent in self.child_dict.keys():
            for widg in self.child_dict[parent]:
                if widg.grid_info()['row'] < widget.grid_info()['row']:
                    continue
                else:
                    self.child_dict[parent].insert(self.child_dict[parent].index(widg), widget)
                    break
            else:
                self.child_dict[parent].append(widget)
        else:
            self.child_dict[parent] = [widget]

    def _update_control_list(self, new_list: list[FieldWidget]):
        """Replaces the parent's childlist with new_list"""
        self.parentwindow.childlist = new_list
        self.control_list = self.parentwindow.childlist
    
    def _remove_from_control_list(self, start_index: int = None, end_index: int = None):
        """Either removes a widget and all its children from the control list, or removes the control list 
           segment [start_index : end_index] INCLUSIVE.
        """
        #FIXME add functionality for just passing a widget to this and having the method figure it out

        new_control_list_start = self.control_list[0:start_index]
        new_control_list_end = self.control_list[end_index + 1:]
        new_control_list_start.extend(new_control_list_end)

        self._update_control_list(new_control_list_start)

        

    def _remove_from_indentation_dict(self, widget: FieldWidget):
        """Removes a widget from the indentation dict."""
        indentation_level = str(widget.indentation)
        self.indentation_dict[indentation_level].remove(widget)
    
    def _clear_empty_childlists(self):
        """Deletes key entries in self.child_dict with empty lists."""
        for key in list(self.child_dict.keys()):
            if len(self.child_dict[key]) == 0:
                del self.child_dict[key]

    
    def _remove_from_child_dict(self, widget: FieldWidget):
        """Removes a widget from its parent's lists in child_dict, and deletes the widget's child_dict key if it has one."""
        # Remove from all parent lists.
        parent = self._get_parent(widget)
        while not parent == None:
            try: # del self.child_dict(widget) will cause this try to fail on all children of this widget, but we need the code to keep going.
                self.child_dict[parent].remove(widget)
            except Exception:
                print(f'could not remove {widget} from {parent} childlist. childlist probably did not exist.')

            oldparent = parent
            parent = parent.parent
            if oldparent == parent: # we have reached the end of the parent chain
                break


        # delete child_dict key if it exists.
        if widget in list(self.child_dict.keys()):
            del self.child_dict[widget]

        # clear out empty lists in child_dict.
        self._clear_empty_childlists()
        
    def _remove_from_lists(self, widget: FieldWidget):
        """Removes a widget and all its children from the indentation, child_dict, and control_list data.
           returns the computed target list once done
        """
        target_list = [widget]
        if widget in self.child_dict.keys():
            target_list.extend(self.child_dict[widget])

        target_start_index = self.control_list.index(target_list[0])
        target_end_index = self.control_list.index(target_list[-1])

        for widg in target_list:
            self._remove_from_indentation_dict(widg)
            self._remove_from_child_dict(widg)

        self._remove_from_control_list(start_index=target_start_index, end_index=target_end_index)

        return target_list

    def _update_lists(self, operation:int = SORT, widget:FieldWidget = None):
        """Update the three control lists associated with this WidgetWindow instance.\n
           operation: (REMOVE/ADD/SORT) the operation that this will perform.\n

           if operation is REMOVE, will return a list of all FieldWidgets being removed.
        """
        if operation == self.SORT: # Sort by row the FieldWidget is in.
            self.control_list.sort(key=FieldWidget.get_row)
            for childlist in self.child_dict.values():
                childlist.sort(key=FieldWidget.get_row)
            for indentlist in self.indentation_dict.values():
                indentlist.sort(key=FieldWidget.get_row)
        
        if operation == self.ADD:
            # FIXME insert the FieldWidget to the index of childlist corresponding to its grid row, or append if its row is len
            self._insert_in_childlist(widget, index=widget.grid_info()['row'])

            # needs to be added to the appropriate indentation level
            widget_indent_level = str(widget.indentation)
            # iterate through the dict list of the targeted indentation level and insert it in the right place
            if widget_indent_level in self.indentation_dict.keys():
                for widg in self.indentation_dict[widget_indent_level]:
                    if widg.grid_info()['row'] < widget.grid_info()['row']:
                        continue
                    else:
                        # Insert this widget at the position and push everything else down.
                        self.indentation_dict[widget_indent_level].insert(self.indentation_dict[widget_indent_level].index(widg), widget)
                        break
                else: # We make it through the whole indentation list without inserting the widget
                    self.indentation_dict[widget_indent_level].append(widget)
            else:
                self.indentation_dict[str(widget_indent_level)] = [widget]
                print(f"self.indentation_dict: {self.indentation_dict}")

            #iterate through the child dict list of the target parent, and its parent, and its parent and insert in correct place
            parent = self._get_parent(widget)
            while not parent == widget:
                self._insert_in_fwidg_childlist(widget=widget, parent=parent)
                old_parent = parent
                parent = self._get_parent(parent)

                if parent == old_parent:
                    break
                

        if operation == self.REMOVE:
            # remove the FieldWidget from any childlist it is in, remove its childlist from childlist dict, 
            # and remove it from its indentation dict.
            return self._remove_from_lists(widget)




    def _swap_widget_up(self, widget: FieldWidget):
        """Swaps a widget with the widget above it in the list and signals the WidgetWindow to do the same with the GUI."""
        target_start_index = self.control_list.index(widget)
        if self._has_children(widget):
            last_child_index = self.control_list.index(self._get_last_child(widget))
        else:
            last_child_index = target_start_index
        target_rowspan = self._get_rowspan(widget)

        # now check the widget above target
        this_indentation_level = self.indentation_dict[str(widget.indentation)]
        index_widget_in_indent_level = this_indentation_level.index(widget)
        # don't need to check above because it should never get to this point if it is at index 0 on its indent level.
        above_widget = this_indentation_level[index_widget_in_indent_level - 1]
        above_widget_start_index = self.control_list.index(above_widget)
        if self._has_children(above_widget):
            above_last_child_index = self.control_list.index(self._get_last_child(above_widget))
        else:
            above_last_child_index = above_widget_start_index
        above_widget_rowspan = self._get_rowspan(above_widget)

        #Create "blocks" - the sections of childlist containing these FieldWidgets and all their children.
        target_block = self.control_list[target_start_index:last_child_index + 1]
        above_widget_block = self.control_list[above_widget_start_index:above_last_child_index + 1]

        if not (self.control_list[0] == above_widget):
            start_list = self.control_list[0:above_widget_start_index]
            start_list.extend(target_block)
            target_block = start_list
        
        if not (self.control_list[-1] == widget):
            end_list = self.control_list[last_child_index + 1:]
            above_widget_block.extend(end_list)
        
        # Now, merge them...
        target_block.extend(above_widget_block)

        # And update the lists in the window and this...
        self.parentwindow.childlist = target_block
        self.control_list = self.parentwindow.childlist

        # Finally, operate on the GUI.
        self.parentwindow.move_widget_up(widget=widget, num_rows=above_widget_rowspan)
        self.parentwindow.move_widget_down(widget=above_widget, num_rows=target_rowspan)

        #...and sort the lists.
        self._update_lists(self.SORT)
    
    def _delete_fieldwidget(self, widget: FieldWidget):
        """Deletes a fieldwidget & all its children, updates the lists, 
           and signals guicontroller to destroy them and move below widgets up."""
        # Signal guicontroller to move below widgets up
        target_index = self.control_list.index(widget)
        target_rowspan = self._get_rowspan(target=widget)
        for widg in self.control_list[target_index + 1:]:
            self.parentwindow.move_widget_up(widg, num_rows=target_rowspan)

        # update lists
        
        target_list = self._update_lists(operation=self.REMOVE, widget=widget)

        # destroy widgets (maybe part of the list updating?)
        for widg in target_list:
            widg.destroy()



    ##INTERFACE##

    def on_event_fieldwidget_hover(self, *args):
        """Queue a tooltip for display after tooltip_creation_delay milliseconds."""
        #print('hovering')
        if (self.parentwindow.current_tooltip == None) and (self.requested_tooltip == None): #Only queue a new tooltip if there is not one on screen already
            self.still_wants_tooltip = True
            self.requested_tooltip = args[0].widget.after(self.tooltip_creation_delay, self._make_tooltip, args[0].widget) # Wait a second before creating the tooltip.
            self.prev_tooltip_requester = args[0].widget
            #print(args[0].widget)
            #print(self.requested_tooltip)
    
    def on_event_fieldwidget_leave(self, *args):
        """Cancel queued Tooltips and destroy existing tooltips, if any."""
        #print('left fieldwidget')
        self.still_wants_tooltip = False

        for tooltip in self.tooltip_list[:]:
            self._destroy_tooltip(tooltip)

        self.prev_tooltip_requester.after_cancel(self.requested_tooltip)

        self.parentwindow.current_tooltip = None # Finally, set current_tooltip to None
        self.requested_tooltip = None

    def on_event_fieldwidget_up(self, *args):
        """Swaps a FieldWidget and all of its children with the FieldWidget above it."""
        widg = args[0]
        indentation = str(widg.indentation)
        if widg.parent == None:
            if not self.indentation_dict[indentation][0] == widg: # make sure this is not at the top of its indentation level
                self._swap_widget_up(widg)
            else:
                print("fwidg is already at the top")
        else: # widg is a child
            if not self._get_first_child(widg.parent) == widg:
                self._swap_widget_up(widg)
            else:
                print("fwidg is already at the top")
                

    def on_event_fieldwidget_down(self, *args):
        """Swaps a FieldWidget and all of its children with the FieldWidget below it."""
        self._update_lists(self.SORT)
        pass

    def on_event_fieldwidget_add_child(self, *args):
        """Creates a new FieldWidget below all children of the target."""
        self._add_new_child_widget(target=args[0])

    def on_event_fieldwidget_delete(self, *args):
        """Deletes a FieldWidget and all its children."""
        self._delete_fieldwidget(args[0])

    def add_fieldwidget(self):
        """Adds a new FieldWidget to the bottom of the list."""
        self._add_new_fieldwidget()




    
if __name__ == "__main__":
    """Testing this module."""
    root = Tk()
    root.minsize(width=300, height=300)
    ww1 = WidgetWindow(root)
    ww1.grid(row=0, column=0)
    #ww1.childcontroller.add_fieldwidget()
    #fw1 = FieldWidget(master=ww1, start_pos=(0,0), tagoptions_list=['test', 'test2'], disabled_elements=['input'], padding=5)

    ab = ttk.Button(master=root, text='+', command=ww1.childcontroller.add_fieldwidget)
    ab.grid(row=0, column=1)
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
#         #print(f"bottom bar row len {calcrow}")
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
        
#         #print(output)

    
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

#         ##print (f"\n\nCHILDBLOCK OUTPUT: {output}\n\n")
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

