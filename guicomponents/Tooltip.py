from tkinter import *
from tkinter import ttk
class Tooltip(ttk.Frame):
    """Hovering Frame containing a custom Label that can be precisely placed anywhere in a parent.
       
    """
    def __init__(self):
        """Creates a Tooltip at x, y pixels.
        
        """