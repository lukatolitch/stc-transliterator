# ------------------------------------------------------------------------------

cpdef unicode transliterate (unicode source_string, object MATCH, dict MAP, unsigned int MAX):
    u"""
        UNICODE VERSION!

        [0] SOURCES:
            [Python.Doc.2.7.7.RE] = Python >> 2.7.7 Documentation >> ... >> 7.2. re — Regular expression operations [2014-12-07]
            [Python.Doc.3.3.1.RE] = Python >> 3.3.1 Documentation >> ... >> 6.2.5.9. Writing a Tokenizer [2014-12-07]
            [Python.Doc.3.4.1.RE] = Python >> 3.4.1 Documentation >> ... >> 6.2.5.9. Writing a Tokenizer [2014-12-07]
            [Stack.MULTISUB] = http://stackoverflow.com/questions/15175142/how-can-i-do-multiple-substitutions-using-regex-in-python [2014-07-06]
            [DiveIntoPython.Performance.RE] = http://www.diveintopython.net/performance_tuning/regular_expressions.html [2014-12-07]
            [DiveIntoPython.Performance.DICT] = http://www.diveintopython.net/performance_tuning/dictionary_lookups.html [2014-12-07]
            [DiveIntoPython.Performance.LIST] = http://www.diveintopython.net/performance_tuning/list_operations.html [2014-12-07]
            [DiveIntoPython.Performance.STRING] = http://www.diveintopython.net/performance_tuning/string_manipulation.html [2014-12-07]

        [1] TLC1 TIME:
            10000 chars in 2e-02 (0.02)    TLC1 sec. [2014-12-24]
            5000  chars in 9e-03 (0.009)   TLC1 sec. [2014-12-24]
            3000  chars in 5e-03 (0.005)   TLC1 sec. [2014-12-24]
            1000  chars in 2e-03 (0.002)   TLC1 sec. [2014-12-24]
            500   chars in 1e-03 (0.001)   TLC1 sec. [2014-12-24]
            100   chars in 2e-04 (0.0002)  TLC1 sec. [2014-12-24]
            10    chars in 5e-05 (0.00005) TLC1 sec. [2014-12-24]

        [2] PROFILE (2014-12-08.001):
            re.match() (MATCH)   27.564 % OF CALLS
            list.append()        27.564 % OF CALLS
            len()                22.392 % OF CALLS
            re.match.group()     22.392 % OF CALLS
            unicode.join()        0.029 % OF CALLS

        [3] LOGIC (2014-12-08.001):
            match != None (CASE M)   80-75 % OF CASES
            match == None (CASE N)   20-25 % OF CASES

    """
    # ----------------------------
    cdef unicode match_string;
    cdef list target_list = [];
    cdef unsigned int i = 0;
    cdef unsigned int l = len(source_string);
    # ----------------------------
    TARGET_LIST_APPEND = target_list.append;
    # ----------------------------
    while (i < l):
        match = MATCH(source_string, i, i+MAX);
        if (match): # (match != None)
            match_string = match.group(0);
            TARGET_LIST_APPEND(MAP[match_string]);
            i += len(match_string);
        else: # (match == None)
            TARGET_LIST_APPEND(source_string[i]);
            i += 1;
    # while (i,l)
    # ----------------------------
    return (u"".join(target_list));
    # ----------------------------

# ------------------------------------------------------------------------------

