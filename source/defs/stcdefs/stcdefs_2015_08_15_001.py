# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------

import keyword as keyword # i.e. the Python language keywords, used by the Python lexer

# from pprint import PrettyPrinter
# pprinter = PrettyPrinter(indent=4, width=80);

# ------------------------------------------------------------------------------

STC_PERFORMED_BITS = {
    # -- PERFORMED BITS:
    # 0010000 u"USER"    [1]    -- A modification was done by the User.
    # 0100000 u"UNDO"    [2.1]  -- A modification was done by an Undo.
    # 1000000 u"REDO"    [2.2]  -- A modification was done by a Redo.
    # 1100000 u"NONUSER" [3.1]* -- A modification was NOT done by the User.
    # 1010000 u"NONUNDO" [3.2]* -- A modification was NOT done by an Undo.
    # 0110000 u"NONREDO" [3.3]* -- A modification was NOT done by a Redo.
    # 1110000 u"ANYONE"  [4]*   -- A modification was done by any one of the three (i.e. by the User, or by an Undo, or by a Redo).
    u"USER":    0x10,               # = 16   (= 2**4) = 0b0010000 (= 0b1 << 0b100 = 0b10 << 0b11 ) = stc.STC_PERFORMED_USER [1]
    u"UNDO":    0x20,               # = 32   (= 2**5) = 0b0100000 (= 0b1 << 0b101 = 0b10 << 0b100) = stc.STC_PERFORMED_UNDO [2.1]
    u"REDO":    0x40,               # = 64   (= 2**6) = 0b1000000 (= 0b1 << 0b110 = 0b10 << 0b101) = stc.STC_PERFORMED_REDO [2.2]
    u"NONUSER": 0x20 | 0x40,        # = 0x60  = 96    = 0b1100000 [3.1]*
    u"NONUNDO": 0x10 | 0x40,        # = 0x50  = 80    = 0b1010000 [3.2]*
    u"NONREDO": 0x10 | 0x20,        # = 0x30  = 48    = 0b0110000 [3.3]*
    u"ANYONE":  0x10 | 0x20 | 0x40, # = 0x70  = 112   = 0b1110000 [4]*
}; # STC_PERFORMED_BITS

STC_MODIFIED_BITS = {
    # -- MODIFIED BITS:
    # 000000000000000001 u"TEXT_INSERTED"      [1.1]  -- A text range was just inserted in to the document.
    # 000000000000000010 u"TEXT_DELETED"       [1.2]  -- A text range was just deleted from the document.
    # 000000000000000011 u"TEXT_CHANGED"       [1]*   -- A text range was just either inserted in to, or deleted from the document.
    # 000000010000000000 u"TEXT_PREINSERT"     [2.1]  -- A text range is about to be inserted in to the document.
    # 000000100000000000 u"TEXT_PREDELETE"     [2.2]  -- A text range is about to be deleted from the document.
    # 000000110000000000 u"TEXT_PRECHANGE"     [2]*   -- A text range is about to be either inserted in to, or deleted from the document.
    # 000000010000000001 u"TEXT_ANYINSERT"     [3.1]* -- A text range is either about to be inserted, or was just inserted in to the document.
    # 000000100000000010 u"TEXT_ANYDELETE"     [3.2]* -- A text range is either about to be deleted, or was just deleted from the document.
    # 000000110000000011 u"TEXT_ANYCHANGE"     [4]*   -- A text range is either about to or was just either inserted in to, or deleted from the document.
    # 000000000000000100 u"STYLE_CHANGED"      [5]    -- A style range has just been modified.
    # 000000001000000000 u"MARKER_CHANGED"     [6]    -- A marker, or markers, have just been modified.
    # 100000000000000000 u"ANNOTATION_CHANGED" [7]    -- One or more annotations have just been modified.
    # ...
    u"TEXT_INSERTED":      0x1,                         # = 1 (= 2**0) = 0b1  (= 0b1 << 0b0              ) = stc.STC_MOD_INSERTTEXT [1.1]
    u"TEXT_DELETED":       0x2,                         # = 2 (= 2**1) = 0b10 (= 0b1 << 0b1 = 0b10 << 0b0) = stc.STC_MOD_DELETETEXT [1.2]
    u"TEXT_CHANGED":       0x1 | 0x2,                   # = 0x3 = 3 = 0b11 [1]*
    u"TEXT_PREINSERT":     0x400,                       # = 1024 (= 2**10) = 0b010000000000 (= 0b1 << 0b1010 = 0b10 << 0b1001) = stc.STC_MOD_BEFOREINSERT [2.1]
    u"TEXT_PREDELETE":     0x800,                       # = 2048 (= 2**11) = 0b100000000000 (= 0b1 << 0b1011 = 0b10 << 0b1010) = stc.STC_MOD_BEFOREDELETE [2.2]
    u"TEXT_PRECHANGE":     0x400 | 0x800,               # = 0xC00 = 3072 = 0b110000000000 [2]*
    u"TEXT_ANYINSERT":     0x1 | 0x400,                 # = 0x401 = 1025 = 0b010000000001 [3.1]*
    u"TEXT_ANYDELETE":     0x2 | 0x800,                 # = 0x802 = 2050 = 0b100000000010 [3.2]*
    u"TEXT_ANYCHANGE":     0x01 | 0x02 | 0x400 | 0x800, # = 0xC03 = 3075 = 0b110000000011 [4]*
    u"STYLE_CHANGED":      0x4,                         # = 4      (= 2**2)  = 0b100                (= 0b1 << 0b10    = 0b10 << 0b1    ) = stc.STC_MOD_CHANGESTYLE      [5]
    u"MARKER_CHANGED":     0x200,                       # = 512    (= 2**9)  = 0b1000000000         (= 0b1 << 0b1001  = 0b10 << 0b1000 ) = stc.STC_MOD_CHANGEMARKER     [6]
    u"ANNOTATION_CHANGED": 0x20000,                     # = 131072 (= 2**17) = 0b100000000000000000 (= 0b1 << 0b10001 = 0b10 << 0b10000) = stc.STC_MOD_CHANGEANNOTATION [7]
    # ...
}; # STC_MODIFIED_BITS

