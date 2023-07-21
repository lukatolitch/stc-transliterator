# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------

import re as re

from lpod.element   import odf_create_element
from lpod.style     import odf_create_style

from lpod.document  import odf_new_document, odf_get_document
from lpod.heading   import odf_create_heading
from lpod.paragraph import odf_create_paragraph
from lpod.span      import odf_create_span
from lpod.list      import odf_create_list, odf_create_list_item
from lpod.image     import odf_create_image
from lpod.frame     import odf_create_frame, odf_create_image_frame

import pprint
PPRINTER = pprint.PrettyPrinter(indent=1, width=80);

# ------------------------------------------------------------------------------

Bookmarker_FONTS = {
    # u"ARIAL":    odf_create_element(u"<style:font-face style:name=\"Font_Arial\" svg:font-family=\"Arial\"/>"),
    # u"TIMES":    odf_create_element(u"<style:font-face style:name=\"Font_Times\" svg:font-family=\"Times New Roman\"/>"),
    # u"VERDANA":  odf_create_element(u"<style:font-face style:name=\"Font_Verdana\" svg:font-family=\"Verdana\"/>"),
    # u"GEORGIA":  odf_create_element(u"<style:font-face style:name=\"Font_Georgia\" svg:font-family=\"Georgia\"/>"),
    u"CONSOLAS": odf_create_element(u"<style:font-face style:name=\"Font_Consolas\" svg:font-family=\"Consolas\"/>"),
};

Bookmarker_Styles_TEXT = {
    u"DEFAULT":      odf_create_style(u"text", parent=u"Default", name=u"Bookmarker_Text_DEFAULT",      display_name=u"Bookmarker_Text_DEFAULT",      style=u"normal"), # the "style" argument needs to be set here...
    u"COMMENT":      odf_create_style(u"text", parent=u"Default", name=u"Bookmarker_Text_COMMENT",      display_name=u"Bookmarker_Text_COMMENT",      style=u"normal"),
    u"BOOKMARK":     odf_create_style(u"text", parent=u"Default", name=u"Bookmarker_Text_BOOKMARK",     display_name=u"Bookmarker_Text_BOOKMARK",     style=u"normal"),
    u"GUID":         odf_create_style(u"text", parent=u"Default", name=u"Bookmarker_Text_GUID",         display_name=u"Bookmarker_Text_GUID",         style=u"normal"),
    u"ID":           odf_create_style(u"text", parent=u"Default", name=u"Bookmarker_Text_ID",           display_name=u"Bookmarker_Text_ID",           style=u"normal"),
    u"INDEX":        odf_create_style(u"text", parent=u"Default", name=u"Bookmarker_Text_INDEX",        display_name=u"Bookmarker_Text_INDEX",        style=u"normal"),
    u"CITE":         odf_create_style(u"text", parent=u"Default", name=u"Bookmarker_Text_CITE",         display_name=u"Bookmarker_Text_CITE",         style=u"normal"),
    u"URL":          odf_create_style(u"text", parent=u"Default", name=u"Bookmarker_Text_URL",          display_name=u"Bookmarker_Text_URL",          style=u"normal"),
    u"SCHEME":       odf_create_style(u"text", parent=u"Default", name=u"Bookmarker_Text_SCHEME",       display_name=u"Bookmarker_Text_SCHEME",       style=u"normal"),
    u"DOMAIN":       odf_create_style(u"text", parent=u"Default", name=u"Bookmarker_Text_DOMAIN",       display_name=u"Bookmarker_Text_DOMAIN",       style=u"normal"),
    u"PATH":         odf_create_style(u"text", parent=u"Default", name=u"Bookmarker_Text_PATH",         display_name=u"Bookmarker_Text_PATH",         style=u"normal"),
    u"STEM":         odf_create_style(u"text", parent=u"Default", name=u"Bookmarker_Text_STEM",         display_name=u"Bookmarker_Text_STEM",         style=u"normal"),
    u"EXT":          odf_create_style(u"text", parent=u"Default", name=u"Bookmarker_Text_EXT",          display_name=u"Bookmarker_Text_EXT",          style=u"normal"),
    u"QUERY":        odf_create_style(u"text", parent=u"Default", name=u"Bookmarker_Text_QUERY",        display_name=u"Bookmarker_Text_QUERY",        style=u"italic"),
    u"FRAGMENT":     odf_create_style(u"text", parent=u"Default", name=u"Bookmarker_Text_FRAGMENT",     display_name=u"Bookmarker_Text_FRAGMENT",     style=u"normal"),
    u"TITLE":        odf_create_style(u"text", parent=u"Default", name=u"Bookmarker_Text_TITLE",        display_name=u"Bookmarker_Text_TITLE",        style=u"italic"),
    u"DESCRIPTIONS": odf_create_style(u"text", parent=u"Default", name=u"Bookmarker_Text_DESCRIPTIONS", display_name=u"Bookmarker_Text_DESCRIPTIONS", style=u"italic"),
    u"KEYWORD":      odf_create_style(u"text", parent=u"Default", name=u"Bookmarker_Text_KEYWORD",      display_name=u"Bookmarker_Text_KEYWORD",      style=u"normal"),
    u"TAGS":         odf_create_style(u"text", parent=u"Default", name=u"Bookmarker_Text_TAGS",         display_name=u"Bookmarker_Text_TAGS",         style=u"normal"),
    u"CHARSET":      odf_create_style(u"text", parent=u"Default", name=u"Bookmarker_Text_CHARSET",      display_name=u"Bookmarker_Text_CHARSET",      style=u"normal"),
    u"ADDED":        odf_create_style(u"text", parent=u"Default", name=u"Bookmarker_Text_ADDED",        display_name=u"Bookmarker_Text_ADDED",        style=u"normal"),
    u"MODIFIED":     odf_create_style(u"text", parent=u"Default", name=u"Bookmarker_Text_MODIFIED",     display_name=u"Bookmarker_Text_MODIFIED",     style=u"normal"),
};

