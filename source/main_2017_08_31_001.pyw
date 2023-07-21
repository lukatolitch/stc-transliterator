# -*- coding: utf-8 -*-
GLOBAL_ENCODING_CURRENT = u"utf-8";

# ------------------------------------------------------------------------------

import os
import re as re
import time as time
import codecs as codecs
import threading as threading

import wx as wx
from wx import stc as stc

from pydispatch import dispatcher as dispatcher

from defs.wxdefs import wxdefs_2015_08_14_001 as wxdefs
from defs.stcdefs import stcdefs_2015_08_15_001 as stcdefs
from defs.threadingdefs import threadingdefs_2015_08_16_001 as threadingdefs
from utils.transliterator import transliterator_v21_2017_08_27_001 as transliterator
from utils.wxutils import wxutils_2015_08_18_001 as wxutils

import pyximport
pyximport.install();
from cutils import cutils_v19_2015_08_18_002 as cutils

# ------------------------------------------------------------------------------

# DEFAULT RUSSIAN TRANSLITERATION:
TRANSLITERATOR_TABLE    = r"input\tables\Cyrillic_Russian_2017_08_27_001.csv";
TRANSLITERATOR_SOURCE   = u"RUSSCII";
TRANSLITERATOR_TARGET   = u"CYRILLIC";
TRANSLITERATOR_ENCODING = u"utf-8"

# COMPLETE RUSSIAN TRANSLITERATION:
# TRANSLITERATOR_TABLE    = r"input\tables\Cyrillic_Russian_Complete_2017_08_26_001.csv";
# TRANSLITERATOR_SOURCE   = u"RUSSCII";
# TRANSLITERATOR_TARGET   = u"РУССКИЙ";
# TRANSLITERATOR_ENCODING = u"utf-8"

# BASHKIR TRANSLITERATION:
# TRANSLITERATOR_TABLE    = r"input\tables\Cyrillic_Bashqort_2015_08_05_003.csv";
# TRANSLITERATOR_SOURCE   = u"ASCII";
# TRANSLITERATOR_TARGET   = u"CYRILLIC";
# TRANSLITERATOR_ENCODING = u"utf-8"

# ------------------------------------------------------------------------------

RE_TABLE = re.compile(u"(^(?P<ID>[^\;]*?)[\;])|([\;])".encode(u"utf-8"), flags=re.DOTALL|re.MULTILINE|re.UNICODE);

# ------------------------------------------------------------------------------

def GET_THREAD (name, daemon):
    u"""
        SOURCES:

        http://thecodeship.com/patterns/guide-to-python-function-decorators/ (2015-06-01 16:51:24)
        http://www.artima.com/weblogs/viewpost.jsp?thread=240808 (2015-06-01 18:26:40)
        https://www.python.org/dev/peps/pep-0318/ (2015-06-01 16:52:47)
        https://www.python.org/dev/peps/pep-3129/ (2015-06-01 18:22:01)
        http://www.artima.com/weblogs/viewpost.jsp?thread=240845 (2015-06-01 18:24:35)
        https://wiki.python.org/moin/PythonDecoratorLibrary (2015-06-01 18:19:19)
        https://wiki.python.org/moin/PythonDecorators (2015-06-02 15:21:22)
        http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/ (2015-06-01 16:50:24)
        http://www.ibm.com/developerworks/ru/library/l-cpdecor/index.html (2015-06-02 15:19:08)
        http://habrahabr.ru/post/46306/ (2015-06-02 15:16:28)
        ...

    """
    # ----------------------------
    def TARGET (target):
        # ----------------------------
        def THREAD (*args, **kwargs):
            thread = threading.Thread(
                target = target,
                args   = args,
                kwargs = kwargs,
            );
            thread.name   = name;
            thread.daemon = daemon;
            return (thread);
        # ----------------------------
        return (THREAD);
    # ----------------------------
    return (TARGET);
    # ----------------------------

# ------------------------------------------------------------------------------