STC_UPDATED_BITS = {
    # -- UPDATED BITS:
    # 0001 u"CONTENT"   [1] -- Contents (i.e. either a text range, or a style range, or one or more markers) have changed.
    # 0010 u"SELECTION" [2] -- A selection range has changed.
    # 0100 u"V_SCROLL"  [3] -- A vertical scroll position has changed.
    # 1000 u"H_SCROLL"  [4] -- A horizontal scroll position has changed.
    u"CONTENT":   0x1, # = 1 (= 2**0) = 0b1    (= 0b1 << 0b0                ) = stc.STC_UPDATE_CONTENT   [1]
    u"SELECTION": 0x2, # = 2 (= 2**1) = 0b10   (= 0b1 << 0b1  = 0b10 << 0b0 ) = stc.STC_UPDATE_SELECTION [2]
    u"V_SCROLL":  0x4, # = 4 (= 2**2) = 0b100  (= 0b1 << 0b10 = 0b10 << 0b1 ) = stc.STC_UPDATE_V_SCROLL  [3]
    u"H_SCROLL":  0x8, # = 8 (= 2**3) = 0b1000 (= 0b1 << 0b11 = 0b10 << 0b10) = stc.STC_UPDATE_H_SCROLL  [4]
}; # STC_UPDATED_BITS

# ------------------------------------------------------------------------------

STC_STYLE_MASKS = {
    # -- STYLE MASK BITS:
    # 11111111 u"8_BIT" [1] -- Use all the 8 (i.e. 5 + 3) bits (i.e. the whole byte) for a style (i.e. no indicator bits).
    # 00011111 u"5_BIT" [2] -- Use only the first 5 bits for a style, leaving the last 3 bits for indicators (i.e. split the byte).
    "8_BIT": (2**8)-1, # = 256-1 = 255 = 0xFF (= 0x100 - 0x1) = 0b11111111 (= 0b100000000 - 0b1) [1]
    "5_BIT": (2**5)-1, # = 32 -1 = 31  = 0x1F (= 0x20  - 0x1) = 0b11111    (= 0b100000    - 0b1) [2]
}; # STC_STYLE_MASKS

STC_STYLE_NAMES = {
    u"DEFAULT": {
        # -- DEFAULT CUSTOM STYLE ID (0):
        0: u"DEFAULT",
        # -- LOWER CUSTOM STYLE IDS (1-31):
        # ...
        # -- RESERVED STC STYLE IDS (32-39):
        32: u"STC_DEFAULT",        # = stc.STC_STYLE_DEFAULT
        33: u"STC_LINENUMBER",     # = stc.STC_STYLE_LINENUMBER
        34: u"STC_BRACELIGHT",     # = stc.STC_STYLE_BRACELIGHT
        35: u"STC_BRACEBAD",       # = stc.STC_STYLE_BRACEBAD
        36: u"STC_CONTROLCHAR",    # = stc.STC_STYLE_CONTROLCHAR
        37: u"STC_INDENTGUIDE",    # = stc.STC_STYLE_INDENTGUIDE
        38: u"STC_CALLTIP",        # = stc.STC_STYLE_CALLTIP
        39: u"STC_LASTPREDEFINED", # = stc.STC_STYLE_LASTPREDEFINED
        # -- UPPER CUSTOM STYLE IDS (40-254):
        # ...
        253: u"ANNOTATION",
        254: u"TEXTMARGIN",
        # -- RESERVED STC PSEUDO-STYLE ID:
        255: u"STC_MAX",           # = stc.STC_STYLE_MAX
    }, # NONE
    u"INPUT": {
        # -- DEFAULT CUSTOM STYLE ID (0):
        0: u"DEFAULT",
        # -- LOWER CUSTOM STYLE IDS (1-31):
        1: u"FROZEN",
        # ...
        # -- RESERVED STC STYLE IDS (32-39):
        32: u"STC_DEFAULT",        # = stc.STC_STYLE_DEFAULT
        33: u"STC_LINENUMBER",     # = stc.STC_STYLE_LINENUMBER
        34: u"STC_BRACELIGHT",     # = stc.STC_STYLE_BRACELIGHT
        35: u"STC_BRACEBAD",       # = stc.STC_STYLE_BRACEBAD
        36: u"STC_CONTROLCHAR",    # = stc.STC_STYLE_CONTROLCHAR
        37: u"STC_INDENTGUIDE",    # = stc.STC_STYLE_INDENTGUIDE
        38: u"STC_CALLTIP",        # = stc.STC_STYLE_CALLTIP
        39: u"STC_LASTPREDEFINED", # = stc.STC_STYLE_LASTPREDEFINED
        # -- UPPER CUSTOM STYLE IDS (40-254):
        # ...
        253: u"ANNOTATION",
        254: u"TEXTMARGIN",
        # -- RESERVED STC PSEUDO-STYLE ID:
        255: u"STC_MAX",            # = stc.STC_STYLE_MAX
    }, # INPUT
    u"OUTPUT": {
        # -- DEFAULT CUSTOM STYLE ID (0):
        0: u"DEFAULT",
        # -- LOWER CUSTOM STYLE IDS (1-31):
        1: u"FROZEN",
        # ...
        # -- RESERVED STC STYLE IDS (32-39):
        32: u"STC_DEFAULT",        # = stc.STC_STYLE_DEFAULT
        33: u"STC_LINENUMBER",     # = stc.STC_STYLE_LINENUMBER
        34: u"STC_BRACELIGHT",     # = stc.STC_STYLE_BRACELIGHT
        35: u"STC_BRACEBAD",       # = stc.STC_STYLE_BRACEBAD
        36: u"STC_CONTROLCHAR",    # = stc.STC_STYLE_CONTROLCHAR
        37: u"STC_INDENTGUIDE",    # = stc.STC_STYLE_INDENTGUIDE
        38: u"STC_CALLTIP",        # = stc.STC_STYLE_CALLTIP
        39: u"STC_LASTPREDEFINED", # = stc.STC_STYLE_LASTPREDEFINED
        # -- UPPER CUSTOM STYLE IDS (40-254):
        # ...
        253: u"ANNOTATION",
        254: u"TEXTMARGIN",
        # -- RESERVED STC PSEUDO-STYLE ID:
        255: u"STC_MAX",            # = stc.STC_STYLE_MAX
    }, # OUTPUT
    u"TABLE": {
        # -- DEFAULT CUSTOM STYLE ID (0):
        0: u"DEFAULT",
        # -- LOWER CUSTOM STYLE IDS (1-31):
        1: u"COMMENT",
        # ...
        # -- RESERVED STC STYLE IDS (32-39):
        32: u"STC_DEFAULT",        # = stc.STC_STYLE_DEFAULT
        33: u"STC_LINENUMBER",     # = stc.STC_STYLE_LINENUMBER
        34: u"STC_BRACELIGHT",     # = stc.STC_STYLE_BRACELIGHT
        35: u"STC_BRACEBAD",       # = stc.STC_STYLE_BRACEBAD
        36: u"STC_CONTROLCHAR",    # = stc.STC_STYLE_CONTROLCHAR
        37: u"STC_INDENTGUIDE",    # = stc.STC_STYLE_INDENTGUIDE
        38: u"STC_CALLTIP",        # = stc.STC_STYLE_CALLTIP
        39: u"STC_LASTPREDEFINED", # = stc.STC_STYLE_LASTPREDEFINED
        # -- UPPER CUSTOM STYLE IDS (40-254):
        # ...
        253: u"ANNOTATION",
        254: u"TEXTMARGIN",
        # -- RESERVED STC PSEUDO-STYLE ID:
        255: u"STC_MAX",            # = stc.STC_STYLE_MAX
    }, # TABLE
}; # STC_STYLE_NAMES

