# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------

import os as os
import hashlib as hashlib
import xml.dom.minidom as minidom

from defs.globaldefs import globaldefs_2015_08_14_001 as globaldefs
from utils.datetimeutils import datetimeutils_2015_08_14_001 as datetimeutils

# ------------------------------------------------------------------------------

TYPE_FOLDER = 0b0; # = 0
TYPE_FILE   = 0b1; # = 1
TYPE_NAME   = {
    0b0: u"folder", # = 0
    0b1: u"file",   # = 1
};

# ------------------------------------------------------------------------------

ATTRS_PATH       = (u"path", u"dir", u"folder", u"basename", u"stem", u"ext", u"segments");
ATTRS_TIME       = (u"created", u"modified", u"accessed");
ATTRS_SIZE       = (u"bytes", u"kilobytes", u"megabytes", u"gigabytes", u"size");
ATTRS_HASH       = (u"md5", u"sha1", u"sha256", u"sha512");
ATTRS_CONTENTS   = (u"contents", u"folders", u"files");
ATTRS_CONTAINERS = (u"tuple", u"list", u"dict");
ATTRS_SEGMENTS   = (u"segments");
ATTRS_TYPE       = (u"type");
ATTRS_XML        = (u"doc", u"node");
ATTRS_FILE = (
    # FILE TYPE ATTRIBUTES:
    u"type",
    # ----------------------------
    # FILE PATH ATTRIBUTES:
    u"path",
    u"dir",
    u"folder",
    u"basename",
    u"stem",
    u"ext",
    u"segments",
    # ----------------------------
    # FILE TIME ATTRIBUTES:
    u"created",
    u"modified",
    u"accessed",
    # ----------------------------
    # FILE SIZE ATTRIBUTES:
    u"bytes",
    u"kilobytes",
    u"megabytes",
    u"gigabytes",
    u"size",
    # ----------------------------
    # FILE HASH ATTRIBUTES:
    u"md5",
    u"sha1",
    u"sha256",
    u"sha512",
    # ----------------------------
    # FILE CONTAINER ATTRIBUTES:
    u"dict",
);
ATTRS_FOLDER = (
    # FOLDER TYPE ATTRIBUTES:
    u"type",
    # ----------------------------
    # FOLDER PATH ATTRIBUTES:
    u"path",
    u"dir",
    u"folder",
    u"basename",
    # u"stem",
    # u"ext",
    u"segments",
    # ----------------------------
    # FOLDER TIME ATTRIBUTES:
    u"created",
    u"modified",
    u"accessed",
    # ----------------------------
    # FOLDER CONTENT ATTRIBUTES:
    u"contents",
    # ----------------------------
    # FOLDER CONTAINER ATTRIBUTES:
    u"dict",
);

# ------------------------------------------------------------------------------

# [1] INSTANCE GET-SET DATA DESCRIPTORS:

class PATH_GETSET_PATH (object):
    def __get__ (self, INSTANCE, CLASS=None):
        path = INSTANCE._path_;
        return (path);
    def __set__ (self, INSTANCE, path):
        INSTANCE._path_ = INSTANCE.get_normal_path(path);

# ------------------------------------------------------------------------------

# [2] INSTANCE GET (READ-ONLY) DATA DESCRIPTORS:

class GET (object):
    def __get__ (self, INSTANCE, CLASS=None):
        return (None);
    def __set__ (self, INSTANCE, arg):
        raise AttributeError;

class PATH_GET_DIR (GET):
    def __get__ (self, INSTANCE, CLASS=None):
        directory = os.path.dirname(INSTANCE.path);
        return (directory);

class PATH_GET_FOLDER (GET):
    def __get__ (self, INSTANCE, CLASS=None):
        folder = os.path.basename(INSTANCE.dir);
        return (folder);

class PATH_GET_BASENAME (GET):
    def __get__ (self, INSTANCE, CLASS=None):
        basename = os.path.basename(INSTANCE.path);
        return (basename);

class PATH_GET_STEM (GET):
    def __get__ (self, INSTANCE, CLASS=None):
        if os.path.isfile(INSTANCE.path):
            stem = os.path.splitext(INSTANCE.basename)[0];
        else:
            stem = INSTANCE.basename;
        return (stem);

class PATH_GET_EXT (GET):
    def __get__ (self, INSTANCE, CLASS=None):
        extension = os.path.splitext(INSTANCE.basename)[1][1:];
        return (extension);

