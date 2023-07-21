# -*- coding: utf-8 -*-
GLOBAL_ENCODING_CURRENT = u"utf-8";

# ------------------------------------------------------------------------------

import os
import time as time
# import codecs as codecs
import threading as threading

import wx as wx
from wx.lib.agw import pygauge as pyg

from pydispatch import dispatcher as dispatcher

from defs.wxdefs import wxdefs_2015_08_14_001 as wxdefs
from defs.threadingdefs import threadingdefs_2015_08_16_001 as threadingdefs
from utils.pathutils import pathutils_2015_08_14_001 as pathutils

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

class WX_GAUGE (pyg.PyGauge):

    def __init__ (self,
        parent,
        range = 100,
        id    = wx.ID_ANY,
        pos   = wx.DefaultPosition,
        size  = wx.DefaultSize,
        style = wx.GA_HORIZONTAL
                | wx.BORDER_NONE
    ):
        pyg.PyGauge.__init__(self, parent=parent, id=id, range=range, pos=pos, size=size, style=style);
        self.range = self.GetRange();
        # ----------------------------
        self.init_style();
        self.reset();
        # ----------------------------

    def init_style (self):
        u""" ... """
        # ----------------------------
        self.SetDoubleBuffered(on=True);
        # ----------------------------
        self.colours = {
            u"background": u"#A0A0A0",
            u"working":    u"#EE0000",
            u"completed":  u"#00EE00",
            u"frozen":     u"#777777",
        };
        # ----------------------------
        self.SetBackgroundColour(colour=self.colours[u"background"]);
        # ----------------------------

    def set_value (self, value):
        u""" ... """
        # ----------------------------
        if (value < self.range):
            pyg.PyGauge.SetValue(self, value=value);
            self.set_working();
        else: # i.e. (value >= self.range)
            pyg.PyGauge.SetValue(self, value=self.range);
            self.set_completed();
        # ----------------------------

    def set_working (self):
        u""" ... """
        # ----------------------------
        self.SetBarColor(colour=self.colours[u"working"]);
        # ----------------------------

    def set_completed (self):
        u""" ... """
        # ----------------------------
        self.SetBarColor(colour=self.colours[u"completed"]);
        # ----------------------------

    def reset (self):
        u""" ... """
        # ----------------------------
        self.set_value(value=0.0);
        # ----------------------------

    def freeze (self):
        u""" ... """
        # ----------------------------
        self.SetBarColor(colour=self.colours[u"frozen"]);
        # ----------------------------

    def unfreeze (self):
        u""" ... """
        # ----------------------------
        value = self.GetValue();
        self.set_value(value=value);
        # ----------------------------

# ------------------------------------------------------------------------------

class WX_PANEL_INPUT (wx.Panel):
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
        # [1] BOX SIZER:
        self.sizer = wx.BoxSizer(orient=wx.HORIZONTAL);
        self.SetSizer(sizer=self.sizer);
        # ----------------------------
        # [2] STATIC BOX SIZER:
        self.box = wx.StaticBox(parent=self, style=wx.SB_NORMAL, label= u"Input Text Document:");
        self.box_sizer = wx.StaticBoxSizer(box=self.box, orient=wx.HORIZONTAL);
        self.sizer.Add(item=self.box_sizer, proportion=1, flag=wx.EXPAND|wx.ALL, border=0);
        # ----------------------------

    def init_controls (self):
        u""" ... """
        # ----------------------------
        # [1] PATH TEXT:
        self.path_text = wx.TextCtrl(parent=self, style=wx.ST_ELLIPSIZE_START);
        self.box_sizer.Add(item=self.path_text, proportion=1, flag=wx.ALIGN_CENTER_VERTICAL, border=0);
        self.path_text.SetFont(font=wx.Font(**wxdefs.FONTS[u"ui_small"]));
        self.path_text.SetForegroundColour(colour=u"#000000");
        # ----------------------------
        # [2] FILE BUTTON:
        self.file_bitmap = wx.Bitmap(name=wxdefs.BITMAPS[u"file"]);
        self.file_button = wx.BitmapButton(parent=self, style=wx.BU_AUTODRAW, bitmap=self.file_bitmap);
        self.box_sizer.Add(item=self.file_button, proportion=0, flag=wx.ALIGN_CENTER_VERTICAL, border=0);
        self.file_button.SetToolTipString(tip=u"Browse Input Text Documents...");
        # ----------------------------

