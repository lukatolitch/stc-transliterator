# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------

import os as os
import wx as wx

# ------------------------------------------------------------------------------

class WX_GLOBALS (object):
    u""" ... """

    def _init__ (self):
        # ----------------------------
        # [1] WX WINDOWS:
        self.progress_panel = None;
        self.controls_panel = None;
        self.message_panel  = None;
        self.gauge_panel    = None;
        self.timer_panel    = None;
        # ...
        # ----------------------------
        # ...
        # ----------------------------

GLOBALS = WX_GLOBALS();

# ------------------------------------------------------------------------------

TEMPLATES = {
    u"progress_value": u"{0:0.02f}%",
    u"progress_time":  u"{0:%Hh, %Mm, %Ss}, {1:s}ms",
    u"title_label":    u"{0:s}:",
};

# ------------------------------------------------------------------------------

FONTS = {
    # [1] DEFINE USER INTERFACE FONTS:
    u"ui": {
        u"pointSize": 9,
        u"face":      u"Segoe UI", # the default windows ui font
        u"family":    wx.FONTFAMILY_DEFAULT,
        u"style":     wx.FONTSTYLE_NORMAL,
        u"weight":    wx.FONTWEIGHT_NORMAL,
        u"underline": False,
        u"encoding":  wx.FONTENCODING_DEFAULT,
    },
    u"ui_bold": {
        u"pointSize": 8,
        u"face":      u"Segoe UI", # the default windows ui font
        u"family":    wx.FONTFAMILY_DEFAULT,
        u"style":     wx.FONTSTYLE_NORMAL,
        u"weight":    wx.FONTWEIGHT_BOLD,
        u"underline": False,
        u"encoding":  wx.FONTENCODING_DEFAULT,
    },
    u"ui_italic": {
        u"pointSize": 9,
        u"face":      u"Segoe UI", # the default windows ui font
        u"family":    wx.FONTFAMILY_DEFAULT,
        u"style":     wx.FONTSTYLE_ITALIC,
        u"weight":    wx.FONTWEIGHT_NORMAL,
        u"underline": False,
        u"encoding":  wx.FONTENCODING_DEFAULT,
    },
    u"ui_small": {
        u"pointSize": 8,
        u"face":      u"Segoe UI", # the default windows ui font
        u"family":    wx.FONTFAMILY_DEFAULT,
        u"style":     wx.FONTSTYLE_NORMAL,
        u"weight":    wx.FONTWEIGHT_NORMAL,
        u"underline": False,
        u"encoding":  wx.FONTENCODING_DEFAULT,
    },
    # ...
    # [2] DEFINE CONSOLAS FONTS:
    u"consolas": {
        u"pointSize": 9,
        u"face":      u"Consolas",
        u"family":    wx.FONTFAMILY_MODERN,
        u"style":     wx.FONTSTYLE_NORMAL,
        u"weight":    wx.FONTWEIGHT_NORMAL,
        u"underline": False,
        u"encoding":  wx.FONTENCODING_DEFAULT,
    },
    u"consolas_bold": {
        u"pointSize": 9,
        u"face":      u"Consolas",
        u"family":    wx.FONTFAMILY_MODERN,
        u"style":     wx.FONTSTYLE_NORMAL,
        u"weight":    wx.FONTWEIGHT_BOLD,
        u"underline": False,
        u"encoding":  wx.FONTENCODING_DEFAULT,
    },
    u"consolas_italic": {
        u"pointSize": 9,
        u"face":      u"Consolas",
        u"family":    wx.FONTFAMILY_MODERN,
        u"style":     wx.FONTSTYLE_ITALIC,
        u"weight":    wx.FONTWEIGHT_NORMAL,
        u"underline": False,
        u"encoding":  wx.FONTENCODING_DEFAULT,
    },
    u"consolas_title": {
        u"pointSize": 9,
        u"face":      u"Consolas",
        u"family":    wx.FONTFAMILY_MODERN,
        u"style":     wx.FONTSTYLE_NORMAL,
        u"weight":    wx.FONTWEIGHT_BOLD,
        u"underline": False,
        u"encoding":  wx.FONTENCODING_DEFAULT,
    },
    # ...
};

# ------------------------------------------------------------------------------

COLOURS = {
    # ----------------------------
    u"red":    u"#FF0000",
    u"green":  u"#00FF00",
    u"blue":   u"#0000FF",
    # ...
    # ----------------------------
    u"white":  u"#FFFFFF",
    u"black":  u"#000000",
    # ----------------------------
    u"gray_7": u"#777777",
    u"grey_9": u"#999999",
    u"grey_A": u"#AAAAAA",
    u"grey_C": u"#CCCCCC",
    u"grey_E": u"#EEEEEE",
    # ...
    # ----------------------------
};

# ------------------------------------------------------------------------------

# This will use the default CWD of the main module,
# and then construct the relative bitmap paths.

# N.B. that I do this here at the start, because
# when the application opens or saves to an other
# location, the CWD is, for some reasons, also changed.

# TO DO: instead of a bitmap name list, a directory
# walk should construct a dict of (1) file names and
# corresponding (2) file types.


BITMAP_NAMES = [
    u"console",
    u"file",
    u"folder",
    u"open",
    u"quit",
    u"save_input",
    u"save_output",
    u"table",
    u"transliterate",
    u"transliterate_ods",
    u"transliterate_txt",
];

BITMAP_TYPE = u"png";

BITMAPS = {};
for bitmap_name in BITMAP_NAMES:
    BITMAPS[bitmap_name] = os.path.join(
        os.getcwd(),
        r"input\icons\{0:s}.{1:s}".format(bitmap_name, BITMAP_TYPE)
    );
# for (bitmap_name)

# ------------------------------------------------------------------------------

if __name__ == u"__main__":

    pass;