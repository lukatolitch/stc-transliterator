# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------

from urllib import quote as quote
from urllib import unquote as unquote

# ------------------------------------------------------------------------------

# [1] ENCODINGS:

ENCODING_DEFAULT    = u"ascii";
ENCODING_CURRENT    = u"utf-8"; # i.e. the Python source files' encoding (cf. the "encoding declaration" line: # -*- coding: utf-8 -*-)
ENCODING_STANDARD   = u"utf-8";
ENCODING_STRING     = u"utf-8";
ENCODING_RE         = u"utf-8";
ENCODING_URL        = u"utf-8";
ENCODING_INPUT      = u"utf-8";
ENCODING_OUTPUT     = u"utf-8";
ENCODING_INPUT_CSV  = u"utf-8";
ENCODING_OUTPUT_CSV = u"utf-8";
ENCODING_INPUT_XML  = u"utf-8";
ENCODING_OUTPUT_XML = u"utf-8";

# ------------------------------------------------------------------------------

# [2] TEMPLATES:

TEMPLATES_REPR = {
    # [1] pathutils:
    u"Path":      u"Path(path:{0.path:s})", # i.e. pathutils.Path()
    # ...

    # [2] urlutils:
    u"URL":       u"URL(url:{0.url:s})", # i.e. urlutils.URL()
    u"URLItem":   u"URLItem(name:{0.name:s}, value:{0.value:s}, count:{0.count:d})", # i.e. urlutils.URLItem()
    # ...

    # [3] bookmarkutils:
    u"Type":      u"Type(spec:{0.spec:s}, name:{0.name:s}, index:{0.index})", # i.e. bookmarkutils.Type()
    u"Bookmark":  u"Bookmark(\"{0.url.url:s}\")", # i.e. bookmarkutils.Bookmark()
    u"Container": u"Container(\"{0.title:s}\")", # i.e. bookmarkutils.Container()
    # ...

    # [4] threadutils:
    u"ThreadData":      u"ThreadData(...)", # i.e. threadutils.ThreadData()
    u"ThreadFilters":   u"ThreadFilters(...)", # i.e. threadutils.ThreadFilters()
    u"BookmarkThreads": u"BookmarkThreads(...)", # i.e. threadutils.BookmarkThreads()
    # ...

    # [5] dispatchutils:
    u"Dispatcher":   u"Dispatcher(...)",
    u"Bookmarker":   u"Bookmarker(...)",
    u"Listener":     u"Listener(...)",
    u"XMLListener":  u"XMLListener(...)",
    u"URLListener":  u"URLListener(...)",
    # ...

    # [6] queueutils:
    u"ITEM":       u"ITEM(name:\"{0.name:s}\")",
    u"MULTIQUEUE": u"MULTIQUEUE(items:{0.items:d}, processors:{0.processors:d}, processed:{0.processed:d})",
    # ...

    # [7] dictutils
    u"IndexedDict": u"IndexedDict()", # i.e. dictutils.IndexedDict()

    u"Table":          u"{0.table:s}",
    u"Transliterator": u"{0.table:s}",

};

TEMPLATES_FORMATS = {
    u"progress_value": u"{0:0.02f}%",
    u"progress_time":  u"{0:%Hh, %Mm, %Ss}, {1:s}ms",
    u"title_label":    u"{0:s}:",
};

TEMPLATES_TIMESTAMP = {
    # ----------------------------
    u"float":    u"{0:f}",
    u"integer":  u"{0:.00f}",
    u"simple":   u"{0:.03f}",
    u"readable": u"{0:,f}",
    # ----------------------------
};