# ------------------------------------------------------------------------------

class WX_PANEL_OUTPUT (wx.Panel):
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
        # [1] BOX SIZER:
        self.sizer = wx.BoxSizer(orient=wx.HORIZONTAL);
        self.SetSizer(sizer=self.sizer);
        # ----------------------------
        # [2] STATIC BOX SIZER:
        self.box = wx.StaticBox(parent=self, style=wx.SB_NORMAL, label=u"Output Directory:");
        self.box_sizer = wx.StaticBoxSizer(box=self.box, orient=wx.HORIZONTAL);
        self.sizer.Add(item=self.box_sizer, proportion=1, flag=wx.EXPAND|wx.ALL, border=0);
        # ----------------------------

    def init_controls (self):
        u""" ... """
        # ----------------------------
        # [1] PATH TEXT:
        self.path_text = wx.TextCtrl(parent=self, style=wx.ST_ELLIPSIZE_START);
        self.box_sizer.Add(item=self.path_text, proportion=1, flag=wx.ALIGN_CENTER_VERTICAL, border=0);
        self.path_text.SetFont(font=wx.Font(**wxdefs.FONTS[u"ui_small"]));
        self.path_text.SetForegroundColour(colour=u"#000000");
        # ----------------------------
        # [2] FOLDER BUTTON:
        self.folder_bitmap = wx.Bitmap(name=wxdefs.BITMAPS[u"folder"]);
        self.folder_button = wx.BitmapButton(parent=self, style=wx.BU_AUTODRAW, bitmap=self.folder_bitmap);
        self.box_sizer.Add(item=self.folder_button, proportion=0, flag=wx.ALIGN_CENTER_VERTICAL, border=0);
        self.folder_button.SetToolTipString(tip=u"Browse Output Folders...");
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
        self.root           = self.GetTopLevelParent();
        self.transliterator = self.root.transliterator;
        self.labels         = self.transliterator.get_column_labels();
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
        self.sizer.Add(item=(-1,-1), proportion=1, flag=wx.EXPAND|wx.ALL, border=0);
        # ----------------------------
        self.source_combo = wx.ComboBox(parent=self, size=(-1,-1), style=wx.CB_DROPDOWN, choices=self.labels);
        self.sizer.Add(item=self.source_combo, proportion=0, flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, border=2);
        self.source_combo.SetMargins(pt=(0,0));
        self.source_combo.SetFont(font=wx.Font(**wxdefs.FONTS[u"ui_small"]));
        self.source_combo.Select(n=self.labels.index(self.transliterator.get_source()));
        # ----------------------------
        self.map_label = wx.StaticText(parent=self, label=u"TO");
        self.sizer.Add(item=self.map_label, proportion=0, flag=wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, border=2);
        self.map_label.SetFont(font=wx.Font(**wxdefs.FONTS[u"ui_small"]));
        self.map_label.SetForegroundColour(colour=u"#777777");
        # ----------------------------
        self.target_combo = wx.ComboBox(parent=self, size=(-1,-1), style=wx.CB_DROPDOWN, choices=self.labels);
        self.sizer.Add(item=self.target_combo, proportion=0, flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, border=2);
        self.target_combo.SetMargins(pt=(0,0));
        self.target_combo.SetFont(font=wx.Font(**wxdefs.FONTS[u"ui_small"]));
        self.target_combo.Select(n=self.labels.index(self.transliterator.get_target()));
        # ----------------------------
        self.sizer.Add(item=(30,-1), proportion=0, flag=wx.ALL, border=0);
        # ----------------------------
        self.filter_checkbox = wx.CheckBox(parent=self, size=(-1,-1), style=wx.CHK_2STATE, label=u"Filter");
        self.sizer.Add(item=self.filter_checkbox, proportion=0, flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, border=2);
        self.filter_checkbox.SetValue(state=False);
        # ----------------------------
        self.transliterate_button = wx.Button(parent=self, size=(-1,-1), style=wx.BU_EXACTFIT, label=u"TRANSLITERATE");
        self.sizer.Add(item=self.transliterate_button, proportion=0, flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, border=2);
        self.transliterate_button.SetFont(font=wx.Font(**wxdefs.FONTS[u"ui_small"]));
        # ----------------------------
        self.sizer.Add(item=(-1,-1), proportion=1, flag=wx.EXPAND|wx.ALL, border=0);
        # ----------------------------