Bookmarker_Styles_PARAGRAPH = {
    u"DEFAULT":       odf_create_style(u"paragraph", parent=u"Default", name=u"Bookmarker_Paragraph_DEFAULT",       display_name=u"Bookmarker_Paragraph_DEFAULT"),
    u"BOOKMARK":      odf_create_style(u"paragraph", parent=u"Default", name=u"Bookmarker_Paragraph_BOOKMARK",      display_name=u"Bookmarker_Paragraph_BOOKMARK"),
    u"BOOKMARK_ODD":  odf_create_style(u"paragraph", parent=u"Default", name=u"Bookmarker_Paragraph_BOOKMARK_ODD",  display_name=u"Bookmarker_Paragraph_BOOKMARK_ODD"),
    u"BOOKMARK_EVEN": odf_create_style(u"paragraph", parent=u"Default", name=u"Bookmarker_Paragraph_BOOKMARK_EVEN", display_name=u"Bookmarker_Paragraph_BOOKMARK_EVEN"),
    u"URL":           odf_create_style(u"paragraph", parent=u"Default", name=u"Bookmarker_Paragraph_URL",           display_name=u"Bookmarker_Paragraph_URL"),
    u"URL_ODD":       odf_create_style(u"paragraph", parent=u"Default", name=u"Bookmarker_Paragraph_URL_ODD",       display_name=u"Bookmarker_Paragraph_URL_ODD"),
    u"URL_EVEN":      odf_create_style(u"paragraph", parent=u"Default", name=u"Bookmarker_Paragraph_URL_EVEN",      display_name=u"Bookmarker_Paragraph_URL_EVEN"),
    u"SPACER":        odf_create_style(u"paragraph", parent=u"Default", name=u"Bookmarker_Paragraph_SPACER",        display_name=u"Bookmarker_Paragraph_SPACER"),
    u"SPACER_URL":    odf_create_style(u"paragraph", parent=u"Default", name=u"Bookmarker_Paragraph_SPACER_URL",    display_name=u"Bookmarker_Paragraph_SPACER_URL"),
    u"HEADER":        odf_create_style(u"paragraph", parent=u"Default", name=u"Bookmarker_Paragraph_HEADER",        display_name=u"Bookmarker_Paragraph_HEADER"),
    u"FOOTER":        odf_create_style(u"paragraph", parent=u"Default", name=u"Bookmarker_Paragraph_FOOTER",        display_name=u"Bookmarker_Paragraph_FOOTER"),
};

# ------------------------------------------------------------------------------

Bookmarker_Text_DEFAULT = Bookmarker_Styles_TEXT[u"DEFAULT"];
Bookmarker_Text_DEFAULT.set_properties(
    # ------------------------------
    area             = u"text", # u"paragraph", u"text"
    # ------------------------------
    font             = u"Font_Consolas",
    size             = u"7pt", # u"12pt", u"36%"
    weight           = u"normal", # u"normal", u"bold"
    # style            = u"normal", # u"normal", u"italic"
    color            = u"#000000",
    background_color = u"transparent", # u"transparent", u"#FFFFFF", ...
    underline        = u"none", # u"none", u"solid", u"dotted", u"dash", u"long_dash", u"dot_dash", u"dot_dot_dash", u"wave"
    display          = u"true", # u"none", u"true", u"condition"
    language         = u"en", # ...
    country          = u"US", # ...
    letter_spacing   = u"0.0",
    # ------------------------------
);

Bookmarker_Text_BOOKMARK = Bookmarker_Styles_TEXT[u"BOOKMARK"];
Bookmarker_Text_BOOKMARK.set_properties(
    # ------------------------------
    area             = u"text", # u"paragraph", u"text"
    # ------------------------------
    font             = u"Font_Consolas",
    size             = u"7pt", # u"12pt", u"36%"
    weight           = u"bold", # u"normal", u"bold"
    # style            = u"normal", # u"normal", u"italic"
    color            = u"#000000",
    background_color = u"transparent", # u"transparent", u"#FFFFFF", ...
    underline        = u"none", # u"none", u"solid", u"dotted", u"dash", u"long_dash", u"dot_dash", u"dot_dot_dash", u"wave"
    display          = u"true", # u"none", u"true", u"condition"
    language         = u"en", # ...
    country          = u"US", # ...
    letter_spacing   = u"0.0",
    # ------------------------------
);

Bookmarker_Text_CITE = Bookmarker_Styles_TEXT[u"CITE"];
Bookmarker_Text_CITE.set_properties(
    # ------------------------------
    area             = u"text", # u"paragraph", u"text"
    # ------------------------------
    font             = u"Font_Consolas",
    size             = u"7pt", # u"12pt", u"36%"
    weight           = u"bold", # u"normal", u"bold"
    # style            = u"normal", # u"normal", u"italic"
    color            = u"#000000",
    background_color = u"#D0D0D0", # u"transparent", u"#FFFFFF", ...
    underline        = u"none", # u"none", u"solid", u"dotted", u"dash", u"long_dash", u"dot_dash", u"dot_dot_dash", u"wave"
    display          = u"true", # u"none", u"true", u"condition"
    language         = u"en", # ...
    country          = u"US", # ...
    letter_spacing   = u"0.0",
    # ------------------------------
);

Bookmarker_Text_TITLE = Bookmarker_Styles_TEXT[u"TITLE"];
Bookmarker_Text_TITLE.set_properties(
    # ------------------------------
    area             = u"text", # u"paragraph", u"text"
    # ------------------------------
    font             = u"Font_Consolas",
    size             = u"7pt", # u"12pt", u"36%"
    weight           = u"normal", # u"normal", u"bold"
    # style            = u"italic", # u"normal", u"italic", u"oblique"
    color            = u"#000000",
    background_color = u"transparent", # u"transparent", u"#FFFFFF", ...
    underline        = u"none", # u"none", u"solid", u"dotted", u"dash", u"long_dash", u"dot_dash", u"dot_dot_dash", u"wave"
    display          = u"true", # u"none", u"true", u"condition"
    language         = u"en", # ...
    country          = u"US", # ...
    letter_spacing   = u"0.0",
    # ------------------------------
);

Bookmarker_Text_URL = Bookmarker_Styles_TEXT[u"URL"];
Bookmarker_Text_URL.set_properties(
    # ------------------------------
    area             = u"text", # u"paragraph", u"text"
    # ------------------------------
    font             = u"Font_Consolas",
    size             = u"7pt", # u"12pt", u"36%"
    weight           = u"bold", # u"normal", u"bold"
    # style            = u"normal", # u"normal", u"italic"
    color            = u"#000000",
    background_color = u"#FFFF00", # u"transparent", u"#FFFFFF", ...
    underline        = u"none", # u"none", u"solid", u"dotted", u"dash", u"long_dash", u"dot_dash", u"dot_dot_dash", u"wave"
    display          = u"true", # u"none", u"true", u"condition"
    language         = u"en", # ...
    country          = u"US", # ...
    letter_spacing   = u"0.0",
    # ------------------------------
);

Bookmarker_Text_SCHEME = Bookmarker_Styles_TEXT[u"SCHEME"];
Bookmarker_Text_SCHEME.set_properties(
    # ------------------------------
    area             = u"text", # u"paragraph", u"text"
    # ------------------------------
    font             = u"Font_Consolas",
    size             = u"7pt", # u"12pt", u"36%"
    weight           = u"bold", # u"normal", u"bold"
    # style            = u"normal", # u"normal", u"italic"
    color            = u"#202020",
    background_color = u"transparent", # u"transparent", u"#FFFFFF", ...
    underline        = u"none", # u"none", u"solid", u"dotted", u"dash", u"long_dash", u"dot_dash", u"dot_dot_dash", u"wave"
    display          = u"true", # u"none", u"true", u"condition"
    language         = u"en", # ...
    country          = u"US", # ...
    letter_spacing   = u"0.0",
    # ------------------------------
);