STC_STYLE_INDICES = dict(
    (
        name,
        dict(
            (value,key) for (key,value) in STC_STYLE_NAMES[name].iteritems()
        ),
    ) for name in STC_STYLE_NAMES.iterkeys()
);

STC_STYLE_COLOURS = {
    u"DEFAULT": {
        u"CARET_FOREGROUND":      u"#0000FF",
        u"CARET_BACKGROUND":      u"#DDE0F0",
        u"WHITESPACE_FOREGROUND": u"#000000",
        u"WHITESPACE_BACKGROUND": u"#FFFFFF",
        u"SELECTION_FOREGROUND":  u"#000000",
        u"SELECTION_BACKGROUND":  u"#FFD7C0",
        u"HOTSPOT_FOREGROUND":    u"#000000",
        u"HOTSPOT_BACKGROUND":    u"#FFFF00",
        u"CALLTIP_HIGHLIGHT":     u"#FF0000",
        u"EDGE":                  u"#777777",
        # ...
    }, # NONE
    u"INPUT": {
        u"CARET_FOREGROUND":      u"#FFFFFF",
        u"CARET_BACKGROUND":      u"#0020C0",
        u"WHITESPACE_FOREGROUND": u"#0077FF",
        u"WHITESPACE_BACKGROUND": u"#FFFFFF",
        u"SELECTION_FOREGROUND":  u"#FFFFFF",
        u"SELECTION_BACKGROUND":  u"#0077FF", # u"#0033EE"
        u"HOTSPOT_FOREGROUND":    u"#000099",
        u"HOTSPOT_BACKGROUND":    u"#0099FF",
        u"CALLTIP_HIGHLIGHT":     u"#FF0000",
        u"CURRENT_LINE":           u"#FFFFFF",
        u"EDGE":                  u"#0022CC",
        # ...
    }, # INPUT
    u"OUTPUT": {
        u"CARET_FOREGROUND":      u"#0000FF",
        u"CARET_BACKGROUND":      u"#DDE0F0",
        u"WHITESPACE_FOREGROUND": u"#0000AA",
        u"WHITESPACE_BACKGROUND": u"#FFFFFF",
        u"SELECTION_FOREGROUND":  u"#000000",
        u"SELECTION_BACKGROUND":  u"#DDA0A0",
        u"HOTSPOT_FOREGROUND":    u"#000077",
        u"HOTSPOT_BACKGROUND":    u"#FFFF00",
        u"CALLTIP_HIGHLIGHT":     u"#FF0000",
        u"CURRENT_LINE":           u"#000077",
        u"EDGE":                  u"#777777",
        # ...
    }, # OUTPUT
    u"TABLE": {
        u"CARET_FOREGROUND":      u"#0000FF",
        u"CARET_BACKGROUND":      u"#DDE0F0",
        u"WHITESPACE_FOREGROUND": u"#0000AA",
        u"WHITESPACE_BACKGROUND": u"#FFFFFF",
        u"SELECTION_FOREGROUND":  u"#000000",
        u"SELECTION_BACKGROUND":  u"#FFD7C0",
        u"HOTSPOT_FOREGROUND":    u"#000077",
        u"HOTSPOT_BACKGROUND":    u"#FFFF00",
        u"CALLTIP_HIGHLIGHT":     u"#FF0000",
        u"CURRENT_LINE":           u"#000077",
        u"EDGE":                  u"#777777",
        # ...
    }, # TABLE
    # ...
}; # STC_STYLE_COLOURS

