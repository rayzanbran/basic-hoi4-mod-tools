from guicomponents.Tooltip import Tooltip
class TooltipController():
    """Controls tooltip display on the GUI."""
    tooltip_creation_delay = 1000 #ms FIXME constant this
    

    def __init__(self, parent):
        self.parent = parent
        self.current_tooltip = None
        self.current_tooltip: Tooltip = None
        self.requested_tooltip = None
        self.still_wants_tooltip = True

    def make_tooltip(self, hover_window, *args):
        if self.still_wants_tooltip:
            self.current_tooltip = Tooltip(target_window=self.parent, hover_window=hover_window, text='test')
    
    # on mouse hover, spawn requisite tooltip 
    def on_mouse_hover(self, *args):
        tooltip_creation_delay = self.tooltip_creation_delay

        if not self.current_tooltip == None:
            self.current_tooltip.destroy()
        
        self.still_wants_tooltip = True
        self.requested_tooltip = args[0].widget.after(tooltip_creation_delay, self.make_tooltip, args[0].widget) # Wait a second before creating the tooltip.
        print(self.requested_tooltip)
        #current_tooltip = Tooltip(root, text='example tooltip')

    # on mouse leave, destroy it or let program know user no longer needs tooltip
    def on_mouse_leave(self, *args):
        self.still_wants_tooltip = False

        if not self.current_tooltip == None:
            self.current_tooltip.destroy()
        
        args[0].widget.after_cancel(self.requested_tooltip)

    