cpdef bytes transliterate_encoded (bytes source_string, object MATCH, dict MAP, unsigned int MAX, unicode ENCODING):
    u"""
        BYTES (ENCODED) VERSION!

        10000 chars in 2e-02 (0.02)    TLC1 sec. [2014-12-24]
        5000  chars in 9e-03 (0.009)   TLC1 sec. [2014-12-24]
        3000  chars in 5e-03 (0.005)   TLC1 sec. [2014-12-24]
        1000  chars in 2e-03 (0.002)   TLC1 sec. [2014-12-24]
        500   chars in 1e-03 (0.001)   TLC1 sec. [2014-12-24]
        100   chars in 2e-04 (0.0002)  TLC1 sec. [2014-12-24]
        10    chars in 5e-05 (0.00005) TLC1 sec. [2014-12-24]
    """
    # ----------------------------
    cdef bytes match_string;
    cdef list target_list = [];
    cdef unsigned int i = 0;
    cdef unsigned int l = len(source_string);
    # ----------------------------
    TARGET_LIST_APPEND = target_list.append;
    # ----------------------------
    while (i < l):
        match = MATCH(source_string, i, i+MAX);
        if (match): # (match != None)
            match_string = match.group(0);
            TARGET_LIST_APPEND(MAP[match_string]);
            i += len(match_string);
        else: # (match == None)
            TARGET_LIST_APPEND(source_string[i]);
            i += 1;
    # while (i,l)
    # ----------------------------
    return (u"".encode(ENCODING).join(target_list));
    # ----------------------------

# ------------------------------------------------------------------------------

cpdef stream_transliterate (unicode input_string, object output_stream, object MATCH, dict MAP, unsigned int MAX, object SEND, object SENDER, int SIGNAL):
    u""" UNICODE STREAM VERSION """
    # ----------------------------
    cdef unicode match_string;
    cdef unsigned int i  = 0;
    cdef unsigned int l  = len(input_string);
    cdef unsigned int j  = 0;
    cdef unsigned int J  = 300;
    cdef unsigned int JJ = J * 3;
    # ----------------------------
    WRITE = output_stream.write;
    # ----------------------------
    while (i < l):
        match = MATCH(input_string, i, i+MAX);
        if (match): # (match != None)
            match_string = match.group(0);
            WRITE(MAP[match_string]);
            if (j >= J):
                SEND(sender=SENDER, signal=SIGNAL, current=i, total=l);
                j = 0;
            else: # (j < J)
                pass;
            i += len(match_string);
            j += 1;
        else: # (match == None)
            WRITE(input_string[i]);
            if (j >= JJ):
                SEND(sender=SENDER, signal=SIGNAL, current=i, total=l);
                j = 0;
            else: # (j < JJ)
                pass;
            i += 1;
            j += 1;
    # while (i,l)
    # ----------------------------
    SEND(sender=SENDER, signal=SIGNAL, current=l, total=l);
    # ----------------------------

# ------------------------------------------------------------------------------

cpdef unicode filter (unicode source_string, object MATCH, dict MAP, unsigned int MAX):
    u"""
        UNICODE VERSION!
    """
    # ----------------------------
    cdef unicode match_string;
    cdef unicode substring;
    cdef list target_list = [];
    cdef unsigned int i = 0;
    cdef unsigned int l = len(source_string);
    cdef unsigned int frozen = False;
    # ----------------------------
    TARGET_LIST_APPEND = target_list.append;
    # ----------------------------
    while (i < l):
        if (not frozen): # (frozen == False)
            # ----------------------------
            match = MATCH(source_string, i, i+MAX);
            if (match): # (match != None)
                match_string = match.group(0);
                TARGET_LIST_APPEND(MAP[match_string]);
                i += len(match_string);
            else: # (match == None)
                substring = source_string[i];
                if (substring == u"<"):
                    frozen = True;
                else: # (substring != u"<")
                    TARGET_LIST_APPEND(source_string[i]);
                i += 1;
            # ----------------------------
        else: # (frozen == True)
            # ----------------------------
            substring = source_string[i];
            if (substring == u">"):
                frozen = False;
            else: # (substring != u">")
                TARGET_LIST_APPEND(source_string[i]);
            i += 1;
            # ----------------------------
    # while (i,l)
    # ----------------------------
    return (u"".join(target_list));
    # ----------------------------

# ------------------------------------------------------------------------------