class PATH_GET_TYPE (GET):
    def __get__ (self, INSTANCE, CLASS=None):
        if os.path.isfile(INSTANCE.path):
            type = TYPE_FILE; # 1
        else:
            type = TYPE_FOLDER; # 0
        return (type);

class PATH_GET_SEGMENTS (GET):
    def __get__ (self, INSTANCE, CLASS=None):
        segments = INSTANCE.path.split(os.sep);
        return (segments);

class PATH_GET_ATTRS (GET):
    def __get__ (self, INSTANCE, CLASS=None):
        if os.path.isfile(INSTANCE.path):
            attributes = ATTRS_FILE;
        else:
            attributes = ATTRS_FOLDER;
        return (attributes);

class PATH_GET_CONTENTS (GET):
    def __get__ (self, INSTANCE, CLASS=None):
        if os.path.isdir(INSTANCE.path):
            contents = os.listdir(INSTANCE.path);
        else:
            contents = [];
        return (contents);

class PATH_GET_FOLDERS (GET):
    def __get__ (self, INSTANCE, CLASS=None):
        if os.path.isdir(INSTANCE.path):
            folders = [basename for basename in os.listdir(INSTANCE.path) if os.path.isdir(os.path.join(INSTANCE.path,basename))];
        else:
            folders = [];
        return (folders);

class PATH_GET_FILES (GET):
    def __get__ (self, INSTANCE, CLASS=None):
        if os.path.isdir(INSTANCE.path):
            files = [basename for basename in os.listdir(INSTANCE.path) if os.path.isfile(os.path.join(INSTANCE.path,basename))];
        else:
            files = [];
        return (files);

class PATH_GET_ITERATOR (GET):
    def __get__ (self, INSTANCE, CLASS=None):
        if os.path.isdir(INSTANCE.path):
            contents = os.listdir(INSTANCE.path);
        else:
            contents = [];
        iterator = iter(contents);
        return (iterator);

class PATH_GET_BYTES (GET):
    def __get__ (self, INSTANCE, CLASS=None):
        _bytes_ = os.path.getsize(INSTANCE.path);
        return (_bytes_);

class PATH_GET_KILOBYTES (GET):
    def __get__ (self, INSTANCE, CLASS=None):
        kilobytes = INSTANCE.bytes / globaldefs.UNIT_WIN_KILO;
        return (kilobytes);

class PATH_GET_MEGABYTES (GET):
    def __get__ (self, INSTANCE, CLASS=None):
        megabytes = INSTANCE.bytes / globaldefs.UNIT_WIN_MEGA;
        return (megabytes);

class PATH_GET_GIGABYTES (GET):
    def __get__ (self, INSTANCE, CLASS=None):
        gigabytes = INSTANCE.bytes / globaldefs.UNIT_WIN_GIGA;
        return (gigabytes);

class PATH_GET_SIZE (GET):
    def __get__ (self, INSTANCE, CLASS=None):
        _bytes_ = INSTANCE.bytes;
        if (_bytes_ < globaldefs.UNIT_WIN_KILO):
            return globaldefs.TEMPLATES_SIZE[u"size_bytes"].format(_bytes_);
        elif (globaldefs.UNIT_WIN_KILO <= _bytes_ < globaldefs.UNIT_WIN_MEGA):
            return globaldefs.TEMPLATES_SIZE[u"size_kilobytes"].format(INSTANCE.kilobytes);
        elif (globaldefs.UNIT_WIN_MEGA <= _bytes_ < globaldefs.UNIT_WIN_GIGA):
            return globaldefs.TEMPLATES_SIZE[u"size_megabytes"].format(INSTANCE.megabytes);
        elif (globaldefs.UNIT_WIN_GIGA <= _bytes_):
            return globaldefs.TEMPLATES_SIZE[u"size_gigabytes"].format(INSTANCE.gigabytes);
        else:
            return globaldefs.TEMPLATES_SIZE[u"size_bytes"].format(_bytes_);
    def __set__ (self, INSTANCE, arg):
        raise AttributeError;

class PATH_GET_CREATED (GET):
    def __get__ (self, INSTANCE, CLASS=None):
        created_datetime = datetimeutils.DateTime.fromtimestamp(os.path.getctime(INSTANCE.path), tz=None);
        return (created_datetime);

class PATH_GET_MODIFIED (GET):
    def __get__ (self, INSTANCE, CLASS=None):
        modified_datetime = datetimeutils.DateTime.fromtimestamp(os.path.getmtime(INSTANCE.path), tz=None);
        return (modified_datetime);

