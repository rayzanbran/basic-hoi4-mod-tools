from tkinter import *
from tkinter import ttk
from WidgetOperationController import WidgetOperationController

class BottomMenuBar(ttk.Frame):
    """ Wrapper frame for the bottom menu bar options. """
    def send_add_new_field_command(self):
        """Tells the controller below the WidgetWindow controller to add a new FieldWidget with the same type as the top block.
           \nIf this fails, adds a new FieldWidget to the WidgetWindow
        """
        try:
            self.controller.control_list[0].add_template_child_command(child_type=self.controller.control_list[0].valid_tagoptions)
        except Exception as e:
            print(f"Could not add a FieldWidget to the first block in WidgetWindow: {e}\n ...Adding it to WidgetWindow instead.")
            self.controller.add_widget()

    def __init__(self, parent, controller):
        super().__init__(parent, padding=5)
        self.controller: WidgetOperationController = controller

        #Buttons
        self.copy_button = ttk.Button(self, text='copy output')
        self.add_new_field_button = ttk.Button(self, text='Add new field', command=self.send_add_new_field_command)
        #self.add_new_field_button.config(state=DISABLED) #TODO disabling this for now, no longer needed?
        self.preview_button = ttk.Button(self, text='preview output', command=self.controller.main_window.process)

        self.create_bottom_frame()
    
    def create_bottom_frame(self):
        self.copy_button.grid(column=0, row=0)
        self.add_new_field_button.grid(column=1, row=0)
        self.preview_button.grid(column=2, row=0)

    
    


