# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------

# TO (EVENTUALLY) DO (2015-08-09):

# IOTable (IndexedDict) [1]
# SortedTable (IOTable) [2]
# MappedTable (SortedTable) [3]
# CachedTable (MappedTable) [4]
# EncodedTable (CachedTable) [5]
# SimpleTransliterator (EncodedTable) [6]
# Transliterator (SimpleTransliterator) [7]
# PyTransliterator (Transliterator) [8]
# SimpleUTF8Transliterator (EncodedTable) [9]
# UTF8Transliterator (SimpleUTF8Transliterator) [10]
# SimpleUnicodeTransliterator (CachedTable) [11]
# UnicodeTransliterator (SimpleUnicodeTransliterator) [12]

# IOTable (IndexedDict) [1]
#  - SortedTable (IOTable) [1.1]
#     - MappedTable (SortedTable) [1.1.1]
#        - CachedTable (MappedTable) [1.1.1.1]
#           - EncodedTable (CachedTable) [1.1.1.1.1]
#              - SimpleTransliterator (EncodedTable) [1.1.1.1.1.1]
#                 - Transliterator (SimpleTransliterator) [1.1.1.1.1.1.1]
#                    - PyTransliterator (Transliterator) [1.1.1.1.1.1.1.1]
#              - SimpleUTF8Transliterator (EncodedTable) [1.1.1.1.1.2]
#                 - UTF8Transliterator (SimpleUTF8Transliterator) [1.1.1.1.1.2.1]
#           - SimpleUnicodeTransliterator (CachedTable) [1.1.1.1.2]
#              - UnicodeTransliterator (SimpleUnicodeTransliterator) [1.1.1.1.2.1]

# ------------------------------------------------------------------------------

# import os as os
import re as re
import csv as csv
# import time as time
import codecs as codecs
# import threading as threading
from collections import OrderedDict as OrderedDict

from pydispatch import dispatcher as dispatcher

from defs.globaldefs import globaldefs_2015_08_14_001 as globaldefs
from defs.threadingdefs import threadingdefs_2015_08_16_001 as threadingdefs
from utils.xmlutils import xmlutils_2015_08_14_001 as xmlutils
from utils.pathutils import pathutils_2015_08_14_001 as pathutils

import pyximport
pyximport.install();
from cutils import cutils_v19_2015_08_18_002 as cutils

# import pprint as pprint
# pprinter = pprint.PrettyPrinter(indent=4, width=80);

# ------------------------------------------------------------------------------

GLOBAL_ENCODING_CURRENT        = u"utf-8";
GLOBAL_ENCODING_TRANSLITERATOR = u"utf-8";

# ------------------------------------------------------------------------------

# GENERAL INSTANCE GET (READ-ONLY) DATA DESCRIPTOR:

class GET (object):
    def __get__ (self, INSTANCE, CLASS=None):
        return (None);
    def __set__ (self, INSTANCE, arg):
        raise AttributeError;

# TABLE INSTANCE GET (READ-ONLY) DATA DESCRIPTORS:

class TABLE_GET_TABLE (GET):
    def __get__ (self, INSTANCE, CLASS=None):
        first_column_width = 32;
        col_width = 16;
        col_labels = INSTANCE.get_column_labels();
        table = (u"-" * 50) + "\n" + "".ljust(first_column_width) + u"".join([col_label.center(col_width) for col_label in col_labels]) + u"\n";
        for (row_label, columns_dict) in (INSTANCE.items()):
            cell = [];
            for (col_label) in (col_labels):
                cell.append(u",".join(INSTANCE[row_label][col_label]).center(col_width));
            # for (col_label)
            table += row_label.ljust(first_column_width) + u"".join(cell) + u"\n";
        # for (row_label, columns_dict)
        return (table);

class TABLE_GET_TRANSPOSED (GET):
    def __get__ (self, INSTANCE, CLASS=None):
        strings = [];
        columns = INSTANCE.get_columns();
        for (col_label, strings_list) in columns.iteritems():
            string = u"{0:s}: {1:s}".format(col_label, strings_list);
            strings.append(string);
        # for (col_label, strings_list)
        string = u"\n".join(strings) + u"\n";
        return (string);

# ------------------------------------------------------------------------------

class TableDialect (csv.Dialect):
    u""" ... """

    def __init__ (self, *args, **kwargs):
        u""" ... """
        # ----------------------------
        self.delimiter        = u";".encode(u"utf-8");
        self.lineterminator   = u"\r\n".encode(u"utf-8");
        self.quoting          = csv.QUOTE_NONE;
        self.doublequote      = False;
        self.escapechar       = None;
        self.skipinitialspace = True;
        self.strict           = False;
        # ----------------------------

# ------------------------------------------------------------------------------

class IndexedDict (OrderedDict):
    u""" ... """

    # [1] CLASS DESCRIPTORS:

    # [1.1] STATIC (CLASS) DESCRIPTORS:
    # [1.1.1] STATIC (CLASS) GET-SET DATA DESCRIPTORS:
    # ...
    # [1.1.2] STATIC (CLASS) GET (READ-ONLY) DATA DESCRIPTORS:
    # ...
    # [1.1.3] STATIC (CLASS) NON-DATA DESCRIPTORS:
    # ...

    # [1.2] INSTANCE DESCRIPTORS:
    # [1.2.1] INSTANCE GET-SET DATA DESCRIPTORS:
    # ...
    # [1.2.2] INSTANCE GET (READ-ONLY) DATA DESCRIPTORS:
    # ...
    # [1.2.3] INSTANCE NON-DATA DESCRIPTORS:
    # ...

    # [2] CLASS CONSTRUCTION:
    # [2.1] CLASS CONSTRUCTOR (INITIALIZER):
    def __init__ (self):
        OrderedDict.__init__(self);
    # [2.2] CLASS RECONSTRUCTOR (CALLER):
    # def __call__ (self, *args, **kwargs):
    #     pass;
    # [2.3] CLASS DESTRUCTOR (DELETER):
    # def __del__ (self):
    #     pass;
    # [2.4] CLASS INSTANTIATOR:
    # def __new__ (self, *args, **kwargs):
    #     pass;

    # [3] CLASS CUSTOM METHODS:
    def get_index (self, key):
        for (index, KEY) in enumerate(self.iterkeys()):
            if (KEY == key):
                return (index);
            else: # i.e. (KEY != key)
                pass; # i.e. ignore...
        # for (index, KEY)
        return (None);

    def get_key (self, index):
        try:
            KEY = self.keys()[index]; # IndexError?
            return (KEY);
        except (IndexError):
            return (None);

    def get_value (self, index):
        try:
            VALUE = self.values()[index]; # IndexError?
            return (VALUE);
        except (IndexError):
            return (None);

    def get_item (self, index):
        try:
            ITEM = self.items()[index]; # IndexError?
            return (ITEM);
        except (IndexError):
            return (None);

    def get_length (self):
        return (len(self));

    # [5] CLASS REPRESENTATION:
    __name__ = u"IndexedDict";
    def __repr__ (self):
        return globaldefs.TEMPLATES_REPR[self.__name__].format(self).encode(globaldefs.ENCODING_CURRENT);
    def __str__ (self):
        return globaldefs.TEMPLATES_REPR[self.__name__].format(self).encode(globaldefs.ENCODING_CURRENT);
    def __unicode__ (self):
        return globaldefs.TEMPLATES_REPR[self.__name__].format(self);

    # [6] CLASS SLOTS RESTRICTION:
    __slots__ = (
        # u"__weakref__",
    );

# ------------------------------------------------------------------------------

