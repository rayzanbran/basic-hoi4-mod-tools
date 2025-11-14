from tkinter import *
from tkinter import ttk
from guihelpers import *

class Tooltip(ttk.Frame):
    """Hovering Frame containing a custom Label that can be precisely placed anywhere in a parent.
       
    """
    def __init__(self, target_window, hover_window, text:str | None = None):
        """Creates a Tooltip at x, y pixels on top of (but within the bounds of) targetwindow.
           hover_window: the element/frame that the pointer is actually over. The tooltip will avoid covering this.
        """
        self.target_window: ttk.Frame = target_window
        self.hover_window: ttk.Label = hover_window

        super().__init__(master=target_window, relief='solid',borderwidth=5, style='tooltip_default_style.TFrame')

        self.tooltip_default_style = ttk.Style() # FIXME constant this

        # Create the tooltip contents
        self.tooltip_text = StringVar(value=text)
        self.tooltip_label: ttk.Label = self.create_own_label(self.tooltip_text.get())
        self.tooltip_label.grid(row=0, column=0)

        self.tooltip_label.update_idletasks() # allows this tooltip to calculate its requested dimensions

        self.margin_x = self.winfo_reqwidth()
        self.margin_y = self.winfo_reqheight()

        # Create yourself
        #self.style = self.tooltip_default_style
        self.place_self()

        #self.tooltip_default_style.theme_use('clam')

    def determine_tooltip_position(self):
        """Determines whether this tooltip should be above/below and to the left/right of the pointer.

        """
        pointer_position = get_pointer_position(self.target_window)
        window_bounds = (self.target_window.winfo_width(), self.target_window.winfo_height())

        side = None
        elevation = None

        # Desired space between the pointer and edges of window to display this widget
        margin_x = self.margin_x
        #print(f"margin_x: {margin_x}")
        margin_y = self.margin_y

        #print(pointer_position)
        #print(f"window_bounds: {window_bounds}")

        # Place the tooltip to the side of the pointer where there is space
        if pointer_position[0] + margin_x > window_bounds[0]:
            side = LEFT
        elif pointer_position[0] - margin_x < 0:
            side = RIGHT
        else: # If there is no danger of the widget going off left or right of window, it doesn't need to be on any particular side
            side = None 

        if pointer_position[1] + margin_y > window_bounds[1]:
            elevation = TOP
        else:
            elevation = BOTTOM

        return ([side, elevation])

    def calc_place_position(self):
        """Calculates the x, y position this Tooltip should be placed in the target window.
           side: left/right side of hover_window
           elevation: top/bottom (above/below) hover_window
        """
        side, elevation = self.determine_tooltip_position() # figure out what side of the hovered window the tooltip should be on

        x_offset = 10 #FIXME constant these
        y_offset = 10

        # Get mouse position relative to the target window.
        x_pos, y_pos = get_pointer_position(self.target_window)

        #print(f"x_pos: {x_pos}, y_pos: {y_pos}")
        # get the pixel position of the bottom of the widget being hovered over
        distance_to_bottom = self.hover_window.winfo_height() - get_pointer_position(self.hover_window)[1]
        #print(f"distance_to_bottom: {distance_to_bottom}")

        if side == LEFT:
            x_offset = -1 * self.margin_x
        elif side == RIGHT:
            x_offset = x_offset
        
        if elevation == TOP:
            y_offset = self.target_window.winfo_y() - y_pos - self.margin_y
        elif elevation == BOTTOM:
            y_offset += distance_to_bottom

        x_pos += x_offset
        y_pos += y_offset

        #print(f"x_pos: {x_pos}, y_pos: {y_pos}")

        return (x_pos, y_pos)
    
    def place_self(self):
        x, y = self.calc_place_position()
        self.place(x=x, y=y)

    def update_text(self, new_text:str):
        self.tooltip_text.set(new_text)
    
    def style_self(self):
        """Applies a color, font, etc."""
    
    def create_own_label(self, text):
        """Create this Tooltip's label and place it in the Tooltip."""

        return ttk.Label(self, text=text, style='tooltip_default_style.TLabel')

if __name__ == "__main__":
    """Testing tooltips."""
    tooltip_creation_delay = 1000 #ms FIXME constant this
    current_tooltip: Tooltip = None
    requested_tooltip = None
    still_wants_tooltip = True
    # Prototype code for what will go in guicontroller
    # on mouse hover, spawn requisite tooltip 
    def on_mouse_hover(*args):
        #global current_tooltip
        global requested_tooltip
        global still_wants_tooltip
        
        still_wants_tooltip = True
        requested_tooltip = args[0].widget.after(tooltip_creation_delay, make_tooltip, args[0].widget) # Wait a second before creating the tooltip.
        #print(requested_tooltip)
        #current_tooltip = Tooltip(root, text='example tooltip')

    # on mouse leave, destroy it or let program know user no longer needs tooltip
    def on_mouse_leave(*args):
        global still_wants_tooltip
        global current_tooltip
        global requested_tooltip

        still_wants_tooltip = False

        if not current_tooltip == None:
            current_tooltip.destroy()
        
        args[0].widget.after_cancel(requested_tooltip)
    

    def make_tooltip(hover_window, *args):
        global current_tooltip
        global still_wants_tooltip

        if still_wants_tooltip:
            current_tooltip = Tooltip(target_window=root, hover_window=hover_window, text='example tooltip')

    import ComponentSetupScripts
    root = Tk()
    ComponentSetupScripts.configure_row_col(root)
    root.minsize(width=300, height=300)


    l = ttk.Label(master=root, text='hover over this to spawn a tooltip')
    l.place(x=0, y=0)

    l.bind('<Enter>', on_mouse_hover)
    l.bind('<Leave>', on_mouse_leave)
    
    root.mainloop()



        