TEMPLATES_DATE = {
    # ----------------------------
    u"standard":    u"{0:%Y-%m-%d}",
    u"compact":     u"{0:%y-%m-%d}",
    # ----------------------------
    u"ISO":         u"{0:%Y%m%d}",   # ISO 8601 DATE (BASIC)
    u"ISO+":        u"{0:%Y-%m-%d}", # ISO 8601 DATE (EXTENDED)
    u"ISOW":        u"{0:%Y%W}",     # ISO 8601 ORDINAL DATE IN WEEKS (BASIC)
    u"ISOW+":       u"{0:%Y-%W}",    # ISO 8601 ORDINAL DATE IN WEEKS (EXTENDED)
    u"ISOD":        u"{0:%Y%j}",     # ISO 8601 ORDINAL DATE IN DAYS (BASIC)
    u"ISOD+":       u"{0:%Y-%j}",    # ISO 8601 ORDINAL DATE IN DAYS (EXTENDED)
    # ----------------------------
    u"local":       u"{0:%x}",       # LOCAL DATE FORMAT
    # ----------------------------
    u"YEAR":        u"{0:%Y}",       # YEAR (2015)
    u"year":        u"{0:%y}",       # year (15)
    u"ymonth":      u"{0:%m}",       # MONTH (OF YEAR)
    u"yweek":       u"{0:%U}",       # WEEK OF YEAR
    u"wday":        u"{0:%d}",       # DAY (OF WEEK)
    u"yday":        u"{0:%j}",       # DAY OF YEAR
    u"wday_id":     u"{0:%a}",       # DAY ID
    u"ymonth_id":   u"{0:%b}",       # MONTH ID
    u"wday_name":   u"{0:%A}",       # DAY NAME
    u"ymonth_name": u"{0:%B}",       # MONTH NAME
    # ----------------------------
};

TEMPLATES_TIME = {
    # ----------------------------
    u"ISO":       u"{0:%H%M%S}",           # ISO 8601 TIME (BASIC)
    u"ISO+":      u"{0:%H:%M:%S}",         # ISO 8601 TIME (EXTEND)
    # ----------------------------
    u"default":   u"{0:%H:%M:%S (%Z)}",
    u"default+":  u"{0:%H:%M:%S.%f (%Z)}",
    u"uniform":   u"{0:%z:%H:%M:%S}",
    u"uniform+":  u"{0:%z:%H:%M:%S.%f}",
    u"simple":    u"{0:%H:%M:%S}",
    u"simple+":   u"{0:%H:%M:%S.%f}",
    u"bookmark":  u"{0:%H:%M:%S}",
    u"bookmark+": u"{0:%H:%M:%S.%f}",
    u"flat":      u"{0:%H_%M_%S}",
    u"flat+":     u"{0:%H_%M_%S_%f}",
    u"readable":  u"{0:%YY,%mM,%dD, %Hh,%Mn,%Ss}",
    u"readable+": u"{0:%YY,%mM,%dD, %Hh,%Mn,%Ss,%fms}",
    # ----------------------------
};

TEMPLATES_DATETIME = {
    # ----------------------------
    u"ISO":       u"{0:%Y%m%dT%H%M%S}",           # ISO 8601 DATETIME (BASIC)
    u"ISO+":      u"{0:%Y-%m-%dT%H:%M:%S}",       # ISO 8601 DATETIME (EXTENDED)
    # ----------------------------
    u"default":   u"{0:%Y-%m-%d %H:%M:%S %z}",
    u"default+":  u"{0:%Y-%m-%d %H:%M:%S.%f %z}",
    u"detailed":  u"{0:%Y-%m-%d %H:%M:%S %Z}",
    u"detailed+": u"{0:%Y-%m-%d %H:%M:%S.%f %Z}",
    u"simple":    u"{0:%Y-%m-%d %H:%M:%S}",
    u"simple+":   u"{0:%Y-%m-%d %H:%M:%S.%f}",
    u"bookmark":  u"{0:%Y-%m-%d, %H:%M:%S} (CET)",
    u"bookmark+": u"{0:%Y-%m-%d, %H:%M:%S.%f} (CET)",
    u"uniform":   u"{0:%Y:%m:%d:%H:%M:%S:%z}",
    u"uniform+":  u"{0:%Y:%m:%d:%H:%M:%S:%f:%z}",
    u"flat":      u"{0:%Y_%m_%d_%H_%M_%S}",
    u"flat+":     u"{0:%Y_%m_%d_%H_%M_%S_%f}",
    u"compact":   u"{0:%Y%m%d%H%M%S}",
    u"compact+":  u"{0:%Y%m%d%H%M%S%f}",
    u"local":     u"{0:%c}",
    # ----------------------------
    u"odt_created":  u"Created: {0:%Y:%m:%d %H:%M:%S}",
    u"odt_modified": u"Modified: {0:%Y:%m:%d %H:%M:%S}",
    u"odt_accessed": u"Accessed: {0:%Y:%m:%d %H:%M:%S}",
    u"odt_taken":    u"Taken: {0:%Y:%m:%d %H:%M:%S}",
    # ----------------------------
};