STC_STYLE_SPECS = {
    u"DEFAULT": {
        # [1] RESERVED STYLES:
        u"STC_DEFAULT":        {u"styleNum": STC_STYLE_INDICES[u"DEFAULT"][u"STC_DEFAULT"],        u"spec": u"face:Consolas,size:9,fore:#000000,back:#FFFFFF"}, # 32
        u"STC_LINENUMBER":     {u"styleNum": STC_STYLE_INDICES[u"DEFAULT"][u"STC_LINENUMBER"],     u"spec": u"face:Consolas,size:9,fore:#777777,back:#E0E0E0"}, # 33
        u"STC_BRACELIGHT":     {u"styleNum": STC_STYLE_INDICES[u"DEFAULT"][u"STC_BRACELIGHT"],     u"spec": u"face:Consolas,size:9,fore:#777777,back:#E0E0E0"}, # 34
        u"STC_BRACEBAD":       {u"styleNum": STC_STYLE_INDICES[u"DEFAULT"][u"STC_BRACEBAD"],       u"spec": u"face:Consolas,size:9,fore:#777777,back:#E0E0E0"}, # 35
        u"STC_CONTROLCHAR":    {u"styleNum": STC_STYLE_INDICES[u"DEFAULT"][u"STC_CONTROLCHAR"],    u"spec": u"face:Consolas,size:9"}, # 36
        u"STC_INDENTGUIDE":    {u"styleNum": STC_STYLE_INDICES[u"DEFAULT"][u"STC_INDENTGUIDE"],    u"spec": u"face:Consolas,size:9,fore:#A0A0A0,back:#FFFFFF"}, # 37
        u"STC_CALLTIP":        {u"styleNum": STC_STYLE_INDICES[u"DEFAULT"][u"STC_CALLTIP"],        u"spec": u"face:Consolas,size:9,fore:#FFFFFF,back:#000077"}, # 38
        u"STC_LASTPREDEFINED": {u"styleNum": STC_STYLE_INDICES[u"DEFAULT"][u"STC_LASTPREDEFINED"], u"spec": u"face:Consolas,size:9,fore:#000000,back:#FFFFFF"}, # 39
        # [2] CUSTOM STYLES:
        u"DEFAULT":            {u"styleNum": STC_STYLE_INDICES[u"DEFAULT"][u"DEFAULT"],            u"spec": u"face:Consolas,size:9,fore:#000000,back:#FFFFFF"}, # 0
        # ...
        u"ANNOTATION":         {u"styleNum": STC_STYLE_INDICES[u"DEFAULT"][u"ANNOTATION"],         u"spec": u"face:Consolas,size:9,fore:#000000,back:#E0E0E0"}, # 253
        u"TEXTMARGIN":         {u"styleNum": STC_STYLE_INDICES[u"DEFAULT"][u"TEXTMARGIN"],         u"spec": u"face:Consolas,size:9,italic,fore:#222222,back:#E0E0E0"}, # 254
    }, # NONE
    u"INPUT": {
        # [1] RESERVED STYLES:
        u"STC_DEFAULT":        {u"styleNum": STC_STYLE_INDICES[u"INPUT"][u"STC_DEFAULT"],        u"spec": u"face:Consolas,size:9,fore:#0099FF,back:#000099"}, # 32
        u"STC_LINENUMBER":     {u"styleNum": STC_STYLE_INDICES[u"INPUT"][u"STC_LINENUMBER"],     u"spec": u"face:Consolas,size:8,fore:#0055EE,back:#0022DD"}, # 33
        u"STC_BRACELIGHT":     {u"styleNum": STC_STYLE_INDICES[u"INPUT"][u"STC_BRACELIGHT"],     u"spec": u"face:Consolas,size:9,fore:#0099FF,back:#000099"}, # 34
        u"STC_BRACEBAD":       {u"styleNum": STC_STYLE_INDICES[u"INPUT"][u"STC_BRACEBAD"],       u"spec": u"face:Consolas,size:9,fore:#0099FF,back:#000099"}, # 35
        u"STC_CONTROLCHAR":    {u"styleNum": STC_STYLE_INDICES[u"INPUT"][u"STC_CONTROLCHAR"],    u"spec": u"face:Consolas,size:9"}, # 36
        u"STC_INDENTGUIDE":    {u"styleNum": STC_STYLE_INDICES[u"INPUT"][u"STC_INDENTGUIDE"],    u"spec": u"face:Consolas,size:9,fore:#0099FF,back:#000099"}, # 37
        u"STC_CALLTIP":        {u"styleNum": STC_STYLE_INDICES[u"INPUT"][u"STC_CALLTIP"],        u"spec": u"face:Consolas,size:9,fore:#000099,back:#FFFFFF"}, # 38
        u"STC_LASTPREDEFINED": {u"styleNum": STC_STYLE_INDICES[u"INPUT"][u"STC_LASTPREDEFINED"], u"spec": u"face:Consolas,size:9,fore:#0099FF,back:#000099"}, # 39
        # [2] CUSTOM STYLES:
        u"DEFAULT":            {u"styleNum": STC_STYLE_INDICES[u"INPUT"][u"DEFAULT"],            u"spec": u"face:Consolas,size:9,fore:#FFFFFF,back:#000099"}, # 0
        u"FROZEN":             {u"styleNum": STC_STYLE_INDICES[u"INPUT"][u"FROZEN"],             u"spec": u"face:Consolas,size:9,fore:#0055EE,back:#000099"}, # 1
        # ...
        u"ANNOTATION":         {u"styleNum": STC_STYLE_INDICES[u"INPUT"][u"ANNOTATION"],         u"spec": u"face:Consolas,size:9,fore:#000000,back:#FFFF00"}, # 253
        u"TEXTMARGIN":         {u"styleNum": STC_STYLE_INDICES[u"INPUT"][u"TEXTMARGIN"],         u"spec": u"face:Consolas,size:9,italic,fore:#FFFFFF,back:#0022DD"}, # 254
    }, # INPUT
    u"OUTPUT": {
        # [1] RESERVED STYLES:
        u"STC_DEFAULT":        {u"styleNum": STC_STYLE_INDICES[u"INPUT"][u"STC_DEFAULT"],        u"spec": u"face:Consolas,size:9,fore:#777777,back:#FFFFFF"}, # 32
        u"STC_LINENUMBER":     {u"styleNum": STC_STYLE_INDICES[u"INPUT"][u"STC_LINENUMBER"],     u"spec": u"face:Consolas,size:8,fore:#777777,back:#E0E0E0"}, # 33
        u"STC_BRACELIGHT":     {u"styleNum": STC_STYLE_INDICES[u"INPUT"][u"STC_BRACELIGHT"],     u"spec": u"face:Consolas,size:9,fore:#777777,back:#E0E0E0"}, # 34
        u"STC_BRACEBAD":       {u"styleNum": STC_STYLE_INDICES[u"INPUT"][u"STC_BRACEBAD"],       u"spec": u"face:Consolas,size:9,fore:#777777,back:#E0E0E0"}, # 35
        u"STC_CONTROLCHAR":    {u"styleNum": STC_STYLE_INDICES[u"INPUT"][u"STC_CONTROLCHAR"],    u"spec": u"face:Consolas,size:9"}, # 36
        u"STC_INDENTGUIDE":    {u"styleNum": STC_STYLE_INDICES[u"INPUT"][u"STC_INDENTGUIDE"],    u"spec": u"face:Consolas,size:9,fore:#A0A0A0,back:#FFFFFF"}, # 37
        u"STC_CALLTIP":        {u"styleNum": STC_STYLE_INDICES[u"INPUT"][u"STC_CALLTIP"],        u"spec": u"face:Consolas,size:9,fore:#FFFFFF,back:#000077"}, # 38
        u"STC_LASTPREDEFINED": {u"styleNum": STC_STYLE_INDICES[u"INPUT"][u"STC_LASTPREDEFINED"], u"spec": u"face:Consolas,size:9,fore:#BF004F,back:#FFFFFF"}, # 39
        # [2] CUSTOM STYLES:
        u"DEFAULT":            {u"styleNum": STC_STYLE_INDICES[u"INPUT"][u"DEFAULT"],            u"spec": u"face:Consolas,size:9,fore:#000077,back:#FFFFFF"}, # 0
        u"FROZEN":             {u"styleNum": STC_STYLE_INDICES[u"INPUT"][u"FROZEN"],             u"spec": u"face:Consolas,size:9,fore:#A0A0A0,back:#FFFFFF"}, # 1
        # ...
        u"ANNOTATION":         {u"styleNum": STC_STYLE_INDICES[u"INPUT"][u"ANNOTATION"],         u"spec": u"face:Consolas,size:9,fore:#000099,back:#FFFF22"}, # 253
        u"TEXTMARGIN":         {u"styleNum": STC_STYLE_INDICES[u"INPUT"][u"TEXTMARGIN"],         u"spec": u"face:Consolas,size:9,italic,fore:#222222,back:#E0E0E0"}, # 254
    }, # OUTPUT
    u"TABLE": {
        # [1] RESERVED STYLES:
        u"STC_DEFAULT":        {u"styleNum": STC_STYLE_INDICES[u"TABLE"][u"STC_DEFAULT"],        u"spec": u"face:Consolas,size:10,fore:#777777,back:#FFFFFF"}, # 32
        u"STC_LINENUMBER":     {u"styleNum": STC_STYLE_INDICES[u"TABLE"][u"STC_LINENUMBER"],     u"spec": u"face:Consolas,size:9,fore:#999999,back:#E0E0E0"}, # 33
        u"STC_BRACELIGHT":     {u"styleNum": STC_STYLE_INDICES[u"TABLE"][u"STC_BRACELIGHT"],     u"spec": u"face:Consolas,size:10,fore:#777777,back:#E0E0E0"}, # 34
        u"STC_BRACEBAD":       {u"styleNum": STC_STYLE_INDICES[u"TABLE"][u"STC_BRACEBAD"],       u"spec": u"face:Consolas,size:10,fore:#777777,back:#E0E0E0"}, # 35
        u"STC_CONTROLCHAR":    {u"styleNum": STC_STYLE_INDICES[u"TABLE"][u"STC_CONTROLCHAR"],    u"spec": u"face:Consolas,size:10"}, # 36
        u"STC_INDENTGUIDE":    {u"styleNum": STC_STYLE_INDICES[u"TABLE"][u"STC_INDENTGUIDE"],    u"spec": u"face:Consolas,size:10,fore:#A0A0A0,back:#FFFFFF"}, # 37
        u"STC_CALLTIP":        {u"styleNum": STC_STYLE_INDICES[u"TABLE"][u"STC_CALLTIP"],        u"spec": u"face:Consolas,size:10,fore:#FFFFFF,back:#000077"}, # 38
        u"STC_LASTPREDEFINED": {u"styleNum": STC_STYLE_INDICES[u"TABLE"][u"STC_LASTPREDEFINED"], u"spec": u"face:Consolas,size:10,fore:#BF004F,back:#FFFFFF"}, # 39
        # [2] CUSTOM STYLES:
        u"DEFAULT":            {u"styleNum": STC_STYLE_INDICES[u"TABLE"][u"DEFAULT"],            u"spec": u"face:Consolas,size:10,bold,fore:#000077,back:#FFFFFF"}, # 0
        u"COMMENT":            {u"styleNum": STC_STYLE_INDICES[u"TABLE"][u"COMMENT"],            u"spec": u"face:Consolas,size:9,fore:#999999,back:#FFFFFF"}, # 1
        # ...
        u"ANNOTATION":         {u"styleNum": STC_STYLE_INDICES[u"TABLE"][u"ANNOTATION"],         u"spec": u"face:Consolas,size:10,fore:#000099,back:#FFFF22"}, # 253
        u"TEXTMARGIN":         {u"styleNum": STC_STYLE_INDICES[u"TABLE"][u"TEXTMARGIN"],         u"spec": u"face:Consolas,size:10,italic,fore:#222222,back:#E0E0E0"}, # 254
    }, # TABLE
    # ...
}; # STC_STYLE_SPECS

