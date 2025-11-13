def main_menu_setup(self):
    """Runs in a MainMenuPane and sets it up."""

def configure_row_col(widget):
    """Configures a widget row/column weights."""
    for i in range(10):
        widget.columnconfigure(i, weight=1)
        widget.rowconfigure(i, weight=1) #FIXME make constants for these