# ------------------------------------------------------------------------------

class WX_PANEL_GAUGE (wx.Panel):
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
        # [1] GAUGE:
        self.gauge = WX_GAUGE(parent=self, size=(-1, 8));
        self.sizer.Add(item=self.gauge, proportion=1, flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, border=0);
        # ----------------------------
        # [2] PROGRESS LABEL:
        self.progress_text = wx.StaticText(parent=self, label=u"{0:.03f}%".format(100.0), size=(55, -1), style=wx.ALIGN_RIGHT);
        self.sizer.Add(item=self.progress_text, proportion=0, flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, border=0);
        self.progress_text.SetFont(font=wx.Font(**wxdefs.FONTS[u"ui_small"]));
        self.progress_text.SetForegroundColour(colour=u"#000000");
        # ----------------------------

# ------------------------------------------------------------------------------

class WX_PANEL_TRANSLITERATE_TEXT (wx.Panel):
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
        self.sizer = wx.BoxSizer(orient=wx.VERTICAL);
        self.SetSizer(sizer=self.sizer);
        # ----------------------------

    def init_controls (self):
        u""" ... """
        # ----------------------------
        self.input_panel = WX_PANEL_INPUT(parent=self);
        self.sizer.Add(item=self.input_panel, proportion=0, flag=wx.EXPAND|wx.ALL, border=2);
        # ----------------------------
        self.output_panel = WX_PANEL_OUTPUT(parent=self);
        self.sizer.Add(item=self.output_panel, proportion=0, flag=wx.EXPAND|wx.ALL, border=2);
        # ----------------------------
        self.controls_panel = WX_PANEL_CONTROLS(parent=self);
        self.sizer.Add(item=self.controls_panel, proportion=0, flag=wx.EXPAND|wx.ALL, border=2);
        # ----------------------------
        self.gauge_panel = WX_PANEL_GAUGE(parent=self);
        self.sizer.Add(item=self.gauge_panel, proportion=0, flag=wx.EXPAND|wx.ALL, border=2);
        # ----------------------------


# ------------------------------------------------------------------------------