# ------------------------------------------------------------------------------

STC_INDICATOR_STYLE = {
    # -- LEXER INDICATOR STYLES (0-7) [1]:
    u"PLAIN":        0, # = stc.STC_INDIC_PLAIN [1.1]
    u"SQUIGGLE":     1, # = stc.STC_INDIC_SQUIGGLE [1.2]
    u"TT":           2, # = stc.STC_INDIC_TT [1.3]
    u"DIAGONAL":     3, # = stc.STC_INDIC_DIAGONAL [1.4]
    u"STRIKE":       4, # = stc.STC_INDIC_STRIKE [1.5]
    u"HIDDEN":       5, # = stc.STC_INDIC_HIDDEN [1.6]
    u"BOX":          6, # = stc.STC_INDIC_BOX [1.7]
    u"ROUNDBOX":     7, # = stc.STC_INDIC_ROUNDBOX [1.8]
    # -- CONTAINER INDICATOR STYLES (8-31) [2]:
    u"STRAIGHTBOX":  8, # = stc.STC_INDIC_STRAIGHTBOX [2.1]
    u"DASH":         9, # = stc.STC_INDIC_DASH [2.2]
    u"DOTS":        10, # = stc.STC_INDIC_DOTS [2.3]
    u"SQUIGGLELOW": 11, # = stc.STC_INDIC_SQUIGGLELOW [2.4]
    u"DOTBOX":      12, # = stc.STC_INDIC_DOTBOX [2.5]
    # ...
    u"MAX":         31, # = stc.STC_INDIC_MAX [2.23]
}; # STC_INDICATOR_STYLE