TEMPLATES_TIMEDELTA = {
    # ----------------------------
    u"compact":  u"{0.years:d}y,{0.months:02d}m,{0.days:02d}d, {0.hours:02d}h,{0.minutes:02d}m,{0.seconds:02d}s",
    u"expanded": u"{0.years:d} years, {0.months:d} months, {0.days:d} days, {0.hours:d} hours, {0.minutes:d} months, {0.seconds:d} seconds",
    # ----------------------------
};

TEMPLATES_TIMEZONE = {
    # ----------------------------
    u"default": u"{0:\"%Z\", %z}",

    u"standard": u"{0.offset_hours:+03d}:{0.offset_minutes:02d}",
    # u"default":  u"UTC{0.offset_hours:+03d}:{0.offset_minutes:02d}",
    # u"detailed": u"UTC{0.offset_hours:+03d}:{0.offset_minutes:02d} \"{0.name:s}\"",
    # ----------------------------
};

TEMPLATES_SIZE = {
    u"size_bytes":     u"{0:,d} B",
    u"size_kilobytes": u"{0:,.03f} KB",
    u"size_megabytes": u"{0:,.03f} MB",
    u"size_gigabytes": u"{0:,.03f} GB",
};

TEMPLATES_HASH = {
    u"md5":    u"MD5 {0:s}",
    u"sha1":   u"SHA1 {0:s}",
    u"sha256": u"SHA256 {0:s}",
    u"sha512": u"SHA512 {0:s}",
};

# ------------------------------------------------------------------------------

# [3] UNITS:

UNIT_WIN_KILO = 1024.0;           # = 1024.0                                                = 2.0**10
UNIT_WIN_MEGA = UNIT_WIN_KILO**2; # = 1048576.0    = 1024.0**2 = (2.0**10)**2 = 2.0**(10*2) = 2.0**20
UNIT_WIN_GIGA = UNIT_WIN_KILO**3; # = 1073741824.0 = 1024.0**3 = (2.0**10)**3 = 2.0**(10*3) = 2.0**30

# ------------------------------------------------------------------------------

# [4] COMPARISON:

CMP_LT = -1; # PYTHON "LESS THAN" COMPARISON CONSTANT
CMP_EQ =  0; # PYTHON "EQUAL (TO)" COMPARISON CONSTANT
CMP_GT =  1; # PYTHON "GREATER THAN" COMPARISON CONSTANT

# ------------------------------------------------------------------------------

FILE_READ_MODE           = u"r";
FILE_WRITE_MODE          = u"w";
FILE_EXTENSION_SEPARATOR = u".";

# ------------------------------------------------------------------------------