class WX_STC_TABLE (stc.StyledTextCtrl):
    u""" ... """

    def __init__ (self,
        parent,
        stc_style,
        id        = wx.ID_ANY,
        pos       = wx.DefaultPosition,
        size      = wx.DefaultSize,
        style     = wx.SUNKEN_BORDER
    ):
        stc.StyledTextCtrl.__init__(self, parent=parent, id=id, pos=pos, size=size, style=style);
        self.style = stcdefs.STC_STYLE(name=stc_style);
        # ----------------------------
        self.init_stc_style();
        self.init_wx_style();
        self.init_stc_handlers();
        self.init_wx_handlers();
        self.init_custom_handlers();
        self.init_stc_document();
        # ----------------------------
        self.premodification_data = (0, 0, 0, 0);
        self.indicated_lines = [0, 0];
        # self.need_indication = True;
        self.repaint = False;
        self.styling = False;
        # self.right_down = (-1, -1);
        # ...
        # ----------------------------
        self.root            = self.GetTopLevelParent();
        self.transliterator  = self.root.transliterator;
        self.transliterating = False;
        # ----------------------------

    def init_stc_style (self):
        u""" SET THE TARGET STC WINDOW STYLES """
        # ----------------------------
        # [1] SET GENERAL SETTINGS:
        self.SetTechnology(technology=stc.STC_TECHNOLOGY_DEFAULT);
        self.SetBufferedDraw(buffered=False); # i.e. "DOUBLE" buffered...
        self.SetTwoPhaseDraw(twoPhase=True);
        self.SetLayoutCache(mode=stcdefs.STC_CACHE_TYPE[u"DOCUMENT"]);
        self.SetCodePage(codePage=stc.STC_CP_UTF8);
        self.SetKeysUnicode(keysUnicode=True);
        self.SetReadOnly(readOnly=False);
        # ...

        # ----------------------------
        # [2] SET LEXER:
        self.SetLexer(lexer=stc.STC_LEX_CONTAINER);
        # [2.1] SET LEXER STYLES:
        for style_spec in self.style.specs.itervalues():
            self.StyleSetSpec(**style_spec);
        # for (style_spec)
        # [2.2] SET LEXER PROPERTIES:
        # ...

        # ----------------------------
        # [3] SET CHARACTER SETS:
        # [3.1] EITHER SET DEFAULT CHARACTER SETS:
        self.SetCharsDefault(); # i.e. set the Scintilla default character sets
        # [3.2] OR SET CUSTOM CHARACTER SETS:
        # self.SetWordChars(characters=u"ABCČĆDĐEFGHIJKLMNOPQRSŠTUVWZŽXYabcčćdđefghijklmnopqrsštuvwzžxyАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдежзийклмнопрстуфхцчшщъыьэюя.,:; _-+%0123456789");
        # self.SetWhitespaceChars(characters=u" \t\n\r");
        # self.SetPunctuationChars(characters=u".,:;!?");

        # ----------------------------
        # [4] SET WHITESPACE:
        self.SetViewWhiteSpace(viewWS=False);
        self.SetWhitespaceForeground(useSetting=True, fore=self.style.colours[u"WHITESPACE_FOREGROUND"]);
        #self.SetWhitespaceBackground(useSetting=True, back=self.style.colours[u"WHITESPACE_BACKGROUND"]);
        self.SetExtraAscent(extraAscent=2.0);
        self.SetExtraDescent(extraDescent=0);

        # ----------------------------
        # [5] SET CARET:
        self.SetCaretStyle(caretStyle=stc.STC_CARETSTYLE_LINE);
        self.SetCaretPeriod(periodMilliseconds=200);
        self.SetCaretWidth(pixelWidth=3);
        self.SetCaretLineVisible(show=True);
        self.SetCaretForeground(fore=self.style.colours[u"CARET_FOREGROUND"]);
        self.SetCaretLineBackground(back=self.style.colours[u"CARET_BACKGROUND"]);
        #self.SetCaretLineBackAlpha(alpha=stc.STC_ALPHA_NOALPHA);

        # ----------------------------
        # [6] SET SELECTION:
        # [6.1] SET SELECTION STYLE:
        #self.SetSelForeground(useSetting=True, fore=self.style.colours[u"SELECTION_FOREGROUND"]);
        self.SetSelBackground(useSetting=True, back=self.style.colours[u"SELECTION_BACKGROUND"]);
        # self.SetSelectionMode(mode=STC_SELECTION_TYPE["THIN"]);
        # [6.2] SET MULTIPLE SELECTION:
        self.SetMultipleSelection(multipleSelection=False);
        # self.SetAdditionalSelectionTyping(additionalSelectionTyping=False);
        # self.SetMultiPaste(multiPaste=stc.STC_MULTIPASTE_ONCE);
        # [6.3] SET SELECTION STYLE:
        # self.SetUndoCollection(collectUndo=True);
        # ...

        # ----------------------------
        # [7] SET HOTSPOT STYLE:
        # self.StyleSetHotSpot(style=self.style.specs[u"DOMAIN"][u"styleNum"], hotspot=True);
        # self.SetHotspotActiveForeground(useSetting=True, fore=self.style.colours[u"HOTSPOT_FOREGROUND"]);
        # self.SetHotspotActiveBackground(useSetting=True, back=self.style.colours[u"HOTSPOT_BACKGROUND"]);
        # self.SetHotspotActiveUnderline(underline=True);
        # self.SetHotspotSingleLine(singleLine=True);

        # ----------------------------
        # [8] SET INDICATORS:
        # [8.1] SET FIRST INDICATOR:
        # self.IndicatorSetStyle(indic=stcdefs.STC_INDICATOR_INDEX[u"FILE"], style=stcdefs.STC_INDICATOR_STYLE[u"BOX"]);
        # self.IndicatorSetForeground(indic=stcdefs.STC_INDICATOR_INDEX[u"FILE"], fore=self.style.colours[u"INDICATOR_FILE"]);
        # self.IndicatorSetUnder(indic=stcdefs.STC_INDICATOR_INDEX[u"FILE"], under=True);
        # self.IndicatorSetAlpha(indicator=stcdefs.STC_INDICATOR_INDEX[u"FILE"], alpha=255);
        # self.IndicatorSetOutlineAlpha(indicator=stcdefs.STC_INDICATOR_INDEX[u"FILE"], alpha=255);
        # [8.1.2] SET SECOND INDICATOR:
        # ...
        # [8.1.3] SET THIRD INDICATOR:
        # ...
        # [8.2] SELECT CURRENT INDICATOR:
        # self.SetIndicatorCurrent(indicator=stcdefs.STC_INDICATOR_INDEX[u"FILE"]);

        # ----------------------------
        # [9] SET INDENTATION:
        self.SetUseTabs(useTabs=True);
        self.SetTabWidth(tabWidth=4);
        # self.SetIndent(indentSize=4);
        # self.SetTabIndents(tabIndents=False);
        # self.SetBackSpaceUnIndents(tabIndents=False);
        self.SetIndentationGuides(indentView=True);

        # ----------------------------
        # [10] SET WRAPPING:
        # [10.1] SET LINE WRAPPING:
        self.SetWrapMode(mode=stcdefs.STC_WRAP_MODE[u"NONE"]);
        self.SetWrapStartIndent(indent=1);
        self.SetWrapIndentMode(mode=stcdefs.STC_WRAP_INDENT_MODE[u"FIXED"]);
        self.SetWrapVisualFlags(wrapVisualFlags=stcdefs.STC_WRAP_FLAG[u"END"]);
        self.SetWrapVisualFlagsLocation(wrapVisualFlagsLocation=stcdefs.STC_WRAP_LOC[u"TEXT_END"]);
        # [10.2] SET LONG LINES MARKING:
        # self.SetEdgeMode(mode=stc.STC_EDGE_LINE);
        # self.SetEdgeColumn(column=80);
        # self.SetEdgeColour(edgeColour=STC_STYLE_COLOURS[u"URL_DARK"][u"EDGE"]);

        # ----------------------------
        # [11] SET END-OF-LINE:
        self.SetEOLMode(eolMode=stc.STC_EOL_CRLF);
        self.SetViewEOL(visible=False);
        self.SetSelEOLFilled(filled=False);

        # ----------------------------
        # [12] SET MARGINS:
        # [12.1] SET PADDING MARGINS:
        self.SetMarginLeft(pixelWidth=5);
        self.SetMarginRight(pixelWidth=5);
        # [12.2] SET DISPLAY MARGINS:
        # [12.2.1] SET LINE MARGIN (0):
        self.SetMarginWidth(margin=0, pixelWidth=40);
        self.SetMarginType(margin=0, marginType=stc.STC_MARGIN_NUMBER);
        self.SetMarginSensitive(margin=0, sensitive=False);
        self.SetMarginCursor(margin=0, cursor=stc.STC_CURSORNORMAL);
        # [12.2.2] SET SYMBOL MARGIN (2):
        self.SetMarginWidth(margin=1, pixelWidth=5);
        self.SetMarginType(margin=1, marginType=stc.STC_MARGIN_SYMBOL);
        self.SetMarginSensitive(margin=1, sensitive=False);
        # self.SetMarginCursor(margin=1, cursor=stc.STC_CURSORNORMAL);
        # self.SetMarginMask(margin=1, mask=stcdefs.STC_MARKER_MASK[u"CURRENT_LINE"]);
        # self.MarkerDefine(
        #     markerNumber = stcdefs.STC_MARKER_NUMBER[u"CURRENT_LINE"],
        #     foreground   = self.style.colours[u"CURRENT_LINE"],
        #     background   = self.style.colours[u"CURRENT_LINE"],
        #     markerSymbol = stcdefs.STC_MARKER_SYMBOL[u"ARROW"],
        # );
        # [12.3] SET FOLDING MARGIN:
        # self.SetFoldMarginColour(useSetting=True, back=u"#0022DD");
        # self.SetFoldMarginHiColour(useSetting=True, fore=u"#0022DD");
        # self.SetFoldFlags(flags=0x4 | 0x10);

        # ----------------------------
        # [13] SET FOLDING MARKERS:
        # self.MarkerDefine(markerNumber=stcdefs.STC_MARKER_NUMBER[u"FOLD"],          markerSymbol=stcdefs.STC_MARKER_SYMBOL[u"BOXPLUS"],           foreground=u"#0022DD", background=u"#FFFFFF");
        # self.MarkerDefine(markerNumber=stcdefs.STC_MARKER_NUMBER[u"FOLD_OPEN"],     markerSymbol=stcdefs.STC_MARKER_SYMBOL[u"BOXMINUS"],          foreground=u"#0022DD", background=u"#FFFFFF");
        # self.MarkerDefine(markerNumber=stcdefs.STC_MARKER_NUMBER[u"FOLD_END"],      markerSymbol=stcdefs.STC_MARKER_SYMBOL[u"BOXPLUSCONNECTED"],  foreground=u"#0022DD", background=u"#FFFFFF");
        # self.MarkerDefine(markerNumber=stcdefs.STC_MARKER_NUMBER[u"FOLD_OPEN_MID"], markerSymbol=stcdefs.STC_MARKER_SYMBOL[u"BOXMINUSCONNECTED"], foreground=u"#0022DD", background=u"#FFFFFF");
        # self.MarkerDefine(markerNumber=stcdefs.STC_MARKER_NUMBER[u"FOLD_MID_TAIL"], markerSymbol=stcdefs.STC_MARKER_SYMBOL[u"TCORNER"],           foreground=u"#0022DD", background=u"#FFFFFF");
        # self.MarkerDefine(markerNumber=stcdefs.STC_MARKER_NUMBER[u"FOLD_TAIL"],     markerSymbol=stcdefs.STC_MARKER_SYMBOL[u"LCORNER"],           foreground=u"#0022DD", background=u"#FFFFFF");
        # self.MarkerDefine(markerNumber=stcdefs.STC_MARKER_NUMBER[u"FOLD_SUB"],      markerSymbol=stcdefs.STC_MARKER_SYMBOL[u"VLINE"],             foreground=u"#0022DD", background=u"#FFFFFF");

        # ----------------------------
        # [14] SET SCROLLING:
        self.SetEndAtLastLine(endAtLastLine=False);
        self.SetYCaretPolicy(
            caretPolicy = stcdefs.STC_POLICY[u"CARET_EVEN"],
            caretSlop   = 5,
        );
        self.SetXCaretPolicy(
            caretPolicy = stcdefs.STC_POLICY[u"CARET_SLOP"]
                            | stcdefs.STC_POLICY[u"CARET_EVEN"],
            caretSlop   = 50,
        );
        self.SetVisiblePolicy(
            visiblePolicy = stc.STC_VISIBLE_SLOP,
            visibleSlop   = 0,
        );

        # ----------------------------
        # [15] SET INTERACTION:
        self.SetMouseDownCaptures(captures=True);
        self.SetMouseDwellTime(periodMilliseconds=1.0*1000); # cf. stc.STC_TIME_FOREVER (i.e. never raise the dwell events)

        # ----------------------------
        # [16] SET CALL TIPS:
        self.CallTipUseStyle(tabSize=10); # i.e. use the special self.style.indices[u"STC_CALLTIP"], instead of the default self.style.indices[u"DEFAULT"]
        self.CallTipSetPosition(above=False);
        # self.CallTipSetForegroundHighlight(fore=self.style.colours[u"CALLTIP_HIGHLIGHT"]);

        # ----------------------------
        # [17] SET ANNOTATIONS:
        # ...

        # ----------------------------
        # [18] SET GLOBAL STYLE DATA:
        # ...
        # ----------------------------

        # ----------------------------
        # [19] RE-SET THE TARGET WINDOW:
        self.Refresh();
        # ----------------------------

    def init_wx_style (self):
        u""" ... """
        # ----------------------------
        self.SetDoubleBuffered(on=False);
        # ...
        # ----------------------------

    def init_stc_handlers (self):
        u""" ... """
        # ----------------------------
        # [1] STC EVENTS:
        # [1.1] MODIFIED EVENT:
        self.SetModEventMask(
            mask = stcdefs.STC_PERFORMED_BITS["ANYONE"]           # (1) handle modifications done by anyone
                    | stcdefs.STC_MODIFIED_BITS["TEXT_ANYCHANGE"] # (2) handle only the text modifications
        );
        self.Bind(event=stc.EVT_STC_MODIFIED, source=self, handler=self.handle_stc_modified);
        # ...
        # [1.2] UPDATED EVENT:
        self.Bind(event=stc.EVT_STC_UPDATEUI, source=self, handler=self.handle_stc_update_ui);
        # ...
        # [1.3] PAINTED EVENT:
        # self.Bind(event=stc.EVT_STC_PAINTED, source=self, handler=self.handle_stc_painted);
        # ...
        # [1.4] STYLE EVENT:
        self.Bind(event=stc.EVT_STC_STYLENEEDED, source=self, handler=self.handle_stc_style_needed);
        # ...
        # [1.5] KEYBOARD EVENT:
        # self.Bind(event=stc.EVT_STC_KEY, source=self, handler=self.handle_stc_key);
        # ...
        # [1.6] CLICK EVENTS:
        # self.Bind(event=stc.EVT_STC_DOUBLECLICK, source=self, handler=self.handle_stc_double_click);
        # self.Bind(event=stc.EVT_STC_INDICATOR_CLICK, source=self, handler=self.handle_stc_indicator_click);
        # self.Bind(event=stc.EVT_STC_INDICATOR_RELEASE, source=self, handler=self.handle_stc_indicator_release);
        # self.Bind(event=stc.EVT_STC_HOTSPOT_CLICK, source=self, handler=self.handle_stc_hotspot_click);
        # self.Bind(event=stc.EVT_STC_HOTSPOT_DCLICK, source=self, handler=self.handle_stc_hotspot_double_click);
        # self.Bind(event=stc.EVT_STC_MARGINCLICK, source=self, handler=self.handle_stc_margin_click);
        # ...
        # [1.7] DWELL EVENTS:
        # self.Bind(event=stc.EVT_STC_DWELLSTART, source=self, handler=self.handle_stc_dwell_start);
        # self.Bind(event=stc.EVT_STC_DWELLEND, source=self,  handler=self.handle_stc_dwell_end);
        # ...
        # ----------------------------

    def init_wx_handlers (self):
        u""" ... """
        # ----------------------------
        # [2] WX (i.e. NON-STC) EVENTS:
        # [2.1] KEYBOARD EVENTS:
        self.Bind(event=wx.EVT_KEY_DOWN, source=self, handler=self.handle_wx_key_down); # to do: override with the accellerator?
        # ...
        # [2.2] MOUSE EVENTS:
        self.Bind(event=wx.EVT_RIGHT_DOWN, source=self, handler=self.handle_wx_right_down);
        # ...
        # [2.3] WINDOW EVENTS:
        # self.Bind(event=wx.EVT_IDLE, source=self.ContainingSizer, handler=self.handle_wx_idle); # n.b. that the source is the containing sizer (i.e. not self)
        # ...
        # ----------------------------

    def init_custom_handlers (self):
        u""" ... """
        # ----------------------------
        # [3] CUSTOM (i.e. NON-WX, NON-STC) EVENTS:
        # dispatcher.connect(
        #     signal   = threadingdefs.GLOBAL_SIGNAL_INDEX[u"STC_INPUT_PAINTED"],
        #     sender   = threadingdefs.GLOBAL_SENDER_ANY,
        #     receiver = self.handle_repainted_input,
        #     weak     = True,
        # );
        # ...
        # ----------------------------

    def init_stc_document (self):
        u""" ... """
        # ----------------------------
        self.document = self.GetDocPointer(); # i.e. get the pointer to the current, default stc document
        # ----------------------------

    def handle_stc_modified (self, event):
        u""" ... """
        # ----------------------------
        modification_type = event.GetModificationType();
        # ----------------------------
        if (modification_type & stcdefs.STC_MODIFIED_BITS["TEXT_PRECHANGE"]):
            if (modification_type & stcdefs.STC_MODIFIED_BITS["TEXT_PREINSERT"]):
                # ----------------------------
                # [1.1] GET PRE-MODIFICATION DATA:
                # a0 = event.GetPosition(); # get the "TEXT_PREINSERT" modification start position
                # b0 = a0 + event.GetLength(); # get the "TEXT_PREINSERT" modification end position
                # A0 = self.LineFromPosition(pos=a0); # get the "TEXT_PREINSERT" modification start line
                # B0 = A0; # get the "TEXT_PREINSERT" modification end line
                # [1.2] GET PRE-MODIFICATION SELECTION DATA:
                # x0 = self.GetSelectionStart(); # get the "TEXT_PREINSERT" selection start position
                # y0 = self.GetSelectionEnd(); # get the "TEXT_PREINSERT" selection end position
                # X0 = self.LineFromPosition(pos=x0); # get the "TEXT_PREINSERT" selection start line
                # Y0 = self.LineFromPosition(pos=y0); # get the "TEXT_PREINSERT" selection end line
                # ----------------------------
                # [2] SET PRE-MODIFICATION DATA:
                # self.premodification_data = (a0, b0, A0, B0);
                pass;
                # ----------------------------
            else: # i.e. (modification_type & stcdefs.STC_MODIFIED_BITS["TEXT_PREDELETE"])
                # ----------------------------
                # [1.1] GET PRE-MODIFICATION DATA:
                # a0 = event.GetPosition(); # get the "TEXT_PREDELETE" modification start position
                # b0 = a0 + event.GetLength(); # get the "TEXT_PREDELETE" modification end position
                # A0 = self.LineFromPosition(pos=a0); # get the "TEXT_PREDELETE" modification start line
                # B0 = self.LineFromPosition(pos=b0); # get the "TEXT_PREDELETE" modification end line
                # [1.2] GET PRE-MODIFICATION SELECTION DATA:
                # x0 = self.GetSelectionStart(); # get the "TEXT_PREDELETE" selection start position
                # y0 = self.GetSelectionEnd(); # get the "TEXT_PREDELETE" selection end position
                # X0 = self.LineFromPosition(pos=x0); # get the "TEXT_PREDELETE" selection start line
                # Y0 = self.LineFromPosition(pos=y0); # get the "TEXT_PREDELETE" selection end line
                # ----------------------------
                # [2] SET PRE-MODIFICATION DATA:
                # self.premodification_data = (a0, b0, A0, B0);
                pass;
                # ----------------------------
        elif (modification_type & stcdefs.STC_MODIFIED_BITS["TEXT_CHANGED"]):
            if (modification_type & stcdefs.STC_MODIFIED_BITS["TEXT_INSERTED"]):
                # ----------------------------
                # [1] GET LAST PRE-MODIFICATION DATA:
                # a0, b0, A0, B0 = self.premodification_data; # get the "TEXT_PREINSERT" modification (or selection) data
                # ----------------------------
                # [2.1] GET MODIFICATION DATA:
                # a1 = event.GetPosition(); # get the "TEXT_INSERTED" modification start position
                # b1 = a1 + event.GetLength(); # get the "TEXT_INSERTED" modification end position
                # A1 = self.LineFromPosition(pos=a1); # get the "TEXT_INSERTED" modification start line
                # B1 = A1 + event.GetLinesAdded(); # get the "TEXT_INSERTED" modification end line
                # [2.1] GET MODIFICATION SELECTION DATA:
                # x1 = self.GetSelectionStart(); # get the "TEXT_INSERTED" selection start position
                # y1 = self.GetSelectionEnd(); # get the "TEXT_INSERTED" selection end position
                # X1 = self.LineFromPosition(pos=x1); # get the "TEXT_INSERTED" selection start line
                # Y1 = self.LineFromPosition(pos=y1); # get the "TEXT_INSERTED" selection end line
                # ----------------------------
                # self.repaint = True;
                pass;
                # ----------------------------
            else: # i.e. (modification_type & stcdefs.STC_MODIFIED_BITS["TEXT_DELETED"])
                # ----------------------------
                # [1] GET LAST PRE-MODIFICATION DATA:
                # a0, b0, A0, B0 = self.premodification_data; # get the "TEXT_PREDELETE" modification (or selection) data
                # ----------------------------
                # [2.1] GET MODIFICATION DATA:
                # a1 = event.GetPosition(); # get the "TEXT_DELETED" modification start position
                # b1 = a1 + event.GetLength(); # get the "TEXT_DELETED" modification end position
                # A1 = self.LineFromPosition(pos=a1); # get the "TEXT_DELETED" modification start line
                # B1 = B0 + event.GetLinesAdded(); # get the "TEXT_DELETED" modification end line
                # [2.1] GET MODIFICATION SELECTION DATA:
                # x1 = self.GetSelectionStart(); # get the "TEXT_DELETED" selection start position
                # y1 = self.GetSelectionEnd(); # get the "TEXT_DELETED" selection end position
                # X1 = self.LineFromPosition(pos=x1); # get the "TEXT_DELETED" selection start line
                # Y1 = self.LineFromPosition(pos=y1); # get the "TEXT_DELETED" selection end line
                # ----------------------------
                # self.repaint = True;
                pass;
                # ----------------------------
        # elif (modification_type & stcdefs.STC_MODIFIED_BITS["STYLE_CHANGED"]): # the modification (but not the update!) masked out by the self.SetModEventMask()
        #     print u"<MODIFIED_STYLE_CHANGED>";
        # elif (modification_type & stcdefs.STC_MODIFIED_BITS["MARKER_CHANGED"]): # the modification (but not the update!) masked out by the self.SetModEventMask()
        #     print u"<MODIFIED_MARKER_CHANGED>";
        # elif (modification_type & stcdefs.STC_MODIFIED_BITS["ANNOTATION_CHANGED"]): # the modification (but not the update!) masked out by the self.SetModEventMask()
        #     print u"<MODIFIED_ANNOTATION_CHANGED>";
        else:
            pass;
        # ----------------------------
        # event.Skip(); # i.e. PROPAGATE THE EVENT FURTHER...
        # ----------------------------

    def handle_stc_update_ui (self, event):
        u""" ... """
        # ----------------------------
        update_type = event.GetUpdated();
        # ----------------------------
        if (update_type & stcdefs.STC_UPDATED_BITS["SELECTION"]): # i.e. SELECTION RANGE CHANGED
            # ----------------------------
            # self.repaint = True;
            pass;
            # ----------------------------
        elif (update_type & stcdefs.STC_UPDATED_BITS[u"V_SCROLL"]): # i.e. VERTICAL SCROLL RANGE CHANGED
            # ----------------------------
            pass;
            # ----------------------------
        else:
            pass;
        # ----------------------------
        event.Skip(); # i.e. PROPAGATE THIS EVENT FURTHER...
        # ----------------------------

    def handle_stc_painted (self, event):
        u""" ... """
        # ----------------------------
        if (self.repaint): # i.e. (self.repaint == True)
            # ----------------------------
            self.repaint = False;
            # ----------------------------
        else: # i.e. (self.repaint == False)
            pass;
        # ----------------------------
        # event.Skip(); # i.e. propagate the event further...
        # ----------------------------

    def handle_stc_style_needed (self, event):
        u""" ... """
        # ----------------------------
        # [1] GET STYLE NEEDED RANGE:
        # [1.1] GET STYLE NEEDED START POSITION:
        # x = self.GetEndStyled();             # get the style needed range start position...
        # A = self.LineFromPosition(pos=x);    # get the style needed range start line...
        # a = self.PositionFromLine(line=A);   # get the style needed extended range start position...
        # [1.2] GET STYLE NEEDED END POSITION:
        # y = event.GetPosition();             # get the style needed range end position...
        # B = self.LineFromPosition(pos=y);    # get the style needed range end line...
        # b = self.GetLineEndPosition(line=B); # get the style needed extended range end position...
        # ----------------------------
        # [2] GET STYLE NEEDED RANGE TEXT:
        # [2.1] GET STYLE NEEDED RANGE UNICODE TEXT:
        # t = self.GetTextRange(startPos=x, endPos=y); # get the style needed range unicode text...
        # T = self.GetTextRange(startPos=a, endPos=b); # get the style needed extended range unicode text...
        # [2.2] GET STYLE NEEDED RANGE UTF-8 TEXT:
        # t = self.GetTextRangeUTF8(startPos=x, endPos=y); # get the style needed range utf-8 text...
        # T = self.GetTextRangeUTF8(startPos=a, endPos=b); # get the style needed extended range utf-8 text...
        # [2.3] GET STYLE NEEDED RANGE CELLS:
        # t = self.GetStyledText(startPos=x, endPos=y); # get the style needed range stc "cell" text...
        # T = self.GetStyledText(startPos=a, endPos=b); # get the style needed extended range stc "cell" text...
        # ----------------------------
        # [3] SET DOCUMENT STYLES:
        if (not self.styling): # i.e. (self.styling == False)
            self.set_document_styles();
        else: # i.e. (self.styling == True)
            pass;
        # ----------------------------
        # event.Skip(); # i.e. PROPAGATE THE EVENT FURTHER...
        # ----------------------------

    def handle_stc_key (self, event):
        u""" ... """
        # ----------------------------
        # ...
        event.Skip(); # i.e. PROPAGATE THE EVENT FURTHER...
        # ----------------------------

    def handle_wx_key_down (self, event):
        u""" ... """
        # ----------------------------
        # [1] GET KEY EVENT DATA:
        # [1.1] GET KEY EVENT KEY DATA:
        key     = event.GetKeyCode();
        charkey = event.GetUnicodeKey(); # UPPER CASE
        # [1.2] GET KEY EVENT MODIFICATION DATA:
        control = event.ControlDown();
        shift   = event.ShiftDown();
        alt     = event.AltDown();
        # [1.3] GET KEY EVENT POSITION DATA:
        # x       = event.GetX();
        # y       = event.GetY();
        # ----------------------------
        # [2] PROCESS KEY EVENT DATA:
        # [2.1] PROCESS MODIFIED KEY EVENT DATA:
        if (control and shift and alt): # i.e. Ctrl+Shift+Alt
            event.Skip();
        elif (control and shift): # i.e. Ctrl+Shift
            event.Skip();
        elif (control and alt): # i.e. Ctrl+Alt
            event.Skip();
        elif (control): # i.e. Ctrl
            if (charkey == ord(u"C")): # i.e. Ctrl+C (COPY)
                event.Skip();
            elif (charkey == ord(u"X")): # i.e. Ctrl+X (CUT)
                event.Skip();
            elif (charkey == ord(u"V")): # i.e. Ctrl+V (PASTE)
                event.Skip();
            else:
                event.Skip();
        elif (shift and alt): # i.e. Shift+Alt
            event.Skip();
        elif (shift): # i.e. Shift
            event.Skip();
        elif (alt): # i.e. Alt
            event.Skip();
        # ----------------------------
        # [2.2] PROCESS SPECIAL KEY EVENT DATA:
        # elif (key in (wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER)): # USED ("CONSUMED") BY STC!
        #     event.Skip();
        # elif (key in (wx.WXK_DELETE, wx.WXK_BACK)): # USED ("CONSUMED") BY STC!
        #     event.Skip();
        # elif (key in (wx.WXK_SPACE, wx.WXK_TAB)): # USED ("CONSUMED") BY STC!
        #     event.Skip();
        # elif (key == wx.WXK_F1): # i.e. F1
        #     event.Skip();
        # elif (key == wx.WXK_F8): # i.e. F8
        #     event.Skip();
        elif (key == wx.WXK_F9): # i.e. F9
            self.toggle_wrap_mode();
        # elif (key == wx.WXK_F10): # i.e. F10
        #     event.Skip();
        # elif (key == wx.WXK_F11): # i.e. F11
        #     event.Skip();
        # elif (key == wx.WXK_F12): # i.e. F12
        #     event.Skip();
        # ...
        # ----------------------------
        # [2.3] PROCESS LITERAL KEY EVENT DATA:
        # elif (key == wx.WXK_NUMPAD0): # USED ("CONSUMED") BY STC!
        #     event.Skip();
        # elif (key == wx.WXK_NUMPAD1): # USED ("CONSUMED") BY STC!
        #     event.Skip();
        # elif (charkey == ord(u"C")): # USED ("CONSUMED") BY STC!
        #     event.Skip();
        # elif (charkey == ord(u"Č")): # USED ("CONSUMED") BY STC!
        #     event.Skip();
        # ...
        # ----------------------------
        # [3] NOTHING PROCESSED:
        else:
            event.Skip(); # i.e. PROPAGATE THE EVENT FURTHER...
        # ----------------------------

    def handle_wx_right_down (self, event):
        u""" ... """
        # ----------------------------
        # self.right_down = event.GetPosition();
        # self.PopupMenu(menu=WX_MENU_STC(parent=self));
        # ----------------------------
        event.Skip(); # i.e. PROPAGATE THE EVENT FURTHER...
        # ----------------------------

    def handle_wx_idle (self, event):
        u""" ... """
        # ----------------------------
        # event.RequestMore(); # i.e. RE-RAISE THE IDLE EVENT (CPU EXPENSIVE, THOUGH)
        event.Skip(); # i.e. propagate the event further...
        # ----------------------------

    def set_document_styles (self):
        u""" ... """
        # ----------------------------
        if (not self.styling): # i.e. (self.styling == False)
            # ----------------------------
            self.styling = True;
            # ----------------------------
            self.ClearDocumentStyle();
            text = self.GetTextUTF8();
            x = 0;
            y = len(text);
            b = 0;
            # ----------------------------
            for match in RE_TABLE.finditer(text):
                # ----------------------------
                a, b = match.span(0);
                # ----------------------------
                if (x < a):
                    # ----------------------------
                    self.StartStyling(pos=x, mask=stcdefs.STC_STYLE_MASKS[u"5_BIT"]);
                    self.SetStyling(length=a-x, style=self.style.indices[u"DEFAULT"]);
                    # ----------------------------
                    self.StartStyling(pos=a, mask=stcdefs.STC_STYLE_MASKS[u"5_BIT"]);
                    self.SetStyling(length=b-a, style=self.style.indices[u"COMMENT"]);
                    # ----------------------------
                else: # (x == a)
                    self.StartStyling(pos=a, mask=stcdefs.STC_STYLE_MASKS[u"5_BIT"]);
                    self.SetStyling(length=b-a, style=self.style.indices[u"COMMENT"]);
                # ----------------------------
                x = b;
                # ----------------------------
            # for (match)
            # ----------------------------
            if (b < y):
                self.StartStyling(pos=b, mask=stcdefs.STC_STYLE_MASKS[u"5_BIT"]);
                self.SetStyling(length=y-b, style=self.style.indices[u"DEFAULT"]);
            else: # (b == y)
                pass;
            # ----------------------------
            self.styling = False;
            # ----------------------------
        else: # i.e. (self.styling == True)
            pass;
        # ----------------------------

    def toggle_wrap_mode (self):
        u""" ... """
        # ----------------------------
        wrap_mode = self.GetWrapMode();
        wrap_name = stcdefs.STC_WRAP_NAME[wrap_mode];
        # ----------------------------
        if (wrap_name == u"NONE"):
            self.SetWrapMode(mode=stcdefs.STC_WRAP_MODE[u"WORD"]);
        elif (wrap_name == u"WORD"):
            self.SetWrapMode(mode=stcdefs.STC_WRAP_MODE[u"CHAR"]);
        else: # i.e. (wrap_name == u"CHAR")
            self.SetWrapMode(mode=stcdefs.STC_WRAP_MODE[u"NONE"]);
        # ----------------------------

# ------------------------------------------------------------------------------