cpdef bytes filter_encoded (bytes source_string, object MATCH, dict MAP, unsigned int MAX, unicode ENCODING):
    u"""
        BYTES (ENCODED) VERSION!
    """
    # ----------------------------
    cdef bytes match_string;
    cdef bytes substring;
    cdef list target_list = [];
    cdef unsigned int i = 0;
    cdef unsigned int l = len(source_string);
    cdef unsigned int frozen = False;
    cdef bytes freeze   = u"<".encode(ENCODING);
    cdef bytes unfreeze = u">".encode(ENCODING);
    # ----------------------------
    TARGET_LIST_APPEND = target_list.append;
    # ----------------------------
    while (i < l):
        if (not frozen): # (frozen == False)
            # ----------------------------
            match = MATCH(source_string, i, i+MAX);
            if (match): # (match != None)
                match_string = match.group(0);
                TARGET_LIST_APPEND(MAP[match_string]);
                i += len(match_string);
            else: # (match == None)
                substring = source_string[i];
                if (substring == freeze): # (substring == u"<".encode(ENCODING))
                    frozen = True;
                else: # (substring != u"<".encode(ENCODING))
                    TARGET_LIST_APPEND(source_string[i]);
                i += 1;
            # ----------------------------
        else: # (frozen == True)
            # ----------------------------
            substring = source_string[i];
            if (substring == unfreeze): # (substring == u">".encode(ENCODING))
                frozen = False;
            else: # (substring != u">".encode(ENCODING))
                TARGET_LIST_APPEND(source_string[i]);
            i += 1;
            # ----------------------------
    # while (i,l)
    # ----------------------------
    return (u"".encode(ENCODING).join(target_list));
    # ----------------------------

# ------------------------------------------------------------------------------

cpdef stream_filter (unicode input_string, object output_stream, object MATCH, dict MAP, unsigned int MAX, object SEND, object SENDER, int SIGNAL):
    u""" UNICODE STREAM VERSION """
    # ----------------------------
    cdef unicode match_string;
    cdef unicode substring;
    cdef unsigned int i = 0;
    cdef unsigned int l = len(input_string);
    cdef unsigned int j  = 0;
    cdef unsigned int J  = 300;
    cdef unsigned int JJ = J * 3;
    cdef unsigned int frozen = False;
    # ----------------------------
    WRITE = output_stream.write;
    # ----------------------------
    while (i < l):
        if (not frozen): # (frozen == False)
            # ----------------------------
            match = MATCH(input_string, i, i+MAX);
            if (match): # (match != None)
                match_string = match.group(0);
                WRITE(MAP[match_string]);
                if (j >= J):
                    SEND(sender=SENDER, signal=SIGNAL, current=i, total=l);
                    j = 0;
                else: # (j < J)
                    pass;
                i += len(match_string);
                j += 1;
            else: # (match == None)
                substring = input_string[i];
                if (substring == u"<"):
                    frozen = True;
                else: # (substring != u"<")
                    WRITE(input_string[i]);
                    if (j >= JJ):
                        SEND(sender=SENDER, signal=SIGNAL, current=i, total=l);
                        j = 0;
                    else: # (j < JJ)
                        pass;
                i += 1;
                j += 1;
            # ----------------------------
        else: # (frozen == True)
            # ----------------------------
            substring = input_string[i];
            if (substring == u">"):
                frozen = False;
            else: # (substring != u">")
                WRITE(input_string[i]);
                if (j >= JJ):
                    SEND(sender=SENDER, signal=SIGNAL, current=i, total=l);
                    j = 0;
                else: # (j < JJ)
                    pass;
            i += 1;
            j += 1;
            # ----------------------------
    # while (i,l)
    # ----------------------------
    SEND(sender=SENDER, signal=SIGNAL, current=l, total=l);
    # ----------------------------

# ------------------------------------------------------------------------------