Bookmarker_Text_DOMAIN = Bookmarker_Styles_TEXT[u"DOMAIN"];
Bookmarker_Text_DOMAIN.set_properties(
    # ------------------------------
    area             = u"text", # u"paragraph", u"text"
    # ------------------------------
    font             = u"Font_Consolas",
    size             = u"7pt", # u"12pt", u"36%"
    weight           = u"bold", # u"normal", u"bold"
    # style            = u"normal", # u"normal", u"italic"
    color            = u"#000000",
    background_color = u"#FFFF00", # u"transparent", u"#FFFFFF", ...
    underline        = u"none", # u"none", u"solid", u"dotted", u"dash", u"long_dash", u"dot_dash", u"dot_dot_dash", u"wave"
    display          = u"true", # u"none", u"true", u"condition"
    language         = u"en", # ...
    country          = u"US", # ...
    letter_spacing   = u"0.0",
    # ------------------------------
);

Bookmarker_Text_PATH = Bookmarker_Styles_TEXT[u"PATH"];
Bookmarker_Text_PATH.set_properties(
    # ------------------------------
    area             = u"text", # u"paragraph", u"text"
    # ------------------------------
    font             = u"Font_Consolas",
    size             = u"7pt", # u"12pt", u"36%"
    weight           = u"normal", # u"normal", u"bold"
    # style            = u"normal", # u"normal", u"italic"
    color            = u"#000000",
    background_color = u"#DFDFDF", # u"transparent", u"#FFFFFF", ...
    underline        = u"none", # u"none", u"solid", u"dotted", u"dash", u"long_dash", u"dot_dash", u"dot_dot_dash", u"wave"
    display          = u"true", # u"none", u"true", u"condition"
    language         = u"en", # ...
    country          = u"US", # ...
    letter_spacing   = u"0.0",
    # ------------------------------
);

Bookmarker_Text_STEM = Bookmarker_Styles_TEXT[u"STEM"];
Bookmarker_Text_STEM.set_properties(
    # ------------------------------
    area             = u"text", # u"paragraph", u"text"
    # ------------------------------
    font             = u"Font_Consolas",
    size             = u"7pt", # u"12pt", u"36%"
    weight           = u"bold", # u"normal", u"bold"
    # style            = u"normal", # u"normal", u"italic"
    color            = u"#000000",
    background_color = u"#CACACA", # u"transparent", u"#FFFFFF", ...
    underline        = u"none", # u"none", u"solid", u"dotted", u"dash", u"long_dash", u"dot_dash", u"dot_dot_dash", u"wave"
    display          = u"true", # u"none", u"true", u"condition"
    language         = u"en", # ...
    country          = u"US", # ...
    letter_spacing   = u"0.0",
    # ------------------------------
);

Bookmarker_Text_EXT = Bookmarker_Styles_TEXT[u"EXT"];
Bookmarker_Text_EXT.set_properties(
    # ------------------------------
    area             = u"text", # u"paragraph", u"text"
    # ------------------------------
    font             = u"Font_Consolas",
    size             = u"7pt", # u"12pt", u"36%"
    weight           = u"bold", # u"normal", u"bold"
    # style            = u"normal", # u"normal", u"italic"
    color            = u"#000000",
    background_color = u"#CACACA", # u"transparent", u"#FFFFFF", ...
    underline        = u"none", # u"none", u"solid", u"dotted", u"dash", u"long_dash", u"dot_dash", u"dot_dot_dash", u"wave"
    display          = u"true", # u"none", u"true", u"condition"
    language         = u"en", # ...
    country          = u"US", # ...
    letter_spacing   = u"0.0",
    # ------------------------------
);

Bookmarker_Text_QUERY = Bookmarker_Styles_TEXT[u"QUERY"];
Bookmarker_Text_QUERY.set_properties(
    # ------------------------------
    area             = u"text", # u"paragraph", u"text"
    # ------------------------------
    font             = u"Font_Consolas",
    size             = u"7pt", # u"12pt", u"36%"
    weight           = u"normal", # u"normal", u"bold"
    # style            = u"normal", # u"normal", u"italic"
    color            = u"#000000",
    background_color = u"transparent", # u"transparent", u"#FFFFFF", ...
    underline        = u"none", # u"none", u"solid", u"dotted", u"dash", u"long_dash", u"dot_dash", u"dot_dot_dash", u"wave"
    display          = u"true", # u"none", u"true", u"condition"
    language         = u"en", # ...
    country          = u"US", # ...
    letter_spacing   = u"0.0",
    # ------------------------------
);

Bookmarker_Text_FRAGMENT = Bookmarker_Styles_TEXT[u"FRAGMENT"];
Bookmarker_Text_FRAGMENT.set_properties(
    # ------------------------------
    area             = u"text", # u"paragraph", u"text"
    # ------------------------------
    font             = u"Font_Consolas",
    size             = u"7pt", # u"12pt", u"36%"
    weight           = u"bold", # u"normal", u"bold"
    # style            = u"normal", # u"normal", u"italic"
    color            = u"#000000",
    background_color = u"transparent", # u"transparent", u"#FFFFFF", ...
    underline        = u"none", # u"none", u"solid", u"dotted", u"dash", u"long_dash", u"dot_dash", u"dot_dot_dash", u"wave"
    display          = u"true", # u"none", u"true", u"condition"
    language         = u"en", # ...
    country          = u"US", # ...
    letter_spacing   = u"0.0",
    # ------------------------------
);

Bookmarker_Text_COMMENT = Bookmarker_Styles_TEXT[u"COMMENT"];
Bookmarker_Text_COMMENT.set_properties(
    # ------------------------------
    area             = u"text", # u"paragraph", u"text"
    # ------------------------------
    font             = u"Font_Consolas",
    size             = u"7pt", # u"12pt", u"36%"
    weight           = u"normal", # u"normal", u"bold"
    # style            = u"normal", # u"normal", u"italic"
    color            = u"#777777",
    background_color = u"transparent", # u"transparent", u"#FFFFFF", ...
    underline        = u"none", # u"none", u"solid", u"dotted", u"dash", u"long_dash", u"dot_dash", u"dot_dot_dash", u"wave"
    display          = u"true", # u"none", u"true", u"condition"
    language         = u"en", # ...
    country          = u"US", # ...
    letter_spacing   = u"0.0",
    # ------------------------------
);

Bookmarker_Text_GUID = Bookmarker_Styles_TEXT[u"GUID"];
Bookmarker_Text_GUID.set_properties(
    # ------------------------------
    area             = u"text", # u"paragraph", u"text"
    # ------------------------------
    font             = u"Font_Consolas",
    size             = u"7pt", # u"12pt", u"36%"
    weight           = u"normal", # u"normal", u"bold"
    # style            = u"normal", # u"normal", u"italic"
    color            = u"#000000",
    background_color = u"transparent", # u"transparent", u"#FFFFFF", ...
    underline        = u"none", # u"none", u"solid", u"dotted", u"dash", u"long_dash", u"dot_dash", u"dot_dot_dash", u"wave"
    display          = u"true", # u"none", u"true", u"condition"
    language         = u"en", # ...
    country          = u"US", # ...
    letter_spacing   = u"0.0",
    # ------------------------------
);