class WX_STC_OUTPUT (stc.StyledTextCtrl):
    u""" ... """

    def __init__ (self,
        parent,
        stc_style,
        id        = wx.ID_ANY,
        pos       = wx.DefaultPosition,
        size      = wx.DefaultSize,
        style     = wx.SUNKEN_BORDER
    ):
        stc.StyledTextCtrl.__init__(self, parent=parent, id=id, pos=pos, size=size, style=style);
        self.style = stcdefs.STC_STYLE(name=stc_style);
        # ----------------------------
        self.init_stc_style();
        self.init_wx_style();
        self.init_stc_handlers();
        self.init_wx_handlers();
        self.init_custom_handlers();
        self.init_stc_document();
        # ----------------------------
        self.premodification_data = (0, 0, 0, 0);
        self.indicated_lines = [0, 0];
        # self.need_indication = True;
        self.repaint = True;
        # self.right_down = (-1, -1);
        # ...
        # ----------------------------
        self.root                   = self.GetTopLevelParent();
        self.transliterator         = self.root.transliterator;
        self.transliterating        = False;
        self.transliteration_needed = False;
        # ----------------------------

    def init_stc_style (self):
        u""" SET THE TARGET STC WINDOW STYLES """
        # ----------------------------
        # [1] SET GENERAL SETTINGS:
        self.SetTechnology(technology=stc.STC_TECHNOLOGY_DEFAULT);
        self.SetBufferedDraw(buffered=False); # i.e. "DOUBLE" buffered...
        self.SetTwoPhaseDraw(twoPhase=True);
        self.SetLayoutCache(mode=stcdefs.STC_CACHE_TYPE[u"DOCUMENT"]);
        self.SetCodePage(codePage=stc.STC_CP_UTF8);
        self.SetKeysUnicode(keysUnicode=True);
        self.SetReadOnly(readOnly=True);
        # ...

        # ----------------------------
        # [2] SET LEXER:
        self.SetLexer(lexer=stc.STC_LEX_CONTAINER);
        # [2.1] SET LEXER STYLES:
        for style_spec in self.style.specs.itervalues():
            self.StyleSetSpec(**style_spec);
        # for (style_spec)
        # [2.2] SET LEXER PROPERTIES:
        # ...

        # ----------------------------
        # [3] SET CHARACTER SETS:
        # [3.1] EITHER SET DEFAULT CHARACTER SETS:
        self.SetCharsDefault(); # i.e. set the Scintilla default character sets
        # [3.2] OR SET CUSTOM CHARACTER SETS:
        # self.SetWordChars(characters=u"ABCČĆDĐEFGHIJKLMNOPQRSŠTUVWZŽXYabcčćdđefghijklmnopqrsštuvwzžxyАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдежзийклмнопрстуфхцчшщъыьэюя.,:; _-+%0123456789");
        # self.SetWhitespaceChars(characters=u" \t\n\r");
        # self.SetPunctuationChars(characters=u".,:;!?");

        # ----------------------------
        # [4] SET WHITESPACE:
        self.SetViewWhiteSpace(viewWS=False);
        self.SetWhitespaceForeground(useSetting=True, fore=self.style.colours[u"WHITESPACE_FOREGROUND"]);
        #self.SetWhitespaceBackground(useSetting=True, back=self.style.colours[u"WHITESPACE_BACKGROUND"]);
        self.SetExtraAscent(extraAscent=0.0);
        self.SetExtraDescent(extraDescent=0);

        # ----------------------------
        # [5] SET CARET:
        self.SetCaretStyle(caretStyle=stc.STC_CARETSTYLE_LINE);
        self.SetCaretPeriod(periodMilliseconds=200);
        self.SetCaretWidth(pixelWidth=3);
        self.SetCaretLineVisible(show=True);
        self.SetCaretForeground(fore=self.style.colours[u"CARET_FOREGROUND"]);
        self.SetCaretLineBackground(back=self.style.colours[u"CARET_BACKGROUND"]);
        #self.SetCaretLineBackAlpha(alpha=stc.STC_ALPHA_NOALPHA);

        # ----------------------------
        # [6] SET SELECTION:
        # [6.1] SET SELECTION STYLE:
        #self.SetSelForeground(useSetting=True, fore=self.style.colours[u"SELECTION_FOREGROUND"]);
        self.SetSelBackground(useSetting=True, back=self.style.colours[u"SELECTION_BACKGROUND"]);
        # self.SetSelectionMode(mode=STC_SELECTION_TYPE["THIN"]);
        # [6.2] SET MULTIPLE SELECTION:
        self.SetMultipleSelection(multipleSelection=False);
        # self.SetAdditionalSelectionTyping(additionalSelectionTyping=False);
        # self.SetMultiPaste(multiPaste=stc.STC_MULTIPASTE_ONCE);
        # [6.3] SET SELECTION STYLE:
        # self.SetUndoCollection(collectUndo=True);
        # ...

        # ----------------------------
        # [7] SET HOTSPOT STYLE:
        # self.StyleSetHotSpot(style=self.style.specs[u"DOMAIN"][u"styleNum"], hotspot=True);
        # self.SetHotspotActiveForeground(useSetting=True, fore=self.style.colours[u"HOTSPOT_FOREGROUND"]);
        # self.SetHotspotActiveBackground(useSetting=True, back=self.style.colours[u"HOTSPOT_BACKGROUND"]);
        # self.SetHotspotActiveUnderline(underline=True);
        # self.SetHotspotSingleLine(singleLine=True);

        # ----------------------------
        # [8] SET INDICATORS:
        # [8.1] SET FIRST INDICATOR:
        # self.IndicatorSetStyle(indic=stcdefs.STC_INDICATOR_INDEX[u"FILE"], style=stcdefs.STC_INDICATOR_STYLE[u"BOX"]);
        # self.IndicatorSetForeground(indic=stcdefs.STC_INDICATOR_INDEX[u"FILE"], fore=self.style.colours[u"INDICATOR_FILE"]);
        # self.IndicatorSetUnder(indic=stcdefs.STC_INDICATOR_INDEX[u"FILE"], under=True);
        # self.IndicatorSetAlpha(indicator=stcdefs.STC_INDICATOR_INDEX[u"FILE"], alpha=255);
        # self.IndicatorSetOutlineAlpha(indicator=stcdefs.STC_INDICATOR_INDEX[u"FILE"], alpha=255);
        # [8.1.2] SET SECOND INDICATOR:
        # ...
        # [8.1.3] SET THIRD INDICATOR:
        # ...
        # [8.2] SELECT CURRENT INDICATOR:
        # self.SetIndicatorCurrent(indicator=stcdefs.STC_INDICATOR_INDEX[u"FILE"]);

        # ----------------------------
        # [9] SET INDENTATION:
        self.SetUseTabs(useTabs=True);
        self.SetTabWidth(tabWidth=4);
        # self.SetIndent(indentSize=4);
        # self.SetTabIndents(tabIndents=False);
        # self.SetBackSpaceUnIndents(tabIndents=False);
        self.SetIndentationGuides(indentView=True);

        # ----------------------------
        # [10] SET WRAPPING:
        # [10.1] SET LINE WRAPPING:
        self.SetWrapMode(mode=stcdefs.STC_WRAP_MODE[u"NONE"]);
        self.SetWrapStartIndent(indent=1);
        self.SetWrapIndentMode(mode=stcdefs.STC_WRAP_INDENT_MODE[u"FIXED"]);
        self.SetWrapVisualFlags(wrapVisualFlags=stcdefs.STC_WRAP_FLAG[u"END"]);
        self.SetWrapVisualFlagsLocation(wrapVisualFlagsLocation=stcdefs.STC_WRAP_LOC[u"TEXT_END"]);
        # [10.2] SET LONG LINES MARKING:
        # self.SetEdgeMode(mode=stc.STC_EDGE_LINE);
        # self.SetEdgeColumn(column=80);
        # self.SetEdgeColour(edgeColour=STC_STYLE_COLOURS[u"URL_DARK"][u"EDGE"]);

        # ----------------------------
        # [11] SET END-OF-LINE:
        self.SetEOLMode(eolMode=stc.STC_EOL_CRLF);
        self.SetViewEOL(visible=False);
        self.SetSelEOLFilled(filled=False);

        # ----------------------------
        # [12] SET MARGINS:
        # [12.1] SET PADDING MARGINS:
        self.SetMarginLeft(pixelWidth=5);
        self.SetMarginRight(pixelWidth=5);
        # [12.2] SET DISPLAY MARGINS:
        # [12.2.1] SET LINE MARGIN (0):
        self.SetMarginWidth(margin=0, pixelWidth=40);
        self.SetMarginType(margin=0, marginType=stc.STC_MARGIN_NUMBER);
        self.SetMarginSensitive(margin=0, sensitive=False);
        self.SetMarginCursor(margin=0, cursor=stc.STC_CURSORNORMAL);
        # [12.2.2] SET SYMBOL MARGIN (2):
        self.SetMarginWidth(margin=1, pixelWidth=10);
        self.SetMarginType(margin=1, marginType=stc.STC_MARGIN_SYMBOL);
        self.SetMarginSensitive(margin=1, sensitive=True);
        self.SetMarginCursor(margin=1, cursor=stc.STC_CURSORNORMAL);
        self.SetMarginMask(margin=1, mask=stcdefs.STC_MARKER_MASK[u"CURRENT_LINE"]);
        self.MarkerDefine(
            markerNumber = stcdefs.STC_MARKER_NUMBER[u"CURRENT_LINE"],
            foreground   = self.style.colours[u"CURRENT_LINE"],
            background   = self.style.colours[u"CURRENT_LINE"],
            markerSymbol = stcdefs.STC_MARKER_SYMBOL[u"ARROW"],
        );
        # [12.3] SET FOLDING MARGIN:
        # self.SetFoldMarginColour(useSetting=True, back=u"#0022DD");
        # self.SetFoldMarginHiColour(useSetting=True, fore=u"#0022DD");
        # self.SetFoldFlags(flags=0x4 | 0x10);

        # ----------------------------
        # [13] SET FOLDING MARKERS:
        # self.MarkerDefine(markerNumber=stcdefs.STC_MARKER_NUMBER[u"FOLD"],          markerSymbol=stcdefs.STC_MARKER_SYMBOL[u"BOXPLUS"],           foreground=u"#0022DD", background=u"#FFFFFF");
        # self.MarkerDefine(markerNumber=stcdefs.STC_MARKER_NUMBER[u"FOLD_OPEN"],     markerSymbol=stcdefs.STC_MARKER_SYMBOL[u"BOXMINUS"],          foreground=u"#0022DD", background=u"#FFFFFF");
        # self.MarkerDefine(markerNumber=stcdefs.STC_MARKER_NUMBER[u"FOLD_END"],      markerSymbol=stcdefs.STC_MARKER_SYMBOL[u"BOXPLUSCONNECTED"],  foreground=u"#0022DD", background=u"#FFFFFF");
        # self.MarkerDefine(markerNumber=stcdefs.STC_MARKER_NUMBER[u"FOLD_OPEN_MID"], markerSymbol=stcdefs.STC_MARKER_SYMBOL[u"BOXMINUSCONNECTED"], foreground=u"#0022DD", background=u"#FFFFFF");
        # self.MarkerDefine(markerNumber=stcdefs.STC_MARKER_NUMBER[u"FOLD_MID_TAIL"], markerSymbol=stcdefs.STC_MARKER_SYMBOL[u"TCORNER"],           foreground=u"#0022DD", background=u"#FFFFFF");
        # self.MarkerDefine(markerNumber=stcdefs.STC_MARKER_NUMBER[u"FOLD_TAIL"],     markerSymbol=stcdefs.STC_MARKER_SYMBOL[u"LCORNER"],           foreground=u"#0022DD", background=u"#FFFFFF");
        # self.MarkerDefine(markerNumber=stcdefs.STC_MARKER_NUMBER[u"FOLD_SUB"],      markerSymbol=stcdefs.STC_MARKER_SYMBOL[u"VLINE"],             foreground=u"#0022DD", background=u"#FFFFFF");

        # ----------------------------
        # [14] SET SCROLLING:
        self.SetEndAtLastLine(endAtLastLine=False);
        self.SetYCaretPolicy(
            caretPolicy = stcdefs.STC_POLICY[u"CARET_EVEN"],
            caretSlop   = 5,
        );
        self.SetXCaretPolicy(
            caretPolicy = stcdefs.STC_POLICY[u"CARET_SLOP"]
                            | stcdefs.STC_POLICY[u"CARET_EVEN"],
            caretSlop   = 50,
        );
        self.SetVisiblePolicy(
            visiblePolicy = stc.STC_VISIBLE_SLOP,
            visibleSlop   = 0,
        );

        # ----------------------------
        # [15] SET INTERACTION:
        self.SetMouseDownCaptures(captures=True);
        self.SetMouseDwellTime(periodMilliseconds=1.0*1000); # cf. stc.STC_TIME_FOREVER (i.e. never raise the dwell events)

        # ----------------------------
        # [16] SET CALL TIPS:
        self.CallTipUseStyle(tabSize=10); # i.e. use the special self.style.indices[u"STC_CALLTIP"], instead of the default self.style.indices[u"DEFAULT"]
        self.CallTipSetPosition(above=False);
        # self.CallTipSetForegroundHighlight(fore=self.style.colours[u"CALLTIP_HIGHLIGHT"]);

        # ----------------------------
        # [17] SET ANNOTATIONS:
        # ...

        # ----------------------------
        # [18] SET GLOBAL STYLE DATA:
        # ...
        # ----------------------------

        # ----------------------------
        # [19] RE-SET THE TARGET WINDOW:
        self.Refresh();
        # ----------------------------

    def init_wx_style (self):
        u""" ... """
        # ----------------------------
        self.SetDoubleBuffered(on=False);
        # ...
        # ----------------------------

    def init_stc_handlers (self):
        u""" ... """
        # ----------------------------
        # [1] STC EVENTS:
        # [1.1] MODIFIED EVENT:
        self.SetModEventMask(
            mask = stcdefs.STC_PERFORMED_BITS["ANYONE"]           # (1) handle modifications done by anyone
                    | stcdefs.STC_MODIFIED_BITS["TEXT_ANYCHANGE"] # (2) handle only the text modifications
        );
        self.Bind(event=stc.EVT_STC_MODIFIED, source=self, handler=self.handle_stc_modified);
        # ...
        # [1.2] UPDATED EVENT:
        self.Bind(event=stc.EVT_STC_UPDATEUI, source=self, handler=self.handle_stc_update_ui);
        # ...
        # [1.3] PAINTED EVENT:
        self.Bind(event=stc.EVT_STC_PAINTED, source=self, handler=self.handle_stc_painted);
        # ...
        # [1.4] STYLE EVENT:
        # self.Bind(event=stc.EVT_STC_STYLENEEDED, source=self, handler=self.handle_stc_style_needed);
        # ...
        # [1.5] KEYBOARD EVENT:
        # self.Bind(event=stc.EVT_STC_KEY, source=self, handler=self.handle_stc_key);
        # ...
        # [1.6] CLICK EVENTS:
        # self.Bind(event=stc.EVT_STC_DOUBLECLICK, source=self, handler=self.handle_stc_double_click);
        # self.Bind(event=stc.EVT_STC_INDICATOR_CLICK, source=self, handler=self.handle_stc_indicator_click);
        # self.Bind(event=stc.EVT_STC_INDICATOR_RELEASE, source=self, handler=self.handle_stc_indicator_release);
        # self.Bind(event=stc.EVT_STC_HOTSPOT_CLICK, source=self, handler=self.handle_stc_hotspot_click);
        # self.Bind(event=stc.EVT_STC_HOTSPOT_DCLICK, source=self, handler=self.handle_stc_hotspot_double_click);
        # self.Bind(event=stc.EVT_STC_MARGINCLICK, source=self, handler=self.handle_stc_margin_click);
        # ...
        # [1.7] DWELL EVENTS:
        # self.Bind(event=stc.EVT_STC_DWELLSTART, source=self, handler=self.handle_stc_dwell_start);
        # self.Bind(event=stc.EVT_STC_DWELLEND, source=self,  handler=self.handle_stc_dwell_end);
        # ...
        # ----------------------------

    def init_wx_handlers (self):
        u""" ... """
        # ----------------------------
        # [2] WX (i.e. NON-STC) EVENTS:
        # [2.1] KEYBOARD EVENTS:
        self.Bind(event=wx.EVT_KEY_DOWN, source=self, handler=self.handle_wx_key_down); # to do: override with the accellerator?
        # ...
        # [2.2] MOUSE EVENTS:
        self.Bind(event=wx.EVT_RIGHT_DOWN, source=self, handler=self.handle_wx_right_down);
        # ...
        # [2.3] WINDOW EVENTS:
        # self.Bind(event=wx.EVT_IDLE, source=self.ContainingSizer, handler=self.handle_wx_idle); # n.b. that the source is the containing sizer (i.e. not self)
        # ...
        # ----------------------------

    def init_custom_handlers (self):
        u""" ... """
        # ----------------------------
        # [3] CUSTOM (i.e. NON-WX, NON-STC) EVENTS:
        dispatcher.connect(
            signal   = threadingdefs.GLOBAL_SIGNAL_INDEX[u"STC_INPUT_PAINTED"],
            sender   = threadingdefs.GLOBAL_SENDER_ANY,
            receiver = self.handle_repainted_input,
            weak     = True,
        );
        # ...
        # ----------------------------

    def init_stc_document (self):
        u""" ... """
        # ----------------------------
        self.document = self.GetDocPointer(); # i.e. get the pointer to the current, default stc document
        # ----------------------------

    def handle_stc_modified (self, event):
        u""" ... """
        # ----------------------------
        modification_type = event.GetModificationType();
        # ----------------------------
        if (modification_type & stcdefs.STC_MODIFIED_BITS["TEXT_PRECHANGE"]):
            if (modification_type & stcdefs.STC_MODIFIED_BITS["TEXT_PREINSERT"]):
                # ----------------------------
                # [1.1] GET PRE-MODIFICATION DATA:
                a0 = event.GetPosition(); # get the "TEXT_PREINSERT" modification start position
                b0 = a0 + event.GetLength(); # get the "TEXT_PREINSERT" modification end position
                A0 = self.LineFromPosition(pos=a0); # get the "TEXT_PREINSERT" modification start line
                B0 = A0; # get the "TEXT_PREINSERT" modification end line
                # [1.2] GET PRE-MODIFICATION SELECTION DATA:
                # x0 = self.GetSelectionStart(); # get the "TEXT_PREINSERT" selection start position
                # y0 = self.GetSelectionEnd(); # get the "TEXT_PREINSERT" selection end position
                # X0 = self.LineFromPosition(pos=x0); # get the "TEXT_PREINSERT" selection start line
                # Y0 = self.LineFromPosition(pos=y0); # get the "TEXT_PREINSERT" selection end line
                # ----------------------------
                # [2] SET PRE-MODIFICATION DATA:
                self.premodification_data = (a0, b0, A0, B0);
                # ----------------------------
            else: # i.e. (modification_type & stcdefs.STC_MODIFIED_BITS["TEXT_PREDELETE"])
                # ----------------------------
                # [1.1] GET PRE-MODIFICATION DATA:
                a0 = event.GetPosition(); # get the "TEXT_PREDELETE" modification start position
                b0 = a0 + event.GetLength(); # get the "TEXT_PREDELETE" modification end position
                A0 = self.LineFromPosition(pos=a0); # get the "TEXT_PREDELETE" modification start line
                B0 = self.LineFromPosition(pos=b0); # get the "TEXT_PREDELETE" modification end line
                # [1.2] GET PRE-MODIFICATION SELECTION DATA:
                # x0 = self.GetSelectionStart(); # get the "TEXT_PREDELETE" selection start position
                # y0 = self.GetSelectionEnd(); # get the "TEXT_PREDELETE" selection end position
                # X0 = self.LineFromPosition(pos=x0); # get the "TEXT_PREDELETE" selection start line
                # Y0 = self.LineFromPosition(pos=y0); # get the "TEXT_PREDELETE" selection end line
                # ----------------------------
                # [2] SET PRE-MODIFICATION DATA:
                self.premodification_data = (a0, b0, A0, B0);
                # ----------------------------
        elif (modification_type & stcdefs.STC_MODIFIED_BITS["TEXT_CHANGED"]):
            if (modification_type & stcdefs.STC_MODIFIED_BITS["TEXT_INSERTED"]):
                # ----------------------------
                # [1] GET LAST PRE-MODIFICATION DATA:
                a0, b0, A0, B0 = self.premodification_data; # get the "TEXT_PREINSERT" modification (or selection) data
                # ----------------------------
                # [2.1] GET MODIFICATION DATA:
                a1 = event.GetPosition(); # get the "TEXT_INSERTED" modification start position
                b1 = a1 + event.GetLength(); # get the "TEXT_INSERTED" modification end position
                A1 = self.LineFromPosition(pos=a1); # get the "TEXT_INSERTED" modification start line
                B1 = A1 + event.GetLinesAdded(); # get the "TEXT_INSERTED" modification end line
                # [2.1] GET MODIFICATION SELECTION DATA:
                # x1 = self.GetSelectionStart(); # get the "TEXT_INSERTED" selection start position
                # y1 = self.GetSelectionEnd(); # get the "TEXT_INSERTED" selection end position
                # X1 = self.LineFromPosition(pos=x1); # get the "TEXT_INSERTED" selection start line
                # Y1 = self.LineFromPosition(pos=y1); # get the "TEXT_INSERTED" selection end line
                # ----------------------------
                self.repaint = True;
                # ----------------------------
            else: # i.e. (modification_type & stcdefs.STC_MODIFIED_BITS["TEXT_DELETED"])
                # ----------------------------
                # [1] GET LAST PRE-MODIFICATION DATA:
                a0, b0, A0, B0 = self.premodification_data; # get the "TEXT_PREDELETE" modification (or selection) data
                # ----------------------------
                # [2.1] GET MODIFICATION DATA:
                a1 = event.GetPosition(); # get the "TEXT_DELETED" modification start position
                b1 = a1 + event.GetLength(); # get the "TEXT_DELETED" modification end position
                A1 = self.LineFromPosition(pos=a1); # get the "TEXT_DELETED" modification start line
                B1 = B0 + event.GetLinesAdded(); # get the "TEXT_DELETED" modification end line
                # [2.1] GET MODIFICATION SELECTION DATA:
                # x1 = self.GetSelectionStart(); # get the "TEXT_DELETED" selection start position
                # y1 = self.GetSelectionEnd(); # get the "TEXT_DELETED" selection end position
                # X1 = self.LineFromPosition(pos=x1); # get the "TEXT_DELETED" selection start line
                # Y1 = self.LineFromPosition(pos=y1); # get the "TEXT_DELETED" selection end line
                # ----------------------------
                self.repaint = True;
                # ----------------------------
        # elif (modification_type & stcdefs.STC_MODIFIED_BITS["STYLE_CHANGED"]): # the modification (but not the update!) masked out by the self.SetModEventMask()
        #     print u"<MODIFIED_STYLE_CHANGED>";
        # elif (modification_type & stcdefs.STC_MODIFIED_BITS["MARKER_CHANGED"]): # the modification (but not the update!) masked out by the self.SetModEventMask()
        #     print u"<MODIFIED_MARKER_CHANGED>";
        # elif (modification_type & stcdefs.STC_MODIFIED_BITS["ANNOTATION_CHANGED"]): # the modification (but not the update!) masked out by the self.SetModEventMask()
        #     print u"<MODIFIED_ANNOTATION_CHANGED>";
        else:
            pass;
        # ----------------------------
        # event.Skip(); # i.e. PROPAGATE THE EVENT FURTHER...
        # ----------------------------

    def handle_stc_update_ui (self, event):
        u""" ... """
        # ----------------------------
        update_type = event.GetUpdated();
        # ----------------------------
        if (update_type & stcdefs.STC_UPDATED_BITS["SELECTION"]): # i.e. SELECTION RANGE CHANGED
            # ----------------------------
            self.repaint = True;
            # ----------------------------
        elif (update_type & stcdefs.STC_UPDATED_BITS[u"V_SCROLL"]): # i.e. VERTICAL SCROLL RANGE CHANGED
            # ----------------------------
            pass;
            # ----------------------------
        else:
            pass;
        # ----------------------------
        event.Skip(); # i.e. PROPAGATE THIS EVENT FURTHER...
        # ----------------------------

    def handle_stc_painted (self, event):
        u""" ... """
        # ----------------------------
        if (self.repaint): # i.e. (self.repaint == True)
            # ----------------------------
            current_line = self.GetCurrentLine();
            self.MarkerDeleteAll(markerNumber=stcdefs.STC_MARKER_NUMBER[u"CURRENT_LINE"]);
            self.MarkerAdd(line=current_line, markerNumber=stcdefs.STC_MARKER_NUMBER[u"CURRENT_LINE"]);
            # ----------------------------
            dispatcher.send(sender=self, signal=threadingdefs.GLOBAL_SIGNAL_INDEX[u"STC_OUTPUT_PAINTED"], current_line=current_line);
            # ----------------------------
            self.repaint = False;
            # ----------------------------
        else: # i.e. (self.repaint == False)
            pass;
        # ----------------------------
        # event.Skip(); # i.e. propagate the event further...
        # ----------------------------

    def handle_stc_style_needed (self, event):
        u""" ... """
        # ----------------------------
        # [1] GET STYLE NEEDED RANGE:
        # [1.1] GET STYLE NEEDED START POSITION:
        # x = self.GetEndStyled();             # get the style needed range start position...
        # A = self.LineFromPosition(pos=x);    # get the style needed range start line...
        # a = self.PositionFromLine(line=A);   # get the style needed extended range start position...
        # [1.2] GET STYLE NEEDED END POSITION:
        # y = event.GetPosition();             # get the style needed range end position...
        # B = self.LineFromPosition(pos=y);    # get the style needed range end line...
        # b = self.GetLineEndPosition(line=B); # get the style needed extended range end position...
        # ----------------------------
        # [2] GET STYLE NEEDED RANGE TEXT:
        # [2.1] GET STYLE NEEDED RANGE UNICODE TEXT:
        # t = self.GetTextRange(startPos=x, endPos=y); # get the style needed range unicode text...
        # T = self.GetTextRange(startPos=a, endPos=b); # get the style needed extended range unicode text...
        # [2.2] GET STYLE NEEDED RANGE UTF-8 TEXT:
        # t = self.GetTextRangeUTF8(startPos=x, endPos=y); # get the style needed range utf-8 text...
        # T = self.GetTextRangeUTF8(startPos=a, endPos=b); # get the style needed extended range utf-8 text...
        # [2.3] GET STYLE NEEDED RANGE CELLS:
        # t = self.GetStyledText(startPos=x, endPos=y); # get the style needed range stc "cell" text...
        # T = self.GetStyledText(startPos=a, endPos=b); # get the style needed extended range stc "cell" text...
        # ----------------------------
        # [3] SET DOCUMENT STYLES:
        # set_document_styles = self.set_document_styles();
        # set_document_styles.start();
        pass;
        # ----------------------------
        # event.Skip(); # i.e. PROPAGATE THE EVENT FURTHER...
        # ----------------------------

    def handle_stc_key (self, event):
        u""" ... """
        # ----------------------------
        # ...
        event.Skip(); # i.e. PROPAGATE THE EVENT FURTHER...
        # ----------------------------

    def handle_wx_key_down (self, event):
        u""" ... """
        # ----------------------------
        # [1] GET KEY EVENT DATA:
        # [1.1] GET KEY EVENT KEY DATA:
        key     = event.GetKeyCode();
        charkey = event.GetUnicodeKey(); # UPPER CASE
        # [1.2] GET KEY EVENT MODIFICATION DATA:
        control = event.ControlDown();
        shift   = event.ShiftDown();
        alt     = event.AltDown();
        # [1.3] GET KEY EVENT POSITION DATA:
        # x       = event.GetX();
        # y       = event.GetY();
        # ----------------------------
        # [2] PROCESS KEY EVENT DATA:
        # [2.1] PROCESS MODIFIED KEY EVENT DATA:
        if (control and shift and alt): # i.e. Ctrl+Shift+Alt
            event.Skip();
        elif (control and shift): # i.e. Ctrl+Shift
            event.Skip();
        elif (control and alt): # i.e. Ctrl+Alt
            event.Skip();
        elif (control): # i.e. Ctrl
            if (charkey == ord(u"C")): # i.e. Ctrl+C (COPY)
                event.Skip();
            elif (charkey == ord(u"X")): # i.e. Ctrl+X (CUT)
                event.Skip();
            elif (charkey == ord(u"V")): # i.e. Ctrl+V (PASTE)
                event.Skip();
            else:
                event.Skip();
        elif (shift and alt): # i.e. Shift+Alt
            event.Skip();
        elif (shift): # i.e. Shift
            event.Skip();
        elif (alt): # i.e. Alt
            event.Skip();
        # ----------------------------
        # [2.2] PROCESS SPECIAL KEY EVENT DATA:
        # elif (key in (wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER)): # USED ("CONSUMED") BY STC!
        #     event.Skip();
        # elif (key in (wx.WXK_DELETE, wx.WXK_BACK)): # USED ("CONSUMED") BY STC!
        #     event.Skip();
        # elif (key in (wx.WXK_SPACE, wx.WXK_TAB)): # USED ("CONSUMED") BY STC!
        #     event.Skip();
        # elif (key == wx.WXK_F1): # i.e. F1
        #     event.Skip();
        # elif (key == wx.WXK_F8): # i.e. F8
        #     event.Skip();
        elif (key == wx.WXK_F9): # i.e. F9
            self.toggle_wrap_mode();
        # elif (key == wx.WXK_F10): # i.e. F10
        #     event.Skip();
        # elif (key == wx.WXK_F11): # i.e. F11
        #     event.Skip();
        # elif (key == wx.WXK_F12): # i.e. F12
        #     event.Skip();
        # ...
        # ----------------------------
        # [2.3] PROCESS LITERAL KEY EVENT DATA:
        # elif (key == wx.WXK_NUMPAD0): # USED ("CONSUMED") BY STC!
        #     event.Skip();
        # elif (key == wx.WXK_NUMPAD1): # USED ("CONSUMED") BY STC!
        #     event.Skip();
        # elif (charkey == ord(u"C")): # USED ("CONSUMED") BY STC!
        #     event.Skip();
        # elif (charkey == ord(u"Č")): # USED ("CONSUMED") BY STC!
        #     event.Skip();
        # ...
        # ----------------------------
        # [3] NOTHING PROCESSED:
        else:
            event.Skip(); # i.e. PROPAGATE THE EVENT FURTHER...
        # ----------------------------

    def handle_wx_right_down (self, event):
        u""" ... """
        # ----------------------------
        # self.right_down = event.GetPosition();
        # self.PopupMenu(menu=WX_MENU_STC(parent=self));
        # ----------------------------
        event.Skip(); # i.e. PROPAGATE THE EVENT FURTHER...
        # ----------------------------

    def handle_wx_idle (self, event):
        u""" ... """
        # ----------------------------
        pass;
        # ----------------------------
        # event.RequestMore(); # i.e. RE-RAISE THE IDLE EVENT (CPU EXPENSIVE, THOUGH)
        event.Skip(); # i.e. propagate the event further...
        # ----------------------------

    def handle_repainted_input (self, current_line):
        u""" ... """
        # ----------------------------
        if (not self.IsFrozen()): # i.e. (self.IsFrozen() == False)
            current_line = min(current_line, self.GetLineCount()-1);
            wx.CallAfter(self.MarkerDeleteAll, markerNumber=stcdefs.STC_MARKER_NUMBER[u"CURRENT_LINE"]);
            wx.CallAfter(self.MarkerAdd, line=current_line, markerNumber=stcdefs.STC_MARKER_NUMBER[u"CURRENT_LINE"]);
            wx.CallAfter(self.GotoLine, line=current_line);
        else: # i.e. (self.IsFrozen() == True)
            pass;
        # ----------------------------

    @GET_THREAD(name=u"transliterate", daemon=True)
    def transliterate (self, source_string, current_line):
        u""" ... """
        # ----------------------------
        if (not self.transliterating): # i.e. (self.transliterating == False)
            # ----------------------------
            self.t = time.clock();
            self.transliterating = True;
            # ----------------------------
            self.Freeze();
            self.SetReadOnly(readOnly=False);
            # ----------------------------
            self.ClearAll();
            # ----------------------------
            segments = self.transliterator.segment(source_string=source_string);
            for (style, text) in segments:
                a = self.GetTextLength();
                self.AppendTextUTF8(text=text);
                b = self.GetTextLength(); # = a + len(text)
                if (style): # i.e. (style == 1)
                    wx.CallAfter(self.StartStyling, pos=a, mask=stcdefs.STC_STYLE_MASKS[u"5_BIT"]);
                    wx.CallAfter(self.SetStyling, length=b-a, style=self.style.indices[u"DEFAULT"]);
                else: # i.e. (style == 0)
                    wx.CallAfter(self.StartStyling, pos=a, mask=stcdefs.STC_STYLE_MASKS[u"5_BIT"]);
                    wx.CallAfter(self.SetStyling, length=b-a, style=self.style.indices[u"FROZEN"]);
            # for (style, string)
            # ----------------------------
            wx.CallAfter(self.transliteration_done, current_line=current_line);
            # ----------------------------
        else: # i.e. (self.transliterating == True)
            self.transliteration_needed = True;
        # ----------------------------

    def transliteration_done (self, current_line):
        u""" ... """
        # ----------------------------
        wx.CallAfter(self.SetReadOnly, readOnly=True);
        wx.CallAfter(self.Thaw);
        # ----------------------------
        self.t = time.clock() - self.t;
        dispatcher.send(sender=self, signal=threadingdefs.GLOBAL_SIGNAL_INDEX[u"STC_TRANSLITERATION_DONE"], t=self.t);
        wx.CallAfter(self.handle_repainted_input, current_line=current_line);
        # ----------------------------
        self.transliterating = False;
        # ----------------------------

    def load_text (self, path):
        u""" ... """
        # ----------------------------
        self.ClearAll();
        # ----------------------------
        file = codecs.open(filename=path, mode=u"r", encoding=u"utf-8");
        text = file.read();
        file.close();
        # ----------------------------
        wx.CallAfter(self.SetText, text=text);
        # ----------------------------

    @GET_THREAD(name=u"save_text", daemon=True)
    def save_text (self, path):
        # ----------------------------
        file = codecs.open(filename=path, mode=u"w", encoding=u"utf-8");
        text = self.GetText();
        file.write(text);
        file.close();
        # ----------------------------

    def toggle_wrap_mode (self):
        u""" ... """
        # ----------------------------
        wrap_mode = self.GetWrapMode();
        wrap_name = stcdefs.STC_WRAP_NAME[wrap_mode];
        # ----------------------------
        if (wrap_name == u"NONE"):
            self.SetWrapMode(mode=stcdefs.STC_WRAP_MODE[u"WORD"]);
        elif (wrap_name == u"WORD"):
            self.SetWrapMode(mode=stcdefs.STC_WRAP_MODE[u"CHAR"]);
        else: # i.e. (wrap_name == u"CHAR")
            self.SetWrapMode(mode=stcdefs.STC_WRAP_MODE[u"NONE"]);
        # ----------------------------