class Table(IndexedDict):
    u""" ... """

    table      = TABLE_GET_TABLE();      # self.table
    transposed = TABLE_GET_TRANSPOSED(); # self.transposed

    def __init__ (self, path):
        u""" ... """
        # ----------------------------
        IndexedDict.__init__(self);
        # ----------------------------
        self._encoded_       = False;
        self._encoding_      = GLOBAL_ENCODING_TRANSLITERATOR;
        # ----------------------------
        self._source_        = None;
        self._target_        = None;
        # ----------------------------
        self._map_           = None;
        self._max_           = None;
        self._match_         = None;
        self._ids_           = None;
        self._indices_       = None;
        self._source_column_ = None;
        self._target_column_ = None;
        # ----------------------------
        self.init_handlers();
        # ----------------------------
        dispatcher.send(sender=self, signal=threadingdefs.GLOBAL_SIGNAL_INDEX[u"TABLE_INITIALIZED"]);
        # ----------------------------
        self.read(path=path);
        # ----------------------------

    def init_handlers (self):
        u""" ... """
        # ----------------------------
        dispatcher.connect(
            signal   = threadingdefs.GLOBAL_SIGNAL_INDEX[u"TABLE_CHANGE_SOURCE"],
            sender   = threadingdefs.GLOBAL_SENDER_ANY,
            receiver = self.handle_change_source,
            weak     = True,
        );
        # ----------------------------
        dispatcher.connect(
            signal   = threadingdefs.GLOBAL_SIGNAL_INDEX[u"TABLE_CHANGE_TARGET"],
            sender   = threadingdefs.GLOBAL_SENDER_ANY,
            receiver = self.handle_change_target,
            weak     = True,
        );
        # ----------------------------
        dispatcher.connect(
            signal   = threadingdefs.GLOBAL_SIGNAL_INDEX[u"TABLE_CHANGE_MAP"],
            sender   = threadingdefs.GLOBAL_SENDER_ANY,
            receiver = self.handle_change_map,
            weak     = True,
        );
        # ----------------------------

    def read (self, path):
        u""" ... """
        # ----------------------------
        self.path = pathutils.Path(path=path);
        # ----------------------------
        if (self.path.exists()): # i.e. self.path.exists() == True
            if (self.path.is_file()): # i.e. self.path.is_file() == True
                if (self.path.ext == u"csv"):
                    # ----------------------------
                    self.read_csv(path=self.path.path);
                    # ----------------------------
                    dispatcher.send(sender=self, signal=threadingdefs.GLOBAL_SIGNAL_INDEX[u"TABLE_READ"]);
                    # ----------------------------
                elif (self.path.ext == u"xml"):
                    # ----------------------------
                    self.read_xml(path=self.path.path);
                    # ----------------------------
                    dispatcher.send(sender=self, signal=threadingdefs.GLOBAL_SIGNAL_INDEX[u"TABLE_READ"]);
                    # ----------------------------
                # elif (self.path.ext == u"..."):
                #     pass;
                else: # i.e. self.path.ext not in (u"csv", u"xml", ...)
                    # ----------------------------
                    self.path = pathutils.Path(path=u"");
                    # ----------------------------
                    raise ValueError(u"Wrong transliterator file type!");
                    # ----------------------------
            else: # i.e. self.path.is_file() == False
                # ----------------------------
                self.path = pathutils.Path(path=u"");
                # ----------------------------
                raise ValueError(u"Not a file path!");
                # ----------------------------
        else: # i.e. self.path.exists() == True
            # ----------------------------
            self.path = pathutils.Path(path=u"");
            # ----------------------------
            raise ValueError(u"File does not exist!");
            # ----------------------------

    def clear (self):
        u""" 1e-05 usecs.  """
        # ----------------------------
        IndexedDict.clear(self);
        # ----------------------------
        self._source_        = None;
        self._target_        = None;
        # ----------------------------
        self._map_           = None;
        self._max_           = None;
        self._match_         = None;
        self._ids_           = None;
        self._indices_       = None;
        self._source_column_ = None;
        self._target_column_ = None;
        # ----------------------------
        dispatcher.send(sender=self, signal=threadingdefs.GLOBAL_SIGNAL_INDEX[u"TABLE_CLEARED"]);
        # ----------------------------

    def reset (self):
        u""" [9e-03, 2e-02] usecs. """
        # ----------------------------
        self._map_     = self.get_current_map();
        self._max_     = self.get_max_source_string_length();
        self._match_   = self.get_current_column_expression().match;
        self._ids_     = self.get_current_row_ids();
        self._indices_ = self.get_current_row_indices();
        self._source_column_, self._target_column_ = self.get_current_columns();
        # ----------------------------
        dispatcher.send(sender=self, signal=threadingdefs.GLOBAL_SIGNAL_INDEX[u"TABLE_RESET"]);
        # ----------------------------

    def encode (self, encoding=GLOBAL_ENCODING_TRANSLITERATOR):
        u""" ... """
        # ----------------------------
        self._encoding_ = encoding;
        self._encoded_  = True;
        # ----------------------------
        dispatcher.send(sender=self, signal=threadingdefs.GLOBAL_SIGNAL_INDEX[u"TABLE_ENCODED"]);
        # ----------------------------
        self.reset();
        # ----------------------------

    def decode (self):
        u""" ... """
        # ----------------------------
        self._encoded_ = False;
        # ----------------------------
        dispatcher.send(sender=self, signal=threadingdefs.GLOBAL_SIGNAL_INDEX[u"TABLE_DECODED"]);
        # ----------------------------
        self.reset();
        # ----------------------------

    def set_map (self, source, target):
        u""" ... """
        # ----------------------------
        self._source_ = source;
        self._target_ = target;
        # ----------------------------
        dispatcher.send(sender=self, signal=threadingdefs.GLOBAL_SIGNAL_INDEX[u"TABLE_REMAPPED"]);
        # ----------------------------
        self.reset();
        # ----------------------------

    def set_source (self, source):
        u""" ... """
        # ----------------------------
        self._source_ = source;
        # ----------------------------
        dispatcher.send(sender=self, signal=threadingdefs.GLOBAL_SIGNAL_INDEX[u"TABLE_REMAPPED"]);
        # ----------------------------
        self.reset();
        # ----------------------------

    def set_target (self, target):
        u""" ... """
        # ----------------------------
        self._target_ = target;
        # ----------------------------
        dispatcher.send(sender=self, signal=threadingdefs.GLOBAL_SIGNAL_INDEX[u"TABLE_REMAPPED"]);
        # ----------------------------
        self.reset();
        # ----------------------------

    def handle_change_map (self, source, target):
        u""" ... """
        # ----------------------------
        self.set_map(source=source, target=target)
        # ----------------------------

    def handle_change_source (self, source):
        u""" ... """
        # ----------------------------
        self.set_source(source=source);
        # ----------------------------

    def handle_change_target (self, target):
        u""" ... """
        # ----------------------------
        self.set_target(target=target);
        # ----------------------------

    def is_encoded (self):
        u""" ... """
        # ----------------------------
        return (self._encoded_);
        # ----------------------------

    def get_encoding (self):
        u""" ... """
        # ----------------------------
        return (self._encoding_);
        # ----------------------------

    def get_source (self):
        u""" ... """
        # ----------------------------
        return (self._source_);
        # ----------------------------

    def get_target (self):
        u""" ... """
        # ----------------------------
        return (self._target_);
        # ----------------------------

    def sort (self, column):
        u""" ... """
        # ----------------------------
        # [1] GET AND DOUBLE-SORT THE ROWS:
        rows = self.items();
        rows.sort(
            key = lambda row: row[1][column][0],
        ); # i.e. the first, default unicode collation sort of the rows by the first (if any) string of the selected column...
        rows.sort(
            key = lambda row: row[1][column][0],
            cmp = lambda string_i, string_j: cmp(string_i.upper(), string_j.upper()), # i.e. a case-indifferent strings comparison...
        ); # i.e. the second, case-indifferent sort of the rows, again by the first (if any) string of the selected column...
        # ----------------------------
        # [2] CLEAR, RE-APPEND, AND RESET THE INDEXED ORDERED DICT:
        IndexedDict.clear(self);
        for (key, value) in rows:
            self[key] = value;
        # for (key, value)
        # ----------------------------
        dispatcher.send(sender=self, signal=threadingdefs.GLOBAL_SIGNAL_INDEX[u"TABLE_SORTED"]);
        # ----------------------------
        self.reset();
        # ----------------------------

    def get_row_labels (self):
        u""" ... """
        # ----------------------------
        return (self.keys());
        # ----------------------------

    def get_column_labels (self):
        u""" ... """
        # ----------------------------
        row_labels = self.keys();
        # ----------------------------
        try:
            # ----------------------------
            first_row_label = row_labels[0]; # IndexError?
            col_labels      = self[first_row_label].keys();
            # ----------------------------
            return (col_labels);
            # ----------------------------
        except (IndexError):
            # ----------------------------
            return ([]);
            # ----------------------------

    def get_rows (self):
        u""" ... """
        # ----------------------------
        rows = [];
        # ----------------------------
        for row_label in self.iterkeys():
            # ----------------------------
            row = {};
            # ----------------------------
            for col_label in self[row_label].iterkeys():
                cell = self[row_label][col_label];
                row[col_label] = self.get_normalized_list_string(cell);
            # for (col_label)
            # ----------------------------
            rows.append(row);
            # ----------------------------
        # for (row_label)
        # ----------------------------
        return (rows);
        # ----------------------------

    def get_columns (self):
        u"""
            [5-04, 3e-03] usecs.

            i.e. get the transpose of the current transliteration table
        """
        # ----------------------------
        COLUMNS = {};
        # ----------------------------
        if (self._encoded_): # i.e. (self._encoded_ == True)
            for columns in self.itervalues():
                for (column, strings) in columns.iteritems():
                    # ----------------------------
                    strings = [string.encode(self._encoding_) for string in strings];
                    # ----------------------------
                    try:
                        COLUMNS[column].append(strings); # KeyError?
                    except (KeyError):
                        COLUMNS[column] = [strings];
                    # ----------------------------
                # for (column, strings)
            # for (columns)
        else: # i.e. (self._encoded_ == False)
            for columns in self.itervalues():
                for (column, strings) in columns.iteritems():
                    try:
                        COLUMNS[column].append(strings); # KeyError?
                    except (KeyError):
                        COLUMNS[column] = [strings];
                # for (column, strings)
            # for (columns)
        # ----------------------------
        return (COLUMNS)
        # ----------------------------

    def get_current_columns (self):
        u""" [2e-04, 6e-04] usecs """
        # ----------------------------
        source_column = [];
        target_column = [];
        # ----------------------------
        if (self._encoded_): # i.e. (self._encoded_ == True)
            # ----------------------------
            for columns in self.itervalues():
                source_column.append([string.encode(self._encoding_) for string in columns[self._source_]]);
                target_column.append([string.encode(self._encoding_) for string in columns[self._target_]]);
            # for (columns)
            # ----------------------------
        else: # i.e. (self._encoded_ == False)
            # ----------------------------
            for columns in self.itervalues():
                source_column.append(columns[self._source_]);
                target_column.append(columns[self._target_]);
            # for (columns)
        # ----------------------------
        return (source_column, target_column);
        # ----------------------------

    def cmp_string_len (self, Si, Sj):
        u""" ... """
        # ----------------------------
        if (len(Si) < len(Sj)):
            return (1);
        elif (len(Si) > len(Sj)):
            return (-1);
        else: # i.e. len(Si) == len(Sj)
            return (0);
        # ----------------------------

    def get_column_expressions (self):
        u""" [2e-03, 3e-02] usecs. """
        # ----------------------------
        col_expressions = {};
        # ----------------------------
        if (self._encoded_): # i.e. (self._encoded_ == True)
            # ----------------------------
            for columns_dict in self.itervalues():
                for (col_label, cell) in columns_dict.iteritems():
                    for string in cell:
                        try:
                            col_expressions[col_label].append(string.encode(self._encoding_)); # KeyError?
                        except (KeyError):
                            col_expressions[col_label] = [string.encode(self._encoding_)];
                    # for (string)
                # for (col_label, cell)
            # for (columns_dict)
            # ----------------------------
            for (col_label, strings) in col_expressions.iteritems():
                sorted_strings = sorted(sorted(strings), cmp=self.cmp_string_len);
                col_expressions[col_label] = re.compile(
                    u"|".encode(self._encoding_).join(
                        [u"%s".encode(self._encoding_)%(string) for string in sorted_strings if string != u"".encode(self._encoding_)]
                    )
                );
            # for (col_label, strings)
            # ----------------------------
        else: # i.e. (self._encoded_ == False)
            # ----------------------------
            for columns_dict in self.itervalues():
                for (col_label, cell) in columns_dict.iteritems():
                    for string in cell:
                        try:
                            col_expressions[col_label].append(string); # KeyError?
                        except (KeyError):
                            col_expressions[col_label] = [string];
                    # for (string)
                # for (col_label, cell)
            # for (columns_dict)
            # ----------------------------
            for (col_label, strings) in col_expressions.iteritems():
                sorted_strings = sorted(sorted(strings), cmp=self.cmp_string_len);
                col_expressions[col_label] = re.compile(
                    u"|".join(
                        [u"%s"%(string) for string in sorted_strings if string != u""]
                    )
                );
            # for (col_label, strings)
        # ----------------------------
        return (col_expressions);
        # ----------------------------

    def get_current_column_expression (self):
        u""" [6e-04, 8e-03] usecs. """
        # ----------------------------
        strings = [];
        # ----------------------------
        for columns in self.itervalues():
            strings.extend([string for string in columns[self._source_]]);
        # for (columns)
        # ----------------------------
        strings.sort();
        strings.sort(cmp=self.cmp_string_len);
        # ----------------------------
        if (self._encoded_): # i.e. (self._encoded_ == True)
            column_expression = re.compile(
                u"|".encode(self._encoding_).join(
                    [u"%s".encode(self._encoding_)%(string.encode(self._encoding_)) for string in strings if string != u"".encode(self._encoding_)]
                )
            );
        else: # i.e. (self._encoded_ == False)
            column_expression = re.compile(
                u"|".join(
                    [u"%s"%(string) for string in strings if string != u""]
                )
            );
        # ----------------------------
        return (column_expression);
        # ----------------------------

    def get_max_string_lengths (self):
        u""" in [1e-03, 2e-03] ([0.001, 0.002]) usecs. """
        # ----------------------------
        lengths = {};
        # ----------------------------
        if (self._encoded_): # i.e. (self._encoded_ == True)
            for columns_dict in self.itervalues():
                for (col_label, strings) in columns_dict.iteritems():
                    try:
                        lengths[col_label] = max([lengths[col_label]] + [len(string.encode(self._encoding_)) for string in strings]);
                    except (KeyError):
                        lengths[col_label] = max(len(string.encode(self._encoding_)) for string in strings);
                # for (col_label, strings)
            # for (columns_dict)
        else: # i.e. (self._encoded_ == False)
            for columns_dict in self.itervalues():
                for (col_label, strings) in columns_dict.iteritems():
                    try:
                        lengths[col_label] = max([lengths[col_label]] + [len(string) for string in strings]);
                    except (KeyError):
                        lengths[col_label] = max(len(string) for string in strings);
                # for (col_label, strings)
            # for (columns_dict)
        # ----------------------------
        return (lengths);
        # ----------------------------

    def get_max_source_string_length (self):
        u""" in [3e-04, 4e-04] ([0.0003, 0.0004]) usecs. """
        # ----------------------------
        max_length = 0;
        # ----------------------------
        if (self._encoded_): # i.e. (self._encoded_ == True)
            for columns in self.itervalues():
                strings = columns[self._source_];
                max_length = max([max_length] + [len(string.encode(self._encoding_)) for string in strings]);
            # for (columns)
        else: # i.e. (self._encoded_ == False)
            for columns in self.itervalues():
                strings = columns[self._source_];
                max_length = max([max_length] + [len(string) for string in strings]);
            # for (columns)
        # ----------------------------
        return (max_length);
        # ----------------------------

    def get_map (self):
        u"""
            3e-03 usecs.

            # ----------------------------
            [1] TRANSLITERATOR MAP (DICT):

                [1.1]
                    MAP = {
                        u"CYRILLIC": {
                            u"RUSSCII": {..., u"щ": u"shh", ...},
                            u"RUSSHR":  {..., u"щ": u"šš", ...},
                            ...
                        },
                        u"RUSSCII": {
                            u"CYRILLIC": {..., u"shh": u"щ", ...},
                            u"RUSSHR":  {..., u"shh": u"šš", ...},
                            ...
                        },
                        u"RUSSHR": {
                            u"CYRILLIC": {..., u"šš": u"щ", ...},
                            u"RUSSCII": {..., u"šš": u"shh", ...},
                            ...
                        },
                        ...
                    };

                [1.2]
                    MAP[u"CYRILLIC"] = {
                        u"RUSSCII": {..., u"щ": u"shh", ...},
                        u"RUSSHR":  {..., u"щ": u"šš", ...},
                        ...
                    };

                [1.3]
                    MAP[u"CYRILLIC"][u"RUSSCII"] = {..., u"щ": u"shh", ...};
                    MAP[u"CYRILLIC"][u"RUSSHR"]  = {..., u"щ": u"šš", ...};

                [1.4]
                    MAP[u"CYRILLIC"][u"RUSSCII"][u"щ"] = u"shh";
                    MAP[u"CYRILLIC"][u"RUSSHR"][u"щ"]  = u"šš";
            # ----------------------------
        """
        # ----------------------------
        source_dict = {};
        target_dict = {};
        for (row_label, columns_dict) in self.iteritems():
            for (col_label, cell) in columns_dict.iteritems():
                for string in cell:
                    try:
                        source_dict[col_label][string] = row_label; # KeyError?
                        try:
                            target_dict[col_label][row_label]; # KeyError?
                        except (KeyError):
                            target_dict[col_label][row_label] = string;
                    except (KeyError):
                        source_dict[col_label] = {string: row_label};
                        target_dict[col_label] = {row_label: string};
                # for (string)
            # for (col_label, cell)
        # for (row_label, columns_dict)
        # ----------------------------
        map_dict = {};
        if (self._encoded_): # i.e. (self._encoded_ == True)
            for (source_column_label, source_columns_dict) in source_dict.iteritems():
                map_dict[source_column_label] = {};
                for (target_column_label, target_columns_dict) in target_dict.iteritems():
                    for (source_string, row_label) in source_columns_dict.iteritems():
                        # ----------------------------
                        source_string = source_string.encode(self._encoding_);
                        target_string = target_columns_dict[row_label].encode(self._encoding_);
                        # ----------------------------
                        try:
                            map_dict[source_column_label][target_column_label][source_string] = target_string; # KeyError?
                        except (KeyError):
                            map_dict[source_column_label][target_column_label] = {source_string: target_string};
                        # ----------------------------
                    # for (source_string, row_label)
                # for (target_column_label, target_columns_dict)
            # for (source_column_label, source_columns_dict)
        else: # i.e. (self._encoded_ == False)
            for (source_column_label, source_columns_dict) in source_dict.iteritems():
                map_dict[source_column_label] = {};
                for (target_column_label, target_columns_dict) in target_dict.iteritems():
                    for (source_string, row_label) in source_columns_dict.iteritems():
                        # ----------------------------
                        target_string = target_columns_dict[row_label];
                        # ----------------------------
                        try:
                            map_dict[source_column_label][target_column_label][source_string] = target_string; # KeyError?
                        except (KeyError):
                            map_dict[source_column_label][target_column_label] = {source_string: target_string};
                        # ----------------------------
                    # for (source_string, row_label)
                # for (target_column_label, target_columns_dict)
            # for (source_column_label, source_columns_dict)
        # ----------------------------
        return (map_dict);
        # ----------------------------

    def get_current_map (self):
        u""" [2e-04, 6e-04] usecs. """
        # ----------------------------
        current_map = {};
        # ----------------------------
        if (self._encoded_): # i.e. (self._encoded_ == True)
            for (id, columns) in self.iteritems():
                # ----------------------------
                source_strings = columns[self._source_];
                target_string  = columns[self._target_][0];
                # ----------------------------
                for source_string in source_strings:
                    current_map[source_string.encode(self._encoding_)] = target_string.encode(self._encoding_);
                # for (source_string)
                # ----------------------------
            # for (id, columns)
        else: # i.e. (self._encoded_ == False)
            for (id, columns) in self.iteritems():
                # ----------------------------
                source_strings = columns[self._source_];
                target_string  = columns[self._target_][0];
                # ----------------------------
                for source_string in source_strings:
                    current_map[source_string] = target_string;
                # for (source_string)
                # ----------------------------
            # for (id, columns)
        # ----------------------------
        return (current_map);
        # ----------------------------

    def get_row_ids (self):
        u""" [1e-03, 2e-03] usecs. """
        # ----------------------------
        row_ids = {};
        for (row_id, columns_dict) in self.iteritems():
            for (col_id, string_list) in columns_dict.iteritems():
                # ----------------------------
                try:
                    row_ids[col_id]; # KeyError?
                except (KeyError):
                    row_ids[col_id] = {};
                # ----------------------------
                for string in string_list:
                    try:
                        row_ids[col_id][string].append(row_id); # KeyError?
                    except (KeyError):
                        row_ids[col_id][string] = [row_id];
                # for (string)
                # ----------------------------
            # for (col_id, string_list)
        # for (row_id, columns_dict)
        # ----------------------------
        return (row_ids);
        # ----------------------------

    def get_current_row_ids (self):
        u""" [3e-04, 5e-04] usecs. """
        # ----------------------------
        row_ids = {};
        # ----------------------------
        for (id, columns) in self.iteritems():
            for string in columns[self._source_]:
                try:
                    row_ids[string].append(id); # KeyError?
                except (KeyError):
                    row_ids[string] = [id];
            # for (string)
        # for (id, columns)
        # ----------------------------
        return (row_ids);
        # ----------------------------

    def get_row_indices (self):
        u""" 2e-02 usecs. """
        # ----------------------------
        row_indices = {};
        # ----------------------------
        for (row_id, columns_dict) in self.iteritems():
            for (col_id, string_list) in columns_dict.iteritems():
                # ----------------------------
                try:
                    row_indices[col_id]; # KeyError?
                except (KeyError):
                    row_indices[col_id] = {};
                # ----------------------------
                for string in string_list:
                    try:
                        index = self.get_index(key=row_id);
                        row_indices[col_id][string].append(index); # KeyError?
                    except (KeyError):
                        index = self.get_index(key=row_id);
                        row_indices[col_id][string] = [index];
                # for (string)
                # ----------------------------
            # for (col_id, string_list)
        # for (row_id, columns_dict)
        # ----------------------------
        return (row_indices);
        # ----------------------------

    def get_current_row_indices (self):
        u""" [3e-03, 4e-03] usecs. """
        # ----------------------------
        row_indices = {};
        # ----------------------------
        for (id, columns) in self.iteritems():
            # ----------------------------
            index = self.get_index(key=id);
            # ----------------------------
            for string in columns[self._source_]:
                try:
                    row_indices[string].append(index); # KeyError?
                except (KeyError):
                    row_indices[string] = [index];
            # for (string)
            # ----------------------------
        # for (id, columns)
        # ----------------------------
        return (row_indices);
        # ----------------------------

    def get_xml (self):
        u""" ... """
        # ----------------------------
        xml_doc = xmlutils.minidom.Document();
        xml_table = xml_doc.createElement(u"table");
        xml_doc.appendChild(xml_table);
        # ----------------------------
        for row_label in self.iterkeys():
            # ----------------------------
            xml_row = xml_doc.createElement(u"row");
            xml_row.setAttribute(u"label", row_label);
            xml_table.appendChild(xml_row);
            # ----------------------------
            for col_label in self[row_label].iterkeys():
                # ----------------------------
                xml_column = xml_doc.createElement(u"column");
                xml_column.setAttribute(u"label", col_label);
                xml_row.appendChild(xml_column);
                # ----------------------------
                for string in self[row_label][col_label]:
                    xml_string = xml_doc.createElement(u"string");
                    xml_string.appendChild(xml_doc.createTextNode(string));
                    xml_column.appendChild(xml_string);
                # for (string)
                # ----------------------------
            # for (col_label)
            # ----------------------------
        # for (row_label)
        # ----------------------------
        return (xml_doc);
        # ----------------------------

    def get_encoded_csv_string (self, csv_string):
        u""" ... """
        return (csv_string.encode(globaldefs.ENCODING_STANDARD));

    def get_decoded_csv_string (self, csv_string):
        u""" ... """
        return (csv_string.decode(globaldefs.ENCODING_STANDARD));

    def get_normalized_csv_string (self, csv_string):
        u""" ... """
        # ----------------------------
        normalized_csv_string = csv_string;
        # ----------------------------
        for normalization in (u"CLEAR_SEPARATOR", u"REDUCE_EMPTY"):
            pattern, replacement  = globaldefs.RE[normalization];
            normalized_csv_string = re.sub(pattern, replacement, normalized_csv_string);
        # for (normalization)
        # ----------------------------
        return (normalized_csv_string);
        # ----------------------------

    def get_normalized_list_string (self, cell):
        u""" ... """
        # ----------------------------
        normalized_string = globaldefs.CSV_SEPARATOR.decode(globaldefs.ENCODING_STANDARD).join(cell);
        # ----------------------------
        for normalization in (u"CLEAR_SEPARATOR", u"REDUCE_EMPTY"):
            pattern, replacement = globaldefs.RE[normalization];
            normalized_string    = re.sub(pattern, replacement, normalized_string);
        # for (normalization)
        # ----------------------------
        return (normalized_string);
        # ----------------------------

    def yield_encoded_csv_rows (self, csv_file):
        u""" ... """
        for csv_row_string in csv_file:
            yield (self.get_encoded_csv_string(csv_row_string));
        # for (csv_row_string)

    def get_normalized_csv_row (self, csv_row):
        u""" ... """
        # ----------------------------
        normalized_csv_row = [];
        # ----------------------------
        for csv_column_string in csv_row:
            decoded_csv_column_string    = self.get_decoded_csv_string(csv_column_string);
            normalized_csv_column_string = self.get_normalized_csv_string(decoded_csv_column_string);
            normalized_csv_row.append(normalized_csv_column_string);
        # for (csv_column_string)
        # ----------------------------
        return (normalized_csv_row);
        # ----------------------------

    def read_csv (self, path=None):
        u"""
            # ----------------------------
            [1] CSV FILE:

                [1.1]
                    "
                    ID;CYRILLIC;RUSSCII;RUSSHR
                    ...
                    U+0449;щ;shh,shch;šš,šč,šć
                    ...
                    "
            # ----------------------------
            [2] TRANSLITERATOR (INDEXED ORDERED DICT):

                [2.1] TRANSLITERATOR ROWS (INDEXED ORDERED DICTS):
                    Transliterator = {
                        ...
                        u"U+0449": {
                            u"CYRILLIC": [u"щ"],
                            u"RUSSCII": [u"shh", u"shch"],
                            u"RUSSHR":  [u"šš", u"šč", u"šć"],
                            ...
                        },
                        ...
                    };

                [2.2] ROW COLUMNS (INDEXED ORDERED DICTS):
                    Transliterator[u"U+0449"] = {
                        u"CYRILLIC": [u"щ"],
                        u"RUSSCII": [u"shh", u"shch"],
                        u"RUSSHR":  [u"šš", u"šč", u"šć"],
                        ...
                    };

                [2.3] COLUMN STRINGS (LISTS):
                    Transliterator[u"U+0449"][u"CYRILLIC"] = [u"щ"];
                    Transliterator[u"U+0449"][u"RUSSCII"] = [u"shh", u"shch"];
                    Transliterator[u"U+0449"][u"RUSSHR"]  = [u"šš", u"šč", u"šć"];

                [2.4] STRINGS:
                    Transliterator[u"U+0449"][u"CYRILLIC"][0] = u"щ"; # DEFAULT
                    Transliterator[u"U+0449"][u"RUSSCII"][0] = u"shh"; # DEFAULT
                    Transliterator[u"U+0449"][u"RUSSCII"][1] = u"shch";
                    Transliterator[u"U+0449"][u"RUSSHR"][0]  = u"šš"; # DEFAULT
                    Transliterator[u"U+0449"][u"RUSSHR"][1]  = u"šč";
                    Transliterator[u"U+0449"][u"RUSSHR"][2]  = u"šć";
            # ----------------------------
        """
        # ----------------------------
        self.clear();
        # ----------------------------
        csv_file   = codecs.open(filename=path, mode=globaldefs.FILE_READ_MODE, encoding=globaldefs.ENCODING_INPUT_CSV); # i.e. open the csv file
        csv_reader = csv.reader(self.yield_encoded_csv_rows(csv_file), dialect=TableDialect()); # i.e. get the csv reader object (see the standard "csv" module)
        csv_rows   = [self.get_normalized_csv_row(csv_row) for csv_row in csv_reader];
        # ----------------------------
        if (csv_rows): # i.e. (csv_rows != [])
            # ----------------------------
            csv_column_labels = csv_rows[0][1:];
            # ----------------------------
            for (csv_row) in (csv_rows[1:]):
                # ----------------------------
                csv_row_label = csv_row[0];
                self[csv_row_label] = IndexedDict();
                # ----------------------------
                for (csv_column_index, csv_cell) in enumerate(csv_row[1:]):
                    # ----------------------------
                    csv_column_label = csv_column_labels[csv_column_index];
                    self[csv_row_label][csv_column_label] = [];
                    # ----------------------------
                    for (csv_string) in (csv_cell.split(globaldefs.CSV_SEPARATOR)):
                        self[csv_row_label][csv_column_label].append(csv_string);
                    # for (csv_string)
                    # ----------------------------
                # for (csv_column_index, csv_cell)
                # ----------------------------
            # for (csv_row)
            # ----------------------------
        else: # i.e. (csv_rows == [])
            pass;
        # ----------------------------

    def read_xml (self, path):
        u"""
            # ----------------------------
            [1] XML FILE:

                [1.1]
                    "
                    <?xml version="1.0" encoding="UTF-8"?>
                    <table>
                    	<row id="U+0449">
                    		<column id="CYRILLIC">
                    			<string>щ</string>
                                ...
                    		</column>
                    		<column id="RUSSCII">
                    			<string>shh</string>
                    			<string>shch</string>
                                ...
                    		</column>
                    		<column id="RUSSHR">
                    			<string>šš</string>
                    			<string>šč</string>
                    			<string>šć</string>
                                ...
                    		</column>
                            ...
                    	</row>
                        ...
                    </table>
                    "
            # ----------------------------
            [2] TRANSLITERATOR (ORDERED DICT):

                [2.1] TRANSLITERATOR ROWS (INDEXED ORDERED DICTS):
                    Transliterator = {
                        ...
                        u"U+0449": {
                            u"CYRILLIC": [u"щ"],
                            u"RUSSCII": [u"shh", u"shch"],
                            u"RUSSHR":  [u"šš", u"šč", u"šć"],
                            ...
                        },
                        ...
                    };

                [2.2] ROW COLUMNS (INDEXED ORDERED DICTS):
                    Transliterator[u"U+0449"] = {
                        u"CYRILLIC": [u"щ"],
                        u"RUSSCII": [u"shh", u"shch"],
                        u"RUSSHR":  [u"šš", u"šč", u"šć"],
                        ...
                    };

                [2.3] COLUMN STRINGS (LISTS):
                    Transliterator[u"U+0449"][u"CYRILLIC"] = [u"щ"];
                    Transliterator[u"U+0449"][u"RUSSCII"] = [u"shh", u"shch"];
                    Transliterator[u"U+0449"][u"RUSSHR"]  = [u"šš", u"šč", u"šć"];

                [2.4] STRINGS:
                    Transliterator[u"U+0449"][u"CYRILLIC"][0] = u"щ"; # DEFAULT
                    Transliterator[u"U+0449"][u"RUSSCII"][0] = u"shh"; # DEFAULT
                    Transliterator[u"U+0449"][u"RUSSCII"][1] = u"shch";
                    Transliterator[u"U+0449"][u"RUSSHR"][0]  = u"šš"; # DEFAULT
                    Transliterator[u"U+0449"][u"RUSSHR"][1]  = u"šč";
                    Transliterator[u"U+0449"][u"RUSSHR"][2]  = u"šć";
            # ----------------------------
        """
        # ----------------------------
        self.clear();
        # ----------------------------
        xml_doc = xmlutils.loadDoc(xmlDocName=path);
        xml_table = xml_doc.documentElement;
        # ----------------------------
        for (xml_row) in (xml_table.childNodes):
            # ----------------------------
            row_label = xml_row.getAttribute(u"label");
            self[row_label] = IndexedDict();
            # ----------------------------
            for (xml_column) in (xml_row.childNodes):
                # ----------------------------
                col_label = xml_column.getAttribute(u"label");
                self[row_label][col_label] = [];
                # ----------------------------
                for (xml_string) in (xml_column.childNodes):
                    try:
                        string = xml_string.childNodes[0].nodeValue;
                        self[row_label][col_label].append(string);
                    except (IndexError): # an empty string node
                        pass;
                # for (xml_string)
                # ----------------------------
            # for (xml_column)
            # ----------------------------
        # for (xml_row)
        # ----------------------------

    def write_csv (self, path):
        u""" ... """
        # ----------------------------
        csv_file = codecs.open(filename=path, mode=globaldefs.FILE_WRITE_MODE, encoding=globaldefs.ENCODING_OUTPUT_CSV, ); # csv_file
        # ----------------------------
        csv_file.write(globaldefs.CSV_DELIMITER.join([globaldefs.CSV_ID] + self.get_column_labels()) + globaldefs.CSV_LINETERMINATOR);
        # ----------------------------
        for row_label in self.iterkeys():
            # ----------------------------
            columns = [row_label];
            # ----------------------------
            for col_label in self[row_label].iterkeys():
                cell = self[row_label][col_label];
                columns.append(self.get_normalized_list_string(cell));
            # for (col_label)
            # ----------------------------
            csv_file.write(globaldefs.CSV_DELIMITER.join(columns) + globaldefs.CSV_LINETERMINATOR);
            # ----------------------------
        # for (row_label)
        # ----------------------------
        csv_file.close();
        # ----------------------------
        dispatcher.send(sender=self, signal=threadingdefs.GLOBAL_SIGNAL_INDEX[u"TABLE_WRITTEN"]);
        # ----------------------------

    def write_xml (self, path):
        u""" ... """
        # ----------------------------
        xml_doc = self.get_xml();
        xmlutils.writeDoc(xmlDoc=xml_doc, fileName=path);
        # ----------------------------
        dispatcher.send(sender=self, signal=threadingdefs.GLOBAL_SIGNAL_INDEX[u"TABLE_WRITTEN"]);
        # ----------------------------

    # [5] CLASS REPRESENTATION:
    __name__ = u"Table";
    def __repr__ (self):
        return globaldefs.TEMPLATES_REPR[self.__name__].format(self).encode(globaldefs.ENCODING_CURRENT);
    def __str__ (self):
        return globaldefs.TEMPLATES_REPR[self.__name__].format(self).encode(globaldefs.ENCODING_CURRENT);
    def __unicode__ (self):
        return globaldefs.TEMPLATES_REPR[self.__name__].format(self);

    # [6] CLASS SLOTS RESTRICTION:
    __slots__ = ();

