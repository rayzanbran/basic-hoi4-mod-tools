from tkinter import *
from tkinter import ttk
from guicomponents import guihelpers

class Tooltip(ttk.Frame):
    """Hovering Frame containing a custom Label that can be precisely placed anywhere in a parent.
       
    """
    def __init__(self, target_window, text:str | None = None):
        """Creates a Tooltip at x, y pixels on top of (but within the bounds of) targetwindow.
        
        """
        self.target_window = target_window
        super().__init__(master=target_window, relief='solid',borderwidth=5, style='tooltip_default_style.TFrame')
        self.tooltip_default_style = ttk.Style(self)

        self.tooltip_text = StringVar(value=text)
        self.tooltip_label = self.create_own_label(self.tooltip_text.get())
        self.tooltip_label.grid(row=0, column=0)

        # Create yourself
        self.style = self.tooltip_default_style
        x, y = self.calc_place_position()
        self.place(x=x, y=y)

        self.tooltip_default_style.theme_use('clam')

    def calc_place_position(self):
        """Calculates the x, y position this Tooltip should be placed in the target window.
        
        """
        import guihelpers
        # FIXME offsets should be such that the tooltip does not cover the area it is describing.
        x_offset = 10 #FIXME constant these
        y_offset = 10

        # Get mouse position relative to the target window. In most cases we can just place the tooltip based on that.
        x_pos, y_pos = guihelpers.get_pointer_position(self.target_window)
        x_pos += x_offset
        y_pos += y_offset

        return (x_pos, y_pos)

        # However, in cases near the edges of the screen...

        #upper edge
        #lower edge
        #left edge
        #right edge
    def update_text(self, new_text:str):
        self.tooltip_text.set(new_text)
    
    def style_self(self):
        """Applies a color, font, etc."""
    
    def create_own_label(self, text):
        """Create this Tooltip's label and place it in the Tooltip."""

        return ttk.Label(self, text=text, style='tooltip_default_style.TLabel')

if __name__ == "__main__":
    """Testing tooltips."""
    current_tooltip: Tooltip = None
    # Prototype code for what will go in guicontroller
    # on mouse hover, spawn requisite tooltip 
    def on_mouse_hover(*args):
        global current_tooltip
        current_tooltip = Tooltip(root, text='example tooltip')

    # on mouse leave, destroy it
    def on_mouse_leave(*args):
        current_tooltip.destroy()

    import ComponentSetupScripts
    root = Tk()
    ComponentSetupScripts.configure_row_col(root)
    root.minsize(width=300, height=300)


    l = ttk.Label(master=root, text='hover over this to spawn a tooltip')
    l.grid(row=0, column=0)

    l.bind('<Enter>', on_mouse_hover)
    l.bind('<Leave>', on_mouse_leave)
    
    root.mainloop()



        
