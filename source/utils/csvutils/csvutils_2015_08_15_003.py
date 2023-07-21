# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------

from lpod.document import odf_get_document, odf_new_document
from lpod.table    import odf_create_table, odf_create_cell

from utils.transliterator import transliterator_v21_2015_08_14_004 as transliterator

# ------------------------------------------------------------------------------

TRANSLITERATOR_TABLE  = r"C:\Users\User\Documents\LukaTolitch_005_PROGRAMMING\004_TRANSLITERATOR\Version_22\input\tables\Cyrillic_Russian_2015_08_19_005.csv";
TRANSLITERATOR_SOURCE = u"RUSSCII";
TRANSLITERATOR_TARGET = u"CYRILLIC";

CSV_SOURCE_PATH = r"C:\Users\User\Documents\LukaTolitch_012_LANGUAGES\Transliteration\Input.ods";
CSV_TARGET_PATH = r"C:\Users\User\Documents\LukaTolitch_012_LANGUAGES\Transliteration\Output.ods";

FILTER = False;

# ------------------------------------------------------------------------------

if __name__ == "__main__":

    # TRANSLITERATE AN ODS DOCUMENT, PAGE BY PAGE, STRING CELL BY STRING CELL:

    t = transliterator.Transliterator(table=TRANSLITERATOR_TABLE);
    t.set_map(source=TRANSLITERATOR_SOURCE, target=TRANSLITERATOR_TARGET);

    source_document = odf_get_document(CSV_SOURCE_PATH);
    source_body = source_document.get_body();

    target_document = odf_new_document(u"spreadsheet");
    target_body = target_document.get_body();

    for source_table in source_body.get_tables():
        # ----------------------------
        name = source_table.get_name();
        width, height = source_table.get_size();
        target_table = odf_create_table(name=name, width=width, height=height);
        # ----------------------------
        for row in range(height):
            for column in range(width):
                source_cell = source_table.get_cell((column, row));
                if (source_cell.get_type() == u"string"):
                    # ----------------------------
                    source_string = source_cell.get_value();
                    # ----------------------------
                    if (FILTER): # i.e. (FILTER == True)
                        target_string = t.filter(source_string=source_string); # FILTER-TRANSLITERATE!
                    else: # i.e. (FILTER == False)
                        target_string = t.transliterate(source_string=source_string); # TRANSLITERATE!
                    # ----------------------------
                    target_cell = odf_create_cell(cell_type=u"string", value=target_string);
                    target_table.set_cell((column, row), cell=target_cell);
                    # ----------------------------
                else: # i.e. (source_cell.get_type() != u"string")
                    # ----------------------------
                    source_value = source_cell.get_value();
                    source_type  = source_cell.get_type();
                    # ----------------------------
                    target_cell = odf_create_cell(cell_type=source_type, value=source_value);
                    target_table.set_cell((column, row), cell=target_cell);
                    # ----------------------------
            # for (column)
        # for (row)
        # ----------------------------
        target_body.append(target_table);
        # ----------------------------
    # for (table)

    target_document.save(CSV_TARGET_PATH);

    print u"\n>> A \"csvutils.py\" is done.";