STC_INDICATOR_INDEX = {
    # -- INDICATOR INDICES:
    u"DEFAULT":   0, # [1] -- The first one of the (only three) indicators
    u"FILE":      1, # [2] -- The second one of the (only three) indicators
    u"UNDEFINED": 2, # [3] -- The third one of the (only three) indicators
}; # STC_INDICATOR_INDEX

STC_INDICATOR_MASK = {
    # -- INDICATOR MASK BITS:
    # 00100000 u"DEFAULT"   [1] -- Selects the first indicator.
    # 01000000 u"FILE"      [2] -- Selects the second indicator.
    # 10000000 u"UNDEFINED" [3] -- Selects the third indicator.
    u"DEFAULT":   0x20, # = 32  (= 2**5) = 0b100000   (= 0b1 << 0b101 = 0b10 << 0b100) = stc.STC_INDIC0_MASK [1]
    u"FILE":      0x40, # = 64  (= 2**6) = 0b1000000  (= 0b1 << 0b110 = 0b10 << 0b101) = stc.STC_INDIC1_MASK [2]
    u"UNDEFINED": 0x80, # = 128 (= 2**7) = 0b10000000 (= 0b1 << 0b111 = 0b10 << 0b110) = stc.STC_INDIC2_MASK [3]
}; # STC_INDICATOR_MASK

STC_INDICATOR_COLOUR = {
    # -- INDICATOR COLOURS:
    u"DEFAULT":   u"#FF0000",
    u"FILE":      u"#000077",
    u"UNDEFINED": u"#00FF00",
}; # STC_INDICATOR_COLOUR

# ------------------------------------------------------------------------------

STC_MARKER_SYMBOL = {
    u"CIRCLE":                0, # = stc.STC_MARK_CIRCLE [1]
    u"ROUNDRECT":             1, # = stc.STC_MARK_ROUNDRECT [2]
    u"ARROW":                 2, # = stc.STC_MARK_ARROW [3]
    u"SMALLRECT":             3, # = stc.STC_MARK_SMALLRECT [4]
    u"SHORTARROW":            4, # = stc.STC_MARK_SHORTARROW [5]
    u"EMPTY":                 5, # = stc.STC_MARK_EMPTY [6]
    u"ARROWDOWN":             6, # = stc.STC_MARK_ARROWDOWN [7]
    u"MINUS":                 7, # = stc.STC_MARK_MINUS [8]
    u"PLUS":                  8, # = stc.STC_MARK_PLUS [9]
    u"VLINE":                 9, # = stc.STC_MARK_VLINE [10]
    u"LCORNER":              10, # = stc.STC_MARK_LCORNER [11]
    u"TCORNER":              11, # = stc.STC_MARK_TCORNER [12]
    u"BOXPLUS":              12, # = stc.STC_MARK_BOXPLUS [13]
    u"BOXPLUSCONNECTED":     13, # = stc.STC_MARK_BOXPLUSCONNECTED [14]
    u"BOXMINUS":             14, # = stc.STC_MARK_BOXMINUS [15]
    u"BOXMINUSCONNECTED":    15, # = stc.STC_MARK_BOXMINUSCONNECTED [16]
    u"LCORNERCURVE":         16, # = stc.STC_MARK_LCORNERCURVE [17]
    u"TCORNERCURVE":         17, # = stc.STC_MARK_TCORNERCURVE [18]
    u"CIRCLEPLUS":           18, # = stc.STC_MARK_CIRCLEPLUS [19]
    u"CIRCLEPLUSCONNECTED":  19, # = stc.STC_MARK_CIRCLEPLUSCONNECTED [20]
    u"CIRCLEMINUS":          20, # = stc.STC_MARK_CIRCLEMINUS [21]
    u"CIRCLEMINUSCONNECTED": 21, # = stc.STC_MARK_CIRCLEMINUSCONNECTED [22]
    u"BACKGROUND":           22, # = stc.STC_MARK_BACKGROUND [23]
    u"DOTDOT":               23, # = stc.STC_MARK_DOTDOTDOT [24]
    u"ARROWS":               24, # = stc.STC_MARK_ARROWS [25]
    u"PIXMAP":               25, # = stc.STC_MARK_PIXMAP [26]
    u"FULLRECT":             26, # = stc.STC_MARK_FULLRECT [27]
    u"LEFTRECT":             27, # = stc.STC_MARK_LEFTRECT [28]
    u"AVAILABLE":            28, # = stc.STC_MARK_AVAILABLE [29]
    u"UNDERLINE":            29, # = stc.STC_MARK_UNDERLINE [30]
    u"RGBAIMAGE":            30, # = stc.STC_MARK_RGBAIMAGE [31]
}; # STC_MARKER_SYMBOL