cpdef list segment (unicode source_string, object MATCH, dict MAP, unsigned int MAX):
    u"""
        UNICODE VERSION
    """
    # ----------------------------
    cdef list frozen            = [];
    cdef list unfrozen          = [];
    cdef list segments          = [];
    cdef unsigned int index     = 0;
    cdef unsigned int length    = len(source_string);
    cdef unsigned int is_frozen = False;
    cdef unicode prestring      = u"";
    cdef unicode substring      = u"";
    # ----------------------------
    while (index < length):
        if (not is_frozen): # (is_frozen == False)
            # ----------------------------
            match = MATCH(source_string, index, index+MAX);
            if (match): # (match != None)
                match_string = match.group(0);
                unfrozen.append(MAP[match_string]);
                index += len(match_string);
            else: # (match == None)
                prestring = substring;
                substring = source_string[index];
                if (prestring not in (u"#", u"<")) and (substring == u"<"):
                    if (unfrozen): # (unfrozen != [])
                        segments.append((1, u"".join(unfrozen)));
                        unfrozen = [];
                    else: # (unfrozen == [])
                        pass;
                    is_frozen = True;
                else: # (prestring in (u"#", u"<") or (substring != u"<")
                    unfrozen.append(substring);
                index += 1;
            # ----------------------------
        else: # (is_frozen == True)
            # ----------------------------
            prestring = substring;
            substring = source_string[index];
            if (prestring not in (u"#", u">")) and (substring == u">"):
                if (frozen): # (frozen != [])
                    segments.append((0, u"".join(frozen)));
                    frozen = [];
                else: # (frozen == [])
                    pass;
                is_frozen = False;
            else: # (prestring in (u"#", u">") or (substring != u">")
                frozen.append(substring);
            index += 1;
            # ----------------------------
    # while (index, length)
    # ----------------------------
    if (unfrozen): # (unfrozen != [])
        segments.append((1, u"".join(unfrozen)));
    else: # (unfrozen == [])
        pass;
    # ----------------------------
    if (frozen): # (frozen != [])
        segments.append((0, u"".join(frozen)));
    else: # (frozen == [])
        pass;
    # ----------------------------
    return (segments);
    # ----------------------------

# ------------------------------------------------------------------------------

cpdef list segment_encoded (bytes source_string, object MATCH, dict MAP, unsigned int MAX, unicode ENCODING):
    u"""
        BYTES (ENCODED) VERSION
    """
    # ----------------------------
    cdef list frozen            = [];
    cdef list unfrozen          = [];
    cdef list segments          = [];
    cdef unsigned int index     = 0;
    cdef unsigned int length    = len(source_string);
    cdef unsigned int is_frozen = False;
    cdef bytes EMPTY            = u"".encode(ENCODING);
    cdef bytes FREEZE           = u"<".encode(ENCODING);
    cdef bytes UNFREEZE         = u">".encode(ENCODING);
    cdef bytes HASH             = u"#".encode(ENCODING);
    cdef bytes prestring        = u"".encode(ENCODING);
    cdef bytes substring        = u"".encode(ENCODING);
    # ----------------------------
    while (index < length):
        if (not is_frozen): # (is_frozen == False)
            # ----------------------------
            match = MATCH(source_string, index, index+MAX);
            if (match): # (match != None)
                match_string = match.group(0);
                try:
                    unfrozen.append(MAP[match_string]);
                    index += len(match_string);
                except (KeyError):
                    pass;
            else: # (match == None)
                prestring = substring;
                substring = source_string[index];
                if (prestring not in (HASH,FREEZE)) and (substring == FREEZE): # (prestring not in (u"#".encode(ENCODING), u"<".encode(ENCODING)) and (substring == u"<".encode(ENCODING))
                    if (unfrozen): # (unfrozen != [])
                        segments.append((1, EMPTY.join(unfrozen)));
                        unfrozen = [];
                    else: # (unfrozen == [])
                        pass;
                    is_frozen = True;
                else: # (substring != u"<".encode(ENCODING))
                    unfrozen.append(substring);
                index += 1;
            # ----------------------------
        else: # (is_frozen == True)
            # ----------------------------
            prestring = substring;
            substring = source_string[index];
            if (prestring not in (HASH,UNFREEZE)) and (substring == UNFREEZE): # (prestring not in (u"#".encode(ENCODING), u">".encode(ENCODING)) and (substring == u">".encode(ENCODING))
                if (frozen): # (frozen != [])
                    segments.append((0, EMPTY.join(frozen)));
                    frozen = [];
                else: # (frozen == [])
                    pass;
                is_frozen = False;
            else: # (substring != u">".encode(ENCODING))
                frozen.append(substring);
            index += 1;
            # ----------------------------
    # while (index, length)
    # ----------------------------
    if (unfrozen): # (unfrozen != [])
        segments.append((1, EMPTY.join(unfrozen)));
    else: # (unfrozen == [])
        pass;
    # ----------------------------
    if (frozen): # (frozen != [])
        segments.append((0, EMPTY.join(frozen)));
    else: # (frozen == [])
        pass;
    # ----------------------------
    return (segments);
    # ----------------------------

