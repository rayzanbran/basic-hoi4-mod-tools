"""Contains the tag options to be used in MenuButtons."""
focus_tag_options = [
    'example1',
    'example2',
    'example3',
    'complete_effect'
]

effect_block_tag_options = [
    'add_political_power',
    'add_stability',
]

# Dictionary of the possible tag lists.
possible_tag_lists = {
    'focus' : focus_tag_options,
    'effect' : effect_block_tag_options
}

# Default tag options when starting a new focus block.
default_focus_tags = ([
    'id',
    'relative_position_id',
    'x',
    'y',
    'cost',
    'complete_effect',
])

# Default text for default tag options when starting a new focus block.
default_focus_text = [
    'TAG_focus_name', # id
    'TAG_other_focus_name', # relative_position_id
    '-1',
    '-1',
    '-1',
    'add child below with effects'
]

# Sets up the dictionary for default focus options by combining the tags with the text.
default_focus_options = {}
for i in range(len(default_focus_tags)):
    default_focus_options[default_focus_tags[i]] = default_focus_text[i]