CSV_DELIMITER        = u";".encode(ENCODING_CURRENT);
CSV_SEPARATOR        = u",".encode(ENCODING_CURRENT);
CSV_LINETERMINATOR   = u"\r\n".encode(ENCODING_CURRENT);
CSV_QUOTECHAR        = unichr(0x0007).encode(ENCODING_CURRENT); # i.e. the (encoded) Unicode "ALERT" control character, used to avoid the usual alphabets
CSV_QUOTING          = 0; # i.e. the QUOTE_MINIMAL from the csv standard module (csv.QUOTE_MINIMAL)
CSV_DOUBLEQUOTE      = True;
CSV_ESCAPECHAR       = None;
CSV_SKIPINITIALSPACE = False;
CSV_STRICT           = False;
CSV_ID               = u"ID".encode(ENCODING_CURRENT); # i.e. the custom ID label string, used when writing a csv table file

# ------------------------------------------------------------------------------

RE = {
    u"CLEAR_SEPARATOR": (b"(\s*),(\s*)", b","), # i.e. remove all the delimiter whitespaces, newlines, tabs, et cet., if any such
    u"REDUCE_EMPTY": (b"\A(\s+)\Z", b""), # i.e. if a string contains only whitespace, newlines, tabs, et cet., reduce it to an empty string
};

# ------------------------------------------------------------------------------

# [5] ESCAPING, ENCODING, ...:

XML_ESCAPE_MAP = (
    # (CHARACTER, ESCAPE)
    (u"&",  u"&amp;"),  # 0 (i.e. the first to escape, the last to un-escape...)
    (u"<",  u"&lt;"),   # 1
    (u">",  u"&gt;"),   # 2
    (u"'",  u"&apos;"), # 3
    (u"\"", u"&quot;"), # 4
);
XML_UNESCAPE_MAP = tuple((escape,character) for (character,escape) in reversed(XML_ESCAPE_MAP)); # i.e. the order reversed, the arguments swapped...

ESCAPE_BYTES = u"\\"; # i.e. the Unicode "BACKSLASH" U+005C codepoint...

