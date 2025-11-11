from tkinter import *
from tkinter import ttk
#from guicomponents import ContentWindow
from guicomponents.guicontroller import guicontroller
from guicomponents.ComponentSetupScripts import *

class MainWindow(ttk.Frame):
    """The MAIN window, which will hold all the gui components.
       Initially, contains the main menu etc
    """

    def __init__(self):
        """Creates the main window in its own Tk instance.
        
        """
        self.root = Tk()
        self.root.title('hoi4 mod tools')
        self.root.minsize(width=1000, height=400) #Minimum size needed for focus creator FIXME constant this

        # ttk superconstructor
        super().__init__(master=self.root)
        configure_row_col(self.root)
        configure_row_col(self)
        self.grid(row=0, column=0)
        

        # create top menu bar - initially hidden

        # create content window
        self.content_window = ttk.Frame(self, padding=5)
        self.content_window.grid(row=0, column=0)
        configure_row_col(self.content_window)
        
        # Register the GUI controller
        self.guicontroller = guicontroller(mainwindow=self)

        # Open the main menu
        self.guicontroller.open_main_menu()
        