# ------------------------------------------------------------------------------

class WX_STC_INPUT (stc.StyledTextCtrl):
    u"""
        -- SOURCES (2015-05-01):

        [001]
         "Scintilla (software) - Wikipedia, the free encyclopedia"
         http://en.wikipedia.org/wiki/Scintilla_(editing_component)
         [2015-04-22 18:55:28 (UTC+01:00), by Luka Tolitch]

        [002]
         "Scintilla and SciTE"
         http://www.scintilla.org/
         [2014-10-30 16:42:27 (UTC+01:00), by Luka Tolitch]

        [003]
         "SciTE"
         http://www.scintilla.org/SciTEDoc.html
         [2014-10-30 16:41:02 (UTC+01:00), by Luka Tolitch]

        [004]
         "Scintilla and SciTE Related Sites"
         http://www.scintilla.org/ScintillaRelated.html
         [2014-10-30 16:43:47 (UTC+01:00), by Luka Tolitch]

        [005]
         "wxStyledTextCtrl - Home"
         http://www.yellowbrain.com/stc/index.html
         [2014-09-21 15:22:03 (UTC+01:00), by Luka Tolitch]

        [006]
         "TextEditors Wiki: ScintillaEditorFamily"
         http://texteditors.org/cgi-bin/wiki.pl?ScintillaEditorFamily
         [2014-11-11 13:08:37 (UTC+01:00), by Luka Tolitch]

        [007]
         "TextEditors Wiki: HomePage"
         http://texteditors.org/cgi-bin/wiki.pl?HomePage
         [2014-11-11 13:09:51 (UTC+01:00), by Luka Tolitch]

        [008]
         "http://sphere.sourceforge.net/flik/docs/scintilla-contain..."
         http://sphere.sourceforge.net/flik/docs/scintilla-container_lexer.html
         [2014-10-30 17:28:44 (UTC+01:00), by Luka Tolitch]

        [009]
         "http://www.scintilla.org/Lexer.txt"
         http://www.scintilla.org/Lexer.txt
         [2014-10-30 17:29:21 (UTC+01:00), by Luka Tolitch]

        [010]
         "wxPython-users - Printing from STC"
         http://wxpython-users.1045709.n5.nabble.com/Printing-from-STC-td2355272.html
         [2015-05-01 12:36:49 (UTC+01:00), by Luka Tolitch]

        [011]
         "SciTE Text Editor v3.5.1"
         http://opensource.ebswift.com/SciTEInstaller/
         [2014-11-11 12:42:37 (UTC+01:00), by Luka Tolitch]

        [012]
         "Newest 'scintilla' Questions - Page 2 - Stack Overflow"
         http://stackoverflow.com/questions/tagged/scintilla?page=2&sort=newest&pagesize=15
         [2014-11-11 13:17:10 (UTC+01:00), by Luka Tolitch]

        [013]
         "python - wxPython - StyledTextCtrl get currently visible ..."
         http://stackoverflow.com/questions/19896965/wxpython-styledtextctrl-get-currently-visible-lines
         [2014-11-11 13:17:57 (UTC+01:00), by Luka Tolitch]

        [014]
         "wxPython-users | Mailing List Archive"
         http://wxpython-users.1045709.n5.nabble.com/
         [2014-11-15 18:32:44 (UTC+01:00), by Luka Tolitch]

        [015]
         "Gmane -- Search"
         http://search.gmane.org/?query=caret&group=gmane.comp.python.wxpython
         [2014-11-15 18:24:19 (UTC+01:00), by Luka Tolitch]

        [016]
         "wxPython-users - Search for 'StyledTextCtrl'"
         http://wxpython-users.1045709.n5.nabble.com/template/NamlServlet.jtp?macro=search_page&node=2269151&query=StyledTextCtrl
         [2014-11-15 18:33:07 (UTC+01:00), by Luka Tolitch]

        [017]
         "Users of wxPython, the the wxWidgets port to Python"
         http://blog.gmane.org/gmane.comp.python.wxpython
         [2014-11-15 18:23:41 (UTC+01:00), by Luka Tolitch]

        [018]
         "Users of wxPython, the the wxWidgets port to Python"
         http://comments.gmane.org/gmane.comp.python.wxpython/18325
         [2014-11-15 18:14:12 (UTC+01:00), by Luka Tolitch]

        [019]
         "Gmane Loom"
         http://article.gmane.org/gmane.comp.python.wxpython/65120
         [2014-11-15 18:28:46 (UTC+01:00), by Luka Tolitch]

        [020]
         "StyledTextCtrl Lexer Quick Reference - wxPyWiki"
         http://wiki.wxpython.org/StyledTextCtrl Lexer Quick Reference
         [2015-04-27 07:43:29 (UTC+01:00), by Luka Tolitch]

        [021]
         "wxpython - wxWidgets: how to change caret style in Styled..."
         http://stackoverflow.com/questions/800332/wxwidgets-how-to-change-caret-style-in-styledtextctrl-sending-a-command-to-sci
         [2015-05-01 14:17:10 (UTC+01:00), by Luka Tolitch]
    """

    _set_document_styles = cutils.set_document_styles; # self._set_document_styles

    def __init__ (self,
        parent,
        stc_style,
        id        = wx.ID_ANY,
        pos       = wx.DefaultPosition,
        size      = wx.DefaultSize,
        style     = wx.SUNKEN_BORDER
    ):
        stc.StyledTextCtrl.__init__(self, parent=parent, id=id, pos=pos, size=size, style=style);
        self.style = stcdefs.STC_STYLE(name=stc_style);
        # ----------------------------
        self.init_stc_style();
        self.init_wx_style();
        self.init_stc_handlers();
        self.init_wx_handlers();
        self.init_custom_handlers();
        self.init_stc_document();
        # ----------------------------
        self.premodification_data = (0, 0, 0, 0);
        self.indicated_lines = [0, 0];
        # self.need_indication = True;
        self.repaint = True;
        self.styling = False;
        # self.right_down = (-1, -1);
        # ...
        # ----------------------------
        self.root           = self.GetTopLevelParent();
        self.transliterator = self.root.transliterator;
        # ----------------------------

    def init_stc_style (self):
        u""" SET THE TARGET STC WINDOW STYLES """
        # ----------------------------
        # [1] SET GENERAL SETTINGS:
        self.SetTechnology(technology=stc.STC_TECHNOLOGY_DEFAULT);
        self.SetBufferedDraw(buffered=False); # i.e. "DOUBLE" buffered...
        self.SetTwoPhaseDraw(twoPhase=True);
        self.SetLayoutCache(mode=stcdefs.STC_CACHE_TYPE[u"DOCUMENT"]);
        self.SetCodePage(codePage=stc.STC_CP_UTF8);
        self.SetKeysUnicode(keysUnicode=True);
        self.SetReadOnly(readOnly=False);
        # ...

        # ----------------------------
        # [2] SET LEXER:
        self.SetLexer(lexer=stc.STC_LEX_CONTAINER);
        # [2.1] SET LEXER STYLES:
        for style_spec in self.style.specs.itervalues():
            self.StyleSetSpec(**style_spec);
        # for (style_spec)
        # [2.2] SET LEXER PROPERTIES:
        # ...

        # ----------------------------
        # [3] SET CHARACTER SETS:
        # [3.1] EITHER SET DEFAULT CHARACTER SETS:
        self.SetCharsDefault(); # i.e. set the Scintilla default character sets
        # [3.2] OR SET CUSTOM CHARACTER SETS:
        # self.SetWordChars(characters=u"ABCČĆDĐEFGHIJKLMNOPQRSŠTUVWZŽXYabcčćdđefghijklmnopqrsštuvwzžxyАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдежзийклмнопрстуфхцчшщъыьэюя.,:; _-+%0123456789");
        # self.SetWhitespaceChars(characters=u" \t\n\r");
        # self.SetPunctuationChars(characters=u".,:;!?");

        # ----------------------------
        # [4] SET WHITESPACE:
        self.SetViewWhiteSpace(viewWS=False);
        self.SetWhitespaceForeground(useSetting=True, fore=self.style.colours[u"WHITESPACE_FOREGROUND"]);
        #self.SetWhitespaceBackground(useSetting=True, back=self.style.colours[u"WHITESPACE_BACKGROUND"]);
        self.SetExtraAscent(extraAscent=0.0);
        self.SetExtraDescent(extraDescent=0);

        # ----------------------------
        # [5] SET CARET:
        self.SetCaretStyle(caretStyle=stc.STC_CARETSTYLE_LINE);
        self.SetCaretPeriod(periodMilliseconds=200);
        self.SetCaretWidth(pixelWidth=3);
        self.SetCaretLineVisible(show=True);
        self.SetCaretForeground(fore=self.style.colours[u"CARET_FOREGROUND"]);
        self.SetCaretLineBackground(back=self.style.colours[u"CARET_BACKGROUND"]);
        #self.SetCaretLineBackAlpha(alpha=stc.STC_ALPHA_NOALPHA);

        # ----------------------------
        # [6] SET SELECTION:
        # [6.1] SET SELECTION STYLE:
        #self.SetSelForeground(useSetting=True, fore=self.style.colours[u"SELECTION_FOREGROUND"]);
        self.SetSelBackground(useSetting=True, back=self.style.colours[u"SELECTION_BACKGROUND"]);
        # self.SetSelectionMode(mode=STC_SELECTION_TYPE["THIN"]);
        # [6.2] SET MULTIPLE SELECTION:
        self.SetMultipleSelection(multipleSelection=False);
        # self.SetAdditionalSelectionTyping(additionalSelectionTyping=False);
        # self.SetMultiPaste(multiPaste=stc.STC_MULTIPASTE_ONCE);
        # [6.3] SET SELECTION STYLE:
        # self.SetUndoCollection(collectUndo=True);
        # ...

        # ----------------------------
        # [7] SET HOTSPOT STYLE:
        # self.StyleSetHotSpot(style=self.style.specs[u"DOMAIN"][u"styleNum"], hotspot=True);
        # self.SetHotspotActiveForeground(useSetting=True, fore=self.style.colours[u"HOTSPOT_FOREGROUND"]);
        # self.SetHotspotActiveBackground(useSetting=True, back=self.style.colours[u"HOTSPOT_BACKGROUND"]);
        # self.SetHotspotActiveUnderline(underline=True);
        # self.SetHotspotSingleLine(singleLine=True);

        # ----------------------------
        # [8] SET INDICATORS:
        # [8.1] SET FIRST INDICATOR:
        # self.IndicatorSetStyle(indic=stcdefs.STC_INDICATOR_INDEX[u"FILE"], style=stcdefs.STC_INDICATOR_STYLE[u"BOX"]);
        # self.IndicatorSetForeground(indic=stcdefs.STC_INDICATOR_INDEX[u"FILE"], fore=self.style.colours[u"INDICATOR_FILE"]);
        # self.IndicatorSetUnder(indic=stcdefs.STC_INDICATOR_INDEX[u"FILE"], under=True);
        # self.IndicatorSetAlpha(indicator=stcdefs.STC_INDICATOR_INDEX[u"FILE"], alpha=255);
        # self.IndicatorSetOutlineAlpha(indicator=stcdefs.STC_INDICATOR_INDEX[u"FILE"], alpha=255);
        # [8.1.2] SET SECOND INDICATOR:
        # ...
        # [8.1.3] SET THIRD INDICATOR:
        # ...
        # [8.2] SELECT CURRENT INDICATOR:
        # self.SetIndicatorCurrent(indicator=stcdefs.STC_INDICATOR_INDEX[u"FILE"]);

        # ----------------------------
        # [9] SET INDENTATION:
        self.SetUseTabs(useTabs=True);
        self.SetTabWidth(tabWidth=4);
        # self.SetIndent(indentSize=4);
        # self.SetTabIndents(tabIndents=False);
        # self.SetBackSpaceUnIndents(tabIndents=False);
        self.SetIndentationGuides(indentView=True);

        # ----------------------------
        # [10] SET WRAPPING:
        # [10.1] SET LINE WRAPPING:
        self.SetWrapMode(mode=stcdefs.STC_WRAP_MODE[u"NONE"]);
        self.SetWrapStartIndent(indent=1);
        self.SetWrapIndentMode(mode=stcdefs.STC_WRAP_INDENT_MODE[u"FIXED"]);
        self.SetWrapVisualFlags(wrapVisualFlags=stcdefs.STC_WRAP_FLAG[u"END"]);
        self.SetWrapVisualFlagsLocation(wrapVisualFlagsLocation=stcdefs.STC_WRAP_LOC[u"TEXT_END"]);
        # [10.2] SET LONG LINES MARKING:
        # self.SetEdgeMode(mode=stc.STC_EDGE_LINE);
        # self.SetEdgeColumn(column=80);
        # self.SetEdgeColour(edgeColour=STC_STYLE_COLOURS[u"URL_DARK"][u"EDGE"]);

        # ----------------------------
        # [11] SET END-OF-LINE:
        self.SetEOLMode(eolMode=stc.STC_EOL_CRLF);
        self.SetViewEOL(visible=False);
        self.SetSelEOLFilled(filled=False);

        # ----------------------------
        # [12] SET MARGINS:
        # [12.1] SET PADDING MARGINS:
        self.SetMarginLeft(pixelWidth=5);
        self.SetMarginRight(pixelWidth=5);
        # [12.2] SET DISPLAY MARGINS:
        # [12.2.1] SET LINE MARGIN (0):
        self.SetMarginWidth(margin=0, pixelWidth=40);
        self.SetMarginType(margin=0, marginType=stc.STC_MARGIN_NUMBER);
        self.SetMarginSensitive(margin=0, sensitive=False);
        self.SetMarginCursor(margin=0, cursor=stc.STC_CURSORNORMAL);
        # [12.2.2] SET SYMBOL MARGIN (2):
        self.SetMarginWidth(margin=1, pixelWidth=10);
        self.SetMarginType(margin=1, marginType=stc.STC_MARGIN_SYMBOL);
        self.SetMarginSensitive(margin=1, sensitive=True);
        self.SetMarginCursor(margin=1, cursor=stc.STC_CURSORNORMAL);
        self.SetMarginMask(margin=1, mask=stcdefs.STC_MARKER_MASK[u"CURRENT_LINE"]);
        self.MarkerDefine(
            markerNumber = stcdefs.STC_MARKER_NUMBER[u"CURRENT_LINE"],
            foreground   = self.style.colours[u"CURRENT_LINE"],
            background   = self.style.colours[u"CURRENT_LINE"],
            markerSymbol = stcdefs.STC_MARKER_SYMBOL[u"ARROW"],
        );
        # [12.3] SET FOLDING MARGIN:
        # self.SetFoldMarginColour(useSetting=True, back=u"#0022DD");
        # self.SetFoldMarginHiColour(useSetting=True, fore=u"#0022DD");
        # self.SetFoldFlags(flags=0x4 | 0x10);

        # ----------------------------
        # [13] SET FOLDING MARKERS:
        # self.MarkerDefine(markerNumber=stcdefs.STC_MARKER_NUMBER[u"FOLD"],          markerSymbol=stcdefs.STC_MARKER_SYMBOL[u"BOXPLUS"],           foreground=u"#0022DD", background=u"#FFFFFF");
        # self.MarkerDefine(markerNumber=stcdefs.STC_MARKER_NUMBER[u"FOLD_OPEN"],     markerSymbol=stcdefs.STC_MARKER_SYMBOL[u"BOXMINUS"],          foreground=u"#0022DD", background=u"#FFFFFF");
        # self.MarkerDefine(markerNumber=stcdefs.STC_MARKER_NUMBER[u"FOLD_END"],      markerSymbol=stcdefs.STC_MARKER_SYMBOL[u"BOXPLUSCONNECTED"],  foreground=u"#0022DD", background=u"#FFFFFF");
        # self.MarkerDefine(markerNumber=stcdefs.STC_MARKER_NUMBER[u"FOLD_OPEN_MID"], markerSymbol=stcdefs.STC_MARKER_SYMBOL[u"BOXMINUSCONNECTED"], foreground=u"#0022DD", background=u"#FFFFFF");
        # self.MarkerDefine(markerNumber=stcdefs.STC_MARKER_NUMBER[u"FOLD_MID_TAIL"], markerSymbol=stcdefs.STC_MARKER_SYMBOL[u"TCORNER"],           foreground=u"#0022DD", background=u"#FFFFFF");
        # self.MarkerDefine(markerNumber=stcdefs.STC_MARKER_NUMBER[u"FOLD_TAIL"],     markerSymbol=stcdefs.STC_MARKER_SYMBOL[u"LCORNER"],           foreground=u"#0022DD", background=u"#FFFFFF");
        # self.MarkerDefine(markerNumber=stcdefs.STC_MARKER_NUMBER[u"FOLD_SUB"],      markerSymbol=stcdefs.STC_MARKER_SYMBOL[u"VLINE"],             foreground=u"#0022DD", background=u"#FFFFFF");

        # ----------------------------
        # [14] SET SCROLLING:
        self.SetEndAtLastLine(endAtLastLine=False);
        self.SetYCaretPolicy(
            caretPolicy = stcdefs.STC_POLICY[u"CARET_EVEN"],
            caretSlop   = 5,
        );
        self.SetXCaretPolicy(
            caretPolicy = stcdefs.STC_POLICY[u"CARET_SLOP"]
                            | stcdefs.STC_POLICY[u"CARET_EVEN"],
            caretSlop   = 50,
        );
        self.SetVisiblePolicy(
            visiblePolicy = stc.STC_VISIBLE_SLOP,
            visibleSlop   = 0,
        );

        # ----------------------------
        # [15] SET INTERACTION:
        self.SetMouseDownCaptures(captures=True);
        self.SetMouseDwellTime(periodMilliseconds=1.0*1000); # cf. stc.STC_TIME_FOREVER (i.e. never raise the dwell events)

        # ----------------------------
        # [16] SET CALL TIPS:
        self.CallTipUseStyle(tabSize=10); # i.e. use the special self.style.indices[u"STC_CALLTIP"], instead of the default self.style.indices[u"DEFAULT"]
        self.CallTipSetPosition(above=False);
        # self.CallTipSetForegroundHighlight(fore=self.style.colours[u"CALLTIP_HIGHLIGHT"]);

        # ----------------------------
        # [17] SET ANNOTATIONS:
        # ...

        # ----------------------------
        # [18] SET GLOBAL STYLE DATA:
        # ...
        # ----------------------------

        # ----------------------------
        # [19] RE-SET THE TARGET WINDOW:
        self.Refresh();
        # ----------------------------

    def init_wx_style (self):
        u""" ... """
        # ----------------------------
        self.SetDoubleBuffered(on=False);
        # ...
        # ----------------------------

    def init_stc_handlers (self):
        u""" ... """
        # ----------------------------
        # [1] STC EVENTS:
        # [1.1] MODIFIED EVENT:
        self.SetModEventMask(
            mask = stcdefs.STC_PERFORMED_BITS["ANYONE"]           # (1) handle modifications done by anyone
                    | stcdefs.STC_MODIFIED_BITS["TEXT_ANYCHANGE"] # (2) handle only the text modifications
        );
        self.Bind(event=stc.EVT_STC_MODIFIED, source=self, handler=self.handle_stc_modified);
        # ...
        # [1.2] UPDATED EVENT:
        self.Bind(event=stc.EVT_STC_UPDATEUI, source=self, handler=self.handle_stc_update_ui);
        # ...
        # [1.3] PAINTED EVENT:
        self.Bind(event=stc.EVT_STC_PAINTED, source=self, handler=self.handle_stc_painted);
        # ...
        # [1.4] STYLE EVENT:
        self.Bind(event=stc.EVT_STC_STYLENEEDED, source=self, handler=self.handle_stc_style_needed);
        # ...
        # [1.5] KEYBOARD EVENT:
        # self.Bind(event=stc.EVT_STC_KEY, source=self, handler=self.handle_stc_key);
        # ...
        # [1.6] CLICK EVENTS:
        # self.Bind(event=stc.EVT_STC_DOUBLECLICK, source=self, handler=self.handle_stc_double_click);
        # self.Bind(event=stc.EVT_STC_INDICATOR_CLICK, source=self, handler=self.handle_stc_indicator_click);
        # self.Bind(event=stc.EVT_STC_INDICATOR_RELEASE, source=self, handler=self.handle_stc_indicator_release);
        # self.Bind(event=stc.EVT_STC_HOTSPOT_CLICK, source=self, handler=self.handle_stc_hotspot_click);
        # self.Bind(event=stc.EVT_STC_HOTSPOT_DCLICK, source=self, handler=self.handle_stc_hotspot_double_click);
        # self.Bind(event=stc.EVT_STC_MARGINCLICK, source=self, handler=self.handle_stc_margin_click);
        # ...
        # [1.7] DWELL EVENTS:
        # self.Bind(event=stc.EVT_STC_DWELLSTART, source=self, handler=self.handle_stc_dwell_start);
        # self.Bind(event=stc.EVT_STC_DWELLEND, source=self,  handler=self.handle_stc_dwell_end);
        # ...
        # ----------------------------

    def init_wx_handlers (self):
        u""" ... """
        # ----------------------------
        # [2] WX (i.e. NON-STC) EVENTS:
        # [2.1] KEYBOARD EVENTS:
        self.Bind(event=wx.EVT_KEY_DOWN, source=self, handler=self.handle_wx_key_down);
        # ...
        # [2.2] MOUSE EVENTS:
        # self.Bind(event=wx.EVT_RIGHT_DOWN, source=self, handler=self.handle_wx_right_down);
        # ...
        # [2.3] WINDOW EVENTS:
        # self.Bind(event=wx.EVT_IDLE, source=self.ContainingSizer, handler=self.handle_wx_idle); # n.b. that the source is the containing sizer (i.e. not self)
        # self.Bind(event=wx.EVT_SET_FOCUS, source=self, handler=self.handle_wx_set_focus);
        # ...
        # ----------------------------

    def init_custom_handlers (self):
        u""" ... """
        # ----------------------------
        # [3] CUSTOM (i.e. NON-WX, NON-STC) EVENTS:
        pass;
        # ----------------------------

    def init_stc_document (self):
        u""" ... """
        # ----------------------------
        self.document = self.GetDocPointer(); # i.e. get the pointer to the current, default stc document
        # ----------------------------

    def handle_stc_modified (self, event):
        u""" ... """
        # ----------------------------
        modification_type = event.GetModificationType();
        # ----------------------------
        if (modification_type & stcdefs.STC_MODIFIED_BITS["TEXT_PRECHANGE"]):
            if (modification_type & stcdefs.STC_MODIFIED_BITS["TEXT_PREINSERT"]):
                # ----------------------------
                # [1.1] GET PRE-MODIFICATION DATA:
                a0 = event.GetPosition(); # get the "TEXT_PREINSERT" modification start position
                b0 = a0 + event.GetLength(); # get the "TEXT_PREINSERT" modification end position
                A0 = self.LineFromPosition(pos=a0); # get the "TEXT_PREINSERT" modification start line
                B0 = A0; # get the "TEXT_PREINSERT" modification end line
                # [1.2] GET PRE-MODIFICATION SELECTION DATA:
                # x0 = self.GetSelectionStart(); # get the "TEXT_PREINSERT" selection start position
                # y0 = self.GetSelectionEnd(); # get the "TEXT_PREINSERT" selection end position
                # X0 = self.LineFromPosition(pos=x0); # get the "TEXT_PREINSERT" selection start line
                # Y0 = self.LineFromPosition(pos=y0); # get the "TEXT_PREINSERT" selection end line
                # ----------------------------
                # [2] SET PRE-MODIFICATION DATA:
                self.premodification_data = (a0, b0, A0, B0);
                # ----------------------------
            else: # i.e. (modification_type & stcdefs.STC_MODIFIED_BITS["TEXT_PREDELETE"])
                # ----------------------------
                # [1.1] GET PRE-MODIFICATION DATA:
                a0 = event.GetPosition(); # get the "TEXT_PREDELETE" modification start position
                b0 = a0 + event.GetLength(); # get the "TEXT_PREDELETE" modification end position
                A0 = self.LineFromPosition(pos=a0); # get the "TEXT_PREDELETE" modification start line
                B0 = self.LineFromPosition(pos=b0); # get the "TEXT_PREDELETE" modification end line
                # [1.2] GET PRE-MODIFICATION SELECTION DATA:
                # x0 = self.GetSelectionStart(); # get the "TEXT_PREDELETE" selection start position
                # y0 = self.GetSelectionEnd(); # get the "TEXT_PREDELETE" selection end position
                # X0 = self.LineFromPosition(pos=x0); # get the "TEXT_PREDELETE" selection start line
                # Y0 = self.LineFromPosition(pos=y0); # get the "TEXT_PREDELETE" selection end line
                # ----------------------------
                # [2] SET PRE-MODIFICATION DATA:
                self.premodification_data = (a0, b0, A0, B0);
                # ----------------------------
        elif (modification_type & stcdefs.STC_MODIFIED_BITS["TEXT_CHANGED"]):
            if (modification_type & stcdefs.STC_MODIFIED_BITS["TEXT_INSERTED"]):
                # ----------------------------
                # [1] GET LAST PRE-MODIFICATION DATA:
                a0, b0, A0, B0 = self.premodification_data; # get the "TEXT_PREINSERT" modification (or selection) data
                # ----------------------------
                # [2.1] GET MODIFICATION DATA:
                a1 = event.GetPosition(); # get the "TEXT_INSERTED" modification start position
                b1 = a1 + event.GetLength(); # get the "TEXT_INSERTED" modification end position
                A1 = self.LineFromPosition(pos=a1); # get the "TEXT_INSERTED" modification start line
                B1 = A1 + event.GetLinesAdded(); # get the "TEXT_INSERTED" modification end line
                # [2.1] GET MODIFICATION SELECTION DATA:
                # x1 = self.GetSelectionStart(); # get the "TEXT_INSERTED" selection start position
                # y1 = self.GetSelectionEnd(); # get the "TEXT_INSERTED" selection end position
                # X1 = self.LineFromPosition(pos=x1); # get the "TEXT_INSERTED" selection start line
                # Y1 = self.LineFromPosition(pos=y1); # get the "TEXT_INSERTED" selection end line
                # ----------------------------
                if self.root.main_panel.controls.interactive_checkbox.IsChecked():
                    wx.CallAfter(self.signal_transliterate);
                else:
                    pass;
                self.repaint = True;
                # ----------------------------
            else: # i.e. (modification_type & stcdefs.STC_MODIFIED_BITS["TEXT_DELETED"])
                # ----------------------------
                # [1] GET LAST PRE-MODIFICATION DATA:
                a0, b0, A0, B0 = self.premodification_data; # get the "TEXT_PREDELETE" modification (or selection) data
                # ----------------------------
                # [2.1] GET MODIFICATION DATA:
                a1 = event.GetPosition(); # get the "TEXT_DELETED" modification start position
                b1 = a1 + event.GetLength(); # get the "TEXT_DELETED" modification end position
                A1 = self.LineFromPosition(pos=a1); # get the "TEXT_DELETED" modification start line
                B1 = B0 + event.GetLinesAdded(); # get the "TEXT_DELETED" modification end line
                # [2.1] GET MODIFICATION SELECTION DATA:
                # x1 = self.GetSelectionStart(); # get the "TEXT_DELETED" selection start position
                # y1 = self.GetSelectionEnd(); # get the "TEXT_DELETED" selection end position
                # X1 = self.LineFromPosition(pos=x1); # get the "TEXT_DELETED" selection start line
                # Y1 = self.LineFromPosition(pos=y1); # get the "TEXT_DELETED" selection end line
                # ----------------------------
                if self.root.main_panel.controls.interactive_checkbox.IsChecked():
                    wx.CallAfter(self.signal_transliterate);
                else:
                    pass;
                self.repaint = True;
                # ----------------------------
        # elif (modification_type & stcdefs.STC_MODIFIED_BITS["STYLE_CHANGED"]): # the modification (but not the update!) masked out by the self.SetModEventMask()
        #     print u"<MODIFIED_STYLE_CHANGED>";
        # elif (modification_type & stcdefs.STC_MODIFIED_BITS["MARKER_CHANGED"]): # the modification (but not the update!) masked out by the self.SetModEventMask()
        #     print u"<MODIFIED_MARKER_CHANGED>";
        # elif (modification_type & stcdefs.STC_MODIFIED_BITS["ANNOTATION_CHANGED"]): # the modification (but not the update!) masked out by the self.SetModEventMask()
        #     print u"<MODIFIED_ANNOTATION_CHANGED>";
        else:
            pass;
        # ----------------------------
        # event.Skip(); # i.e. PROPAGATE THE EVENT FURTHER...
        # ----------------------------

    def handle_stc_update_ui (self, event):
        u""" ... """
        # ----------------------------
        update_type = event.GetUpdated();
        # ----------------------------
        if (update_type & stcdefs.STC_UPDATED_BITS["SELECTION"]): # i.e. SELECTION RANGE CHANGED
            # ----------------------------
            self.repaint = True;
            # ----------------------------
        elif (update_type & stcdefs.STC_UPDATED_BITS[u"V_SCROLL"]): # i.e. VERTICAL SCROLL RANGE CHANGED
            # ----------------------------
            pass;
            # ----------------------------
        else:
            pass;
        # ----------------------------
        event.Skip(); # i.e. PROPAGATE THIS EVENT FURTHER...
        # ----------------------------

    def handle_stc_painted (self, event):
        u""" ... """
        # ----------------------------
        if (self.repaint): # i.e. (self.repaint == True)
            # ----------------------------
            current_line = self.GetCurrentLine();
            self.MarkerDeleteAll(markerNumber=stcdefs.STC_MARKER_NUMBER[u"CURRENT_LINE"]);
            self.MarkerAdd(line=current_line, markerNumber=stcdefs.STC_MARKER_NUMBER[u"CURRENT_LINE"]);
            # ----------------------------
            dispatcher.send(sender=self, signal=threadingdefs.GLOBAL_SIGNAL_INDEX[u"STC_INPUT_PAINTED"], current_line=current_line);
            # ----------------------------
            self.repaint = False;
            # ----------------------------
        else: # i.e. (self.repaint == False)
            pass;
        # ----------------------------
        # event.Skip(); # i.e. propagate the event further...
        # ----------------------------

    def handle_stc_style_needed (self, event):
        u""" ... """
        # ----------------------------
        # [1] GET STYLE NEEDED RANGE:
        # [1.1] GET STYLE NEEDED START POSITION:
        # x = self.GetEndStyled();             # get the style needed range start position...
        # A = self.LineFromPosition(pos=x);    # get the style needed range start line...
        # a = self.PositionFromLine(line=A);   # get the style needed extended range start position...
        # [1.2] GET STYLE NEEDED END POSITION:
        # y = event.GetPosition();             # get the style needed range end position...
        # B = self.LineFromPosition(pos=y);    # get the style needed range end line...
        # b = self.GetLineEndPosition(line=B); # get the style needed extended range end position...
        # ----------------------------
        # [2] GET STYLE NEEDED RANGE TEXT:
        # [2.1] GET STYLE NEEDED RANGE UNICODE TEXT:
        # t = self.GetTextRange(startPos=x, endPos=y); # get the style needed range unicode text...
        # T = self.GetTextRange(startPos=a, endPos=b); # get the style needed extended range unicode text...
        # [2.2] GET STYLE NEEDED RANGE UTF-8 TEXT:
        # t = self.GetTextRangeUTF8(startPos=x, endPos=y); # get the style needed range utf-8 text...
        # T = self.GetTextRangeUTF8(startPos=a, endPos=b); # get the style needed extended range utf-8 text...
        # [2.3] GET STYLE NEEDED RANGE CELLS:
        # t = self.GetStyledText(startPos=x, endPos=y); # get the style needed range stc "cell" text...
        # T = self.GetStyledText(startPos=a, endPos=b); # get the style needed extended range stc "cell" text...
        # ----------------------------
        # [3] SET DOCUMENT STYLES:
        if (not self.styling): # i.e. (self.styling == False)
            self.set_document_styles();
        else: # i.e. (self.styling == True)
            pass;
        # ----------------------------
        # event.Skip(); # i.e. PROPAGATE THE EVENT FURTHER...
        # ----------------------------

    def handle_stc_key (self, event):
        u""" ... """
        # ----------------------------
        # ...
        event.Skip(); # i.e. PROPAGATE THE EVENT FURTHER...
        # ----------------------------

    def handle_wx_key_down (self, event):
        u""" ... """
        # ----------------------------
        # [1] GET KEY EVENT DATA:
        # [1.1] GET KEY EVENT KEY DATA:
        key     = event.GetKeyCode();
        charkey = event.GetUnicodeKey(); # UPPER CASE
        # [1.2] GET KEY EVENT MODIFICATION DATA:
        control = event.ControlDown();
        shift   = event.ShiftDown();
        alt     = event.AltDown();
        # [1.3] GET KEY EVENT POSITION DATA:
        # x       = event.GetX();
        # y       = event.GetY();
        # ----------------------------
        # [2] PROCESS KEY EVENT DATA:
        # [2.1] PROCESS MODIFIED KEY EVENT DATA:
        if (control and shift and alt): # i.e. Ctrl+Shift+Alt
            event.Skip();
        elif (control and shift): # i.e. Ctrl+Shift
            event.Skip();
        elif (control and alt): # i.e. Ctrl+Alt
            event.Skip();
        elif (control): # i.e. Ctrl
            if (charkey == ord(u"C")): # i.e. Ctrl+C (COPY)
                event.Skip();
            elif (charkey == ord(u"X")): # i.e. Ctrl+X (CUT)
                event.Skip();
            elif (charkey == ord(u"V")): # i.e. Ctrl+V (PASTE)
                event.Skip();
            else:
                event.Skip();
        elif (shift and alt): # i.e. Shift+Alt
            event.Skip();
        elif (shift): # i.e. Shift
            event.Skip();
        elif (alt): # i.e. Alt
            event.Skip();
        # ----------------------------
        # [2.2] PROCESS SPECIAL KEY EVENT DATA:
        # elif (key in (wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER)): # USED ("CONSUMED") BY STC!
        #     event.Skip();
        # elif (key in (wx.WXK_DELETE, wx.WXK_BACK)): # USED ("CONSUMED") BY STC!
        #     event.Skip();
        # elif (key in (wx.WXK_SPACE, wx.WXK_TAB)): # USED ("CONSUMED") BY STC!
        #     event.Skip();
        # elif (key == wx.WXK_F1): # i.e. F1
        #     event.Skip();
        # elif (key == wx.WXK_F8): # i.e. F8
        #     event.Skip();
        elif (key == wx.WXK_F9): # i.e. F9
            self.toggle_wrap_mode();
        # elif (key == wx.WXK_F10): # i.e. F10
        #     event.Skip();
        # elif (key == wx.WXK_F11): # i.e. F11
        #     event.Skip();
        # elif (key == wx.WXK_F12): # i.e. F12
        #     event.Skip();
        # ...
        # ----------------------------
        # [2.3] PROCESS LITERAL KEY EVENT DATA:
        # elif (key == wx.WXK_NUMPAD0): # USED ("CONSUMED") BY STC!
        #     event.Skip();
        # elif (key == wx.WXK_NUMPAD1): # USED ("CONSUMED") BY STC!
        #     event.Skip();
        # elif (charkey == ord(u"C")): # USED ("CONSUMED") BY STC!
        #     event.Skip();
        # elif (charkey == ord(u"Č")): # USED ("CONSUMED") BY STC!
        #     event.Skip();
        # ...
        # ----------------------------
        # [3] NOTHING PROCESSED:
        else:
            event.Skip(); # i.e. PROPAGATE THE EVENT FURTHER...
        # ----------------------------

    def handle_wx_right_down (self, event):
        u""" ... """
        # ----------------------------
        # self.right_down = event.GetPosition();
        # self.PopupMenu(menu=WX_MENU_STC(parent=self));
        # ----------------------------
        event.Skip(); # i.e. PROPAGATE THE EVENT FURTHER...
        # ----------------------------

    def handle_wx_idle (self, event):
        u""" ... """
        # ----------------------------
        # event.RequestMore(); # i.e. RE-RAISE THE IDLE EVENT (CPU EXPENSIVE, THOUGH)
        event.Skip(); # i.e. propagate the event further...
        # ----------------------------

    def signal_transliterate (self):
        u""" ... """
        # ----------------------------
        dispatcher.send(sender=self, signal=threadingdefs.GLOBAL_SIGNAL_INDEX[u"STC_TRANSLITERATE"]);
        # ----------------------------

    def signal_current_line (self):
        u""" ... """
        # ----------------------------
        current_line = self.GetCurrentLine();
        dispatcher.send(sender=self, signal=threadingdefs.GLOBAL_SIGNAL_INDEX[u"STC_INPUT_PAINTED"], current_line=current_line);
        # ----------------------------

    def set_default_text (self):
        u""" ... """
        # ----------------------------
        self.ClearAll();
        # ----------------------------
        file = codecs.open(
            filename = r"input\texts\Text_Default_2015_08_14_001.txt", # i.e. the default, welcomming text
            mode     = u"r",
            encoding = u"utf-8",
        );
        text = file.read();
        file.close();
        # ----------------------------
        self.SetText(text=text);
        # ----------------------------

    def load_text (self, path):
        u""" ... """
        # ----------------------------
        self.ClearAll();
        # ----------------------------
        file = codecs.open(filename=path, mode=u"r", encoding=u"utf-8");
        text = file.read();
        file.close();
        # ----------------------------
        wx.CallAfter(self.SetText, text=text);
        # ----------------------------

    @GET_THREAD(name=u"save_text", daemon=True)
    def save_text (self, path):
        # ----------------------------
        file = codecs.open(filename=path, mode=u"w", encoding=u"utf-8");
        text = self.GetText();
        file.write(text);
        file.close();
        # ----------------------------

    def set_document_styles (self):
        u""" ... """
        # ----------------------------
        if (not self.styling): # i.e. (self.styling == False)
            # ----------------------------
            self.styling = True;
            # ----------------------------
            self._set_document_styles(self, self.transliterator._encoding_);
            # ----------------------------
            self.styling = False;
            # ----------------------------
        else: # i.e. (self.styling == True)
            pass;
        # ----------------------------

    def toggle_wrap_mode (self):
        u""" ... """
        # ----------------------------
        wrap_mode = self.GetWrapMode();
        wrap_name = stcdefs.STC_WRAP_NAME[wrap_mode];
        # ----------------------------
        if (wrap_name == u"NONE"):
            self.SetWrapMode(mode=stcdefs.STC_WRAP_MODE[u"WORD"]);
        elif (wrap_name == u"WORD"):
            self.SetWrapMode(mode=stcdefs.STC_WRAP_MODE[u"CHAR"]);
        else: # i.e. (wrap_name == u"CHAR")
            self.SetWrapMode(mode=stcdefs.STC_WRAP_MODE[u"NONE"]);
        # ----------------------------

