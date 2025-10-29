from tkinter import *
from tkinter import ttk
import TagOptions

class FieldWidget(ttk.Frame):
    """ 
    Self-contained container with a text entry box, descriptor tag, and movement and delete buttons.

    """
    def __init__():
        """Creates a dummy FieldWidget."""
    
    def __init__(self, parent, controller, row, col):
        """ Creates an instance of this object in the parent ttk frame in row row and column col. """
        super().__init__(master=parent, padding=5)
        self.controller = controller
        self.parent = parent
        print(f"parent of {self} in {row}, {col}: {parent}")
        self.user_input_str = StringVar()
        self.tag_str = StringVar()
        self.parent.columnconfigure(0, weight=1)
        self.current_row_span = 1

        self.childlist = None # Empty instance variable to store a child if we create one 
        self.childcontroller = None

        self.input_entry = ttk.Entry(self, textvariable=self.user_input_str)


        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
       
        FieldWidget.create_widget(self, row=row, col=col)
        
    
    def change_grid_position(self, row: int | None = None, col: int | None = None, change_rowspan: int | None = None):
        """Changes this FieldWidget's position in the parent frame."""
        if row == None:
            row = self.grid_info()['row']
        
        if col == None:
            col = self.grid_info()['column']

        if change_rowspan == None:
            change_rowspan = 0
    
        self.grid_forget()
        self.grid(row=row, column=col, padx=5, pady=5, rowspan=self.current_row_span + change_rowspan)
    
    def move_down_command(self):
        """Moves this widget frame down in the overall grid."""
        prev_col = self.grid_info()['column']
        prev_row = self.grid_info()['row']
        self.grid_forget()
        self.change_grid_position(row=(prev_row + 1), col=prev_col)
    
    def send_move_up_command(self):
        self.controller.swap_up(self)

    def send_move_down_command(self):
        self.controller.move_down(self)

    def send_delete_command(self):
        self.controller.delete_fieldwidget(self, True)
    
    def delete_widget(self):
        if not self.childlist == None:
            for child in self.childlist:
                child.delete_widget()
        
        self.grid_forget()
        self.destroy()

    def get_text_entry(self, text):
        print(text)
        print(self.input_entry.get())
        print(self.user_input_str.get())
    
    def add_child_command(self):
        import WidgetOperationController

        if self.childlist == None:
            self.childlist = []
            self.childcontroller = WidgetOperationController.WidgetOperationController(self, self.childlist, self.controller.main_window)
            self.childcontroller.add_new_child(row_override=1) # The first time, we need to tell it to place on next row
        else:
            self.childcontroller.add_new_child()
            print(self.childlist)
        
    def regrid(self):
        """Updates this widget's positioning"""
        self.change_grid_position()

    def create_widget(self, row, col):
        """Creates the elements of this widget."""
        self.grid(row=row, column=col,padx=5, pady=5)

        # tags menu
        #FIXME: extend menubutton to create a class that has all the options for each of the categories
        tag_option_button = ttk.Menubutton(self, text= '', textvariable= self.tag_str)
        tag_option_button.grid(row=0, column=1)
        tag_option_menu = Menu()

        for i in TagOptions.focus_tag_options:
            tag_option_menu.add_radiobutton(label=i, variable=self.tag_str)
        
        tag_option_button['menu'] = tag_option_menu


        # value entry
        self.input_entry.grid(row=0, column=2, sticky=E)
        self.input_entry.bind('<Return>', func=self.get_text_entry)

        # move up/down buttons
        ttk.Button(self, text='Up', command=self.send_move_up_command).grid(row=0, column=0, sticky=E)

        # delete button
        ttk.Button(self, text = 'Delete', command=self.send_delete_command).grid(row=0, column=5, sticky=E) #command = delete_command
        # add child button
        ttk.Button(self, text = 'Add Child', command=self.add_child_command).grid(row=0, column=4, sticky=E) #command = add_child_command


if __name__ == "__main__":
    """Testing this class"""
    root = Tk()
    FieldWidget(root, 0, 0)

    root.mainloop()

        