class PATH_GET_ACCESSED (GET):
    def __get__ (self, INSTANCE, CLASS=None):
        accessed_datetime = datetimeutils.DateTime.fromtimestamp(os.path.getatime(INSTANCE.path), tz=None);
        return (accessed_datetime);

class PATH_GET_NOW (GET):
    def __get__ (self, INSTANCE, CLASS=None):
        now_datetime = datetimeutils.DateTime.now(tz=None);
        return (now_datetime);

class PATH_GET_MD5 (GET):
    def __get__ (self, INSTANCE, CLASS=None):
        file = open(INSTANCE.path, mode=u"rb");
        data = file.read();
        file.close();
        md5 = hashlib.md5(data).hexdigest().upper();
        return (globaldefs.TEMPLATES_HASH[u"md5"].format(INSTANCE.partition_string(md5)));

class PATH_GET_SHA1 (GET):
    def __get__ (self, INSTANCE, CLASS=None):
        file = open(INSTANCE.path, mode=u"rb");
        data = file.read();
        file.close();
        sha1 = hashlib.sha1(data).hexdigest().upper();
        return (globaldefs.TEMPLATES_HASH[u"sha1"].format(INSTANCE.partition_string(sha1)));

class PATH_GET_SHA256 (GET):
    def __get__ (self, INSTANCE, CLASS=None):
        file = open(INSTANCE.path, mode=u"rb");
        data = file.read();
        file.close();
        sha256 = hashlib.sha256(data).hexdigest().upper();
        return (globaldefs.TEMPLATES_HASH[u"sha256"].format(INSTANCE.partition_string(sha256)));

class PATH_GET_SHA512 (GET):
    def __get__ (self, INSTANCE, CLASS=None):
        file = open(INSTANCE.path, mode=u"rb");
        data = file.read();
        file.close();
        sha512 = hashlib.sha512(data).hexdigest().upper();
        return (globaldefs.TEMPLATES_HASH[u"sha512"].format(INSTANCE.partition_string(sha512)));

class PATH_GET_TUPLE (GET):
    def __get__ (self, INSTANCE, CLASS=None):
        _tuple_ = tuple(INSTANCE.__getattribute__(attr) for attr in INSTANCE.attrs if attr not in ATTRS_CONTAINERS);
        return (_tuple_);

class PATH_GET_LIST (GET):
    def __get__ (self, INSTANCE, CLASS=None):
        _list_ = list(INSTANCE.__getattribute__(attr) for attr in INSTANCE.attrs if attr not in ATTRS_CONTAINERS);
        return (_list_);

class PATH_GET_DICT (GET):
    def __get__ (self, INSTANCE, CLASS=None):
        _dict_ = dict((attr, INSTANCE.__getattribute__(attr)) for attr in INSTANCE.attrs if attr not in ATTRS_CONTAINERS);
        return (_dict_);

class PATH_GET_XMLDOC (GET):
    def __get__ (self, INSTANCE, CLASS=None):
        xml_doc = minidom.Document();
        xml_root = xml_doc.createElement(TYPE_NAME[INSTANCE.type]);
        xml_doc.appendChild(xml_root);
        for attr in INSTANCE.attrs:
            if (attr not in ATTRS_XML):
                if (attr not in ATTRS_CONTAINERS):
                    if (attr not in ATTRS_CONTENTS):
                        if (attr not in ATTRS_SEGMENTS):
                            xml_node = xml_doc.createElement(attr);
                            xml_contents = xml_doc.createTextNode(unicode(INSTANCE.__getattribute__(attr)));
                            xml_node.appendChild(xml_contents);
                            xml_root.appendChild(xml_node);
                        else:
                            pass;
                    else:
                        pass;
                else:
                    pass;
            else:
                pass;
        # for (key, value)
        return (xml_doc);

class PATH_GET_XMLNODE (GET):
    def __get__ (self, INSTANCE, CLASS=None):
        xml_doc = INSTANCE.doc;
        xml_node = xml_doc.documentElement;
        return (xml_node);

class PATH_GET_BOOL (GET):
    def __get__ (self, INSTANCE, CLASS=None):
        _bool_ = INSTANCE.exists();
        return (_bool_);

# ------------------------------------------------------------------------------

# [3] INSTANCE METHODS:

def PATH_IS_ABS (INSTANCE):
    return os.path.isabs(INSTANCE._path_);

