from FieldWidget import *
class WidgetOperationController:
    """Class for managing lists of Widgets.

    """
    def __init__(self, parent, control_list: list, main_window):
        """Defines this object's parent, the list of widgets it will be managing,
           and the top level window which has no parent (except the Tk root).
        
        """
        self.parent = parent
        self.control_list = control_list
        self.main_window = main_window
    
    def swap(self, index1, index2):
        """Swaps two widgets in the list AND the GUI display.
        Expects a FieldWidget object.
        """
        cached = self.control_list[index1]
        self.control_list[index1] = self.control_list[index2]
        self.control_list[index2] = cached
    
    def add_widget_row_size(self, widget: FieldWidget):
        """Adds another row in the GUI to a fieldwidget."""
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

    def move_widget_up(self, widget: FieldWidget | None = None):
        """Moves a FieldWidget up."""
        prev_row = widget.grid_info()['row']
        prev_col = widget.grid_info()['column']

        widget.grid_forget()
        widget.change_grid_position(row=prev_row - 1, col=prev_col)

    def move_up(self, widget: FieldWidget):
        """New move_up method. See above and move_down."""

        # Move up in the list

        # Move up in the GUI.

    def swap_up(self, widget: FieldWidget):
        """TODO: Make this swap a widget with the widget above it in the list."""
        #raise Exception("FIXME implement swap_up")
    
        # Swap up in the list.
        index_of = self.control_list.index(widget)
        other_widget: FieldWidget = self.control_list[index_of - 1]
        if index_of < 1: # If this is the first element in the list, cannot swap up.
            curr_row, curr_column = widget.grid_info()['row'], widget.grid_info()['column']
            print(f"row{curr_row} column{curr_column}")
            raise IndexError
        else:
            cache = self.control_list[index_of - 1]
            self.control_list[index_of - 1] = widget
            self.control_list[index_of] = cache
            # Swap up in the GUI.
            curr_row, curr_column = widget.grid_info()['row'], widget.grid_info()['column']
            print(f"row{curr_row} column{curr_column}")
            # Move this one up by the one above's number of children, and move the other one down 
            # by this one's number of children.
            other_curr_row, other_curr_column = other_widget.grid_info()['row'], other_widget.grid_info()['column']
            widget.change_grid_position(curr_row - other_widget.current_row_span, curr_column)
            print(f"other rowspan {other_widget.current_row_span}")
            other_widget.change_grid_position(other_curr_row + widget.current_row_span, other_curr_column)


        # Need to account for children:
        # Move the other piece down by the row size of this one


    def move_down(self, widget: FieldWidget):
        """Moves a fieldwidget down, both in the control_list and the GUI.
           If calling this, it must be run from the bottom up.
           After being run, must pop the element in the index after the argument widget 
           or the first element (it will be junk)
        """
        # TODO: move down in the list
        index_of = self.control_list.index(widget)
        if index_of == len(self.control_list) - 1: # If this is the end of the list
            # Add a dummy value to the end of the list
            # and then put this into it
            self.control_list.append(self.control_list[index_of])
            self.control_list[index_of + 1] = self.control_list[index_of] 

            # Now modify the GUI
            curr_row, curr_column = widget.grid_info()['row'], widget.grid_info()['column']
            widget.change_grid_position(row = curr_row + 1, col = curr_column) # Now set this one's position to be one down

        else: # Otherwise, if this is any other index...
            # Just move it down because the one below this will already have been moved down
            self.control_list[index_of + 1] = self.control_list[index_of]
            # Now modify the GUI
            curr_row, curr_column = widget.grid_info()['row'], widget.grid_info()['column']
            widget.change_grid_position(row = curr_row + 1, col= curr_column)
            
    def move_all_down(self, widget: FieldWidget | None = None):
        if widget == None:
            widget = self.control_list[0] # If no widget is supplied, move everything below the first index down
        
        """Moves all FieldWidgets below a specified widget down.
        A dummy value will propagate to the top and should be removed.
        """
        for i in range(len(self.control_list) - 1, 0, -1):
            try:
                if i > self.control_list.index(widget):
                    self.move_down(self.control_list[i])
                if (len(self.control_list) > 1) and (self.control_list.index(widget) < len(self.control_list) - 1):
                    print(self.control_list.pop(self.control_list.index(widget) + 1)) # Clearing the dummy value
            except Exception: # There will be an exception if we are adding children at the end of the list.
                continue #TODO: add a calculator for the needed row?
       

        print(self.control_list)
        self.main_window.reapply_bottom_menu()
    
    def move_all_up(self, widget: FieldWidget | None = None):
        if widget == None:
            widget = self.control_list[len(self.control_list) - 1] # If no widget is supplied, move everything down
        
        """Moves all FieldWidgets below a specified widget down."""
        for i in range(len(self.control_list) -1, 0, -1):
            if i < self.control_list.index(widget):
                if i == 0:
                    self.control_list.insert(self.control_list[i])
                    self.move_widget_up(self.control_list[i])
                else:
                    self.control_list[i + 1] = self.control_list[i]
                    self.move_widget_down(self.control_list[i])
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
        
        
        self.control_list.pop(self.control_list.index(widget))


    def add_widget(self):
        """Adds a new FieldWidget to the menu"""
        self.main_window.bottom_menu_bar.grid_forget()
        self.control_list.append(FieldWidget(self.parent, self, self.main_window.calc_row_len(), 0))
        self.main_window.reapply_bottom_menu()
