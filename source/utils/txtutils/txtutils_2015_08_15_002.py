# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------

from utils.transliterator import transliterator_v21_2015_08_18_001 as transliterator

# ------------------------------------------------------------------------------

TRANSLITERATOR_TABLE  = r"C:\Users\User\Documents\LukaTolitch_005_PROGRAMMING\004_TRANSLITERATOR\Version_22\input\tables\Cyrillic_Russian_2015_08_15_005.csv";
TRANSLITERATOR_SOURCE = u"CYRILLIC";
TRANSLITERATOR_TARGET = u"RUSSCII";

INPUT_TXT  = r"C:\Users\User\Documents\LukaTolitch_005_PROGRAMMING\004_TRANSLITERATOR\Version_22\input\texts\Text_Input_2015_08_15_001.txt";
OUTPUT_TXT = r"C:\Users\User\Documents\LukaTolitch_005_PROGRAMMING\004_TRANSLITERATOR\Version_22\output\Text_Output_2015_08_15_001.txt";

FILTER = False;

# ------------------------------------------------------------------------------

if __name__ == "__main__":

    # STREAM-TRANSLITERATE A TXT DOCUMENT:

    t = transliterator.Transliterator(table=TRANSLITERATOR_TABLE);
    t.set_map(source=TRANSLITERATOR_SOURCE, target=TRANSLITERATOR_TARGET);

    t.stream(
        input_path  = INPUT_TXT,
        output_path = OUTPUT_TXT,
		filter      = FILTER,
    );

    print u"\n>> A \"txtutils.py\" is done.";