STC_MARKER_NUMBER = {
    # (TOTAL 32 MARKER INDICES)
    # -- CUSTOM MARKER INDICES [1]:
    u"TEXT":          0, # (marker mask: 0b00001) [1.1]
    u"CURRENT_LINE":   1, # (marker mask: 0b00010) [1.2]
    # ...
    # -- FOLDING MARKER INDICES [2]:
    u"FOLD_END":      25, # = stc.STC_MARKNUM_FOLDEREND     (marker mask: 0b11001) [2.1]
    u"FOLD_OPEN_MID": 26, # = stc.STC_MARKNUM_FOLDEROPENMID (marker mask: 0b11010) [2.2]
    u"FOLD_MID_TAIL": 27, # = stc.STC_MARKNUM_FOLDERMIDTAIL (marker mask: 0b11011) [2.3]
    u"FOLD_TAIL":     28, # = stc.STC_MARKNUM_FOLDERTAIL    (marker mask: 0b11100) [2.4]
    u"FOLD_SUB":      29, # = stc.STC_MARKNUM_FOLDERSUB     (marker mask: 0b11101) [2.5]
    u"FOLD":          30, # = stc.STC_MARKNUM_FOLDER        (marker mask: 0b11110) [2.6]
    u"FOLD_OPEN":     31, # = stc.STC_MARKNUM_FOLDEROPEN    (marker mask: 0b11111) [2.7]
    # ...
}; # STC_MARKER_NUMBER

STC_MARKER_MASK = {
    # -- CUSTOM MARKER MASKS [1]:
    u"TEXT":          0b00001, # (marker index: 0) [1.1]
    u"CURRENT_LINE":   0b00010, # (marker index: 1) [1.2]
    # ...
    # -- FOLDING MARKER MASKS [2]:
    u"FOLD_END":      0b11001, # (marker index: 25) [2.1]
    u"FOLD_OPEN_MID": 0b11010, # (marker index: 26) [2.2]
    u"FOLD_MID_TAIL": 0b11011, # (marker index: 27) [2.3]
    u"FOLD_TAIL":     0b11100, # (marker index: 28) [2.4]
    u"FOLD_SUB":      0b11101, # (marker index: 29) [2.5]
    u"FOLD":          0b11110, # (marker index: 30) [2.6]
    u"FOLD_OPEN":     0b11111, # (marker index: 31) [2.7]
}; # STC_MARKER_MASK

# ------------------------------------------------------------------------------

STC_ANNOTATION_INDEX = {
    u"HIDDEN":   0, # = stc.STC_ANNOTATION_HIDDEN
    u"STANDARD": 1, # = stc.STC_ANNOTATION_STANDARD
    u"BOXED":    2, # = stc.STC_ANNOTATION_BOXED
}; # STC_ANNOTATION_INDEX

# ------------------------------------------------------------------------------

STC_WRAP_MODE = {
    # -- STC WRAP MODES:
    u"NONE": 0, # = stc.STC_WRAP_NONE [1]
    u"WORD": 1, # = stc.STC_WRAP_WORD [2]
    u"CHAR": 2, # = stc.STC_WRAP_CHAR [3]
}; # STC_WRAP_MODE
STC_WRAP_NAME = dict((mode,name) for (name,mode) in STC_WRAP_MODE.iteritems()); # i.e. STC WRAP MODE NAMES

STC_WRAP_FLAG = {
    # -- WRAP FLAGS:
    u"NONE":   0b000, # = 0 = stc.STC_WRAPVISUALFLAG_NONE   [1]
    u"END":    0b001, # = 1 = stc.STC_WRAPVISUALFLAG_END    [2]
    u"START":  0b010, # = 2 = stc.STC_WRAPVISUALFLAG_START  [3]
    u"MARGIN": 0b100, # = 4 = stc.STC_WRAPVISUALFLAG_MARGIN [4]
}; # STC_WRAP_FLAG

STC_WRAP_LOC = {
    # -- WRAP FLAG LOCATIONS:
    u"DEFAULT":    0, # = stc.STC_WRAPVISUALFLAGLOC_DEFAULT       [1]
    u"TEXT_END":   1, # = stc.STC_WRAPVISUALFLAGLOC_END_BY_TEXT   [2]
    u"TEXT_START": 2, # = stc.STC_WRAPVISUALFLAGLOC_START_BY_TEXT [3]
}; # STC_WRAP_LOC

STC_WRAP_INDENT_MODE = {
    u"FIXED":  0, # = stc.STC_WRAPINDENT_FIXED  [1]
    u"SAME":   1, # = stc.STC_WRAPINDENT_SAME   [2]
    u"INDENT": 2, # = stc.STC_WRAPINDENT_INDENT [3]
};
# ------------------------------------------------------------------------------

STC_SELECTION_TYPE = {
    # -- SELECTION TYPES:
    u"STREAM":    0, # stc.STC_SEL_STREAM    [1]
    u"RECTANGLE": 1, # stc.STC_SEL_RECTANGLE [2]
    u"LINES":     2, # stc.STC_SEL_LINES     [3]
    u"THIN":      3, # stc.STC_SEL_THIN      [4]
}; # STC_SELECTION_TYPE