# ------------------------------------------------------------------------------

class WX_PANEL_CONTROLS (wx.Panel):
    u""" ... """

    def __init__ (self,
        parent,
        id    = wx.ID_ANY,
        pos   = wx.DefaultPosition,
        size  = wx.DefaultSize,
        style = wx.BORDER_NONE
    ):
        wx.Panel.__init__(self, parent=parent, id=id, pos=pos, size=size, style=style);
        # ----------------------------
        self.init_style();
        self.init_sizers();
        self.init_controls();
        # ----------------------------

    def init_style (self):
        u""" ... """
        # ----------------------------
        self.SetDoubleBuffered(on=True);
        # ----------------------------

    def init_sizers (self):
        u""" ... """
        # ----------------------------
        self.sizer = wx.BoxSizer(orient=wx.HORIZONTAL);
        self.SetSizer(sizer=self.sizer);
        # ----------------------------

    def init_controls (self):
        u""" ... """
        # ----------------------------
        self.table_bitmap = wx.Bitmap(
            name = wxdefs.BITMAPS[u"table"],
            type = wx.BITMAP_TYPE_PNG,
        );
        self.table_button = wx.BitmapButton(
            parent = self,
            size   = (-1,-1),
            style  = wx.BU_AUTODRAW,
            bitmap = self.table_bitmap,
        );
        self.table_button.SetToolTipString(tip=u"Edit Transliterator Table...");
        self.sizer.Add(item=self.table_button, proportion=0, flag=wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL | wx.ALL, border=2);
        # ----------------------------
        self.parent = self.GetTopLevelParent();
        self.transliterator = self.parent.transliterator;
        self.labels = self.transliterator.get_column_labels();

        self.source_combo = wx.ComboBox(parent=self, size=(-1,-1), style=wx.CB_DROPDOWN, choices=self.labels);
        self.sizer.Add(item=self.source_combo, proportion=0, flag=wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL | wx.ALL, border=2);
        self.source_combo.SetMargins(pt=(0,0));
        self.source_combo.SetFont(font=wx.Font(**wxdefs.FONTS[u"ui_small"]));
        self.source_combo.Select(n=self.labels.index(self.transliterator.get_source()));

        self.to_label = wx.StaticText(parent=self, label=u"TO");
        self.sizer.Add(item=self.to_label, proportion=0, flag=wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL | wx.RIGHT | wx.ALL, border=2);
        self.to_label.SetFont(font=wx.Font(**wxdefs.FONTS[u"ui_small"]));
        self.to_label.SetForegroundColour(colour=u"#777777");

        self.target_combo = wx.ComboBox(parent=self, size=(-1,-1), style=wx.CB_DROPDOWN, choices=self.labels);
        self.sizer.Add(item=self.target_combo, proportion=0, flag=wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL | wx.ALL, border=2);
        self.target_combo.SetMargins(pt=(0,0));
        self.target_combo.SetFont(font=wx.Font(**wxdefs.FONTS[u"ui_small"]));
        self.target_combo.Select(n=self.labels.index(self.transliterator.get_target()));
        # ----------------------------
        self.sizer.Add(item=(-1,-1), proportion=1, flag=wx.EXPAND | wx.ALL, border=0);
        # ----------------------------
        self.interactive_checkbox = wx.CheckBox(parent=self, size=(-1,-1), style=wx.CHK_2STATE, label=u"Interactive");
        self.sizer.Add(item=self.interactive_checkbox, proportion=0, flag=wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL | wx.ALL, border=2);
        self.interactive_checkbox.SetValue(state=True);
        # ----------------------------
        self.transliterate_button = wx.Button(parent=self, size=(-1,-1), style=wx.BU_EXACTFIT, label=u"TRANSLITERATE");
        self.sizer.Add(item=self.transliterate_button, proportion=0, flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.ALL, border=2);
        self.transliterate_button.SetFont(font=wx.Font(**wxdefs.FONTS[u"ui_small"]));
        # ----------------------------