def PATH_EXISTS (INSTANCE):
    return os.path.exists(INSTANCE._path_);

def PATH_IS_FOLDER (INSTANCE):
    return os.path.isdir(INSTANCE._path_);

def PATH_IS_FILE (INSTANCE):
    return os.path.isfile(INSTANCE._path_);

def PATH_GET_NORMAL_PATH (INSTANCE, path):
    try:
        decoded_path = path.decode(globaldefs.ENCODING_CURRENT); # a UnicodeEncodeError?
    except (UnicodeEncodeError):
        decoded_path = path;
    normalized_path = os.path.normpath(decoded_path);
    return (normalized_path);

def PATH_GET_RELATIVE_PATH (INSTANCE, path):
    try:
        relative_path = os.path.join(os.pardir, os.path.relpath(INSTANCE.dir, path)); #  a ValueError?
        return (relative_path);
    except (ValueError):
        return (INSTANCE.path);

def PATH_PARTITION_STRING (INSTANCE, string, size=2**2):
    strings = [string[i:i+size] for i in range(0, len(string), size)];
    return u" ".join(strings);

# ------------------------------------------------------------------------------

class Path(object):
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
    # [1.2.1.1] INSTANCE PATH GET-SET DATA DESCRIPTORS:
    path      = PATH_GETSET_PATH();   # [1.2.1.1.1] self.path (...)
    # [1.2.2] INSTANCE GET (READ-ONLY) DATA DESCRIPTORS:
    # [1.2.2.1] INSTANCE PATH GET (READ-ONLY) DATA DESCRIPTORS:
    dir       = PATH_GET_DIR();       # [1.2.2.1.1] self.dir (...)
    folder    = PATH_GET_FOLDER();    # [1.2.2.1.2] self.folder (...)
    basename  = PATH_GET_BASENAME();  # [1.2.2.1.3] self.basename (...)
    stem      = PATH_GET_STEM();      # [1.2.2.1.4] self.stem (...)
    ext       = PATH_GET_EXT();       # [1.2.2.1.5] self.ext (...)
    segments  = PATH_GET_SEGMENTS();  # [1.2.2.1.6] self.segments (...)
    # [1.2.2.2] INSTANCE TYPE GET (READ-ONLY) DATA DESCRIPTORS:
    type      = PATH_GET_TYPE();      # [1.2.2.2.1] self.type (...)
    # [1.2.2.3] INSTANCE SIZE GET (READ-ONLY) DATA DESCRIPTORS:
    bytes     = PATH_GET_BYTES();     # [1.2.2.3.1] self.bytes (...)
    kilobytes = PATH_GET_KILOBYTES(); # [1.2.2.3.2] self.kilobytes (...)
    megabytes = PATH_GET_MEGABYTES(); # [1.2.2.3.3] self.megabytes (...)
    gigabytes = PATH_GET_GIGABYTES(); # [1.2.2.3.4] self.gigabytes (...)
    size      = PATH_GET_SIZE();      # [1.2.2.3.5] self.size (...)
    # [1.2.2.4] INSTANCE TIME GET (READ-ONLY) DATA DESCRIPTORS:
    created   = PATH_GET_CREATED();   # [1.2.2.4.1] self.created (...)
    modified  = PATH_GET_MODIFIED();  # [1.2.2.4.2] self.modified (...)
    accessed  = PATH_GET_ACCESSED();  # [1.2.2.4.3] self.accessed (...)
    now       = PATH_GET_NOW();       # [1.2.2.4.4] self.now (...)
    # [1.2.2.5] INSTANCE HASH (CHECKSUM) GET (READ-ONLY) DATA DESCRIPTORS:
    md5       = PATH_GET_MD5();       # [1.2.2.5.1] self.md5 (...)
    sha1      = PATH_GET_SHA1();      # [1.2.2.5.2] self.sha1 (...)
    sha256    = PATH_GET_SHA256();    # [1.2.2.5.3] self.sha256 (...)
    sha512    = PATH_GET_SHA512();    # [1.2.2.5.4] self.sha512 (...)
    # [1.2.2.6] INSTANCE CONTENTS GET (READ-ONLY) DATA DESCRIPTORS:
    contents  = PATH_GET_CONTENTS();  # [1.2.2.6.1] self.contents (...)
    folders   = PATH_GET_FOLDERS();   # [1.2.2.6.2] self.folders (...)
    files     = PATH_GET_FILES();     # [1.2.2.6.3] self.files (...)
    # [1.2.2.7] INSTANCE CONTAINERS GET (READ-ONLY) DATA DESCRIPTORS:
    attrs     = PATH_GET_ATTRS();     # [1.2.2.7.1] self.attrs (...)
    iterator  = PATH_GET_ITERATOR();  # [1.2.2.7.2] self.iterator (...)
    tuple     = PATH_GET_TUPLE();     # [1.2.2.7.3] self.tuple (...)
    list      = PATH_GET_LIST();      # [1.2.2.7.4] self.list (...)
    dict      = PATH_GET_DICT();      # [1.2.2.7.5] self.dict (...)
    doc       = PATH_GET_XMLDOC();    # [1.2.2.7.6] self.doc (...)
    node      = PATH_GET_XMLNODE();   # [1.2.2.7.7] self.node (...)
    # [1.2.2.8] OTHER INSTANCE GET (READ-ONLY) DATA DESCRIPTORS:
    bool      = PATH_GET_BOOL();      # [1.2.2.8.1] self.bool (...)
    # [1.2.3] INSTANCE NON-DATA DESCRIPTORS:
    # ...

    # [1.3] INSTANCE METHODS:
    # [1.3.1] INSTANCE TEST (BOOLEAN) METHODS:
    is_abs            = PATH_IS_ABS;
    exists            = PATH_EXISTS;
    is_folder         = PATH_IS_FOLDER;
    is_file           = PATH_IS_FILE;
    # [1.3.2] OTHER INSTANCE METHODS:
    get_normal_path   = PATH_GET_NORMAL_PATH;
    get_relative_path = PATH_GET_RELATIVE_PATH;
    partition_string  = PATH_PARTITION_STRING;
    # ...

    # [2] CLASS CONSTRUCTION:
    # [2.1] CLASS CONSTRUCTOR (INITIALIZER):
    def __init__ (self, path=None):
        if (path):
            self._path_ = self.get_normal_path(path);
        else:
            self._path_ = os.getcwd();
    # [2.2] CLASS RECONSTRUCTOR (CALLER):
    def __call__ (self, path):
        self._path_ = self.get_normal_path(path);
    # [2.3] CLASS DESTRUCTOR (DELETER):
    # def __del__ (self):
    #     pass;
    # [2.4] CLASS INSTANTIATOR:
    # def __new__ (self, *args, **kwargs):
    #     pass;

    # [3] CLASS CUSTOM METHODS:
    # ...

    # [4] CLASS SPECIAL METHODS:
    def __nonzero__ (self):
        return self.exists();
    def __len__ (self):
        return len(self.contents);
    def __iter__ (self):
        return self.iterator;
    def __contains__ (self, basename):
        if (basename in self.contents):
            return (True);
        else:
            return (False);
    def __getitem__ (self, index):
        return self.contents[index];

    # [5] CLASS REPRESENTATION:
    __name__ = u"Path";
    def __repr__ (self):
        return globaldefs.TEMPLATES_REPR[self.__name__].format(self).encode(globaldefs.ENCODING_CURRENT);
    def __str__ (self):
        return globaldefs.TEMPLATES_REPR[self.__name__].format(self).encode(globaldefs.ENCODING_CURRENT);
    def __unicode__ (self):
        return globaldefs.TEMPLATES_REPR[self.__name__].format(self);

    # [6] CLASS SLOTS RESTRICTION:
    __slots__ = (
        u"_path_",
        u"__weakref__",
    );

# ------------------------------------------------------------------------------

import pprint as pprint
pprinter = pprint.PrettyPrinter(indent=4, width=80);

if __name__ == u"__main__":

    folderpath = r"C:\Users\User\Documents\LukaTolitch_005_PROGRAMMING\004_BOOKMARKS\Version_11\output";
    filepath   = r"C:\Users\User\Documents\LukaTolitch_005_PROGRAMMING\004_BOOKMARKS\Version_11\output\bookmarks_2015_05_24_002.xml";

    print u"-"*80;

    path = Path(path=folderpath);
    print path;
    pprinter.pprint(path.dict);
    # print path.node.toprettyxml();

    print u"-"*80;

    path(path=filepath);
    # pprinter.pprint(path.dict);
    print path.node.toprettyxml();

    print u"-"*80;

    print path.exists();
    print path.is_abs();

    print u"\n>> A \"pathutils.py\" is done.";