Bookmarker_Text_ID = Bookmarker_Styles_TEXT[u"ID"];
Bookmarker_Text_ID.set_properties(
    # ------------------------------
    area             = u"text", # u"paragraph", u"text"
    # ------------------------------
    font             = u"Font_Consolas",
    size             = u"7pt", # u"12pt", u"36%"
    weight           = u"normal", # u"normal", u"bold"
    # style            = u"normal", # u"normal", u"italic"
    color            = u"#000000",
    background_color = u"transparent", # u"transparent", u"#FFFFFF", ...
    underline        = u"none", # u"none", u"solid", u"dotted", u"dash", u"long_dash", u"dot_dash", u"dot_dot_dash", u"wave"
    display          = u"true", # u"none", u"true", u"condition"
    language         = u"en", # ...
    country          = u"US", # ...
    letter_spacing   = u"0.0",
    # ------------------------------
);
Bookmarker_Text_KEYWORD = Bookmarker_Styles_TEXT[u"KEYWORD"];
Bookmarker_Text_KEYWORD.set_properties(
    # ------------------------------
    area             = u"text", # u"paragraph", u"text"
    # ------------------------------
    font             = u"Font_Consolas",
    size             = u"7pt", # u"12pt", u"36%"
    weight           = u"normal", # u"normal", u"bold"
    # style            = u"normal", # u"normal", u"italic"
    color            = u"#000000",
    background_color = u"transparent", # u"transparent", u"#FFFFFF", ...
    underline        = u"none", # u"none", u"solid", u"dotted", u"dash", u"long_dash", u"dot_dash", u"dot_dot_dash", u"wave"
    display          = u"true", # u"none", u"true", u"condition"
    language         = u"en", # ...
    country          = u"US", # ...
    letter_spacing   = u"0.0",
    # ------------------------------
);

Bookmarker_Text_TAGS = Bookmarker_Styles_TEXT[u"TAGS"];
Bookmarker_Text_TAGS.set_properties(
    # ------------------------------
    area             = u"text", # u"paragraph", u"text"
    # ------------------------------
    font             = u"Font_Consolas",
    size             = u"7pt", # u"12pt", u"36%"
    weight           = u"normal", # u"normal", u"bold"
    # style            = u"normal", # u"normal", u"italic"
    color            = u"#000000",
    background_color = u"transparent", # u"transparent", u"#FFFFFF", ...
    underline        = u"none", # u"none", u"solid", u"dotted", u"dash", u"long_dash", u"dot_dash", u"dot_dot_dash", u"wave"
    display          = u"true", # u"none", u"true", u"condition"
    language         = u"en", # ...
    country          = u"US", # ...
    letter_spacing   = u"0.0",
    # ------------------------------
);

Bookmarker_Text_CHARSET = Bookmarker_Styles_TEXT[u"CHARSET"];
Bookmarker_Text_CHARSET.set_properties(
    # ------------------------------
    area             = u"text", # u"paragraph", u"text"
    # ------------------------------
    font             = u"Font_Consolas",
    size             = u"7pt", # u"12pt", u"36%"
    weight           = u"normal", # u"normal", u"bold"
    # style            = u"normal", # u"normal", u"italic"
    color            = u"#000000",
    background_color = u"transparent", # u"transparent", u"#FFFFFF", ...
    underline        = u"none", # u"none", u"solid", u"dotted", u"dash", u"long_dash", u"dot_dash", u"dot_dot_dash", u"wave"
    display          = u"true", # u"none", u"true", u"condition"
    language         = u"en", # ...
    country          = u"US", # ...
    letter_spacing   = u"0.0",
    # ------------------------------
);

Bookmarker_Text_DESCRIPTIONS = Bookmarker_Styles_TEXT[u"DESCRIPTIONS"];
Bookmarker_Text_DESCRIPTIONS.set_properties(
    # ------------------------------
    area             = u"text", # u"paragraph", u"text"
    # ------------------------------
    font             = u"Font_Consolas",
    size             = u"7pt", # u"12pt", u"36%"
    weight           = u"normal", # u"normal", u"bold"
    # style            = u"italic", # u"normal", u"italic"
    color            = u"#000000",
    background_color = u"transparent", # u"transparent", u"#FFFFFF", ...
    underline        = u"none", # u"none", u"solid", u"dotted", u"dash", u"long_dash", u"dot_dash", u"dot_dot_dash", u"wave"
    display          = u"true", # u"none", u"true", u"condition"
    language         = u"en", # ...
    country          = u"US", # ...
    letter_spacing   = u"0.0",
    # ------------------------------
);

Bookmarker_Text_ADDED = Bookmarker_Styles_TEXT[u"ADDED"];
Bookmarker_Text_ADDED.set_properties(
    # ------------------------------
    area             = u"text", # u"paragraph", u"text"
    # ------------------------------
    font             = u"Font_Consolas",
    size             = u"7pt", # u"12pt", u"36%"
    weight           = u"normal", # u"normal", u"bold"
    # style            = u"normal", # u"normal", u"italic"
    color            = u"#000000",
    background_color = u"transparent", # u"transparent", u"#FFFFFF", ...
    underline        = u"none", # u"none", u"solid", u"dotted", u"dash", u"long_dash", u"dot_dash", u"dot_dot_dash", u"wave"
    display          = u"true", # u"none", u"true", u"condition"
    language         = u"en", # ...
    country          = u"US", # ...
    letter_spacing   = u"0.0",
    # ------------------------------
);

Bookmarker_Text_MODIFIED = Bookmarker_Styles_TEXT[u"MODIFIED"];
Bookmarker_Text_MODIFIED.set_properties(
    # ------------------------------
    area             = u"text", # u"paragraph", u"text"
    # ------------------------------
    font             = u"Font_Consolas",
    size             = u"7pt", # u"12pt", u"36%"
    weight           = u"normal", # u"normal", u"bold"
    # style            = u"normal", # u"normal", u"italic"
    color            = u"#000000",
    background_color = u"transparent", # u"transparent", u"#FFFFFF", ...
    underline        = u"none", # u"none", u"solid", u"dotted", u"dash", u"long_dash", u"dot_dash", u"dot_dot_dash", u"wave"
    display          = u"true", # u"none", u"true", u"condition"
    language         = u"en", # ...
    country          = u"US", # ...
    letter_spacing   = u"0.0",
    # ------------------------------
);