# ------------------------------------------------------------------------------

class Transliterator (Table):
    u""" ... """

    _transliterate         = cutils.transliterate;         # i.e. self._transliterate
    _transliterate_encoded = cutils.transliterate_encoded; # i.e. self._transliterate_encoded
    _filter                = cutils.filter;                # i.e. self._filter
    _filter_encoded        = cutils.filter_encoded;        # i.e. self._filter_encoded
    _segment               = cutils.segment;               # i.e. self._segment
    _segment_encoded       = cutils.segment_encoded;       # i.e. self._segment_encoded
    _ranges                = cutils.ranges;                # i.e. self._ranges
    _ranges_encoded        = cutils.ranges_encoded;        # i.e. self._ranges_encoded
    _derive                = cutils.derive;                # i.e. self._derive
    _derive_encoded        = cutils.derive_encoded;        # i.e. self._derive_encoded
    _integrate             = cutils.integrate;             # i.e. self._integrate
    _integrate_encoded     = cutils.integrate_encoded;     # i.e. self._integrate_encoded
    _parse                 = cutils.parse;                 # i.e. self._parse
    _parse_encoded         = cutils.parse_encoded;         # i.e. self._parse_encoded
    _stream_transliterate  = cutils.stream_transliterate;  # i.e. self._stream_transliterate
    _stream_filter         = cutils.stream_filter;         # i.e. self._stream_filter

    def __init__ (self, table):
        u""" ... """
        # ----------------------------
        Table.__init__(self, path=table);
        # ----------------------------
        dispatcher.send(sender=self, signal=threadingdefs.GLOBAL_SIGNAL_INDEX[u"TRANSLITERATOR_INITIALIZED"]);
        # ----------------------------

    def transliterate (self, source_string):
        u"""
            The Cython versions of
            both the unicode and bytes (encoded)
            "transliterate" methods
            (see the "cutils" for implementation)
        """
        # ----------------------------
        if (self._encoded_): # i.e. (self._encoded_ == True)
            target_string = self._transliterate_encoded(source_string, self._match_, self._map_, self._max_, self._encoding_); # i.e. returns a bytes (encoded) string...
        else: # i.e. (self._encoded_ == False)
            target_string = self._transliterate(source_string, self._match_, self._map_, self._max_); # i.e. returns a unicode string...
        # ----------------------------
        # dispatcher.send(sender=self, signal=threadingdefs.GLOBAL_SIGNAL_INDEX[u"TRANSLITERATOR_TRANSLITERATED"], target_string=target_string);
        # ----------------------------
        return (target_string);
        # ----------------------------

    def filter (self, source_string):
        u"""
            The Cython versions of
            both the unicode and bytes (encoded)
            "filter" methods
            (see the "cutils" for implementation)
        """
        # ----------------------------
        if (self._encoded_): # i.e. (self._encoded_ == True)
            target_string = self._filter_encoded(source_string, self._match_, self._map_, self._max_, self._encoding_); # i.e. returns a bytes (encode) string...
        else: # i.e. (self._encoded_ == False)
            target_string = self._filter(source_string, self._match_, self._map_, self._max_); # i.e. returns a unicode string...
        # ----------------------------
        # dispatcher.send(sender=self, signal=threadingdefs.GLOBAL_SIGNAL_INDEX[u"TRANSLITERATOR_FILTERED"], target_string=target_string);
        # ----------------------------
        return (target_string);
        # ----------------------------

    def segment (self, source_string):
        u"""
            The Cython versions of
            both the unicode and bytes (encoded)
            "segment" (or: "partition") methods
            (see the "cutils" for implementation)
        """
        # ----------------------------
        if (self._encoded_): # i.e. (self._encoded_ == True)
            segments = self._segment_encoded(source_string, self._match_, self._map_, self._max_, self._encoding_); # i.e. returns a list of integer types and bytes (encoded) string tuples...
        else: # i.e. (self._encoded_ == False)
            segments = self._segment(source_string, self._match_, self._map_, self._max_); # i.e. returns a list of integer types and unicode string tuples...
        # ----------------------------
        # dispatcher.send(sender=self, signal=threadingdefs.GLOBAL_SIGNAL_INDEX[u"TRANSLITERATOR_SEGMENTED"], segments=segments);
        # ----------------------------
        return (segments);
        # ----------------------------

    def ranges (self, source_string):
        u"""
            The Cython versions of
            both the unicode and bytes (encoded)
            "ranges" methods
            (see the "cutils" for implementation)
        """
        # ----------------------------
        if (self._encoded_): # i.e. (self._encoded_ == True)
            ranges = self._ranges_encoded(source_string, self._encoding_);
        else: # i.e. (self._encoded_ == False)
            ranges = self._ranges(source_string);
        # ----------------------------
        # dispatcher.send(sender=self, signal=threadingdefs.GLOBAL_SIGNAL_INDEX[u"TRANSLITERATOR_RANGES"], ranges=ranges);
        # ----------------------------
        return (ranges);
        # ----------------------------

    def derive (self, source_string):
        u"""
            The Cython versions of
            both the unicode and bytes (encoded)
            "derive" (or: "identify") methods
            (see the "cutils" for implementation)
        """
        # ----------------------------
        if (self._encoded_): # i.e. (self._encoded_ == True)
            source_indices = self._derive_encoded(source_string, self._match_, self._max_, self._indices_); # i.e. return a list of derived row indices, with the bytes (encoded) underived substrings...
        else: # i.e. (self._encoded_ == False)
            source_indices = self._derive(source_string, self._match_, self._max_, self._indices_); # i.e. return a list of derived row indices, with the unicode underived substrings...
        # ----------------------------
        # dispatcher.send(sender=self, signal=threadingdefs.GLOBAL_SIGNAL_INDEX[u"TRANSLITERATOR_DERIVED"], derivations=source_indices);
        # ----------------------------
        return (source_indices);
        # ----------------------------

    def integrate (self, derivations):
        u"""
            The Cython versions of
            both the unicode and bytes (encoded)
            "integrate" (or: "render") methods
            (see the "cutils" for implementation)
        """
        # ----------------------------
        if (self._encoded_): # i.e. (self._encoded_ == True)
            target_string = self._integrate_encoded(derivations, self._target_column_, self._encoding_); # i.e. returns a bytes (encoded) string...
        else: # i.e. (self._encoded_ == False)
            target_string = self._integrate(derivations, self._target_column_); # i.e. returns a unicode string...
        # ----------------------------
        # dispatcher.send(sender=self, signal=threadingdefs.GLOBAL_SIGNAL_INDEX[u"TRANSLITERATOR_INTEGRATED"], target_string=target_string);
        # ----------------------------
        return (target_string);
        # ----------------------------

    def parse (self, source_string):
        u"""
            The Cython versions of
            both the unicode and bytes (encoded)
            "parse" (or: "debug") methods
            (see the "cutils" for implementation)
        """
        # ----------------------------
        if (self._encoded_): # i.e. (self._encoded_ == True)
            parse_list = self._parse_encoded(source_string, self._match_, self._max_, self._ids_, self._indices_);
        else: # i.e. (self._encoded_ == False)
            parse_list = self._parse(source_string, self._match_, self._max_, self._ids_, self._indices_);
        # ----------------------------
        # dispatcher.send(sender=self, signal=threadingdefs.GLOBAL_SIGNAL_INDEX[u"TRANSLITERATOR_PARSED"], parse_list=parse_list);
        # ----------------------------
        return (parse_list);
        # ----------------------------

    def stream (self, input_path, output_path, filter=False):
        u"""
            The Cython versions of
            both the "transliterate" and "filter"
            streaming methods
            (see the "cutils" for implementation)
        """
        # ----------------------------
        input_stream  = codecs.open(input_path, mode=u"r", encoding=u"utf-8");
        input_string  = input_stream.read();
        output_stream = codecs.open(output_path, mode=u"w", encoding=u"utf-8");
        # ----------------------------
        dispatcher.send(sender=self, signal=threadingdefs.GLOBAL_SIGNAL_INDEX[u"TRANSLITERATOR_STREAM_START"]);
        # ----------------------------
        if (filter): # i.e. (filter == True)
            self._stream_filter(
                input_string  = input_string,
                output_stream = output_stream,
                MATCH         = self._match_,
                MAP           = self._map_,
                MAX           = self._max_,
                SEND          = dispatcher.send,
                SENDER        = self,
                SIGNAL        = threadingdefs.GLOBAL_SIGNAL_INDEX[u"TRANSLITERATOR_STREAM_STEP"]
            );
        else: # i.e. (filter == False)
            self._stream_transliterate(
                input_string  = input_string,
                output_stream = output_stream,
                MATCH         = self._match_,
                MAP           = self._map_,
                MAX           = self._max_,
                SEND          = dispatcher.send,
                SENDER        = self,
                SIGNAL        = threadingdefs.GLOBAL_SIGNAL_INDEX[u"TRANSLITERATOR_STREAM_STEP"]
            );
        # ----------------------------
        dispatcher.send(sender=self, signal=threadingdefs.GLOBAL_SIGNAL_INDEX[u"TRANSLITERATOR_STREAM_END"]);
        # ----------------------------
        input_stream.close();
        output_stream.close();
        # ----------------------------



    def print_parse (self, source_string):
        u""" ... """
        PARSE = self.parse(source_string);
        print u"(";
        for (string, ids, indices) in PARSE:
            print u"\t({0:s}, {1:s}, {2:s}),".format(string, ids, indices);
        print u");";

    def print_derivation (self, source_string):
        u""" ... """
        derivation_list = self.derive(source_string=source_string);
        derivation_string = u"[" + u", ".join([unicode(index) for index in derivation_list]) + u"]";
        print (derivation_string);

    def print_integration (self, derivations):
        u""" ... """
        integration = self.integrate(derivations=derivations);
        if (self._encoded_):
            print (u"{0:>16s}: \"{1:s}\"".encode(self._encoding_).format(self._target_, integration));
        else:
            print (u"{0:>16s}: \"{1:s}\"".format(self._target_, integration));



    # [5] CLASS REPRESENTATION:
    __name__ = u"Transliterator";
    def __repr__ (self):
        return globaldefs.TEMPLATES_REPR[self.__name__].format(self).encode(globaldefs.ENCODING_CURRENT);
    def __str__ (self):
        return globaldefs.TEMPLATES_REPR[self.__name__].format(self).encode(globaldefs.ENCODING_CURRENT);
    def __unicode__ (self):
        return globaldefs.TEMPLATES_REPR[self.__name__].format(self);

    # [6] CLASS SLOTS RESTRICTION:
    __slots__ = ();

