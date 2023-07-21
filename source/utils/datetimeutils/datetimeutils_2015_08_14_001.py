# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------

from datetime               import *
from dateutil.parser        import *
from dateutil.relativedelta import *
# from dateutil.rrule         import *
from dateutil.tz            import *
# from dateutil.tzwin         import *
# from dateutil.zoneinfo      import *

from defs.globaldefs import globaldefs_2015_08_14_001 as globaldefs

# ------------------------------------------------------------------------------

def parse_timestamp (ts):
    u""" ... """
    # ----------------------------
    dt = datetime.fromtimestamp(int(ts)*1e-06, tz=tzlocal());
    # ----------------------------
    return (dt);
    # ----------------------------

# ------------------------------------------------------------------------------

def get_timestamp (dt):
    u""" ... """
    # ----------------------------
    td = dt - datetime.fromtimestamp(0.0, tz=tzutc());
    ts = td.total_seconds();
    # ----------------------------
    return (ts);
    # ----------------------------

# ------------------------------------------------------------------------------

def get_delta_string (td):
    u""" ... """
    # ----------------------------
    attrs  = (u"years", u"months", u"days", u"hours", u"minutes", u"seconds");
    # ----------------------------
    strings = [];
    for attr in attrs:
        # ----------------------------
        value = td.__getattribute__(attr);
        # ----------------------------
        if (value > 0):
            # ----------------------------
            if (value == 1):
                string = u"{0:d} {1:s}".format(value, attr[:-1]);
            else: # i.e. (value > 1)
                string = u"{0:d} {1:s}".format(value, attr);
            # ----------------------------
            strings.append(string);
            # ----------------------------
        else:
            pass;
        # ----------------------------
    # for (attr)
    # ----------------------------
    string = u", ".join(strings);
    # ----------------------------
    return (string);
    # ----------------------------

# ------------------------------------------------------------------------------

