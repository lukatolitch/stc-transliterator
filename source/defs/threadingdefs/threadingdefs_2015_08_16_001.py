# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------

from pydispatch import dispatcher as dispatcher

# ------------------------------------------------------------------------------

GLOBAL_ENCODING_CURRENT = u"utf-8";

# ------------------------------------------------------------------------------

GLOBAL_SIGNALS = [
    # ----------------------------
    # [1] THREADING SIGNALS:
    u"THREAD_START",
    u"THREAD_PAUSE",
    u"THREAD_RESUME",
    u"THREAD_STEP",
    u"THREAD_STOP",
    u"THREAD_DONE",
    u"THREAD_END",
    # ...
    # ----------------------------
    # [2] TABLE SIGNALS:
    u"TABLE_INITIALIZED",
    u"TABLE_READ",
    u"TABLE_CLEARED",
    u"TABLE_REMAPPED",
    u"TABLE_RESET",
    u"TABLE_ENCODED",
    u"TABLE_DECODED",
    u"TABLE_SORTED",
    u"TABLE_WRITTEN",
    # ...
    u"TABLE_CHANGE_SOURCE",
    u"TABLE_CHANGE_TARGET",
    u"TABLE_CHANGE_MAP",
    # ...
    # ----------------------------
    # [3] TRANSLITERATOR SIGNALS:
    u"TRANSLITERATOR_INITIALIZED",
    u"TRANSLITERATOR_TRANSLITERATED",
    u"TRANSLITERATOR_FILTERED",
    u"TRANSLITERATOR_SEGMENTED",
    u"TRANSLITERATOR_DERIVED",
    u"TRANSLITERATOR_INTEGRATED",
    u"TRANSLITERATOR_PARSED",
    u"TRANSLITERATOR_STREAM_START",
    u"TRANSLITERATOR_STREAM_STEP",
    u"TRANSLITERATOR_STREAM_END",
    # ...
    # ----------------------------
    # [4] WX SIGNALS:
    u"YIELD_START",
    u"YIELD_STEP",
    u"YIELD_END",
    # ...
    # [5] STC_SIGNALS:
    u"STC_INPUT_UPDATE",
    u"STC_OUTPUT_UPDATE",
    u"STC_INPUT_PAINTED",
    u"STC_OUTPUT_PAINTED",
    u"STC_TRANSLITERATE",
    u"STC_TRANSLITERATION_DONE",
    # ...
]; # GLOBAL_SIGNALS

GLOBAL_SIGNAL_COUNT = len(GLOBAL_SIGNALS);
GLOBAL_SIGNAL_INDEX = dict((name,index) for (index,name) in enumerate(GLOBAL_SIGNALS));
GLOBAL_SIGNAL_NAME  = dict((index,name) for (name,index) in GLOBAL_SIGNAL_INDEX.iteritems());

GLOBAL_SENDER_ANY       = dispatcher.Any;
GLOBAL_SENDER_ANONYMOUS = dispatcher.Anonymous;

# ------------------------------------------------------------------------------