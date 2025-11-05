from guicomponents import *
from guicomponents import ContentWindow
from guicomponents.FieldWidget import *
from GlobalSettings import *
class WidgetOperationController:
    """Class for managing lists of Widgets.

    """
    def __init__(self, parent, control_list: list, main_window):
        """Defines this object's parent, the list of widgets it will be managing,
           and the top level window which has no parent except the Tk root.
        
        """
        self.master: FieldWidget = parent
        self.control_list = control_list
        self.main_window = main_window
    
    def swap(self, index1: int, index2: int):
        """Swaps two widgets in this controller's control list.\n
           index1: index of first widget to be swapped.\n
           index2: index of second widget to be swapped.
        """
        cached = self.control_list[index1]
        self.control_list[index1] = self.control_list[index2]
        self.control_list[index2] = cached

    def move_widget_x(self, widget: FieldWidget, increment: int):
        """Move a FieldWidget in the GUI by increment rows.\n
           increment should be negative to move up / positive to move down.
        """
        try:
            widget.regrid(change_x=increment)
        except Exception as e:
            print(f"move_widget_x failed at {self.master}: {e}")
        self.main_window.reapply_bottom_menu() # Whenever a widget moves we should do this
    
    def move_widget_up(self, widget: FieldWidget, increment: int = 1):
        """Moves a FieldWidget up in the GUI.\n
           <b>Note:</b> This should not be used on the top Widget in the GUI.
        """
        self.move_widget_x(widget, int(-1 * increment))
    
    def move_widget_down(self, widget: FieldWidget, increment: int = 1):
        """Moves a FieldWidget down in the GUI.\n
           <b>Note:</b> This should not be used on the bottom Widget in the GUI.
        """
        self.move_widget_x(widget, int(increment))

    def swap_widget_up(self, widget: FieldWidget):
        """Swaps a widget with the one above it, in the GUI and the controlled list.\n
           Should not be used on the topmost widget in the GUI.
        """
        # Check the index of the widget passed.

        # Operate on the control list.
        neighbor = self.control_list[self.control_list.index(widget) - 1]
        self.swap(self.control_list.index(widget), self.control_list.index(neighbor))

        # Operate on the GUI.
        self.move_widget_up(widget)
        self.move_widget_down(neighbor)
    
    def swap_widget_down(self, widget: FieldWidget):
        """Swaps a widget with the one below it, in the GUI and the controlled list.\n
           Should not be used on the bottom widget in the GUI.
        """
        # Check the index of the widget passed.

        # Operate on the control list.
        neighbor = self.control_list[self.control_list.index(widget) + 1]
        self.swap(self.control_list.index(widget), self.control_list.index(neighbor))

        # Operate on the GUI.
        try:
            self.move_widget_up(neighbor)
        except Exception as e:
            print(f"could not move {neighbor} up in swap_widget_down {widget}: {e}")
        self.move_widget_down(widget)

    def add_widget(self):
        """Adds a new FieldWidget to the menu.
           FIXME if there are parent blocks in the menu, the new field should be a child of the bottom-most parent.
           Otherwise, should create a new parent block.
        """
        self.main_window.bottom_menu_bar.grid_forget()
        self.control_list.append(FieldWidget(self.master, self, self.main_window.calc_row_len(), 0))
        try:
            self.master.regrid(change_rowspan=1)
        except Exception as e:
            print(f"add_widget could not change rowspan in {self.master}: {e}") # No problem if we can't
        self.main_window.reapply_bottom_menu()

    def move_all_down(self, widget: FieldWidget):
        """Moves all FieldWidgets below a specified Widget down."""
        # First, create a dummy at the end of the list (will propagate to the index below widget and be deleted)
        # This is ONLY for the satisfaction of the control list.
        self.control_list.append('dummy')
        dummy = self.control_list[len(self.control_list) - 1] # now name it

        # Then, swap it up to the index below the specified widget
        while self.control_list.index(dummy) > self.control_list.index(widget) + 1:
            self.swap_widget_down(self.control_list[self.control_list.index(dummy) - 1])

        #  Finally, delete dummy.
        print(f"{self.master} childcontroller list: {self.control_list}")
        print(f"dummy object index: {self.control_list.index(dummy)}")
        while True: # Purge every single dummy
            try:
                self.control_list.remove(dummy)
            except Exception:
                break

    def add_new_child_widget(self, **kwargs):
        """Adds a new child of the parent FieldWidget to the control list and GUI.
        
        """
        # Need to calculate the row it should appear in WITHIN ITS PARENT'S FRAME
        self.control_list.append(FieldWidget(parent=self.master, controller=self, row=self.master.current_row_span, col=FWIDG_CHILD_DEF_COL, **kwargs))
        self.main_window.reapply_bottom_menu()

    def add_new_child(self, **kwargs):
        """Add a new child of the parent FieldWidget.
           Accepts all arguments accepted by FieldWidget.__init__() (and, by extension, those accepted by ttk.Frame)
           \nHowever, kwargs should only contain ttk.Frame arguments.
        """
        print("FIXME add kwargs parsing in FieldWidget init")

        # Create the FieldWidget and add it to the GUI and the controlled list.
        self.add_new_child_widget(**kwargs)

        # Now, for every parent all the way back up to the main window, we need to:
        # Portion the parent another GUI row
        # move every FieldWidget below it down
        operating_on: FieldWidget = self.master
        prev = None # save the previously-operated-on FieldWidget so we can tell its parent to move everything below it down
        while True:
            # Portion another GUI row if this is a FieldWidget
            if isinstance(operating_on, FieldWidget):
                operating_on.regrid(change_rowspan=1)
            # move every fieldwidget below this one in this widget's parent's control list down
            try:
            # Before we do anything, just check to make sure that there is actually anything below this widget
                if not operating_on.childcontroller.control_list[operating_on.childcontroller.control_list.index(prev) + 1] == None:
                    operating_on.childcontroller.move_all_down(prev)
            except Exception as e:
                # if we can't do it, not that big of a deal. There is probably nothing below this FieldWidget anyway.
                print(f'could not move all fieldwidgets below {operating_on} down: {e}')

            prev = operating_on
            try:
                operating_on = operating_on.master
            except Exception:
                break # Once we have reached the WidgetWindow, we can stop going up the tree.

        self.main_window.reapply_bottom_menu()

    



    ###---FIXME EVERYTHING BELOW THIS HAS NOT BEEN REWRITTEN FIXME---###--------------------------------------

    def decrease_widget_row_size(self, widget: FieldWidget, pass_row_span: int = 1):
        """Decrements the row span of this widget. Simple because the space is already reclaimed by the grid."""
        if not isinstance(widget, ContentWindow.WidgetWindow): # The WidgetWindow should not be operated on because it is not a sub-container.
            widget.current_row_span -= pass_row_span
            #curr_row = widget.grid_info()['row']
            widget.regrid()

    def calc_child_rows(self):
        """Calculates the total number of rows the parent should occupy."""
        row = self.master.current_row_span
        for controlled in self.control_list:
            if not controlled.childlist == None:
                row += controlled.childcontroller.calc_child_rows()
        
        return row

    def regrid_all(self):
        for widget in self.control_list:
            widget.regrid()
    def delete_fieldwidget_operation(self, widget: FieldWidget):
        """FIXME"""

    def delete_fieldwidget(self, widget: FieldWidget, move_others_up: bool | None = True):
        """Deletes a FieldWidget and moves up the widgets below it on the GUI if move_others_up."""
        thiswidget = widget
        prev = widget
        deleted_span = widget.current_row_span
        print(f"deleted span {deleted_span}")
        widget.delete_widget()

        while not isinstance(thiswidget, ContentWindow.WidgetWindow): # If this is a child
            # Perform the actions of this function on each of the widget parent childcontrollers:
            # Decrease the size of the child container and move up all the containers below it.
            prev = thiswidget
            thiswidget: FieldWidget = thiswidget.master
            thiswidget.childcontroller.decrease_widget_row_size(thiswidget, pass_row_span=deleted_span)
            unit_index = thiswidget.childcontroller.control_list.index(prev)
            print(f"unit_index {unit_index}")

            if move_others_up:
                for i in range(unit_index + 1, len(thiswidget.childcontroller.control_list)):
                    curr_row = thiswidget.childcontroller.control_list[i].grid_info()['row']
                    print(f"current row {curr_row} will be {curr_row - deleted_span}")
                    thiswidget.childcontroller.control_list[i].regrid(change_x= -1 * deleted_span)   
                    print(f"new curr_row = {thiswidget.childcontroller.control_list[i].grid_info()['row']}")         
        
        
        self.control_list.remove(widget)


    