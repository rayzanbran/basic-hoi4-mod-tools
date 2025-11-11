from tkinter import *
from tkinter import ttk
from GlobalSettings import *
import TagOptions


class FieldWidget(ttk.Frame):
    """ 
    Container with a text entry box, descriptor tag, and movement and delete buttons.

    """
    def __init__(self, parent, controller, row, col, valid_tagoptions: str = FWIDG_FOCUS_BLOCK, default_tagoption: str | None = None, template: str | None = None, disabled_elements: tuple | None = None, **kwargs):
        """Creates an instance of this object in the parent ttk frame in row row and column col.
           Accepts same arguments as ttk.Frame.\n
           default_tagoption: the option of the dropdown menu that will be selected by default.\n
           valid_tagoptions: The list of options that will be selectable in this widget's dropdown window.\n
           template: the script (usually creating children) defined in FieldWidgetTemplates.py
           that will be run on this FieldWidget after creation.\n
           disabled_elements: which of the elements on this FieldWidget will not be interactable.
           **kwargs: any keyworded arguments that can go to ttk.Frame.

        """
        print(kwargs)

        # Parse kwargs
        # Need to pop them or tkinter will get mad at us
        self.valid_tagoptions = valid_tagoptions
        self.template = template
        if 'child_type' in kwargs:
            self.valid_tagoptions = kwargs.pop('child_type')
        if 'child_template' in kwargs:
            self.template = kwargs.pop('child_template')
        if 'sticky' in kwargs:
            sticky = kwargs.pop('sticky')
        else:
            sticky = None
        
        # Set the variables deciding the states of each of the elements in this FieldWidget
        if not disabled_elements == None:
            self.add_button_disabled, self.delete_button_disabled, self.up_button_disabled, self.tag_select_disabled, self.key_entry_disabled = self.parse_disabled_elements(disabled_elements)
        else:
            self.add_button_disabled, self.delete_button_disabled, self.up_button_disabled, self.tag_select_disabled, self.key_entry_disabled = NORMAL, NORMAL, NORMAL, NORMAL, NORMAL

        # Check if this block is a valid parent; if not, disable the add child button.
        if not TagOptions.check_valid_parent(default_tagoption):
            self.add_button_disabled = DISABLED

        super().__init__(master=parent, **kwargs)
        #self.master = parent
        self.controller: WidgetOperationController = controller
        print(f"master of {self} in {row}, {col}: {self.master}")

        # Setting up StringVars
        self.user_input_str = StringVar()
        self.tag_str = StringVar()

        self.master.columnconfigure(0, weight=1)
        self.current_row_span = 1

        self.childlist = None # Empty instance variable to store a child if we create one 
        self.childcontroller = None #...child controller if we create one

        self.input_entry = ttk.Entry(self, textvariable=self.user_input_str) # FIXME Why is this an instance variable?

        # Set the tags that will be selectable in the dropdown list.
        self.valid_tagoptions_list = TagOptions.possible_tag_lists[self.valid_tagoptions]

        # Weight column expansion 
        # FIXME change weights?
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
       
        self.create_widget(row=row, col=col, default_tagoption=default_tagoption, sticky=sticky)

        # Apply a template if one has been defined.
        if not self.template == None:
         self.apply_fieldwidget_template(self.template)
        
    def parse_disabled_elements(self, inputuple: tuple):
        """Parses the disabled buttons string tuple and returns a tuple of ttk states that will be given to ttk elements config.
        
        """
        add_button_disabled = DISABLED if FWIDG_ADD in inputuple else NORMAL
        
        delete_button_disabled = DISABLED if FWIDG_DEL in inputuple else NORMAL
        
        up_button_disabled = DISABLED if FWIDG_UP in inputuple else NORMAL
        
        key_entry_disabled = DISABLED if FWIDG_KEY_ENTRY in inputuple else NORMAL

        tag_select_disabled = DISABLED if FWIDG_TAG_SELECT in inputuple else NORMAL
        
        return ([add_button_disabled, delete_button_disabled, up_button_disabled, key_entry_disabled, tag_select_disabled])
    
    def move(self, change_x: int | None = 0, change_y: int | None = 0):
        """Moves this FieldWidget on the GUI by change_x rows and change_y columns.\n
           <b>Should only be called in regrid.</b>
        """
        # Get the current coordinates of this widget in its parent frame
        curr_x = self.grid_info()['row']
        curr_y = self.grid_info()['column']

        self.grid_forget()
        self.grid(row =curr_x + change_x, column=curr_y + change_y, padx=5, pady=5, rowspan = self.current_row_span)

    def change_rowspan(self, change_rowspan: int):
        """Changes the rowspan of this FieldWidget by change_rowspan.\n
           <b>Should only be called in regrid.</b>
        """
        self.current_row_span += change_rowspan
        print(f"{self} rowspan {self.current_row_span}")
    
    def regrid(self, change_x: int | None = 0, change_y: int | None = 0, change_rowspan: int | None = 0):
        """Changes this FieldWidget's position and/or rowspan in the parent frame.\n
           This should be called when doing either of the above.
        """
        # Change rowspan
        self.change_rowspan(change_rowspan)
    
        # Move widget
        self.move(change_x, change_y)
    
    def send_move_up_command(self):
        if self.grid_info()['row'] > 0: # Check that we are not already at the top
            self.controller.swap_widget_up(self)

    def send_delete_command(self):
        self.controller.delete_fieldwidget(self, True)
    
    def delete_widget(self):
        """Deletes this FieldWidget and all of its children."""
        if not self.childlist == None:
            for child in self.childlist:
                child.delete_widget()
        
        self.grid_forget()
        self.destroy()

    #FIXME remove this or figure out what it does??
    def get_text_entry(self, text):
        """"""
        print(text)
        print(self.input_entry.get())
        print(self.user_input_str.get())


    
    def add_child_command(self):
        """Tells this FieldWidget's child controller to create a new child."""
        from WidgetOperationController import WidgetOperationController

        if self.childlist == None: # If child infrastructure has not been initialized yet, initialize it
            self.childlist = []
            self.childcontroller = WidgetOperationController(self, self.childlist, self.controller.main_window, self.controller.tooltipcontroller)
            self.childcontroller.add_new_child(child_type=self.valid_tagoptions) # The first time, we need to tell it to place on next row
        else:
            self.childcontroller.add_new_child(child_type=self.valid_tagoptions)
            print(self.childlist)
    
    def add_template_child_command(self, child_type: str | None = None, child_template: str | None = None, default_tagoption: str | None = None, **kwargs):
        """Allows creation of a new child with a specified type and/or template.\n
            If no type is specified, one will be located with get_template_for_children
            """
        import WidgetOperationController

        child_type = self.tag_str.get()
        try:
            example = TagOptions.possible_tag_lists(child_type)
        except Exception as e:
            print(f"Could not set {self} child_type to {self.tag_str.get()}, setting it to {self.valid_tagoptions}.")
            child_type = self.valid_tagoptions

        if self.childlist == None:
            self.childlist = []
            self.childcontroller = WidgetOperationController.WidgetOperationController(self, self.childlist, self.controller.main_window, self.controller.tooltipcontroller)
            self.childcontroller.add_new_child(valid_tagoptions=child_type, child_template=child_template, default_tagoption=default_tagoption, **kwargs)
        else:
            self.childcontroller.add_new_child(valid_tagoptions=child_type, child_template=child_template, default_tagoption=default_tagoption, **kwargs)
            print(self.childlist)

    def check_tag_val(self):
        """Check the currently selected tag value and enable/disable the appropriate fields."""
        tag_val = self.tag_str.get()
        if TagOptions.check_valid_parent(tag_val):
            self.enable_button(self.add_child_button)
        else:
            self.disable_button(self.add_child_button)
    
    def get_tag_val(self):
        """Returns the value of self.tag_str"""
        return self.tag_str.get()

    def create_widget(self, row, col, sticky, default_tagoption: str | None = None):
        """Grids this FieldWidget in the parent frame at row,col and creates its elements.\n
           default_tagoption: the pre-filled option to be placed in this widget's dropdown menu.

        """
        if sticky == None:
            sticky = FWIDG_DEFAULT_STICKY
        
        self.grid(row=row, column=col,padx=FIELDWIDGET_PADX, pady=FIELDWIDGET_PADY, columnspan=5)

        # tags menu
        #FIXME: extend menubutton to create a class that has all the options for each of the categories
        self.tag_option_button = ttk.Menubutton(self, text= '', textvariable= self.tag_str)
        self.tag_option_button.grid(row=0, column=1)
        tag_option_menu = Menu()
        #tag_option_menu.add_command(command=self.check_tag_val)
        self.tag_option_button.config(state=self.key_entry_disabled)

        for i in self.valid_tagoptions_list:
            tag_option_menu.add_radiobutton(label=i, variable=self.tag_str, command=self.check_tag_val)
        
        self.tag_option_button['menu'] = tag_option_menu

        # Set the default tag option.
        if not default_tagoption == None:
            self.set_default_tagoption(default_tagoption)


        # value entry setup
        self.input_entry.grid(row=0, column=2, sticky=FWIDG_EL_STICK_DIR)
        self.input_entry.bind('<Return>', func=self.get_text_entry)
        self.input_entry.config(state=self.tag_select_disabled)

        # move up/down buttons
        self.up_button = ttk.Button(self, text='Up', command=self.send_move_up_command)
        self.up_button.config(state=self.up_button_disabled)
        self.up_button.grid(row=0, column=0, sticky=FWIDG_EL_STICK_DIR)

        # delete button
        self.delete_button = ttk.Button(self, text = 'Delete', command=self.send_delete_command)
        self.delete_button.config(state=self.delete_button_disabled)
        self.delete_button.grid(row=0, column=4, sticky=FWIDG_EL_STICK_DIR) #command = delete_command
        # add child button
        self.add_child_button = ttk.Button(self, text = 'Add Child', command=self.add_template_child_command)
        self.add_child_button.config(state=self.add_button_disabled)
        self.add_child_button.grid(row=0, column=3, sticky=FWIDG_EL_STICK_DIR) #command = add_child_command

        # Tooltip stuff
        self.bind('<Enter>', self.controller.tooltipcontroller.on_mouse_hover)
        self.bind('<Leave>', self.controller.tooltipcontroller.on_mouse_leave)

    def set_default_tagoption(self, default_tagoption):
        """Set the default value of this widget's menu field."""
        print(f"Set default tagoption of {self} to {default_tagoption}")
        self.tag_str.set(default_tagoption)
        #self.set_textbox_str(TagOptions.default_focus_options[default_tagoption])
        self.update()

    def set_textbox_str(self, text: str):
        #TODO: convert this into a tooltip
        """Set the starting value of this widget's text entry box."""
        self.user_input_str.set(text)

    def apply_fieldwidget_template(self, template:str):
        print("entered twilight zone")
        """Apply a pre-defined template to this FieldWidget."""
        self.valid_tagoptions = template #FIXME is this line correct?
        import FieldWidgetTemplates
        # Search FieldWidgetTemplates dictionary for the script to run on this instance
        try:
            FieldWidgetTemplates.template_dict[template](self)
        except Exception as e:
            print(f"could not apply template {template} to {self}: {e}")
    
    def enable_button(self, button: ttk.Button):
        """Enables the specified Button within this FieldWidget."""
        button.config(state=NORMAL)
    
    def disable_button(self, button: ttk.Button):
        """Disables the specified Button within this FieldWidget."""
        button.config(state=DISABLED)

if __name__ == "__main__":
    from WidgetOperationController import WidgetOperationController
    """Testing this class"""
    root = Tk()
    FieldWidget(root, WidgetOperationController(), row=0, col=0)

    root.mainloop()

        
