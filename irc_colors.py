# taken from https://code.google.com/p/pybslib/source/browse/trunk/lib/colors.py?r=2

class Colors:

    #Removes all previously applied color and formatting attributes.
    NORMAL = u"\u000f"

    #Bold text.
    BOLD = u"\u0002";
    
    #Underlined text.
    UNDERLINE = u"\u001f";

    #Reversed text (may be rendered as italic text in some clients).
    REVERSE = u"\u0016";
    
    #White coloured text.
    WHITE = u"\u000300";
    
    #Black coloured text.
    BLACK = u"\u000301";
    
    #Dark blue coloured text.
    DARK_BLUE = u"\u000302";
    
    #Dark green coloured text.
    DARK_GREEN = u"\u000303";
    
    #Red coloured text.
    RED = u"\u000304";
    
    #Brown coloured text.
    BROWN = u"\u000305";
    
    #Purple coloured text.
    PURPLE = u"\u000306";
    
    #Olive coloured text.
    OLIVE = u"\u000307";
    
    #Yellow coloured text.
    YELLOW = u"\u000308";
    
    #Green coloured text.
    GREEN = u"\u000309";
    
    #Teal coloured text.
    TEAL = u"\u000310";
    
    #Cyan coloured text.
    CYAN = u"\u000311";

    #Blue coloured text.
    BLUE = u"\u000312";
    
    #Magenta coloured text.
    MAGENTA = u"\u000313";
    
    #Dark gray coloured text.
    DARK_GRAY = u"\u000314";
    
    #Light gray coloured text.
    LIGHT_GRAY = u"\u000315";

    COLORS={'WHITE':WHITE,
            'DARK_BLUE':DARK_BLUE,
            'DARK_GREEN':DARK_GREEN,
            'RED':RED,
            'BROWN':BROWN,
            'PURPLE':PURPLE,
            'OLIVE':OLIVE,
            'YELLOW':YELLOW,
            'GREEN':GREEN,
            'TEAL':TEAL,
            'CYAN':CYAN,
            'BLUE':BLUE,
            'MAGENTA':MAGENTA,
            'DARK_GRAY':DARK_GRAY,
            'LIGHT_GRAY':LIGHT_GRAY
            }
