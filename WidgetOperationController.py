from FieldWidget import *
class WidgetOperationController:
    """Class for managing lists of Widgets.

    """
    def __init__(self, parent, control_list: list, main_window):
        """Defines this object's parent, the list of widgets it will be managing,
           and the top level window which has no parent except the Tk root.
        
        """
        self.parent = parent
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
        prev_row = widget.grid_info()['row']
        prev_col = widget.grid_info()['column']

        widget.grid_forget()
        widget.change_grid_position(row=prev_row + increment, col=prev_col)

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

    def add_widget(self):
        """Adds a new FieldWidget to the menu"""
        self.main_window.bottom_menu_bar.grid_forget()
        self.control_list.append(FieldWidget(self.parent, self, self.main_window.calc_row_len(), 0))
        self.main_window.reapply_bottom_menu()

    def move_all_down(self, widget: FieldWidget):
        """Moves all FieldWidgets below a specified Widget down."""
        # First, create a dummy FieldWidget at the end of the list (will propagate to the index below widget and be deleted)
        # This is ONLY for the satisfaction of the control list. The GUI is NOT a factor here 
        # besides creating and destroying the visible object.
        self.add_widget()
        dummy = self.control_list[len(self.control_list) - 1] # now name it

        # Then, swap it up to the index below the specified widget
        while self.control_list.index(dummy) > self.control_list.index(widget) + 1:
            self.swap_widget_up(dummy)

        #  Finally, delete dummy.
        print(f"{self.parent} childcontroller list: {self.control_list}")
        print(f"dummy object index: {self.control_list.index(dummy)}")
        self.delete_fieldwidget(dummy)
        #raise Exception("FIXME: implement deleting dummy at top of list")




    

    def add_widget_row_size(self, widget: FieldWidget):
        """Portions another GUI row to a FieldWidget."""
        import MainWindow

        # Regrid the widget. FIXME: Does this actually do anything?
        prev_row = widget.grid_info()['row']
        prev_column = widget.grid_info()['column']
        #widget.grid_forget()
        widget.change_grid_position(row=prev_row, col=prev_column, change_rowspan=1)

        widget.current_row_span += 1
        widget.controller.move_all_down(widget) # Need to tell this widget's parent to move the widgets below it down
        # We need to keep reaching through until we hit the end
        print(f"widget {widget} row size {widget.current_row_span}") #debug

        # Then, keep going up the parentage chain and tell each successive parent
        # to move all of its children down by 1. Recursive!!!
        widget = widget.parent
        while isinstance(widget, FieldWidget): # As long as we are not operating on the Main Window...
            prev_row = widget.grid_info()['row']
            prev_column = widget.grid_info()['column']
            #widget.grid_forget()
            widget.change_grid_position(row=prev_row, col=prev_column, change_rowspan=1) # Regrid this widget with a rowspan that is one larger.
            widget.current_row_span += 1
            widget.controller.move_all_down(widget) # Also need to tell the parent window to move down children below this

            print(f"widget {widget} row size {widget.current_row_span}")
            widget = widget.parent # Keep going up the parent chain and doing this again.

    def decrease_widget_row_size(self, widget: FieldWidget, pass_row_span: int = 1):
        """Decrements the row span of this widget. Simple because the space is already reclaimed by the grid."""
        import MainWindow
        if not isinstance(widget, MainWindow.MainWindow): # The mainwindow should not be operated on because it is not a sub-container.
            widget.current_row_span -= pass_row_span
            #curr_row = widget.grid_info()['row']
            widget.change_grid_position()

    def calc_child_rows(self):
        """Calculates the total number of rows the parent should occupy."""
        row = self.parent.current_row_span
        for controlled in self.control_list:
            if not controlled.childlist == None:
                row += controlled.childcontroller.calc_child_rows()
        
        return row


    def add_new_child(self, row_override: int | None = 0, child_type: str | None = 'focus', child_template: str | None = None, default_tagoption: str | None = None):
        """Adds a new child to this group.\n
           child_type: The name of the list of valid tag options for this widget.
        """
        # Create a FieldWidget to be positioned below the parent widget on the gui
        self.control_list.append(FieldWidget(parent=self.parent, controller=self, 
                                             row = self.parent.grid_info()['row'] + self.parent.current_row_span, 
                                             col=0, valid_tagoptions=child_type, template=child_template, 
                                             default_tagoption=default_tagoption))
        
        self.add_widget_row_size(self.parent) # Increase the portioned row span for the parent widget
        self.main_window.reapply_bottom_menu()

    def regrid_all(self):
        for widget in self.control_list:
            widget.regrid()
    def delete_fieldwidget_operation(self, widget: FieldWidget):
        """FIXME"""

    def delete_fieldwidget(self, widget: FieldWidget, move_others_up: bool | None = True):
        """Deletes a FieldWidget and moves up the widgets below it on the GUI if move_others_up."""
        import MainWindow
        thiswidget = widget
        prev = widget
        deleted_span = widget.current_row_span
        print(f"deleted span {deleted_span}")
        widget.delete_widget()

        while not isinstance(thiswidget, MainWindow.MainWindow): # If this is a child
            # Perform the actions of this function on each of the widget parent childcontrollers:
            # Decrease the size of the child container and move up all the containers below it.
            prev = thiswidget
            thiswidget = thiswidget.parent
            thiswidget.childcontroller.decrease_widget_row_size(thiswidget, pass_row_span=deleted_span)
            unit_index = thiswidget.childcontroller.control_list.index(prev)
            print(f"unit_index {unit_index}")

            if move_others_up:
                for i in range(unit_index + 1, len(thiswidget.childcontroller.control_list)):
                    curr_row = thiswidget.childcontroller.control_list[i].grid_info()['row']
                    print(f"current row {curr_row} will be {curr_row - deleted_span}")
                    thiswidget.childcontroller.control_list[i].change_grid_position(row=curr_row - deleted_span)   
                    print(f"new curr_row = {thiswidget.childcontroller.control_list[i].grid_info()['row']}")         
        
        
        self.control_list.remove(widget)


    