# ------------------------------------------------------------------------------

class WX_PANEL_STATUSBAR (wx.Panel):

    def __init__ (self, *args, **kwargs):
        # ----------------------------
        wx.Panel.__init__(self, *args, **kwargs);
        # ----------------------------
        self.init_style();
        self.init_sizers();
        self.init_controls();
        self.init_handlers();
        # ----------------------------

    def init_style (self):
        # ----------------------------
        self.SetDoubleBuffered(on=True);
        # ----------------------------

    def init_sizers (self):
        u""" ... """
        # ----------------------------
        self.sizer = wx.BoxSizer(orient=wx.HORIZONTAL);
        self.SetSizer(sizer=self.sizer);
        # ----------------------------

    def init_controls (self):
        u""" ... """
        # ----------------------------
        # [1] CONSTRUCT THE TRANSLITERATION LABELS:
        # [1.1] CONSTRUCT THE TRANSLITERATION TITLE LABEL:
        self.transliteration_title = wx.StaticText(parent=self, label=u"STC Transliterated in");
        self.sizer.Add(item=self.transliteration_title, proportion=0, flag=wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border=4);
        self.transliteration_title.SetFont(font=wx.Font(**wxdefs.FONTS[u"ui_small"]));
        self.transliteration_title.SetForegroundColour(colour=wxdefs.COLOURS[u"gray_7"]);
        # [1.2] CONSTRUCT THE TRANSLITERATION DATA LABEL:
        self.transliteration_data = wx.StaticText(parent=self);
        self.sizer.Add(item=self.transliteration_data, proportion=0, flag=wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border=4);
        self.transliteration_data.SetFont(font=wx.Font(**wxdefs.FONTS[u"ui_small"]));
        self.transliteration_data.SetForegroundColour(colour=wxdefs.COLOURS[u"black"]);
        # [1.3] CONSTRUCT THE TRANSLITERATION SUFFIX LABEL:
        self.transliteration_suffix = wx.StaticText(parent=self, label=u"usecs.");
        self.sizer.Add(item=self.transliteration_suffix, proportion=0, flag=wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border=4);
        self.transliteration_suffix.SetFont(font=wx.Font(**wxdefs.FONTS[u"ui_small"]));
        self.transliteration_suffix.SetForegroundColour(colour=wxdefs.COLOURS[u"gray_7"]);
        # ----------------------------

    def init_handlers (self):
        u""" ... """
        # ----------------------------
        dispatcher.connect(
            signal   = threadingdefs.GLOBAL_SIGNAL_INDEX[u"STC_TRANSLITERATION_DONE"],
            sender   = threadingdefs.GLOBAL_SENDER_ANY,
            receiver = self.handle_stc_transliteration_done,
            weak     = True,
        );
        # ----------------------------

    def handle_stc_transliteration_done (self, t):
        u""" ... """
        # ----------------------------
        transliteration_text = u"{0:.00e} ({0:.07f})".format(t);
        self.transliteration_data.SetLabelText(text=transliteration_text);
        # ----------------------------
        wx.CallAfter(self.sizer.Layout);
        wx.CallAfter(self.Refresh);
        # ----------------------------