# ------------------------------------------------------------------------------

cpdef list ranges (unicode source_string):
    u"""
        UNICODE VERSION
    """
    # ----------------------------
    cdef list ranges = [];
    # ----------------------------
    cdef unsigned int l = len(source_string);
    cdef unsigned int i = 0;
    cdef unsigned int j = 0;
    cdef unicode x      = u"";
    cdef unicode y      = source_string[0];
    cdef unsigned f;
    # ----------------------------
    if (y == u"<"):
        f = True;
    else: # (y != u"<")
        f = False;
    # ----------------------------
    while (j < l):
        x = y;
        y = source_string[j];
        if (f): # (f == True)
            if (x not in (u"#", u">") and (y == u">")):
                ranges.append((0, i, j+1));
                i = j + 1;
                f = False;
            else: # (x in (u"#", u"<") or (y != u"<"))
                pass;
        else: # (f == False)
            if (x not in (u"#", u"<") and (y == u"<")):
                ranges.append((1, i, j));
                i = j;
                f = True;
            else: # (x in (u"#", u"<") or (y != u"<"))
                pass;
        j += 1;
    # while (j, l)
    # ----------------------------
    if (f): # (f == True)
        if (i < j):
            ranges.append((0, i, j));
        else: # (i == j)
            pass;
    else: # (f == False)
        if (i < j):
            ranges.append((1, i, j));
        else: # (i == j)
            pass;
    # ----------------------------
    return (ranges)
    # ----------------------------

# ------------------------------------------------------------------------------

cpdef list ranges_encoded (bytes source_string, unicode ENCODING):
    u"""
        BYTES (ENCODED) VERSION
    """
    # ----------------------------
    cdef list ranges = [];
    # ----------------------------
    cdef unsigned int l = len(source_string);
    cdef unsigned int i = 0;
    cdef unsigned int j = 0;
    cdef bytes x        = u"".encode(ENCODING);
    cdef bytes y        = source_string[0];
    cdef bytes FREEZE   = u"<".encode(ENCODING);
    cdef bytes UNFREEZE = u">".encode(ENCODING);
    cdef bytes HASH     = u"#".encode(ENCODING);
    cdef unsigned f;
    # ----------------------------
    if (y == FREEZE): # (y == u"<".encode(ENCODED))
        f = True;
    else: # (y != u"<".encode(ENCODED))
        f = False;
    # ----------------------------
    while (j < l):
        x = y;
        y = source_string[j];
        if (f): # (f == True)
            if (x not in (HASH, UNFREEZE) and (y == UNFREEZE)): # (x not in (u"#".encode(ENCODING), u">".encode(ENCODING)) and (y == u">".encode(ENCODING)))
                ranges.append((0, i, j+1));
                i = j + 1;
                f = False;
            else: # (x in (u"#".encode(ENCODING), u"<".encode(ENCODING)) or (y != u"<".encode(ENCODING)))
                pass;
        else: # (f == False)
            if (x not in (HASH, FREEZE) and (y == FREEZE)): # (x not in (u"#".encode(ENCODING), u"<".encode(ENCODING) and (y == u"<".encode(ENCODING)))
                ranges.append((1, i, j));
                i = j;
                f = True;
            else: # (x in (u"#".encode(ENCODING), u"<".encode(ENCODING)) or (y != u"<".encode(ENCODING)))
                pass;
        j += 1;
    # while (j, l)
    # ----------------------------
    if (f): # (f == True)
        if (i < j):
            ranges.append((0, i, j));
        else: # (i == j)
            pass;
    else: # (f == False)
        if (i < j):
            ranges.append((1, i, j));
        else: # (i == j)
            pass;
    # ----------------------------
    return (ranges)
    # ----------------------------

