from tkinter import *
from tkinter import ttk
from guiconfig import *

class FieldWidget(ttk.Frame):
    """Self-contained Frame with the elements needed for creating one line of hoi4 code."""
    def __init__(self, start_pos: tuple[int] = None, tagoptions_list: list[str] = None, disabled_elements: list[str] = None, indentation = 0, **kwargs):
        """Passes **kwargs to ttk.Frame constructor.\n
           start_pos: tuple (x, y) describing the starting grid position of this FieldWidget.\n
           tagoptions_list: the list of tag options that will be selectable in this FWidget.\n
           disabled_elements: the elements in this FWidget that will be disabled.
        """
        if 'parent' in kwargs:
            self.parent = kwargs.pop('parent')
        else:
            self.parent = None

        super().__init__(**kwargs)

        print(self.master)

        self.indentation = indentation # Starting indentation level.

        self.start_pos = start_pos # Set the starting position of this Widget - this will not be useful later.

        self.childlist = []

        # Create variables tracking elements of this Widget
        self.input_str = StringVar()
        self.tag_str = StringVar()

        # Create the elements of this Widget
        self.el_state_dict = self._parse_disabled_elements(disabled_elements_list=disabled_elements)
        self.inputfield, self.tagselector, self.tag_select_menu, self.add_child_button, self.delete_button = (
            self._create_elements(disabled_elements=self.el_state_dict))
        
        # Set the selectable tag options
        if not tagoptions_list == None:
            self.set_tag_options(tagoptions_list)

        # Handle tooltips
        self.tooltip_text = None

        self._grid_elements()
        self._bind_guiactions()
    
    def _parse_disabled_elements(self, disabled_elements_list):
        """Returns a dictionary of ttk state constants mapped to string nicknames for the elements of a FieldWidget."""

        output_dict = {
            'input' :  NORMAL,
            'tag' : NORMAL,
            'del' : NORMAL,
            'add' : NORMAL
        }
        if not disabled_elements_list == None:
            for element in disabled_elements_list:
                if element in output_dict:
                    output_dict[element] = DISABLED
        
        return output_dict
    
    def _send_create_child_command(self):
        """Tells the controller to create a new child of this FieldWidget."""
        print(f"send_create_child_command @ {self}")
        self.master.childcontroller.on_event_fieldwidget_add_child(self) #target=self
    
    def _send_swap_up_command(self):
        """Tells the controller to swap this FieldWidget up."""

        print(f"send_swap_up_command @ {self}")
        self.master.childcontroller.on_event_fieldwidget_up(self)
    
    def _send_delete_command(self):
        """Tells the controller to delete this FieldWidget and all of its children."""
        print(f"send_delete_command in {self}")
        self.master.childcontroller.on_event_fieldwidget_delete(self)

    def _create_elements(self, disabled_elements = None):
        """Creates the elements of this FieldWidget and returns them.
           disabled_elements: a dictionary of ttk states
        """
        from functools import partial
        inputfield = ttk.Entry(master=self, textvariable=self.input_str, state=disabled_elements['input'])
        tagselector = ttk.Menubutton(master=self, text='', textvariable=self.tag_str, state=disabled_elements['tag'])
        tag_select_menu = Menu(master=tagselector, tearoff=0)
        tagselector['menu'] = tag_select_menu

        add_child_button = ttk.Button(master=self, text='Add Child', state=disabled_elements['add'], command=self._send_create_child_command)
        delete_button = ttk.Button(master=self, text='Delete', state=disabled_elements['del'], command=self._send_delete_command)

        return (inputfield, tagselector, tag_select_menu, add_child_button, delete_button)

    def _on_tagselector_change(self):
        """Actions to be taken when a new radiobutton is selected in the tagselector."""

    def _set_position(self, coords: tuple = None, **kwargs):
        """Sets the grid position of this FieldWidget.\n
           coords: tuple (x, y).\n
           kwargs: passed to ttk.Frame.grid

        """
        kwargs['sticky'] = (N, W)
        kwargs['padx'] = (self.indentation * PIXEL_PER_INDENT, 0)
        if not coords == None:
            self.grid_forget()
            self.grid(column=coords[0], row=coords[1], **kwargs)
        else:
            self.grid(**kwargs)
    
    def _clear_tag_options(self, menu: Menu):
        """Clears the options in this FieldWidget's optionslist."""
        menu.option_clear()
    
    def _add_tag_options(self, menu: Menu, optionslist: list):
        """Adds radiobutton options to Menu from optionslist."""
        for option in optionslist:
            menu.add_radiobutton(label=option, variable=self.tag_str)
    
    def _grid_elements(self):
        """Create the elements of this Widget that do not need to be stored in instance vars.
        Grid all the elements of this FieldWidget, as well as gridding this FieldWidget in its parent.
        """
        ttk.Button(master=self, text='Up', command=self._send_swap_up_command).grid(row=0, column=0)
        
        self.inputfield.grid(row=0, column=1)
        self.tagselector.grid(row=0, column=2)
        self.add_child_button.grid(row=0, column=3)
        self.delete_button.grid(row=0, column=4)

        if not self.start_pos == None:
            self._set_position(coords=self.start_pos)
    
    def _change_element_state(self, element: ttk.Button | ttk.Entry | ttk.Menubutton, newstate):
        """Changes the state of element to newstate."""
        element.state(newstate)
    
    #FIXME once guicontroller is updated, add the commands to .bind()
    def _bind_guiactions(self):
        
        """Binds GUI actions for tooltip display and destruction to this FieldWidget."""
        # self.bind('<Enter>', self.master.childcontroller.on_event_fieldwidget_hover) #, self.controller.on_mouse_enter_fieldwidget -> callback to guicontroller
        # self.bind('<Leave>', self.master.childcontroller.on_event_fieldwidget_leave) #, self.controller.on_mouse_leave_fieldwidget 

        # # Need to bind 'enter' for all elements of this fieldwidget...
        # self.add_child_button.bind('<Enter>', self.master.childcontroller.on_event_fieldwidget_hover)
        # self.delete_button.bind('<Enter>', self.master.childcontroller.on_event_fieldwidget_hover)
        # self.tag_select_menu.bind('<Enter>', self.master.childcontroller.on_event_fieldwidget_hover)
        # self.inputfield.bind('<Enter>', self.master.childcontroller.on_event_fieldwidget_hover)

    ##INTERFACE##

    def change_position(self, change_x: int = 0, change_y: int = 0):
        """Changes this grid's position by change_x rows and change_y column."""
        prev_pos = (self.grid_info()['column'], self.grid_info()['row'])
        new_pos = (prev_pos[0] + change_x, prev_pos[1] + change_y)

        self._set_position(coords = new_pos)
    
    def update_layout(self, coords:tuple = None, **kwargs):
        """Sets the grid position of this FieldWidget and/or passes any ttk.Widget.grid kwargs to .grid()."""
        self._set_position(coords, **kwargs)

    def extend_tag_options(self, optionslist: list[str]):
        """Adds the strings in optionslist to the end of this FieldWidget's optionslist."""
        self._add_tag_options(menu=self.tag_select_menu, optionslist=optionslist)

    def set_tag_options(self, optionslist: list[str]):
        """Sets the radiobutton options in this FieldWidget's tag_select_menu to optionslist.\n
           optionslist: list of tag options as strings.
        """
        self._clear_tag_options(menu=self.tag_select_menu)
        self._add_tag_options(menu=self.tag_select_menu, optionslist=optionslist)
    
    def update_tooltip(self, new_text: str):
        """Updates the text of the tooltip this FieldWidget will display."""
        self.tooltip_text = new_text

    def enable_element(self, element):
        """Enables element of this FieldWidget."""
        self._change_element_state(element, NORMAL)
    
    def disable_element(self, element):
        """Disables element of this FieldWidget."""
        self._change_element_state(element, DISABLED)
    
    def get_row(self):
        """Returns the grid row of this FieldWidget"""
        return self.grid_info()['row']
    
    def get_parent(self):
        """Get the parent of this FieldWidget."""
        return self.parent


if __name__ == "__main__":
    """Testing this class."""
    import guihelpers
    root = Tk()
    root.minsize(width=300, height=300)
    fw = FieldWidget(start_pos=(0,0), master=root, tagoptions_list=['test'], disabled_elements=['input', 'add'])
    root.mainloop()