CONTROL_CHARACTERS = [
	{u"codepoint":0x0000, u"name":u"NULL"},
	{u"codepoint":0x0001, u"name":u"START OF HEADING"},
	{u"codepoint":0x0002, u"name":u"START OF TEXT"},
	{u"codepoint":0x0003, u"name":u"END OF TEXT"},
	{u"codepoint":0x0004, u"name":u"END OF TRANSMISSION"},
	{u"codepoint":0x0005, u"name":u"ENQUIRY"},
	{u"codepoint":0x0006, u"name":u"ACKNOWLEDGE"},
	{u"codepoint":0x0007, u"name":u"BELL"},
	{u"codepoint":0x0008, u"name":u"BACKSPACE"},
	{u"codepoint":0x0009, u"name":u"CHARACTER TABULATION"},
	{u"codepoint":0x000A, u"name":u"LINE FEED (LF)"},
	{u"codepoint":0x000B, u"name":u"LINE TABULATION"},
	{u"codepoint":0x000C, u"name":u"FORM FEED (FF)"},
	{u"codepoint":0x000D, u"name":u"CARRIAGE RETURN (CR)"},
	{u"codepoint":0x000E, u"name":u"SHIFT OUT"},
	{u"codepoint":0x000F, u"name":u"SHIFT IN"},
	{u"codepoint":0x0010, u"name":u"DATA LINK ESCAPE"},
	{u"codepoint":0x0011, u"name":u"DEVICE CONTROL ONE"},
	{u"codepoint":0x0012, u"name":u"DEVICE CONTROL TWO"},
	{u"codepoint":0x0013, u"name":u"DEVICE CONTROL THREE"},
	{u"codepoint":0x0014, u"name":u"DEVICE CONTROL FOUR"},
	{u"codepoint":0x0015, u"name":u"NEGATIVE ACKNOWLEDGE"},
	{u"codepoint":0x0016, u"name":u"SYNCHRONOUS IDLE"},
	{u"codepoint":0x0017, u"name":u"END OF TRANSMISSION BLOCK"},
	{u"codepoint":0x0018, u"name":u"CANCEL"},
	{u"codepoint":0x0019, u"name":u"END OF MEDIUM"},
	{u"codepoint":0x001A, u"name":u"SUBSTITUTE"},
	{u"codepoint":0x001B, u"name":u"ESCAPE"},
	{u"codepoint":0x001C, u"name":u"INFORMATION SEPARATOR FOUR"},
	{u"codepoint":0x001D, u"name":u"INFORMATION SEPARATOR THREE"},
	{u"codepoint":0x001E, u"name":u"INFORMATION SEPARATOR TWO"},
	{u"codepoint":0x001F, u"name":u"INFORMATION SEPARATOR ONE"},
	{u"codepoint":0x007F, u"name":u"DELETE"},
	{u"codepoint":0x0080, u"name":u""},
	{u"codepoint":0x0081, u"name":u""},
	{u"codepoint":0x0082, u"name":u"BREAK PERMITTED HERE"},
	{u"codepoint":0x0083, u"name":u"NO BREAK HERE"},
	{u"codepoint":0x0084, u"name":u""},
	{u"codepoint":0x0085, u"name":u"NEXT LINE (NEL)"},
	{u"codepoint":0x0086, u"name":u"START OF SELECTED AREA"},
	{u"codepoint":0x0087, u"name":u"END OF SELECTED AREA"},
	{u"codepoint":0x0088, u"name":u"CHARACTER TABULATION SET"},
	{u"codepoint":0x0089, u"name":u"CHARACTER TABULATION WITH JUSTIFICATION"},
	{u"codepoint":0x008A, u"name":u"LINE TABULATION SET"},
	{u"codepoint":0x008B, u"name":u"PARTIAL LINE FORWARD"},
	{u"codepoint":0x008C, u"name":u"PARTIAL LINE BACKWARD"},
	{u"codepoint":0x008D, u"name":u"REVERSE LINE FEED"},
	{u"codepoint":0x008E, u"name":u"SINGLE SHIFT TWO"},
	{u"codepoint":0x008F, u"name":u"SINGLE SHIFT THREE"},
	{u"codepoint":0x0090, u"name":u"DEVICE CONTROL STRING"},
	{u"codepoint":0x0091, u"name":u"PRIVATE USE ONE"},
	{u"codepoint":0x0092, u"name":u"PRIVATE USE TWO"},
	{u"codepoint":0x0093, u"name":u"SET TRANSMIT STATE"},
	{u"codepoint":0x0094, u"name":u"CANCEL CHARACTER"},
	{u"codepoint":0x0095, u"name":u"MESSAGE WAITING"},
	{u"codepoint":0x0096, u"name":u"START OF GUARDED AREA"},
	{u"codepoint":0x0097, u"name":u"END OF GUARDED AREA"},
	{u"codepoint":0x0098, u"name":u"START OF STRING"},
	{u"codepoint":0x0099, u"name":u""},
	{u"codepoint":0x009A, u"name":u"SINGLE CHARACTER INTRODUCER"},
	{u"codepoint":0x009B, u"name":u"CONTROL SEQUENCE INTRODUCER"},
	{u"codepoint":0x009C, u"name":u"STRING TERMINATOR"},
	{u"codepoint":0x009D, u"name":u"OPERATING SYSTEM COMMAND"},
	{u"codepoint":0x009E, u"name":u"PRIVACY MESSAGE"},
	{u"codepoint":0x009F, u"name":u"APPLICATION PROGRAM COMMAND"},
];

CONTROL_RANGES = [
    (0x0000, 0x001F),
    (0x007F, 0x009F),
];

CONTROL_STRING = u"".join([unichr(control[u"codepoint"]) for control in CONTROL_CHARACTERS]);

def GET_ESCAPED_STRING (string):
    u""" ESCAPE ALL (i.e. URL, XML, BYTES, ...) """
    # ----------------------------
    string = GET_URL_ESCAPED_STRING(string);   # i.e. the escape step 1...
    string = GET_BYTES_ESCAPED_STRING(string); # i.e. the escape step 2...
    string = GET_XML_ESCAPED_STRING(string);   # i.e. the escape step 3...
    # ----------------------------
    return (string);
    # ----------------------------