# ------------------------------------------------------------------------------

class TransliteratorListener (object):
    u""" A dummy transliterator events listener """

    def __init__ (self):
        self.init_handlers();

    def init_handlers (self):
        u"""
            u"TABLE_INITIALIZED",
            u"TABLE_READ",
            u"TABLE_CLEARED",
            u"TABLE_REMAPPED",
            u"TABLE_RESET",
            u"TABLE_ENCODED",
            u"TABLE_DECODED",
            u"TABLE_SORTED",
            u"TABLE_WRITTEN",
            u"TRANSLITERATOR_INITIALIZED",
            u"TRANSLITERATOR_TRANSLITERATED",
            u"TRANSLITERATOR_FILTERED",
            u"TRANSLITERATOR_SEGMENTED",
            u"TRANSLITERATOR_DERIVED",
            u"TRANSLITERATOR_INTEGRATED",
            u"TRANSLITERATOR_PARSED",
        """
        # ----------------------------
        dispatcher.connect(
            signal   = threadingdefs.GLOBAL_SIGNAL_INDEX[u"TABLE_INITIALIZED"],
            sender   = threadingdefs.GLOBAL_SENDER_ANY,
            receiver = self.handle_table_initialized,
            weak     = True,
        );
        # ----------------------------
        dispatcher.connect(
            signal   = threadingdefs.GLOBAL_SIGNAL_INDEX[u"TABLE_READ"],
            sender   = threadingdefs.GLOBAL_SENDER_ANY,
            receiver = self.handle_table_read,
            weak     = True,
        );
        # ----------------------------
        dispatcher.connect(
            signal   = threadingdefs.GLOBAL_SIGNAL_INDEX[u"TABLE_CLEARED"],
            sender   = threadingdefs.GLOBAL_SENDER_ANY,
            receiver = self.handle_table_cleared,
            weak     = True,
        );
        # ----------------------------
        dispatcher.connect(
            signal   = threadingdefs.GLOBAL_SIGNAL_INDEX[u"TABLE_REMAPPED"],
            sender   = threadingdefs.GLOBAL_SENDER_ANY,
            receiver = self.handle_table_remapped,
            weak     = True,
        );
        # ----------------------------
        dispatcher.connect(
            signal   = threadingdefs.GLOBAL_SIGNAL_INDEX[u"TABLE_RESET"],
            sender   = threadingdefs.GLOBAL_SENDER_ANY,
            receiver = self.handle_table_reset,
            weak     = True,
        );
        # ----------------------------
        dispatcher.connect(
            signal   = threadingdefs.GLOBAL_SIGNAL_INDEX[u"TABLE_ENCODED"],
            sender   = threadingdefs.GLOBAL_SENDER_ANY,
            receiver = self.handle_table_encoded,
            weak     = True,
        );
        # ----------------------------
        dispatcher.connect(
            signal   = threadingdefs.GLOBAL_SIGNAL_INDEX[u"TABLE_DECODED"],
            sender   = threadingdefs.GLOBAL_SENDER_ANY,
            receiver = self.handle_table_decoded,
            weak     = True,
        );
        # ----------------------------
        dispatcher.connect(
            signal   = threadingdefs.GLOBAL_SIGNAL_INDEX[u"TABLE_SORTED"],
            sender   = threadingdefs.GLOBAL_SENDER_ANY,
            receiver = self.handle_table_sorted,
            weak     = True,
        );
        # ----------------------------
        dispatcher.connect(
            signal   = threadingdefs.GLOBAL_SIGNAL_INDEX[u"TABLE_WRITTEN"],
            sender   = threadingdefs.GLOBAL_SENDER_ANY,
            receiver = self.handle_table_written,
            weak     = True,
        );
        # ----------------------------
        dispatcher.connect(
            signal   = threadingdefs.GLOBAL_SIGNAL_INDEX[u"TRANSLITERATOR_INITIALIZED"],
            sender   = threadingdefs.GLOBAL_SENDER_ANY,
            receiver = self.handle_transliterator_initialized,
            weak     = True,
        );
        # ----------------------------
        dispatcher.connect(
            signal   = threadingdefs.GLOBAL_SIGNAL_INDEX[u"TRANSLITERATOR_TRANSLITERATED"],
            sender   = threadingdefs.GLOBAL_SENDER_ANY,
            receiver = self.handle_transliterator_transliterated,
            weak     = True,
        );
        # ----------------------------
        dispatcher.connect(
            signal   = threadingdefs.GLOBAL_SIGNAL_INDEX[u"TRANSLITERATOR_FILTERED"],
            sender   = threadingdefs.GLOBAL_SENDER_ANY,
            receiver = self.handle_transliterator_filtered,
            weak     = True,
        );
        # ----------------------------
        dispatcher.connect(
            signal   = threadingdefs.GLOBAL_SIGNAL_INDEX[u"TRANSLITERATOR_SEGMENTED"],
            sender   = threadingdefs.GLOBAL_SENDER_ANY,
            receiver = self.handle_transliterator_segmented,
            weak     = True,
        );
        # ----------------------------
        dispatcher.connect(
            signal   = threadingdefs.GLOBAL_SIGNAL_INDEX[u"TRANSLITERATOR_DERIVED"],
            sender   = threadingdefs.GLOBAL_SENDER_ANY,
            receiver = self.handle_transliterator_derived,
            weak     = True,
        );
        # ----------------------------
        dispatcher.connect(
            signal   = threadingdefs.GLOBAL_SIGNAL_INDEX[u"TRANSLITERATOR_INTEGRATED"],
            sender   = threadingdefs.GLOBAL_SENDER_ANY,
            receiver = self.handle_transliterator_integrated,
            weak     = True,
        );
        # ----------------------------
        dispatcher.connect(
            signal   = threadingdefs.GLOBAL_SIGNAL_INDEX[u"TRANSLITERATOR_PARSED"],
            sender   = threadingdefs.GLOBAL_SENDER_ANY,
            receiver = self.handle_transliterator_parsed,
            weak     = True,
        );
        # ----------------------------
        dispatcher.connect(
            signal   = threadingdefs.GLOBAL_SIGNAL_INDEX[u"TRANSLITERATOR_STREAM_STEP"],
            sender   = threadingdefs.GLOBAL_SENDER_ANY,
            receiver = self.handle_transliterator_stream_step,
            weak     = True,
        );
        # ----------------------------

    def handle_table_initialized (self):
        print u"<TABLE_INITIALIZED>";
    def handle_table_read (self):
        print u"<TABLE_READ>";
    def handle_table_cleared (self):
        print u"<TABLE_CLEARED>";
    def handle_table_remapped (self):
        print u"<TABLE_REMAPPED>";
    def handle_table_reset (self):
        print u"<TABLE_RESET>";
    def handle_table_encoded (self):
        print u"<TABLE_ENCODED>";
    def handle_table_decoded (self):
        print u"<TABLE_DECODED>";
    def handle_table_sorted (self):
        print u"<TABLE_SORTED>";
    def handle_table_written (self):
        print u"<TABLE_WRITTEN>";
    def handle_transliterator_initialized (self):
        print u"<TRANSLITERATOR_INITIALIZED>";
    def handle_transliterator_transliterated (self):
        print u"<TRANSLITERATOR_TRANSLITERATED>";
    def handle_transliterator_filtered (self):
        print u"<TRANSLITERATOR_FILTERED>";
    def handle_transliterator_segmented (self):
        print u"<TRANSLITERATOR_SEGMENTED>";
    def handle_transliterator_derived (self):
        print u"<TRANSLITERATOR_DERIVED>";
    def handle_transliterator_integrated (self):
        print u"<TRANSLITERATOR_INTEGRATED>";
    def handle_transliterator_parsed (self):
        print u"<TRANSLITERATOR_PARSED>";
    def handle_transliterator_stream_step (self, current, total):
        print u"Stream: {0:.02f}%".format((current/float(total))*100.0);

