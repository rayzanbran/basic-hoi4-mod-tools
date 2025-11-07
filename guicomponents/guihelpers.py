from tkinter import *
from tkinter import ttk
def get_pointer_position(root: Tk):
    """Gets the pointer's coordinates within the root and returns a tuple (x,y)
       relative to the specified root\n
       root: the Tk root to look in.
    
    """
    x = root.winfo_pointerx()
    y = root.winfo_pointery()

    abs_x = x - root.winfo_rootx()
    abs_y = y - root.winfo_rooty()

    return (abs_x, abs_y)

def get_pointer_position_frame(root: ttk.Frame):
    """Gets the pointer's coordinates within a frame and returns a tuple (x,y)
       relative to the specified frame\n
       root: the ttk frame to look in.
    
    """
    x = root.winfo_pointerx()
    y = root.winfo_pointery()

    # Need to not only consider the position of the root on the screen 
    # but the position of this window within the root
    abs_x = x - root.winfo_rootx() - root.winfo_x()
    abs_y = y - root.winfo_rooty() - root.winfo_y()

    return (abs_x, abs_y)