# ------------------------------------------------------------------------------

cpdef list set_document_styles (object WINDOW, unicode ENCODING):
    u"""
        BYTES (ENCODED) VERSION
    """
    # ----------------------------
    cdef bytes source_string         = WINDOW.GetTextUTF8();
    cdef unsigned int l              = len(source_string);
    cdef unsigned int i              = 0;
    cdef unsigned int j              = 0;
    cdef bytes x                     = u"".encode(ENCODING);
    cdef bytes y                     = source_string[0];
    cdef bytes FREEZE                = u"<".encode(ENCODING);
    cdef bytes UNFREEZE              = u">".encode(ENCODING);
    cdef bytes HASH                  = u"#".encode(ENCODING);
    cdef unsigned int f;
    cdef unsigned int STYLE_MASK     = 31; # = (2**5) - 1 = "5-BIT"
    cdef unsigned int STYLE_UNFROZEN = WINDOW.style.indices[u"DEFAULT"];
    cdef unsigned int STYLE_FROZEN   = WINDOW.style.indices[u"FROZEN"];
    # ----------------------------
    WINDOW.ClearDocumentStyle();
    # ----------------------------
    if (y == FREEZE): # (y == u"<".encode(ENCODED))
        f = True;
    else: # (y != u"<".encode(ENCODED))
        f = False;
    # ----------------------------
    while (j < l):
        x = y;
        y = source_string[j];
        if (f): # (f == True)
            if (x not in (HASH, UNFREEZE) and (y == UNFREEZE)): # (x not in (u"#".encode(ENCODING), u">".encode(ENCODING)) and (y == u">".encode(ENCODING)))
                WINDOW.StartStyling(pos=i, mask=STYLE_MASK);
                WINDOW.SetStyling(length=j-i+1, style=STYLE_FROZEN);
                i = j + 1;
                f = False;
            else: # (x in (u"#".encode(ENCODING), u"<".encode(ENCODING)) or (y != u"<".encode(ENCODING)))
                pass;
        else: # (f == False)
            if (x not in (HASH, FREEZE) and (y == FREEZE)): # (x not in (u"#".encode(ENCODING), u"<".encode(ENCODING) and (y == u"<".encode(ENCODING)))
                WINDOW.StartStyling(pos=i, mask=STYLE_MASK);
                WINDOW.SetStyling(length=j-i, style=STYLE_UNFROZEN);
                i = j;
                f = True;
            else: # (x in (u"#".encode(ENCODING), u"<".encode(ENCODING)) or (y != u"<".encode(ENCODING)))
                pass;
        j += 1;
    # while (j, l)
    # ----------------------------
    if (f): # (f == True)
        if (i < j):
            WINDOW.StartStyling(pos=i, mask=STYLE_MASK);
            WINDOW.SetStyling(length=j-i, style=STYLE_FROZEN);
        else: # (i == j)
            pass;
    else: # (f == False)
        if (i < j):
            WINDOW.StartStyling(pos=i, mask=STYLE_MASK);
            WINDOW.SetStyling(length=j-i, style=STYLE_UNFROZEN);
        else: # (i == j)
            pass;
    # ----------------------------