# ------------------------------------------------------------------------------

class WX_PANEL_TABLE (wx.Panel):
    u""" ... """

    def __init__ (self,
        parent,
        id    = wx.ID_ANY,
        pos   = wx.DefaultPosition,
        size  = wx.DefaultSize,
        style = wx.BORDER_NONE
    ):
        wx.Panel.__init__(self, parent=parent, id=id, pos=pos, size=size, style=style);
        self.root = self.GetTopLevelParent();
        self.transliterator = self.root.transliterator;
        # ----------------------------
        self.init_style();
        self.init_sizers();
        self.init_controls();
        self.init_view();
        # ----------------------------

    def init_style (self):
        u""" ... """
        # ----------------------------
        self.SetDoubleBuffered(on=True);
        # ----------------------------

    def init_sizers (self):
        u""" ... """
        # ----------------------------
        self.sizer = wx.BoxSizer(orient=wx.VERTICAL);
        self.SetSizer(sizer=self.sizer);
        # ----------------------------

    def init_controls (self):
        u""" ... """
        # ----------------------------
        self.table_text = WX_STC_TABLE(parent=self, stc_style=u"TABLE");
        self.sizer.Add(item=self.table_text, proportion=1, flag=wx.EXPAND | wx.ALL, border=0);
        # ----------------------------
        file = codecs.open(
            filename = self.transliterator.path.path,
            mode     = u"r",
            encoding = u"utf-8",
        );
        text = file.read();
        file.close();
        self.table_text.SetText(text=text);
        # ----------------------------

    def init_view (self):
        # ----------------------------
        # self.Fit();
        self.Refresh();
        # ----------------------------

# ------------------------------------------------------------------------------

class WX_PANEL_CONSOLE (wx.Panel):
    u""" ... """

    def __init__ (self,
        parent,
        id    = wx.ID_ANY,
        pos   = wx.DefaultPosition,
        size  = wx.DefaultSize,
        style = wx.BORDER_NONE
    ):
        wx.Panel.__init__(self, parent=parent, id=id, pos=pos, size=size, style=style);
        # ----------------------------
        self.init_style();
        self.init_sizers();
        self.init_controls();
        self.init_view();
        # ----------------------------

    def init_style (self):
        u""" ... """
        # ----------------------------
        self.SetDoubleBuffered(on=True);
        # ----------------------------

    def init_sizers (self):
        u""" ... """
        # ----------------------------
        self.sizer = wx.BoxSizer(orient=wx.VERTICAL);
        self.SetSizer(sizer=self.sizer);
        # ----------------------------

    def init_controls (self):
        u""" ... """
        # ----------------------------
        self.splitter = wx.SplitterWindow(
            parent = self,
            id     = wx.ID_ANY,
            pos    = wx.DefaultPosition,
            size   = wx.DefaultSize,
            style  =  wx.SP_NO_XP_THEME
                        | wx.SP_LIVE_UPDATE
        );
        self.sizer.Add(item=self.splitter, proportion=1, flag=wx.EXPAND | wx.ALL, border=0);
        self.splitter.SetDoubleBuffered(on=True);
        self.splitter.SetSashGravity(gravity=0.5);
        self.splitter.SetMinimumPaneSize(min=25);
        # ----------------------------
        self.output_text = WX_STC_OUTPUT(parent=self.splitter, stc_style=u"OUTPUT");
        self.input_text  = WX_STC_INPUT( parent=self.splitter, stc_style=u"INPUT" );
        self.splitter.SplitHorizontally(window1=self.output_text, window2=self.input_text, sashPosition=0.0);
        # ----------------------------
        self.controls = WX_PANEL_CONTROLS(parent=self);
        self.sizer.Add(item=self.controls, proportion=0, flag=wx.EXPAND | wx.ALL, border=0);
        # ----------------------------

    def init_view (self):
        # ----------------------------
        self.Fit();
        self.Refresh();
        # ----------------------------

# ------------------------------------------------------------------------------

class WX_STATUSBAR (wx.StatusBar):

    def __init__ (self,
        parent,
        id    = wx.ID_ANY,
        style = wx.STB_DEFAULT_STYLE
                | wx.STB_SIZEGRIP
                | wx.STB_ELLIPSIZE_END
                | wx.STB_SHOW_TIPS
    ):
        wx.StatusBar.__init__(self, parent=parent, id=id, style=style);
        # ----------------------------
        self.init_style();
        self.init_controls();
        self.init_handlers();
        # ----------------------------

    def init_style (self):
        # ----------------------------
        self.SetDoubleBuffered(on=True);
        # ----------------------------

    def init_controls (self):
        # ----------------------------
        self.SetFieldsCount(number=2);
        self.SetStatusWidths(widths=[150,-1]);
        # self.SetStatusStyles(styles=[wx.SB_NORMAL, wx.SB_FLAT, wx.SB_RAISED]);
        # ----------------------------
        self.SetStatusText(number=0, text=u"");
        # ----------------------------
        self.status_panel = WX_PANEL_STATUSBAR(parent=self);
        self.set_status_position();
        # ----------------------------

    def init_handlers (self):
        # ----------------------------
        self.Bind(event=wx.EVT_SIZE, source=self, handler=self.handle_size);
        # ----------------------------

    def handle_size (self, event):
        self.set_status_position();
        event.Skip();

    def set_status_position (self):
        u""" SOURCE: "StatusBar.py" """
        # ----------------------------
        rect = self.GetFieldRect(i=1);
        rect.x += 1;
        rect.y += 1;
        self.status_panel.SetRect(rect=rect, sizeFlags=wx.SIZE_AUTO);
        # ----------------------------
        self.Refresh();
        # ----------------------------

# ------------------------------------------------------------------------------

class WX_FRAME_TABLE (wx.Frame):
    u""" ... """

    def __init__ (self,
        parent,
        id    = wx.ID_ANY,
        title = u"CSV Table Editor (Minimal)",
        pos   = wx.DefaultPosition,
        size  = (600, 600), # wx.DefaultSize,
        style = wx.DEFAULT_FRAME_STYLE
                # | wx.WS_EX_TRANSIENT
                # | wx.FRAME_NO_TASKBAR
    ):
        wx.Frame.__init__(self, parent=parent, id=id, title=title, pos=pos, size=size, style=style);
        self.root = parent;
        self.transliterator = self.root.transliterator;
        # ----------------------------
        self.init_style();
        self.init_icons();
        self.init_menubar();
        self.init_menubar_accelerator();
        self.init_controls();
        self.init_handlers();
        self.init_view();
        # ----------------------------

    def init_style (self):
        u""" ... """
        # ----------------------------
        pass;
        # ----------------------------

    def init_icons (self):
        u""" ... """
        # ----------------------------
        self.icon = wx.Icon(
            name = wxdefs.BITMAPS[u"table"],
            type = wx.BITMAP_TYPE_PNG ,
        );
        self.SetIcon(icon=self.icon);
        # ----------------------------

    def init_menubar (self):
        u""" ... """
        # ----------------------------
        self.file_menu = wx.Menu();
        self.open = self.file_menu.Append(id=wx.ID_ANY, text=u"&Open CSV Table...\t(Ctrl+O)", help=u"");
        self.save = self.file_menu.Append(id=wx.ID_ANY, text=u"&Save CSV Table...\t(Ctrl+S)", help=u"");
        self.save_as = self.file_menu.Append(id=wx.ID_ANY, text=u"&Save CSV Table As...\t(Ctrl+Shift+S)", help=u"");
        self.file_menu.AppendSeparator();
        self.apply = self.file_menu.Append(id=wx.ID_ANY, text=u"&Apply...\t(Ctrl+F12)", help=u"");
        self.file_menu.AppendSeparator();
        self.quit = self.file_menu.Append(id=wx.ID_ANY, text=u"&Quit...\t(Ctrl+Q)", help=u"");
        self.menubar = wx.MenuBar();
        self.menubar.Append(menu=self.file_menu, title="&File");
        self.SetMenuBar(menubar=self.menubar);
        # ----------------------------

    def init_menubar_accelerator (self):
        u""" ... """
        # ----------------------------
        self.accelerator_table = wx.AcceleratorTable(
            n = [
                (wx.ACCEL_CTRL,                ord(u"O"),  self.open.GetId()   ),
                (wx.ACCEL_CTRL,                ord(u"S"),  self.save.GetId()   ),
                (wx.ACCEL_CTRL|wx.ACCEL_SHIFT, ord(u"S"),  self.save_as.GetId()),
                (wx.ACCEL_CTRL,                wx.WXK_F12, self.apply.GetId()  ),
                (wx.ACCEL_CTRL,                ord(u"W"),  self.quit.GetId()   ),
            ], # i.e. (modifier_flag, key_code, item_id)
        );
        self.SetAcceleratorTable(accel=self.accelerator_table);
        # ----------------------------

    def init_controls (self):
        u""" ... """
        # ----------------------------
        # [1] ...:
        self.table_panel = WX_PANEL_TABLE(parent=self);
        # ----------------------------

    def init_handlers (self):
        u""" ... """
        # ----------------------------
        self.Bind(event=wx.EVT_CLOSE, source=self, handler=self.handle_close);
        # ----------------------------
        self.Bind(event=wx.EVT_MENU, source=self.open,    handler=self.handle_menu_open);
        self.Bind(event=wx.EVT_MENU, source=self.save,    handler=self.handle_menu_save);
        self.Bind(event=wx.EVT_MENU, source=self.save_as, handler=self.handle_menu_save_as);
        self.Bind(event=wx.EVT_MENU, source=self.apply,   handler=self.handle_menu_apply);
        self.Bind(event=wx.EVT_MENU, source=self.quit,    handler=self.handle_menu_quit);
        # ----------------------------

    def init_view (self):
        u""" ... """
        # ----------------------------
        # self.Fit();
        self.Show(show=True);
        # self.CenterOnParent(dir=wx.BOTH);
        # self.CenterOnScreen(dir=wx.BOTH);
        # ----------------------------

    def handle_close (self, event):
        u""" ... """
        # ----------------------------
        self.root.editing_table = False;
        event.Skip(); # i.e. propagate the wx.EVT_CLOSE event further...
        # ----------------------------

    def handle_menu_open (self, event):
        print u"<handle_menu_open>";

    def handle_menu_save (self, event):
        print u"<handle_menu_save>";

    def handle_menu_save_as (self, event):
        print u"<handle_menu_save_as>";

    def handle_menu_apply (self, event):
        print u"<handle_menu_apply>";

    def handle_menu_quit (self, event):
        self.Close(); # i.e. generate the wx.EVT_CLOSE event, handled by the "handle_close" method...

# ------------------------------------------------------------------------------

