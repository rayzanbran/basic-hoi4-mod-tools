"""Global settings for specific values."""
FIELDWIDGET_PADX = 5
FIELDWIDGET_PADY = 5
FWIDG_EL_STICK_DIR = 'e' # The direction(s) in which the FieldWidget elements will be sticky.
FWIDG_CHILD_DEF_COL = 4 # The default column in which FieldWidget children will be placed.
FWIDG_DEFAULT_STICKY = 'E'
FWIDG_CHILD_DEFAULT_STICKY = 'W'

# Possible FieldWidget Types
FWIDG_FOCUS_BLOCK = 'focus'
FWIDG_EFFECT_BLOCK = 'complete_effect'

# Possible FieldWidget Elements
# Buttons
FWIDG_ADD = 'add'
FWIDG_DEL = 'delete'
FWIDG_UP = 'up'
# Entry Fields
FWIDG_KEY_ENTRY = 'keyentry'

# Dropdown Radiobutton Menus
FWIDG_TAG_SELECT = 'tagselector'

POSSIBLE_FIELDWIDGET_ELS = (FWIDG_ADD, FWIDG_DEL, FWIDG_UP, FWIDG_KEY_ENTRY, FWIDG_TAG_SELECT)

# Template Settings
TAG_LIST_IGNORE_CHARACTER = '-' # The character that will cause a tag to be ignored and not generate a child in a template