# ------------------------------------------------------------------------------

cpdef list parse (unicode source_string, object MATCH, unsigned int MAX, dict IDS, dict INDICES):
    u"""
        UNICODE VERSION

        10000 chars in 2e-02 (0.02)    TLC1 sec. [2014-12-24]
        5000  chars in 1e-02 (0.01)    TLC1 sec. [2014-12-24]
        3000  chars in 6e-03 (0.006)   TLC1 sec. [2014-12-24]
        1000  chars in 2e-03 (0.002)   TLC1 sec. [2014-12-24]
        500   chars in 1e-03 (0.001)   TLC1 sec. [2014-12-24]
        100   chars in 3e-04 (0.0003)  TLC1 sec. [2014-12-24]
        10    chars in 7e-05 (0.00007) TLC1 sec. [2014-12-24]
    """
    # ----------------------------
    cdef list parse_list = [];
    cdef list match_indices;
    cdef unsigned int i = 0;
    cdef unsigned int j = 0;
    cdef unsigned int l = len(source_string);
    # ----------------------------
    PARSE_LIST_APPEND = parse_list.append;
    # ----------------------------
    while (j < l):
        match = MATCH(source_string, j, j+MAX);
        if (match): # (match != None)
            if (i < j):
                PARSE_LIST_APPEND((source_string[i:j], [], []));
            else: # (i == j)
                pass;
            match_string  = match.group(0);
            match_ids     = IDS[match_string];
            match_indices = INDICES[match_string];
            PARSE_LIST_APPEND((match_string, match_ids, match_indices));
            j += len(match_string);
            i = j;
        else: # (match == None)
            j += 1;
    # while (i,l)
    if (i < j):
        PARSE_LIST_APPEND((source_string[i:j], [], []));
    else: # (i == j)
        pass;
    # ----------------------------
    return (parse_list);
    # ----------------------------

# ------------------------------------------------------------------------------

cpdef list parse_encoded (bytes source_string, object MATCH, unsigned int MAX, dict INDEX):
    u"""
        BYTES (ENCODED) VERSION

        10000 chars in 2e-02 (0.02)    TLC1 sec. [2014-12-24]
        5000  chars in 1e-02 (0.01)    TLC1 sec. [2014-12-24]
        3000  chars in 6e-03 (0.006)   TLC1 sec. [2014-12-24]
        1000  chars in 2e-03 (0.002)   TLC1 sec. [2014-12-24]
        500   chars in 1e-03 (0.001)   TLC1 sec. [2014-12-24]
        100   chars in 3e-04 (0.0003)  TLC1 sec. [2014-12-24]
        10    chars in 7e-05 (0.00007) TLC1 sec. [2014-12-24]
    """
    # ----------------------------
    cdef list parse_list = [];
    cdef list match_indices;
    cdef unsigned int i = 0;
    cdef unsigned int j = 0;
    cdef unsigned int l = len(source_string);
    # ----------------------------
    PARSE_LIST_APPEND = parse_list.append;
    # ----------------------------
    while (j < l):
        match = MATCH(source_string, j, j+MAX);
        if (match): # (match != None)
            if (i < j):
                PARSE_LIST_APPEND((source_string[i:j], []));
            else: # (i == j)
                pass;
            match_string  = match.group(0);
            match_indices = INDEX[match_string];
            PARSE_LIST_APPEND((match_string, match_indices));
            j += len(match_string);
            i = j;
        else: # (match == None)
            j += 1;
    # while (i,l)
    if (i < j):
        PARSE_LIST_APPEND((source_string[i:j], []));
    else: # (i == j)
        pass;
    # ----------------------------
    return (parse_list);
    # ----------------------------

# ------------------------------------------------------------------------------