class WX_FRAME_CONSOLE (wx.Frame):
    u""" ... """

    def __init__ (self,
        parent,
        id    = wx.ID_ANY,
        title = u"Personal STC Transliterator (Minimal)",
        pos   = wx.DefaultPosition,
        size  = (500, 250), # wx.DefaultSize,
        style = wx.DEFAULT_FRAME_STYLE
                # | wx.WS_EX_TRANSIENT
                # | wx.FRAME_NO_TASKBAR
    ):
        wx.Frame.__init__(self, parent=parent, id=id, title=title, pos=pos, size=size, style=style);
        # ----------------------------
        self.init_style();
        self.init_icons();
        self.init_transliterator();
        self.init_menubar();
        self.init_controls();
        self.init_statusbar();
        self.init_handlers();
        self.init_view();
        # ----------------------------
        self.editing_table = False;
        # ----------------------------

    def init_style (self):
        u""" ... """
        # ----------------------------
        self.SetMinSize(minSize=(500,250));
        # ----------------------------

    def init_icons (self):
        u""" ... """
        # ----------------------------
        self.icon = wx.Icon(name=wxdefs.BITMAPS[u"console"], type=wx.BITMAP_TYPE_PNG);
        self.SetIcon(icon=self.icon);
        # ----------------------------

    def init_transliterator (self):
        u""" Initializes the transliterator used by the STC windows """
        # ----------------------------
        self.transliterator = transliterator.Transliterator(table=TRANSLITERATOR_TABLE);
        self.transliterator.set_map(source=TRANSLITERATOR_SOURCE, target=TRANSLITERATOR_TARGET);
        self.transliterator.encode(encoding=TRANSLITERATOR_ENCODING);
        self.labels = self.transliterator.get_column_labels();
        # ----------------------------

    def init_menubar (self):
        u""" ... """
        # ----------------------------
        # [1] INITIALIZE MENUBAR ICONS
        self.menubar_icons = {
            u"open":              wx.Bitmap(name=wxdefs.BITMAPS[u"open"],               type=wx.BITMAP_TYPE_PNG),
            u"save_input":        wx.Bitmap(name=wxdefs.BITMAPS[u"save_input"],         type=wx.BITMAP_TYPE_PNG),
            u"save_output":       wx.Bitmap(name=wxdefs.BITMAPS[u"save_output"],        type=wx.BITMAP_TYPE_PNG),
            u"quit":              wx.Bitmap(name=wxdefs.BITMAPS[u"quit"],               type=wx.BITMAP_TYPE_PNG),
            u"table":             wx.Bitmap(name=wxdefs.BITMAPS[u"table"],              type=wx.BITMAP_TYPE_PNG),
            u"transliterate":     wx.Bitmap(name=wxdefs.BITMAPS[u"transliterate"],      type=wx.BITMAP_TYPE_PNG),
            u"transliterate_txt": wx.Bitmap(name=wxdefs.BITMAPS[u"transliterate_txt"],  type=wx.BITMAP_TYPE_PNG),
            u"transliterate_ods": wx.Bitmap(name=wxdefs.BITMAPS[u"transliterate_ods"],  type=wx.BITMAP_TYPE_PNG),
        };
        # ----------------------------
        # [1] INIT MENUBAR:
        self.menubar = wx.MenuBar();
        self.SetMenuBar(menubar=self.menubar);
        # ----------------------------
        # [2] INIT "FILE" MENU:
        self.file_menu = wx.Menu();
        # [2.1] INIT "FILE" MENU ITEMS:
        self.open_item        = wx.MenuItem(parentMenu=self.file_menu, id=wx.ID_ANY, kind=wx.ITEM_NORMAL, text=u"&Open...\t(Ctrl+O)", help=u"Open a Text File...");
        self.save_input_item  = wx.MenuItem(parentMenu=self.file_menu, id=wx.ID_ANY, kind=wx.ITEM_NORMAL, text=u"Save &Input As...\t(Ctrl+S)", help=u"Save Input Text...");
        self.save_output_item = wx.MenuItem(parentMenu=self.file_menu, id=wx.ID_ANY, kind=wx.ITEM_NORMAL, text=u"&Save Output As...\t(Ctrl+Shift+S)", help=u"Save Transliterated Text...");
        self.quit_item        = wx.MenuItem(parentMenu=self.file_menu, id=wx.ID_ANY, kind=wx.ITEM_NORMAL, text=u"&Quit...\t(Ctrl+W)", help=u"Quit App...");
        # [2.2] SET "FILE" MENU ICONS:
        self.open_item.SetBitmap(bmp=self.menubar_icons[u"open"]);
        self.save_input_item.SetBitmap(bmp=self.menubar_icons[u"save_input"]);
        self.save_output_item.SetBitmap(bmp=self.menubar_icons[u"save_output"]);
        self.quit_item.SetBitmap(bmp=self.menubar_icons[u"quit"]);
        # [2.3] APPEND "FILE" MENU ITEMS:
        self.file_menu.AppendItem(item=self.open_item);
        self.file_menu.AppendItem(item=self.save_input_item);
        self.file_menu.AppendItem(item=self.save_output_item);
        self.file_menu.AppendSeparator();
        self.file_menu.AppendItem(item=self.quit_item);
        # [2.4] APPEND "FILE" MENU:
        self.menubar.Append(menu=self.file_menu, title="&File");
        # ----------------------------
        # [3] INIT "TRANSLITERATE" MENU:
        self.transliterate_menu = wx.Menu();
        # [3.1] INIT "TRANSLITERATE" MENU ITEMS:
        self.transliterate_item     = wx.MenuItem(parentMenu=self.transliterate_menu, id=wx.ID_ANY, kind=wx.ITEM_NORMAL, text=u"&Transliterate...\t(F12)", help=u"Transliterate...");
        self.transliterate_txt_item = wx.MenuItem(parentMenu=self.transliterate_menu, id=wx.ID_ANY, kind=wx.ITEM_NORMAL, text=u"Transliterate T&XT File...\t(Ctrl+F12)", help=u"Transliterate TXT File...");
        self.transliterate_ods_item = wx.MenuItem(parentMenu=self.transliterate_menu, id=wx.ID_ANY, kind=wx.ITEM_NORMAL, text=u"Transliterate O&DS File...\t(Ctrl+Shift+F12)", help=u"Transliterate ODS File...");
        self.transliterate_ods_item.Enable(enable=False);
        self.edit_table_item        = wx.MenuItem(parentMenu=self.transliterate_menu, id=wx.ID_ANY, kind=wx.ITEM_NORMAL, text=u"&Edit Table...\t(Ctrl+T)", help=u"Edit Transliteration Table...");
        # [3.2] SET "TRANSLITERATE" MENU ICONS:
        self.transliterate_item.SetBitmap(bmp=self.menubar_icons[u"transliterate"]);
        self.transliterate_txt_item.SetBitmap(bmp=self.menubar_icons[u"transliterate_txt"]);
        # self.transliterate_ods_item.SetBitmap(bmp=self.menubar_icons[u"transliterate_ods"]);
        self.edit_table_item.SetBitmap(bmp=self.menubar_icons[u"table"]);
        # [3.3] APPEND "TRANSLITERATE" MENU ITEMS:
        self.transliterate_menu.AppendItem(item=self.transliterate_item);
        self.transliterate_menu.AppendItem(item=self.transliterate_txt_item);
        self.transliterate_menu.AppendItem(item=self.transliterate_ods_item);
        self.transliterate_menu.AppendSeparator();
        self.transliterate_menu.AppendItem(item=self.edit_table_item);
        # [3.4] APPEND "TRANSLITERATE" MENU:
        self.menubar.Append(menu=self.transliterate_menu, title="&Transliterate");
        # ----------------------------
        # [4] INIT MENUBAR SHORCUT ACCELERATOR:
        self.accelerator_table = wx.AcceleratorTable(
            n = [
                (wx.ACCEL_CTRL,                ord(u"O"),  self.open_item.GetId()             ),
                (wx.ACCEL_CTRL,                ord(u"S"),  self.save_input_item.GetId()       ),
                (wx.ACCEL_CTRL|wx.ACCEL_SHIFT, ord(u"S"),  self.save_output_item.GetId()      ),
                (wx.ACCEL_CTRL,                ord(u"W"),  self.quit_item.GetId()             ),
                (0,                            wx.WXK_F12, self.transliterate_item.GetId()    ),
                (wx.ACCEL_CTRL,                wx.WXK_F12, self.transliterate_txt_item.GetId()),
                (wx.ACCEL_CTRL|wx.ACCEL_SHIFT, wx.WXK_F12, self.transliterate_ods_item.GetId()),
                (wx.ACCEL_CTRL,                ord(u"T"),  self.edit_table_item.GetId()       ),
            ], # i.e. (MODIFIER FLAG, KEY CODE, ITEM ID)
        );
        self.SetAcceleratorTable(accel=self.accelerator_table);
        # ----------------------------

    def init_controls (self):
        u""" ... """
        # ----------------------------
        self.main_panel = WX_PANEL_CONSOLE(parent=self);
        # ----------------------------

    def init_statusbar (self):
        u""" ... """
        # ----------------------------
        # [2] CONSTRUCT AND SET THE STATUS BAR:
        self.status_bar = WX_STATUSBAR(parent=self);
        self.SetStatusBar(statBar=self.status_bar);
        # ----------------------------

    def init_handlers (self):
        u""" ... """
        # ----------------------------
        # [1] FRAME EVENTS:
        self.Bind(event=wx.EVT_CLOSE, source=self, handler=self.handle_close);
        # ----------------------------
        # [2] MENU EVENTS:
        # [2.1] "FILE" MENU EVENTS:
        self.Bind(event=wx.EVT_MENU, source=self.open_item,        handler=self.handle_menu_open);
        self.Bind(event=wx.EVT_MENU, source=self.save_input_item,  handler=self.handle_menu_save_input);
        self.Bind(event=wx.EVT_MENU, source=self.save_output_item, handler=self.handle_menu_save_output);
        self.Bind(event=wx.EVT_MENU, source=self.quit_item,        handler=self.handle_menu_quit);
        # [2.2] "TRANSLITERATE" MENU EVENTS:
        self.Bind(event=wx.EVT_MENU, source=self.transliterate_item,     handler=self.handle_menu_transliterate);
        self.Bind(event=wx.EVT_MENU, source=self.transliterate_txt_item, handler=self.handle_menu_transliterate_txt);
        self.Bind(event=wx.EVT_MENU, source=self.edit_table_item,        handler=self.handle_menu_edit_table);
        # ----------------------------
        # [3] CONTROL EVENTS:
        # [3.1] BUTTON EVENTS:
        self.Bind(event=wx.EVT_BUTTON, source=self.main_panel.controls.table_button,         handler=self.handle_button_table);
        self.Bind(event=wx.EVT_BUTTON, source=self.main_panel.controls.transliterate_button, handler=self.handle_button_transliterate);
        # [3.2] COMBO EVENTS:
        self.Bind(event=wx.EVT_COMBOBOX, source=self.main_panel.controls.source_combo, handler=self.handle_combo_source_changed);
        self.Bind(event=wx.EVT_COMBOBOX, source=self.main_panel.controls.target_combo, handler=self.handle_combo_target_changed);
        # ----------------------------
        # [4] CUSTOM EVENTS
        dispatcher.connect(
            signal   = threadingdefs.GLOBAL_SIGNAL_INDEX[u"STC_TRANSLITERATE"],
            sender   = threadingdefs.GLOBAL_SENDER_ANY,
            receiver = self.handle_transliterate,
        );
        # ----------------------------

    def init_view (self):
        u""" ... """
        # ----------------------------
        # self.Fit();
        self.Show(show=True);
        # self.CenterOnParent(dir=wx.BOTH);
        self.CenterOnScreen(dir=wx.BOTH);
        # ----------------------------
        self.main_panel.input_text.SetFocus();
        self.main_panel.input_text.set_default_text();
        # self.main_panel.input_text.SetSelection(0, 0);
        # ----------------------------

    def handle_close (self, event):
        u""" ... """
        # ----------------------------
        # self.stop_all_threads();
        event.Skip(); # i.e. propagate the wx.EVT_CLOSE event further...
        # ----------------------------

    def handle_menu_open (self, event):
        u""" ... """
        # ----------------------------
        # [1] CONSTRUCT THE FILE DIALOG:
        file_dialog = wx.FileDialog(
            parent      = self,
            message     = u"Open an Input Text...",
            defaultDir  = os.getcwd(),
            defaultFile = u"",
            wildcard    = u"Any Text Type (*.*)|*.*",
            style       = wx.FD_OPEN | wx.FD_CHANGE_DIR,
        );
        # ----------------------------
        # [2] HANDLE THE FILE DIALOG RESULT:
        if (file_dialog.ShowModal() == wx.ID_OK):
            path = file_dialog.GetPath();
            self.main_panel.input_text.load_text(path=path);
        else: # (file_dialog.ShowModal() == wx.ID_CANCEL)
            pass;
        # ----------------------------
        # [3] DESTROY THE FILE DIALOG:
        file_dialog.Destroy();
        # ----------------------------
        # event.Skip(); # i.e. propagate the event further...
        # ----------------------------

    def handle_menu_save_input (self, event):
        u""" ... """
        # ----------------------------
        # [1] CONSTRUCT THE FILE DIALOG:
        file_dialog = wx.FileDialog(
            parent      = self,
            message     = u"Save a Input Text as...",
            defaultDir  = os.getcwd(),
            defaultFile = u"",
            wildcard    = u"Any Text Type (*.*)|*.*",
            style       = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT | wx.FD_CHANGE_DIR,
        );
        # ----------------------------
        # [2] HANDLE THE FILE DIALOG RESULT:
        if (file_dialog.ShowModal() == wx.ID_OK):
            path = file_dialog.GetPath();
            save_input_text_thread = self.main_panel.input_text.save_text(path=path);
            save_input_text_thread.start();
        else: # (file_dialog.ShowModal() == wx.ID_CANCEL)
            pass;
        # ----------------------------
        # [3] DESTROY THE FILE DIALOG:
        file_dialog.Destroy();
        # ----------------------------
        # event.Skip(); # i.e. propagate the event further...
        # ----------------------------

    def handle_menu_save_output (self, event):
        u""" ... """
        # ----------------------------
        # [1] CONSTRUCT THE FILE DIALOG:
        file_dialog = wx.FileDialog(
            parent      = self,
            message     = u"Save a Transliterated Text as...",
            defaultDir  = os.getcwd(),
            defaultFile = u"",
            wildcard    = u"Any Text Type (*.*)|*.*",
            style       = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT | wx.FD_CHANGE_DIR,
        );
        # ----------------------------
        # [2] HANDLE THE FILE DIALOG RESULT:
        if (file_dialog.ShowModal() == wx.ID_OK):
            path = file_dialog.GetPath();
            save_output_text_thread = self.main_panel.output_text.save_text(path=path);
            save_output_text_thread.start();
        else: # (file_dialog.ShowModal() == wx.ID_CANCEL)
            pass;
        # ----------------------------
        # [3] DESTROY THE FILE DIALOG:
        file_dialog.Destroy();
        # ----------------------------
        # event.Skip(); # i.e. propagate the event further...
        # ----------------------------

    def handle_menu_quit (self, event):
        u""" ... """
        # ----------------------------
        self.Close();
        # ----------------------------
        # event.Skip(); # i.e. propagate the event further...
        # ----------------------------

    def handle_menu_transliterate (self, event):
        u""" ... """
        # ----------------------------
        wx.CallAfter(self.handle_transliterate);
        # ----------------------------
        # event.Skip(); # i.e. propagate the event further...
        # ----------------------------

    def handle_menu_transliterate_txt (self, event):
        u""" ... """
        # ----------------------------
        transliterate_text_frame = wxutils.WX_FRAME_TRANSLITERATE_TEXT(parent=self);
        # ----------------------------
        # event.Skip(); # i.e. propagate the event further...
        # ----------------------------

    def handle_menu_edit_table (self, event):
        u""" ... """
        # ----------------------------
        if (self.editing_table): # i.e. (self.editing_table == True)
            pass; # i.e. ignore...
        else: # i.e. (self.editing_table == False)
            table_frame = WX_FRAME_TABLE(parent=self);
            self.editing_table = True;
        # ----------------------------
        # event.Skip(); # i.e. propagate the event further...
        # ----------------------------

    def handle_button_table (self, event):
        u""" ... """
        # ----------------------------
        if (self.editing_table): # i.e. (self.editing_table == True)
            pass; # i.e. ignore...
        else: # i.e. (self.editing_table == False)
            table_frame = WX_FRAME_TABLE(parent=self);
            self.editing_table = True;
        # ----------------------------
        # event.Skip(); # i.e. propagate the event further...
        # ----------------------------

    def handle_button_transliterate (self, event):
        u""" ... """
        # ----------------------------
        wx.CallAfter(self.handle_transliterate);
        # ----------------------------
        # event.Skip(); # i.e. propagate the event further...
        # ----------------------------

    def handle_transliterate (self):
        u""" ... """
        # ----------------------------
        source_string = self.main_panel.input_text.GetTextUTF8();
        current_line  = self.main_panel.input_text.GetCurrentLine();
        # ----------------------------
        if not self.main_panel.output_text.transliterating: # i.e. (self.main_panel.output_text.transliterating == False)
            transliterate = self.main_panel.output_text.transliterate(
                source_string = source_string,
                current_line  = current_line,
            );
            transliterate.start();
        else: # i.e. (self.main_panel.output_text.transliterating == True)
            # self.main_panel.output_text.transliteration_needed = True;
            pass;
        # ----------------------------
        self.main_panel.input_text.SetFocus();
        # ----------------------------
        # event.Skip(); # i.e. propagate the event further...
        # ----------------------------

    def handle_combo_source_changed (self, event):
        u""" ... """
        # ----------------------------
        source = event.GetString();
        dispatcher.send(sender=self, signal=threadingdefs.GLOBAL_SIGNAL_INDEX[u"TABLE_CHANGE_SOURCE"], source=source);
        self.handle_transliterate();
        # event.Skip(); # i.e. propagate the event further...
        # ----------------------------

    def handle_combo_target_changed (self, event):
        u""" ... """
        # ----------------------------
        target = event.GetString();
        dispatcher.send(sender=self, signal=threadingdefs.GLOBAL_SIGNAL_INDEX[u"TABLE_CHANGE_TARGET"], target=target);
        self.handle_transliterate();
        # event.Skip(); # i.e. propagate the event further...
        # ----------------------------
    
# ------------------------------------------------------------------------------

class WX_APP (wx.App):
    u""" ... """

    def __init__ (self, *args, **kwargs):
        u""" ... """
        # ----------------------------
        wx.App.__init__(self, *args, **kwargs);
        # ----------------------------
        self.init_controls();
        self.init_threads();
        # ----------------------------

    def init_controls (self):
        u""" ... """
        # ----------------------------
        self.input_frame = WX_FRAME_CONSOLE(parent=None);
        # ----------------------------

    def init_threads (self):
        u""" ... """
        # ----------------------------
        # [1] CONSTRUCT AND SET THE YIELD THREAD EVENTS:
        # [1.1] CONSTRUCT AND SET THE "RUN" THREAD EVENT:
        self.run = threading.Event();
        self.run.set();
        # ----------------------------
        # [2] CONSTRUCT, SET, AND START THE YIELD THREAD:
        # n.b. that this is the wx gui main thread regular periodic yield
        # mechanism, that keep the main thread from blocking. Eventual longer
        # sub-threaded processes need to provide their own, local yield
        # mechanism...
        self.yielder_thread = self.yielder(run=self.run, delay=0.123);
        self.yielder_thread.start();
        # ----------------------------

    @GET_THREAD(name=u"yielder_thread", daemon=True)
    def yielder (self, run, delay):
        u""" ... """
        # ----------------------------
        while (run.is_set()):
            wx.YieldIfNeeded();
            time.sleep(delay);
        # while (run)
        # ----------------------------

# ------------------------------------------------------------------------------

if __name__ == u"__main__":

    app = WX_APP(redirect=False);
    app.MainLoop();

    print u"\n>> The \"main.pyw\" is done.";