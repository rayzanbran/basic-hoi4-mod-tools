from tkinter import *
from tkinter import ttk

class BottomMenuBar(ttk.Frame):
    """ Wrapper frame for the bottom menu bar options. """
    def send_add_new_field_command(self):
        self.controller.add_widget()

    def __init__(self, parent, controller):
        super().__init__(parent, padding=5)
        self.controller = controller

        #Buttons
        self.copy_button = ttk.Button(self, text='copy output')
        self.add_new_field_button = ttk.Button(self, text='Add new field', command=self.send_add_new_field_command)
        self.add_new_field_button.config(state=DISABLED) #TODO disabling this for now, no longer needed?
        self.preview_button = ttk.Button(self, text='preview output', command=self.controller.main_window.process)

        self.create_bottom_frame()
    
    def create_bottom_frame(self):
        self.copy_button.grid(column=0, row=0)
        self.add_new_field_button.grid(column=1, row=0)
        self.preview_button.grid(column=2, row=0)

    
    