cpdef list derive (unicode source_string, object MATCH, unsigned int MAX, dict INDICES):
    u""" UNICODE VERSION """
    # ----------------------------
    cdef list derivation_list = [];
    cdef list match_indices;
    cdef unsigned int i = 0;
    cdef unsigned int j = 0;
    cdef unsigned int l = len(source_string);
    # ----------------------------
    PARSE_LIST_APPEND = derivation_list.append;
    # ----------------------------
    while (j < l):
        match = MATCH(source_string, j, j+MAX);
        if (match): # (match != None)
            if (i < j):
                PARSE_LIST_APPEND(source_string[i:j]);
            else: # (i == j)
                pass;
            match_string = match.group(0);
            match_index  = INDICES[match_string][0];
            PARSE_LIST_APPEND(match_index);
            j += len(match_string);
            i = j;
        else: # (match == None)
            j += 1;
    # while (i,l)
    if (i < j):
        PARSE_LIST_APPEND(source_string[i:j]);
    else: # (i == j)
        pass;
    # ----------------------------
    return (derivation_list);
    # ----------------------------

# ------------------------------------------------------------------------------

cpdef list derive_encoded (bytes source_string, object MATCH, unsigned int MAX, dict INDICES):
    u""" BYTES (ENCODED) VERSION """
    # ----------------------------
    cdef list derivation_list = [];
    cdef list match_indices;
    cdef unsigned int i = 0;
    cdef unsigned int j = 0;
    cdef unsigned int l = len(source_string);
    # ----------------------------
    PARSE_LIST_APPEND = derivation_list.append;
    # ----------------------------
    while (j < l):
        match = MATCH(source_string, j, j+MAX);
        if (match): # (match != None)
            if (i < j):
                PARSE_LIST_APPEND(source_string[i:j]);
            else: # (i == j)
                pass;
            match_string = match.group(0);
            match_index  = INDICES[match_string][0];
            PARSE_LIST_APPEND(match_index);
            j += len(match_string);
            i = j;
        else: # (match == None)
            j += 1;
    # while (i,l)
    if (i < j):
        PARSE_LIST_APPEND(source_string[i:j]);
    else: # (i == j)
        pass;
    # ----------------------------
    return (derivation_list);
    # ----------------------------

# ------------------------------------------------------------------------------

cpdef unicode integrate (list DERIVATIONS, list TARGET_STRINGS):
    u""" UNICODE VERSION """
    # ----------------------------
    cdef list integrations = [];
    cdef object derivation;
    # ----------------------------
    for derivation in DERIVATIONS:
        # ----------------------------
        if isinstance(derivation, int): # i.e. isinstance(derivation, int) == True, i.e. if a "derivation" is a derived row index integer
            # ----------------------------
            value = TARGET_STRINGS[derivation][0];
            integrations.append(value);
            # ----------------------------
        else: # i.e. isinstance(derivation, int) == False, i.e. if a "derivation" is not a derived row index integer, but an underived source string itself
            integrations.append(derivation);
        # ----------------------------
    # for (derivation)
    # ----------------------------
    return (u"".join(integrations));
    # ----------------------------

# ------------------------------------------------------------------------------

cpdef bytes integrate_encoded (list DERIVATIONS, list TARGET_STRINGS, unicode encoding):
    u""" BYTES (ENCODED) VERSION """
    # ----------------------------
    cdef list integrations = [];
    cdef object derivation;
    # ----------------------------
    for derivation in DERIVATIONS:
        # ----------------------------
        if isinstance(derivation, int): # i.e. isinstance(derivation, int) == True, i.e. if a "derivation" is a derived row index integer
            # ----------------------------
            value = TARGET_STRINGS[derivation][0];
            integrations.append(value);
            # ----------------------------
        else: # i.e. isinstance(derivation, int) == False, i.e. if a "derivation" is not a derived row index integer, but an underived source string itself
            integrations.append(derivation);
        # ----------------------------
    # for (derivation)
    # ----------------------------
    return (u"".encode(encoding).join(integrations));
    # ----------------------------

# ------------------------------------------------------------------------------