# ------------------------------------------------------------------------------

if __name__ == "__main__":

    # ----------------------------

    t = Transliterator(table=r"C:\Users\User\Documents\LukaTolitch_005_PROGRAMMING\004_TRANSLITERATOR\Version_22\input\tables\Cyrillic_Russian_2015_08_15_005.csv");
    t.set_map(source=u"RUSSCII", target=u"CYRILLIC");

    l = TransliteratorListener();

    # ----------------------------

    encoding = u"utf-8";
    t.encode(encoding=encoding);

    source_string = u"#<<Dobro po<zh>alovat'!#>>".encode(encoding);

    target_string = t.transliterate(source_string=source_string);
    print u"transliterate(): \"{0:s}\"".encode(encoding).format(target_string);

    target_string = t.filter(source_string=source_string);
    print u"filter(): \"{0:s}\"".encode(encoding).format(target_string);

    segments = t.segment(source_string=source_string);
    print u"segment(): [";
    for (style, string) in segments:
        print u"\t({0:d}, \"{1:s}\"),".encode(encoding).format(style, string);
    # for (style, string)
    print u"]";

    ranges = t.ranges(source_string=source_string);
    print u"ranges(): [";
    for (style, start, end) in ranges:
        print u"\t({0:d}, {1:d}, {2:d}), # \"{3:s}\"".encode(encoding).format(style, start, end, source_string[start:end]);
    # for (style, start, end)
    print u"]";

    t.decode();

    # ----------------------------

    # t.set_map(source=u"RUSSCII", target=u"CYRILLIC");

    input_path  = r"C:\Users\User\Documents\LukaTolitch_005_PROGRAMMING\004_TRANSLITERATOR\Version_22\output\Text_Output_2015_08_15_001.txt";

    output_path = r"C:\Users\User\Documents\LukaTolitch_005_PROGRAMMING\004_TRANSLITERATOR\Version_22\output\Text_Output_TRANSLITERATED_2015_08_16_001.txt";
    t.stream(
        input_path  = input_path,
        output_path = output_path,
    );

    output_path = r"C:\Users\User\Documents\LukaTolitch_005_PROGRAMMING\004_TRANSLITERATOR\Version_22\output\Text_Output_FILTERED_2015_08_16_001.txt";
    t.stream(
        input_path  = input_path,
        output_path = output_path,
        filter      = True,
    );

    # ----------------------------

    print (u"\n>> A \"transliterator.py\" is done!");