Bookmarker_Text_INDEX = Bookmarker_Styles_TEXT[u"INDEX"];
Bookmarker_Text_INDEX.set_properties(
    # ------------------------------
    area             = u"text", # u"paragraph", u"text"
    # ------------------------------
    font             = u"Font_Consolas",
    size             = u"7pt", # u"12pt", u"36%"
    weight           = u"normal", # u"normal", u"bold"
    # style            = u"normal", # u"normal", u"italic"
    color            = u"#000000",
    background_color = u"transparent", # u"transparent", u"#FFFFFF", ...
    underline        = u"none", # u"none", u"solid", u"dotted", u"dash", u"long_dash", u"dot_dash", u"dot_dot_dash", u"wave"
    display          = u"true", # u"none", u"true", u"condition"
    language         = u"en", # ...
    country          = u"US", # ...
    letter_spacing   = u"0.0",
    # ------------------------------
);

# ------------------------------------------------------------------------------

Bookmarker_Paragraph_DEFAULT = Bookmarker_Styles_PARAGRAPH[u"DEFAULT"];
Bookmarker_Paragraph_DEFAULT.set_properties(
    area             = u"paragraph",
    align            = u"left", # u"start", u"end", u"left", u"right", u"center", u"justify"
    align_last       = u"start", # u"start", u"end", u"center"
    indent           = u"0.0cm",
    margin_left      = u"0.0cm",
    margin_right     = u"0.0cm",
    margin_top       = u"0.0cm",
    margin_bottom    = u"0.25cm",
    border           = u"0.0mm none #000000",
    padding_left     = u"0.0cm",
    padding_right    = u"0.0cm",
    padding_top      = u"0.0cm",
    padding_bottom   = u"0.0cm",
    line_height      = u"0.333cm", # u"none", u"0.5cm", u"12pt", ...
    line_spacing     = u"none", # u"none", u"0.5cm", u"12pt", ...
    break_before     = u"auto", # u"auto", u"page", u"column"
    break_after      = u"auto", # u"auto", u"page", u"column"
    keep_with_next   = u"auto", # u"auto", u"allways"
    together         = u"auto", # u"auto", u"allways"
    background_color = u"transparent"
);
Bookmarker_Paragraph_DEFAULT.set_properties(
    area           = u"text", # u"paragraph", u"text"
    font           = u"Font_Consolas",
    size           = u"6pt", # u"12pt", u"36%"
    weight         = u"normal", # u"normal", u"bold"
    style          = u"normal", # u"normal", u"italic"
    color          = u"#000000",
    underline      = u"none", # u"none", u"solid", u"dotted", u"dash", u"long_dash", u"dot_dash", u"dot_dot_dash", u"wave"
    display        = u"true", # u"none", u"true", u"condition"
    language       = u"en", # ...
    country        = u"US", # ...
    letter_spacing = u"0.0",
);

# ------------------------------------------------------------------------------

Bookmarker_Paragraph_BOOKMARK = Bookmarker_Styles_PARAGRAPH[u"BOOKMARK"];
Bookmarker_Paragraph_BOOKMARK.set_properties(
    area             = u"paragraph", # i.e. set the paragraph properties
    align            = u"left", # u"start", u"end", u"left", u"right", u"center", u"justify"
    align_last       = u"start", # u"start", u"end", u"center"
    indent           = u"0.0cm",
    margin_left      = u"0.0cm",
    margin_right     = u"0.0cm",
    margin_top       = u"0.0cm",
    margin_bottom    = u"0.0",
    border_top       = u"0.0mm none #FFFFFF",
    padding_left     = u"0.0cm",
    padding_right    = u"0.0cm",
    padding_top      = u"0.0cm",
    padding_bottom   = u"0.0cm",
    line_height      = u"none", # u"none", u"0.5cm", u"12pt", ...
    line_spacing     = u"none", # u"none", u"0.5cm", u"12pt", ...
    break_before     = u"auto", # u"auto", u"page", u"column"
    break_after      = u"auto", # u"auto", u"page", u"column"
    keep_with_next   = u"auto", # u"auto", u"allways"
    together         = u"auto", # u"auto", u"allways"
    background_color = u"transparent"
);
Bookmarker_Paragraph_BOOKMARK.set_properties(
    area           = u"text", # i.e. set the text properties
    font           = u"Font_Consolas",
    size           = u"6pt", # u"12pt", u"36%"
    weight         = u"normal", # u"normal", u"bold"
    style          = u"normal", # u"normal", u"italic"
    color          = u"#000000",
    underline      = u"none", # u"none", u"solid", u"dotted", u"dash", u"long_dash", u"dot_dash", u"dot_dot_dash", u"wave"
    display        = u"true", # u"none", u"true", u"condition"
    language       = u"en", # ...
    country        = u"US", # ...
    letter_spacing = u"0.0",
);

# ------------------------------------------------------------------------------

Bookmarker_Paragraph_BOOKMARK_EVEN = Bookmarker_Styles_PARAGRAPH[u"BOOKMARK_EVEN"];
Bookmarker_Paragraph_BOOKMARK_EVEN.set_properties(
    area             = u"paragraph", # i.e. set the paragraph properties
    align            = u"left", # u"start", u"end", u"left", u"right", u"center", u"justify"
    align_last       = u"start", # u"start", u"end", u"center"
    indent           = u"0.0cm",
    margin_left      = u"0.0cm",
    margin_right     = u"0.0cm",
    margin_top       = u"0.0cm",
    margin_bottom    = u"0.0",
    border           = u"0.01mm solid #FFFFFF",
    padding_left     = u"0.2cm",
    padding_right    = u"0.1cm",
    padding_top      = u"0.5cm",
    padding_bottom   = u"0.5cm",
    line_height      = u"none", # u"none", u"0.5cm", u"12pt", ...
    line_spacing     = u"none", # u"none", u"0.5cm", u"12pt", ...
    break_before     = u"auto", # u"auto", u"page", u"column"
    break_after      = u"auto", # u"auto", u"page", u"column"
    keep_with_next   = u"auto", # u"auto", u"allways"
    together         = u"auto", # u"auto", u"allways"
    background_color = u"#FFFFFF"
);
# Bookmarker_Paragraph_BOOKMARK_EVEN.set_properties(
#     area           = u"text", # i.e. set the text properties
#     font           = u"Font_Consolas",
#     size           = u"6pt", # u"12pt", u"36%"
#     weight         = u"normal", # u"normal", u"bold"
#     style          = u"normal", # u"normal", u"italic"
#     color          = u"#000000",
#     underline      = u"none", # u"none", u"solid", u"dotted", u"dash", u"long_dash", u"dot_dash", u"dot_dot_dash", u"wave"
#     display        = u"true", # u"none", u"true", u"condition"
#     language       = u"en", # ...
#     country        = u"US", # ...
#     letter_spacing = u"0.0",
# );

# ------------------------------------------------------------------------------