def GET_UNESCAPED_STRING (string):
    u""" UN-ESCAPE ALL (i.e. URL, XML, BYTES, ...) """
    # ----------------------------
    string = GET_URL_UNESCAPED_STRING(string);   # i.e. the un-escape step 1...
    string = GET_BYTES_UNESCAPED_STRING(string); # i.e. the un-escape step 2...
    string = GET_XML_UNESCAPED_STRING(string);   # i.e. the un-escape step 3...
    # ----------------------------
    return (string);
    # ----------------------------

def GET_XML_NORMAL_STRING (string):
    u""" ... """
    # ----------------------------
    string = GET_URL_UNESCAPED_STRING(string); # i.e. the un-escape step 1...
    string = GET_BYTES_ESCAPED_STRING(string); # i.e. the escape step 2...
    string = GET_XML_ESCAPED_STRING(string);   # i.e. the escape step 3...
    # ----------------------------
    return (string);
    # ----------------------------

def GET_URL_ESCAPED_STRING (string):
    u""" URL PERCENT-ENCODING ESCAPE """
    # ----------------------------
    try:
        encoded = string.encode(ENCODING_STRING);
        quoted  = quote(encoded);
        decoded = quoted.decode(ENCODING_STRING); # a UnicodeDecodeError?
        final   = decoded;
    except (UnicodeDecodeError):
        final   = string;
    # ----------------------------
    return (final);
    # ----------------------------

def GET_URL_UNESCAPED_STRING (string):
    u""" URL PERCENT-DECODING UN-ESCAPE """
    # ----------------------------
    try:
        encoded  = string.encode(ENCODING_STRING);
        unquoted = unquote(encoded);
        decoded  = unquoted.decode(ENCODING_STRING); # a UnicodeDecodeError?
        final    = decoded;
    except (UnicodeDecodeError):
        final    = string;
    # ----------------------------
    return (final);
    # ----------------------------

def GET_XML_ESCAPED_STRING (string):
    u""" XML ESCAPE """
    # ----------------------------
    escaped = string;
    for (source, target) in XML_ESCAPE_MAP:
        escaped = escaped.replace(source, target);
    # for (source, target)
    # ----------------------------
    return (escaped);
    # ----------------------------

def GET_XML_UNESCAPED_STRING (string):
    u""" XML UN-ESCAPE """
    # ----------------------------
    unescaped = string;
    for (source, target) in XML_UNESCAPE_MAP:
        unescaped = unescaped.replace(source, target);
    # for (source, target)
    # ----------------------------
    return (unescaped);
    # ----------------------------

def GET_BYTES_ESCAPED_STRING (string):
    u""" BYTES (BACKSLASH) ESCAPE """
    # ----------------------------
    return string.replace(
        ESCAPE_BYTES,
        quote(ESCAPE_BYTES)
    );
    # ----------------------------

def GET_BYTES_UNESCAPED_STRING (string):
    u""" BYTES (BACKSLASH) UN-ESCAPE """
    # ----------------------------
    return string.replace(
        quote(ESCAPE_BYTES),
        ESCAPE_BYTES
    );
    # ----------------------------

def GET_CONTROL_ESCAPED_STRING (string):
    u""" UNICODE "CONTROL" CODEPOINTS ESCAPE """
    # ----------------------------
    escaped_list = [];
    for character in string:
        match = False;
        for control_range in CONTROL_RANGES:
            if ord(character) in control_range:
                match = True;
                break; # for (control_range)
            else:
                pass;
        # for (control_range)
        if (match == True):
            escaped_list.append(u"?");
        else: # i.e. (match == False)
            escaped_list.append(character);
    # for (character)
    # ----------------------------
    escaped_string = u"".join(escaped_list);
    return (escaped_string);
    # ----------------------------

# ------------------------------------------------------------------------------

if __name__ == u"__main__":

    pass;