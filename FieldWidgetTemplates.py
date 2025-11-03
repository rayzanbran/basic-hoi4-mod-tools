import FieldWidget
from TagOptions import *
"""Template scripts for FieldWidgets that create their children.
   Should be called by a FieldWidget object in the apply_fieldwidget_template method
"""
def template_focus_block_main(self: FieldWidget.FieldWidget):
    """Sets up Fieldwidgets with the minimum necessary fields for a focus block -
       as children of a FieldWidget.
    """
    for key in default_focus_tags:
        self.add_template_child_command(child_type='focus', default_tagoption=key)

    pass


def template_character_block(self: FieldWidget.FieldWidget):
    """Sets up a Fieldwidget with children for creating a character"""
    for key in default_character_tags:
        self.add_template_child_command(child_type='character', default_tagoption=key)

    pass

def template_timed_idea_block(self:FieldWidget.FieldWidget):
    """Sets up a FieldWidget for creating a timed idea block."""

    pass






# Dictionary mapping functions to keys
template_dict = {
    'focus' : template_focus_block_main,
    'character' : template_character_block
}