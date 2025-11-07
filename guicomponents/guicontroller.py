#from guicomponents import MainWindow
#from guicomponents import ContentWindow

class guicontroller:
    """Controls GUI-changing operations (on-actions)"""
    def __init__(self, mainwindow):
        """
        mainwindow: the the MainWindow this guicontroller is registered to.
        """
        from guicomponents import MainWindow
        self.mainwindow: MainWindow.MainWindow = mainwindow # The Window this instance is registered to
        self.current_content_pane = None # initialize with none
        self.register_content_pane()

    def register_content_pane(self):
        """Updates the content pane in this controller to be the parent's content frame."""
        self.current_content_pane = self.mainwindow.content_window
    
    def clear_parent_content_pane(self):
        # Destroy the child currently in the content window.
        for child in self.mainwindow.content_window.winfo_children():
            child.destroy()

    def change_parent_content_pane(self, new_pane):
        """Updates the parent's content pane with a new pane and registers the new pane with this controller.
        
        """
        new_pane.grid(row=1, column=0, padx=5, pady=5) #FIXME define constants for this
        self.register_content_pane()

    def resize_parent(self, new_size):
        self.mainwindow.root.geometry(newGeometry=new_size)

    # Opening settings pane
    def open_settings_pane(self):
        """"""
        # Place the settings pane on top of the current Content pane


    # Opening tool panes
    def open_focus_pane(self):
        """
        NOTE: this clears anything currently in the content frame.
        """
        from guicomponents import ContentWindow
        self.clear_parent_content_pane()

        # Replace mainwindow's content pane with a new focus pane
        #self.resize_parent(ContentWindow.WidgetWindow.size)
        self.change_parent_content_pane(ContentWindow.WidgetWindow(parent=self.mainwindow.content_window))

    def open_main_menu(self):
        """Replace parent content pane with the main menu.
           NOTE: clears anything currently in the content frame.
        """
        from guicomponents import ContentWindow
        self.clear_parent_content_pane()
        self.change_parent_content_pane(ContentWindow.MainMenuPane(parent=self.mainwindow.content_window))
        

    # Returning to the main menu?

    