STC_POLICY = {
    # -- CARET POLICIES [1]:
    # 00001 u"CARET_SLOP"   [1.1]
    # 00100 u"CARET_STRICT" [1.2]
    # 01000 u"CARET_EVEN"   [1.3]
    # 10000 u"CARET_JUMPS"  [1.4]
    u"CARET_SLOP":   0x1,  # = 1  (= 2**0) = 0b1     (= 0b1 << 0b0                 ) = stc.STC_CARET_SLOP   [1.1]
    u"CARET_STRICT": 0x4,  # = 4  (= 2**2) = 0b100   (= 0b1 << 0b10  = 0b10 << 0b1 ) = stc.STC_CARET_STRICT [1.2]
    u"CARET_EVEN":   0x8,  # = 8  (= 2**3) = 0b1000  (= 0b1 << 0b11  = 0b10 << 0b10) = stc.STC_CARET_EVEN   [1.3]
    u"CARET_JUMPS":  0x10, # = 16 (= 2**4) = 0b10000 (= 0b1 << 0b100 = 0b10 << 0b11) = stc.STC_CARET_JUMPS  [1.4]
    # -- LINE VISIBILITY POLICIES [2]:
    # 001 LINE_SLOP [2.1]
    # 100 LINE_STRICT [2.2]
    u"LINE_SLOP":    0x1,  # = 1 (= 2**0) = 0b1   (= 0b1 << 0b0               ) = stc.STC_VISIBLE_SLOP   [2.1]
    u"LINE_STRICT":  0x4,  # = 4 (= 2**2) = 0b100 (= 0b1 << 0b10 = 0b10 << 0b1) = stc.STC_VISIBLE_STRICT [2.2]
}; # STC_POLICY

STC_CACHE_TYPE = {
    # -- CACHE TYPES:
    u"NONE":     0, # = stc.STC_CACHE_NONE     [1]
    u"CARET":    1, # = stc.STC_CACHE_CARET    [2]
    u"PAGE":     2, # = stc.STC_CACHE_PAGE     [3]
    u"DOCUMENT": 3, # = stc.STC_CACHE_DOCUMENT [4]
}; # STC_CACHE_TYPE

# ------------------------------------------------------------------------------

STC_KEY_MODIFIER = {
    # -- KEY MODIFIERS:
    # 001 u"SHIFT"
    # 010 u"CONTROL"
    # 100 u"ALT"
    u"SHIFT":   0b1,   # (= 0b1 << 0b0)  = 0x1 = 1 (= 2**0)
    u"CONTROL": 0b10,  # (= 0b1 << 0b1)  = 0x2 = 2 (= 2**1)
    u"ALT":     0b100, # (= 0b1 << 0b10) = 0x4 = 4 (= 2**2)
}; # STC_KEY_MODIFIER

# ------------------------------------------------------------------------------

STC_LINE_STATE = {
    u"DEFAULT":   0b00,
    u"MATCHED":   0b01,
    u"INDICATED": 0b10,
    # ...
}; # STC_LINE_STATE

# ------------------------------------------------------------------------------

# MISC STC LEXER DATA:

STC_LEXER_PY_KEYWORDS_1 = u" ".join(keyword.kwlist);
STC_LEXER_PY_KEYWORDS_2 = u" ".join([u"self"]);

# ------------------------------------------------------------------------------

class STC_GET (object):
    u""" ... """
    def __get__ (self, INSTANCE, CLASS=None):
        return (None);
    def __set__ (self, INSTANCE, arg):
        raise AttributeError;

class STC_GET_STYLE_SPECS (STC_GET):
    u""" GET THE CORRESPONDING STC STYLE SPECIFICATION DATA DICT """
    def __get__ (self, INSTANCE, CLASS=None):
        style_specs = STC_STYLE_SPECS[INSTANCE.name];
        return (style_specs);

class STC_GET_STYLE_NAMES (STC_GET):
    u""" GET THE CORRESPONDING STC STYLE NAMES DICT """
    def __get__ (self, INSTANCE, CLASS=None):
        style_names = STC_STYLE_NAMES[INSTANCE.name];
        return (style_names);

class STC_GET_STYLE_INDICES (STC_GET):
    u""" GET THE CORRESPONDING STC STYLE INDEX DICT """
    def __get__ (self, INSTANCE, CLASS=None):
        style_indices = STC_STYLE_INDICES[INSTANCE.name];
        return (style_indices);

class STC_GET_STYLE_COLOURS (STC_GET):
    u""" GET THE CORRESPONDING STC STYLE ADDITIONAL COLOURS DICT """
    def __get__ (self, INSTANCE, CLASS=None):
        style_colours = STC_STYLE_COLOURS[INSTANCE.name];
        return (style_colours);
    
class STC_STYLE (object):
    u""" A STC STYLE DATA OBJECT """

    # THE CLASS DESCRIPTORS:
    specs   = STC_GET_STYLE_SPECS();   # eq. self.specs (e.g. url_stc.style.specs[u"..."], et cet.)
    names   = STC_GET_STYLE_NAMES();   # eq. self.names (e.g. url_stc.style.names[u"..."], et cet.)
    indices = STC_GET_STYLE_INDICES(); # eq. self.indices (e.g. url_stc.style.indices[u"..."], et cet.)
    colours = STC_GET_STYLE_COLOURS(); # eq. self.colours (e.g. url_stc.style.colours[u"..."], et cet.)

    def __init__ (self, name):
        u""" SET THE STC STYLE NAME """
        # ----------------------------
        self.name = name; # i.e. set a style name...
        # ----------------------------

    def __call__ (self, name):
        u""" RE-SET THE STC STYLE NAME """
        # ----------------------------
        self.name = name; # i.e. re-set a style name...
        # ----------------------------

# ------------------------------------------------------------------------------

# ...

# ------------------------------------------------------------------------------