Bookmarker_Paragraph_BOOKMARK_ODD = Bookmarker_Styles_PARAGRAPH[u"BOOKMARK_ODD"];
Bookmarker_Paragraph_BOOKMARK_ODD.set_properties(
    area             = u"paragraph", # i.e. set the paragraph properties
    align            = u"left", # u"start", u"end", u"left", u"right", u"center", u"justify"
    align_last       = u"start", # u"start", u"end", u"center"
    indent           = u"0.0cm",
    margin_left      = u"0.0cm",
    margin_right     = u"0.0cm",
    margin_top       = u"0.0cm",
    margin_bottom    = u"0.0cm",
    border           = u"0.01mm solid #E0E0E0",
    padding_left     = u"0.2cm",
    padding_right    = u"0.1cm",
    padding_top      = u"0.4cm",
    padding_bottom   = u"0.4cm",
    line_height      = u"none", # u"none", u"0.5cm", u"12pt", ...
    line_spacing     = u"none", # u"none", u"0.5cm", u"12pt", ...
    break_before     = u"auto", # u"auto", u"page", u"column"
    break_after      = u"auto", # u"auto", u"page", u"column"
    keep_with_next   = u"auto", # u"auto", u"allways"
    together         = u"auto", # u"auto", u"allways"
    background_color = u"#E0E0E0"
);
# Bookmarker_Paragraph_BOOKMARK_ODD.set_properties(
#     area           = u"text", # i.e. set the text properties
#     font           = u"Font_Consolas",
#     size           = u"6pt", # u"12pt", u"36%"
#     weight         = u"normal", # u"normal", u"bold"
#     style          = u"normal", # u"normal", u"italic"
#     color          = u"#000000",
#     underline      = u"none", # u"none", u"solid", u"dotted", u"dash", u"long_dash", u"dot_dash", u"dot_dot_dash", u"wave"
#     display        = u"true", # u"none", u"true", u"condition"
#     language       = u"en", # ...
#     country        = u"US", # ...
#     letter_spacing = u"0.0",
# );

# ------------------------------------------------------------------------------

Bookmarker_Paragraph_URL = Bookmarker_Styles_PARAGRAPH[u"URL"];
Bookmarker_Paragraph_URL.set_properties(
    area             = u"paragraph", # i.e. set the paragraph properties
    align            = u"left", # u"start", u"end", u"left", u"right", u"center", u"justify"
    align_last       = u"start", # u"start", u"end", u"center"
    indent           = u"0.0cm",
    margin_left      = u"0.0cm",
    margin_right     = u"0.0cm",
    margin_top       = u"0.0cm",
    margin_bottom    = u"0.0",
    border_top       = u"0.05mm solid #000000",
    border_bottom    = u"0.01mm solid #FFFFFF",
    border_left      = u"0.01mm solid #FFFFFF",
    border_right     = u"0.01mm solid #FFFFFF",
    padding_left     = u"0.2cm",
    padding_right    = u"0.1cm",
    padding_top      = u"0.1cm",
    padding_bottom   = u"0.1cm",
    line_height      = u"none", # u"none", u"0.5cm", u"12pt", ...
    line_spacing     = u"none", # u"none", u"0.5cm", u"12pt", ...
    break_before     = u"auto", # u"auto", u"page", u"column"
    break_after      = u"auto", # u"auto", u"page", u"column"
    keep_with_next   = u"auto", # u"auto", u"allways"
    together         = u"auto", # u"auto", u"allways"
    background_color = u"#FFFFFF"
);
# Bookmarker_Paragraph_BOOKMARK.set_properties(
#     area           = u"text", # i.e. set the text properties
#     font           = u"Font_Consolas",
#     size           = u"6pt", # u"12pt", u"36%"
#     weight         = u"normal", # u"normal", u"bold"
#     style          = u"normal", # u"normal", u"italic"
#     color          = u"#000000",
#     underline      = u"none", # u"none", u"solid", u"dotted", u"dash", u"long_dash", u"dot_dash", u"dot_dot_dash", u"wave"
#     display        = u"true", # u"none", u"true", u"condition"
#     language       = u"en", # ...
#     country        = u"US", # ...
#     letter_spacing = u"0.0",
# );

# ------------------------------------------------------------------------------

Bookmarker_Paragraph_URL_EVEN = Bookmarker_Styles_PARAGRAPH[u"URL_EVEN"];
Bookmarker_Paragraph_URL_EVEN.set_properties(
    area             = u"paragraph", # i.e. set the paragraph properties
    align            = u"left", # u"start", u"end", u"left", u"right", u"center", u"justify"
    align_last       = u"start", # u"start", u"end", u"center"
    indent           = u"0.0cm",
    margin_left      = u"0.0cm",
    margin_right     = u"0.0cm",
    margin_top       = u"0.0cm",
    margin_bottom    = u"0.0",
    border           = u"0.01mm solid #FFFFFF",
    padding_left     = u"0.2cm",
    padding_right    = u"0.1cm",
    padding_top      = u"0.2cm",
    padding_bottom   = u"0.2cm",
    line_height      = u"none", # u"none", u"0.5cm", u"12pt", ...
    line_spacing     = u"none", # u"none", u"0.5cm", u"12pt", ...
    break_before     = u"auto", # u"auto", u"page", u"column"
    break_after      = u"auto", # u"auto", u"page", u"column"
    keep_with_next   = u"auto", # u"auto", u"allways"
    together         = u"auto", # u"auto", u"allways"
    background_color = u"#FFFFFF"
);
# Bookmarker_Paragraph_URL_EVEN.set_properties(
#     area           = u"text", # i.e. set the text properties
#     font           = u"Font_Consolas",
#     size           = u"6pt", # u"12pt", u"36%"
#     weight         = u"normal", # u"normal", u"bold"
#     style          = u"normal", # u"normal", u"italic"
#     color          = u"#000000",
#     underline      = u"none", # u"none", u"solid", u"dotted", u"dash", u"long_dash", u"dot_dash", u"dot_dot_dash", u"wave"
#     display        = u"true", # u"none", u"true", u"condition"
#     language       = u"en", # ...
#     country        = u"US", # ...
#     letter_spacing = u"0.0",
# );

# ------------------------------------------------------------------------------

Bookmarker_Paragraph_URL_ODD = Bookmarker_Styles_PARAGRAPH[u"URL_ODD"];
Bookmarker_Paragraph_URL_ODD.set_properties(
    area             = u"paragraph", # i.e. set the paragraph properties
    align            = u"left", # u"start", u"end", u"left", u"right", u"center", u"justify"
    align_last       = u"start", # u"start", u"end", u"center"
    indent           = u"0.0cm",
    margin_left      = u"0.0cm",
    margin_right     = u"0.0cm",
    margin_top       = u"0.0cm",
    margin_bottom    = u"0.0cm",
    border           = u"0.01mm solid #E0E0E0",
    padding_left     = u"0.2cm",
    padding_right    = u"0.1cm",
    padding_top      = u"0.2cm",
    padding_bottom   = u"0.2cm",
    line_height      = u"none", # u"none", u"0.5cm", u"12pt", ...
    line_spacing     = u"none", # u"none", u"0.5cm", u"12pt", ...
    break_before     = u"auto", # u"auto", u"page", u"column"
    break_after      = u"auto", # u"auto", u"page", u"column"
    keep_with_next   = u"auto", # u"auto", u"allways"
    together         = u"auto", # u"auto", u"allways"
    background_color = u"#DFDFDF"
);
# Bookmarker_Paragraph_URL_ODD.set_properties(
#     area           = u"text", # i.e. set the text properties
#     font           = u"Font_Consolas",
#     size           = u"6pt", # u"12pt", u"36%"
#     weight         = u"normal", # u"normal", u"bold"
#     style          = u"normal", # u"normal", u"italic"
#     color          = u"#000000",
#     underline      = u"none", # u"none", u"solid", u"dotted", u"dash", u"long_dash", u"dot_dash", u"dot_dot_dash", u"wave"
#     display        = u"true", # u"none", u"true", u"condition"
#     language       = u"en", # ...
#     country        = u"US", # ...
#     letter_spacing = u"0.0",
# );