class WX_FRAME_TRANSLITERATE_TEXT (wx.MiniFrame):
    u""" ... """

    def __init__ (self,
        parent,
        id    = wx.ID_ANY,
        title = u"Transliterate Text Document",
        pos   = wx.DefaultPosition,
        size  = (900, 200),
        style = wx.CAPTION
                | wx.CLOSE_BOX
                # | wx.RESIZE_BORDER
                | wx.WS_EX_TRANSIENT
                | wx.FRAME_NO_TASKBAR
    ):
        wx.MiniFrame.__init__(self, parent=parent, id=id, title=title, pos=pos, size=size, style=style);
        self.parent = parent;
        # ----------------------------
        self.init_style();
        self.init_transliterator();
        self.init_controls();
        self.init_handlers();
        self.init_view();
        # ----------------------------

    def init_style (self):
        u""" ... """
        # ----------------------------
        self.icon = wx.Icon(name=wxdefs.BITMAPS[u"transliterate_txt"]);
        self.SetIcon(icon=self.icon);
        # ----------------------------

    def init_transliterator (self):
        u""" ... """
        # ----------------------------
        self.transliterator = self.parent.transliterator;
        self.labels = self.transliterator.get_column_labels();
        self.encoded = self.transliterator.is_encoded();
        if (self.encoded): # i.e. (self.encoded = True)
            self.encoding = self.transliterator.get_encoding();
            self.transliterator.decode();
        else: # i.e. (self.encoded = False)
            pass;
        # ----------------------------
        self.parent.Disable();
        # ----------------------------

    def init_controls (self):
        u""" ... """
        # ----------------------------
        self.main_panel = WX_PANEL_TRANSLITERATE_TEXT(parent=self);
        # ----------------------------

    def init_handlers (self):
        u""" ... """
        # ----------------------------
        self.Bind(event=wx.EVT_CLOSE, source=self, handler=self.handle_close);
        # ----------------------------
        self.Bind(event=wx.EVT_BUTTON, source=self.main_panel.input_panel.file_button, handler=self.handle_button_file);
        self.Bind(event=wx.EVT_BUTTON, source=self.main_panel.output_panel.folder_button, handler=self.handle_button_folder);
        self.Bind(event=wx.EVT_BUTTON, source=self.main_panel.controls_panel.transliterate_button, handler=self.handle_button_transliterate);
        # ----------------------------
        self.Bind(event=wx.EVT_COMBOBOX, source=self.main_panel.controls_panel.source_combo, handler=self.handle_combo_source_changed);
        self.Bind(event=wx.EVT_COMBOBOX, source=self.main_panel.controls_panel.target_combo, handler=self.handle_combo_target_changed);
        # ----------------------------
        dispatcher.connect(
            signal   = threadingdefs.GLOBAL_SIGNAL_INDEX[u"TRANSLITERATOR_STREAM_START"],
            sender   = threadingdefs.GLOBAL_SENDER_ANY,
            receiver = self.handle_stream_start,
        );
        dispatcher.connect(
            signal   = threadingdefs.GLOBAL_SIGNAL_INDEX[u"TRANSLITERATOR_STREAM_STEP"],
            sender   = threadingdefs.GLOBAL_SENDER_ANY,
            receiver = self.handle_stream_step,
        );
        dispatcher.connect(
            signal   = threadingdefs.GLOBAL_SIGNAL_INDEX[u"TRANSLITERATOR_STREAM_END"],
            sender   = threadingdefs.GLOBAL_SENDER_ANY,
            receiver = self.handle_stream_end,
        );
        # ----------------------------

    def init_view (self):
        u""" ... """
        # ----------------------------
        # self.Fit();
        self.Show(show=True);
        self.CenterOnParent(dir=wx.BOTH);
        # self.CenterOnScreen(dir=wx.BOTH);
        # ----------------------------

    def handle_button_file (self, event):
        u""" ... """
        # ----------------------------
        # [1] CONSTRUCT THE INPUT FILE DIALOG:
        file_dialog = wx.FileDialog(
            parent      = self,
            message     = u"Select Input Text Document...",
            defaultDir  = r"C:\Users\User\Documents",
            defaultFile = u"",
            wildcard    = u"Text files (*.txt)|*.txt|All files (*.*)|*.*",
            style       = wx.FD_OPEN
                            | wx.FD_CHANGE_DIR,
        );
        # ----------------------------
        # [2] HANDLE THE INPUT FILE DIALOG RESULT:
        if (file_dialog.ShowModal() == wx.ID_OK):
            # ----------------------------
            path      = file_dialog.GetPath();
            directory = file_dialog.GetDirectory();
            # ----------------------------
            self.main_panel.input_panel.path_text.SetValue(value=path);
            self.main_panel.output_panel.path_text.SetValue(value=directory);
            # ----------------------------
        else: # (file_dialog.ShowModal() == wx.ID_CANCEL)
            pass;
        # ----------------------------
        # [3] DESTROY THE INPUT FILE DIALOG:
        file_dialog.Destroy();
        # ----------------------------
        # event.Skip(); # i.e. propagate the event further...
        # ----------------------------

    def handle_button_folder (self, event):
        u""" ... """
        # ----------------------------
        # [1] CONSTRUCT THE OUTPUT DIRECTORY DIALOG:
        directory_dialog = wx.DirDialog(
            parent      = self,
            message     = u"Select Output Folder...",
            defaultPath = r"C:\Users\User\Documents",
            style       = wx.DD_DEFAULT_STYLE
                            | wx.DD_CHANGE_DIR,
        );
        # ----------------------------
        # [2] HANDLE THE OUTPUT DIRECTORY DIALOG RESULT:
        if (directory_dialog.ShowModal() == wx.ID_OK):
            # ----------------------------
            path = directory_dialog.GetPath();
            # ----------------------------
            self.main_panel.output_panel.path_text.SetValue(value=path);
            # ----------------------------
        else: # (directory_dialog.ShowModal() == wx.ID_CANCEL)
            pass;
        # ----------------------------
        # [3] DESTROY THE OUTPUT DIRECTORY DIALOG:
        directory_dialog.Destroy();
        # ----------------------------
        # event.Skip(); # i.e. propagate the event further...
        # ----------------------------

    def handle_button_transliterate (self, event):
        # ----------------------------
        input_value  = self.main_panel.input_panel.path_text.GetValue();
        if (input_value): # i.e. (input_value != u"")
            # ----------------------------
            input_path = pathutils.Path(path=input_value);
            input_stem = input_path.stem;
            input_ext  = input_path.ext;
            # ----------------------------
            output_value = self.main_panel.output_panel.path_text.GetValue();
            if (output_value): # i.e. (output_value != u"")
                output_dir = output_value;
            else: # i.e. (output_value == u"")
                output_dir = input_path.dir;
            output_basename = u"{0:s}_TRANSLITERATED.{1:s}".format(input_stem, input_ext);
            output_path     = os.path.join(output_dir, output_basename);
            # ----------------------------
            filter_value = self.main_panel.controls_panel.filter_checkbox.GetValue();
            # ----------------------------
            stream_thread = threading.Thread(
                target = self.transliterator.stream,
                kwargs = {
                    u"input_path":  input_path.path,
                    u"output_path": output_path,
                    u"filter":      filter_value,
                },
            );
            stream_thread.daemon = True;
            stream_thread.start();
            # ----------------------------
        else: # i.e. (input_value == u"")
            pass;
        # ----------------------------

    def handle_close (self, event):
        u""" ... """
        # ----------------------------
        if (self.encoded): # i.e. (self.encoded == True)
            self.transliterator.encode(encoding=self.encoding);
        else: # i.e. (self.encoded == False)
            pass;
        # ----------------------------
        source_label = self.transliterator.get_source();
        source_index = self.labels.index(source_label);
        target_label = self.transliterator.get_target();
        target_index = self.labels.index(target_label);
        wx.CallAfter(self.parent.main_panel.controls.source_combo.Select, n=source_index);
        wx.CallAfter(self.parent.main_panel.controls.target_combo.Select, n=target_index);
        wx.CallAfter(self.parent.main_panel.controls.Refresh);
        wx.CallAfter(self.parent.Enable);
        # ----------------------------
        event.Skip(); # i.e. propagate the wx.EVT_CLOSE event further...
        # ----------------------------

    def handle_stream_start (self):
        u""" ... """
        # ----------------------------
        self.main_panel.input_panel.Disable();
        self.main_panel.output_panel.Disable();
        self.main_panel.controls_panel.Disable();
        self.EnableCloseButton(enable=False);
        # ----------------------------

    def handle_stream_step (self, current, total):
        u""" ... """
        # ----------------------------
        percent = (current / float(total)) * 100;
        # ----------------------------
        wx.CallAfter(self.main_panel.gauge_panel.gauge.set_value, value=percent);
        wx.CallAfter(self.main_panel.gauge_panel.progress_text.SetLabelText, text=u"{0:.03f}%".format(percent));
        wx.CallAfter(self.main_panel.gauge_panel.Refresh);
        # ----------------------------

    def handle_stream_end (self):
        u""" ... """
        # ----------------------------
        self.main_panel.input_panel.Enable();
        self.main_panel.output_panel.Enable();
        self.main_panel.controls_panel.Enable();
        self.EnableCloseButton(enable=True);
        # ----------------------------

    def handle_combo_source_changed (self, event):
        u""" ... """
        # ----------------------------
        source = event.GetString();
        dispatcher.send(sender=self, signal=threadingdefs.GLOBAL_SIGNAL_INDEX[u"TABLE_CHANGE_SOURCE"], source=source);
        # ----------------------------
        # event.Skip(); # i.e. propagate the event further...
        # ----------------------------

    def handle_combo_target_changed (self, event):
        u""" ... """
        # ----------------------------
        target = event.GetString();
        dispatcher.send(sender=self, signal=threadingdefs.GLOBAL_SIGNAL_INDEX[u"TABLE_CHANGE_TARGET"], target=target);
        # ----------------------------
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
        self.input_frame = WX_FRAME_TRANSLITERATE_TEXT(parent=None);
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
        self.yielder_thread = self.yielder(run=self.run, delay=0.137);
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

    print u"\n>> A \"stcutils.pyw\" is done.";