if __name__ == u"__main__":

    # ----------------------------

    print u"-" * 80;

    # [0] TIMEZONES:

    utc = tzutc();
    utc_dt = datetime(2015, 06, 13, tzinfo=utc);
    print u"[UTC] name:\"{0:s}\", offset:{1:s}".format(utc_dt.tzname(), utc_dt.utcoffset());
    print u"[UTC]: " + globaldefs.TEMPLATES_TIMEZONE[u"default"].format(utc_dt);

    cet = tzlocal();
    cet_dt = datetime(2015, 06, 13, tzinfo=cet);
    print u"[CET] name:\"{0:s}\", offset:{1:s}".format(cet_dt.tzname(), cet_dt.utcoffset());
    print u"[CET]: " + globaldefs.TEMPLATES_TIMEZONE[u"default"].format(cet_dt);

    custom = tzstr(u"UTC+01:00CET");
    custom_dt = datetime(2015, 06, 13, tzinfo=custom);
    print u"[CUSTOM] name:\"{0:s}\", offset:{1:s}".format(custom_dt.tzname(), custom_dt.utcoffset());
    print u"[CUSTOM]: " + globaldefs.TEMPLATES_TIMEZONE[u"default"].format(custom_dt);

    # ----------------------------

    print u"-" * 80;

    # [1] GET BOKMARK DATETIMES:

    # [1.1] GET THE BOOKMARK "ADDED" and "MODIFIED" DATETIMES FROM FIREFOX JSON TIMESTAMPS:
    added    = parse_timestamp(ts=u"1363281607000000");
    modified = parse_timestamp(ts=u"1403436856000000");
    print u"Added:    " + globaldefs.TEMPLATES_DATETIME[u"bookmark"].format(added);
    print u"Modified: " + globaldefs.TEMPLATES_DATETIME[u"bookmark"].format(modified);

    # [1.2] GET THE (TIME)DELTA OF THE ABOVE "ADDED" and "MODIFIED" DATETIMES:
    delta = relativedelta(modified, added);
    # print u"Delta:    " + globaldefs.TEMPLATES_TIMEDELTA[u"compact"].format(delta);
    # print u"Delta:    " + globaldefs.TEMPLATES_TIMEDELTA[u"expanded"].format(delta);
    print u"Delta:    " + get_delta_string(td=delta);

    # [1.3] GET (BACK) THE TIMESTAMPS OF THE ABOVE "ADDED" and "MODIFIED" DATETIMES:
    added_ts = get_timestamp(dt=added);
    # print u"Added:    " + globaldefs.TEMPLATES_TIMESTAMP[u"integer"].format(added_ts);
    print u"Added:    " + globaldefs.TEMPLATES_TIMESTAMP[u"float"].format(added_ts);
    # print u"Added:    " + globaldefs.TEMPLATES_TIMESTAMP[u"readable"].format(added_ts);
    modified_ts = get_timestamp(dt=modified);
    # print u"Modified: " + globaldefs.TEMPLATES_TIMESTAMP[u"integer"].format(modified_ts);
    print u"Modified: " + globaldefs.TEMPLATES_TIMESTAMP[u"float"].format(modified_ts);
    # print u"Modified: " + globaldefs.TEMPLATES_TIMESTAMP[u"readable"].format(modified_ts);
    # ----------------------------

    print u"-" * 80;

    # [2] GET (MIXED) DATETIME DATA:

    utc_then = parse(u"2014-05-03, 11:25:00 UTC");
    print u"[UTC] Then:  " + globaldefs.TEMPLATES_DATETIME[u"bookmark"].format(utc_then);
    utc_now = datetime.now(tz=tzutc());
    print u"[UTC] Now:   " + globaldefs.TEMPLATES_DATETIME[u"bookmark"].format(utc_now);
    utc_delta = relativedelta(utc_now, utc_then);
    # print u"[UTC] Delta: " + globaldefs.TEMPLATES_TIMEDELTA[u"compact"].format(utc_delta);
    # print u"[UTC] Delta: " + globaldefs.TEMPLATES_TIMEDELTA[u"expanded"].format(utc_delta);
    print u"[UTC] Delta: " + get_delta_string(td=utc_delta);

    print u"-" * 80;

    cet_then = parse(u"2014-05-03, 11:25:00", tzinfos=tzlocal);
    print u"[CET] Then:  " + globaldefs.TEMPLATES_DATETIME[u"bookmark"].format(cet_then);
    cet_now = datetime.now(tz=tzlocal());
    print u"[CET] Now:   " + globaldefs.TEMPLATES_DATETIME[u"bookmark"].format(cet_now);
    cet_delta = relativedelta(cet_now, cet_then);
    # print u"[CET] Delta: " + globaldefs.TEMPLATES_TIMEDELTA[u"compact"].format(cet_delta);
    # print u"[CET] Delta: " + globaldefs.TEMPLATES_TIMEDELTA[u"expanded"].format(cet_delta);
    print u"[CET] Delta: " + get_delta_string(td=utc_delta);

    print u"-" * 80;

    cet_then = parse(u"2014-05-03, 11:25:00", tzinfos=tzlocal);
    print u"[CUSTOM] Then:  " + globaldefs.TEMPLATES_DATETIME[u"bookmark"].format(cet_then);
    cet_now = datetime.now(tz=tzstr(u"UTC+01:00CET"));
    print u"[CUSTOM] Now:   " + globaldefs.TEMPLATES_DATETIME[u"bookmark"].format(cet_now);
    cet_delta = relativedelta(cet_now, cet_then);
    # print u"[CET] Delta: " + globaldefs.TEMPLATES_TIMEDELTA[u"compact"].format(cet_delta);
    # print u"[CET] Delta: " + globaldefs.TEMPLATES_TIMEDELTA[u"expanded"].format(cet_delta);
    print u"[CUSTOM] Delta: " + get_delta_string(td=utc_delta);

    print u"-" * 80;

    mixed_delta = relativedelta(utc_now, cet_then);
    # print u"[...] Delta: " + globaldefs.TEMPLATES_TIMEDELTA[u"compact"].format(mixed_delta);
    # print u"[...] Delta: " + globaldefs.TEMPLATES_TIMEDELTA[u"expanded"].format(mixed_delta);
    print u"[...] Delta: " + get_delta_string(td=utc_delta);

    # ----------------------------

    print u"-" * 80;