# ------------------------------------------------------------------------------

Bookmarker_Paragraph_SPACER = Bookmarker_Styles_PARAGRAPH[u"SPACER"];
Bookmarker_Paragraph_SPACER.set_properties(
    area             = u"paragraph", # i.e. set the paragraph properties
    align            = u"left", # u"start", u"end", u"left", u"right", u"center", u"justify"
    align_last       = u"start", # u"start", u"end", u"center"
    indent           = u"0.0cm",
    margin_left      = u"0.0cm",
    margin_right     = u"0.0cm",
    margin_top       = u"0.01cm",
    margin_bottom    = u"0.01cm",
    border           = u"0.0mm none #000000",
    padding_left     = u"0.0cm",
    padding_right    = u"0.0cm",
    padding_top      = u"0.0cm",
    padding_bottom   = u"0.0cm",
    line_height      = u"none", # u"none", u"0.5cm", u"12pt", ...
    line_spacing     = u"none", # u"none", u"0.5cm", u"12pt", ...
    break_before     = u"auto", # u"auto", u"page", u"column"
    break_after      = u"auto", # u"auto", u"page", u"column"
    keep_with_next   = u"auto", # u"auto", u"allways"
    together         = u"auto", # u"auto", u"allways"
    background_color = u"transparent"
);
Bookmarker_Paragraph_SPACER.set_properties(
    area           = u"text", # i.e. set the text properties
    font           = u"Font_Consolas",
    size           = u"6pt", # u"12pt", u"36%"
    weight         = u"normal", # u"normal", u"bold"
    style          = u"normal", # u"normal", u"italic"
    color          = u"#000000",
    underline      = u"none", # u"none", u"solid", u"dotted", u"dash", u"long_dash", u"dot_dash", u"dot_dot_dash", u"wave"
    display        = u"true", # u"none", u"true", u"condition"
    language       = u"en", # ...
    country        = u"US", # ...
    letter_spacing = u"0.0",
);

# ------------------------------------------------------------------------------

Bookmarker_Paragraph_SPACER_URL = Bookmarker_Styles_PARAGRAPH[u"SPACER_URL"];
Bookmarker_Paragraph_SPACER_URL.set_properties(
    area             = u"paragraph", # i.e. set the paragraph properties
    align            = u"left", # u"start", u"end", u"left", u"right", u"center", u"justify"
    align_last       = u"start", # u"start", u"end", u"center"
    indent           = u"0.0cm",
    margin_left      = u"0.0cm",
    margin_right     = u"0.0cm",
    margin_top       = u"0.0cm",
    margin_bottom    = u"0.01cm",
    border           = u"0.0mm none #000000",
    padding_left     = u"0.0cm",
    padding_right    = u"0.0cm",
    padding_top      = u"0.0cm",
    padding_bottom   = u"0.0cm",
    line_height      = u"none", # u"none", u"0.5cm", u"12pt", ...
    line_spacing     = u"none", # u"none", u"0.5cm", u"12pt", ...
    break_before     = u"auto", # u"auto", u"page", u"column"
    break_after      = u"auto", # u"auto", u"page", u"column"
    keep_with_next   = u"auto", # u"auto", u"allways"
    together         = u"auto", # u"auto", u"allways"
    background_color = u"transparent"
);
Bookmarker_Paragraph_SPACER_URL.set_properties(
    area           = u"text", # i.e. set the text properties
    font           = u"Font_Consolas",
    size           = u"6pt", # u"12pt", u"36%"
    weight         = u"normal", # u"normal", u"bold"
    style          = u"normal", # u"normal", u"italic"
    color          = u"#000000",
    underline      = u"none", # u"none", u"solid", u"dotted", u"dash", u"long_dash", u"dot_dash", u"dot_dot_dash", u"wave"
    display        = u"true", # u"none", u"true", u"condition"
    language       = u"en", # ...
    country        = u"US", # ...
    letter_spacing = u"0.0",
);

# ------------------------------------------------------------------------------

Bookmarker_Paragraph_HEADER = Bookmarker_Styles_PARAGRAPH[u"HEADER"];
Bookmarker_Paragraph_HEADER.set_properties(
    area             = u"paragraph",
    align            = u"left", # u"start", u"end", u"left", u"right", u"center", u"justify"
    align_last       = u"start", # u"start", u"end", u"center"
    indent           = u"0.0cm",
    margin_left      = u"0.0cm",
    margin_right     = u"0.0cm",
    margin_top       = u"0.0cm",
    margin_bottom    = u"0.5cm",
    border           = u"0.0mm none #000000",
    padding_left     = u"0.0cm",
    padding_right    = u"0.0cm",
    padding_top      = u"0.0cm",
    padding_bottom   = u"0.0cm",
    line_height      = u"none", # u"none", u"0.5cm", u"12pt", ...
    line_spacing     = u"none", # u"none", u"0.5cm", u"12pt", ...
    break_before     = u"auto", # u"auto", u"page", u"column"
    break_after      = u"auto", # u"auto", u"page", u"column"
    keep_with_next   = u"auto", # u"auto", u"allways"
    together         = u"auto", # u"auto", u"allways"
    background_color = u"transparent"
);
Bookmarker_Paragraph_HEADER.set_properties(
    area           = u"text", # u"paragraph", u"text"
    font           = u"Font_Consolas",
    size           = u"10pt", # u"12pt", u"36%"
    weight         = u"bold", # u"normal", u"bold"
    style          = u"normal", # u"normal", u"italic"
    color          = u"#000000",
    underline      = u"none", # u"none", u"solid", u"dotted", u"dash", u"long_dash", u"dot_dash", u"dot_dot_dash", u"wave"
    display        = u"true", # u"none", u"true", u"condition"
    language       = u"en", # ...
    country        = u"US", # ...
    letter_spacing = u"0.0",
);

# ------------------------------------------------------------------------------

