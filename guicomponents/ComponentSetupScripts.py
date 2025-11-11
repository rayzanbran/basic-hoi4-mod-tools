def main_menu_setup(self):
    """Runs in a MainMenuPane and sets it up."""

def configure_row_col(widget):
    """Configures a widget row/column weights."""
    widget.rowconfigure(0, weight=1) #FIXME make constants for these
    widget.columnconfigure(0, weight=1)