Bookmarker_Paragraph_FOOTER = Bookmarker_Styles_PARAGRAPH[u"FOOTER"];
Bookmarker_Paragraph_FOOTER.set_properties(
    area             = u"paragraph",
    align            = u"right", # u"start", u"end", u"left", u"right", u"center", u"justify"
    align_last       = u"start", # u"start", u"end", u"center"
    indent           = u"0.0cm",
    margin_left      = u"0.0cm",
    margin_right     = u"0.0cm",
    margin_top       = u"0.5cm",
    margin_bottom    = u"0.0cm",
    border           = u"0.0mm none #000000",
    padding_left     = u"0.0cm",
    padding_right    = u"0.0cm",
    padding_top      = u"0.0cm",
    padding_bottom   = u"0.0cm",
    line_height      = u"none", # u"none", u"0.5cm", u"12pt", ...
    line_spacing     = u"none", # u"none", u"0.5cm", u"12pt", ...
    break_before     = u"auto", # u"auto", u"page", u"column"
    break_after      = u"auto", # u"auto", u"page", u"column"
    keep_with_next   = u"auto", # u"auto", u"allways"
    together         = u"auto", # u"auto", u"allways"
    background_color = u"transparent"
);
Bookmarker_Paragraph_FOOTER.set_properties(
    area           = u"text", # u"paragraph", u"text"
    font           = u"Font_Consolas",
    size           = u"6pt", # u"12pt", u"36%"
    weight         = u"normal", # u"normal", u"bold"
    style          = u"normal", # u"normal", u"italic"
    color          = u"#666666",
    underline      = u"none", # u"none", u"solid", u"dotted", u"dash", u"long_dash", u"dot_dash", u"dot_dot_dash", u"wave"
    display        = u"true", # u"none", u"true", u"condition"
    language       = u"en", # ...
    country        = u"US", # ...
    letter_spacing = u"25.0",
);

# ------------------------------------------------------------------------------

Bookmarker_Page_LAYOUT = odf_create_style(
    u"page-layout", # style family
    name = u"Bookmarker_Layout_Default",
    # parent = u"Default",
);
Bookmarker_Page_LAYOUT.set_properties(
    # [1] PAGE PROPERTIES:
    area          = u"page-layout",
    # [2.1] PAGE SIZE PROPERTIES:
    page_width    = u"29.7cm",
    page_height   = u"21.0cm",
    # [2.2] PAGE MARGINS PROPERTIES:
    margin_top    = u"0.5cm",
    margin_bottom = u"0.5cm",
    margin_left   = u"0.5cm",
    margin_right  = u"0.5cm",
);

Bookmarker_Page_MASTER = odf_create_element(
u"""
    <style:master-page
        style:name="Default"
        style:page-layout-name="Bookmarker_Layout_Default">
        <style:footer>
            <text:p text:style-name="Bookmarker_Paragraph_FOOTER">[PAGE <text:page-number text:select-page="current"/> OF <text:page-count style:num-format="1"/>]</text:p>
        </style:footer>
    </style:master-page>
""");

# ------------------------------------------------------------------------------

ODF_MULTISPACE = re.compile(u"([\ ])+|([\t])+|([\n\r])+|([\r])+");

def GET_ACTUAL_ODF_STRING_LENGTH (string):
    u"""
        N.B. does not handle the INITIAL multiple continuous spaces...

        if multiple continuous 0x0020 (i.e. the Unicode "SPACE", i.e. " ") characters...
        if multiple continuous 0x0009 (i.e. the Unicode "TABULATION", i.e. "\t") characters...
        if multiple continuous 0x000A (i.e. the Unicode "END OF LINE, LINE FEED, NEW LINE", i.e. "\n") characters...
        if multiple continuous 0x000D (i.e. the Unicode "CARRIAGE RETURN", i.e. "\r") characters...
    """
    odf_string = ODF_MULTISPACE.sub(repl=u"\1", string=string); # i.e. collapse multiple continuous spaces to a single such space...
    odf_length = len(odf_string);
    return (odf_length);

# ------------------------------------------------------------------------------

if __name__ == u"__main__":

    # ----------------------------

    path     = r"C:\Users\User\Documents\LukaTolitch_005_PROGRAMMING\004_BOOKMARKS\Version_15\source\resources\templates\Bookmarks_Template_Kjitajskjij_2015_06_09_002.odt";
    document = odf_get_document(path_or_file=path);
    body     = document.get_body();

    # ----------------------------

    print u"\n\n-- DOCUMENT \"TYPE\":";
    print document.get_type(); # i.e. u"text" is an ".odt" document, et cet.

    print u"\n\n-- DOCUMENT \"META\":";
    print document.get_formated_meta();

    print u"\n\n-- DOCUMENT \"PARTS\":";
    parts = document.get_parts();
    for (index, part) in enumerate(parts):
        if (part != None):
            print u"\t\"{0:s}\"".format(part);

    print u"\n\n-- DOCUMENT \"GET\" METHODS:"
    get_attrs = [attr for attr in dir(document) if attr.startswith(u"get_")];
    for (index, get_attr) in enumerate(get_attrs):
        print u"\t[{0:03d}] .{1:s}(...)".format(index, get_attr);

    print u"\n\n-- DOCUMENT \"SET\" METHODS:"
    set_attrs = [attr for attr in dir(document) if attr.startswith(u"set_")];
    for (index, set_attr) in enumerate(set_attrs):
        print u"\t[{0:03d}] .{1:s}(...)".format(index, set_attr);

    print u"\n\n-- DOCUMENT \"TEXT STYLES\":";
    styles = document.get_styles(family=u"text");
    for (index, style) in enumerate(styles):
        # ----------------------------
        name         = style.get_name();
        display_name = style.get_display_name();
        print u"\t[{0:d}] \"{1:s}\" (\"{2:s}\"):".format(index, name, display_name);
        # ----------------------------
        properties = style.get_properties(area=u"text");
        if (properties != None):
            for (key,value) in sorted(properties.items()):
                print u"\t\t{2:{0:s}<{1:d}s}{3:s}".format(u" ", 24, u"\"{0:s}\":".format(key), value);
            # for (key,value)
        # ----------------------------
    # for (index, style)

    print u"\n\n-- DOCUMENT \"PARAGRAPH STYLES\":";
    styles = document.get_styles(family=u"paragraph");
    for (index, style) in enumerate(styles):
        # ----------------------------
        name         = style.get_name();
        display_name = style.get_display_name();
        print u"\t[{0:d}] \"{1:s}\" (\"{2:s}\"):".format(index, name, display_name);
        # ----------------------------
        properties = style.get_properties(area=u"paragraph");
        if (properties != None):
            for (key,value) in sorted(properties.items()):
                print u"\t\t{2:{0:s}<{1:d}s}{3:s}".format(u" ", 24, u"\"{0:s}\":".format(key), value);
            # for (key,value)
        # ----------------------------
    # for (index, style)

    # ----------------------------

    print u"\n\n-- BODY \"IMAGES\":";
    images = body.get_images();
    for (index, image) in enumerate(images):
        if (image != None):
            print u"\tImage: \"{0:s}\":".format(image);
            print u"\t\tImage URL:  \"{0:s}\"".format(image.get_url());

    # ----------------------------

    document.get_style()