# *** LEVEL 1 - HIDE ROWS BY REGEX MATCH
# In this exercise we will use a logic we already know but adjust it slightly
# We will hide rows in a XSLX file by matching the values in certain cells with a regex expression
# If the regex matches, we want to hide that row

import os
import re
import openpyxl

from pathlib import Path

sample_file = os.path.join('files', 'sample_translation.xlsx')


# TASK 1

# Write a function "hide_row_by_regex" that hides rows in an XLSX based on the the cell value in a certain column
# E.g. in a row the cell value for the column "Source" matches a regular expression, hide the entire row
# It should take three positional argument:
# - "xlsx_path": for the path to an XLSX file that should be edited
# - "column_name": for the name of the column in the header row. Not that this is not the column letter!
# - "regex": the regular expression to check cell values with
# It should take one keyworded argument:
# - "out_file_suffix": the suffix added to a new XLSX saved by the function. The default value should be "_cols_hidden"
# It shouldn't return anything but save a new file after it's done
# Hint: The logic is very similar to our function "toggle_non_translatable_background_color"!

# TODO: Write your code here! Feel free to delete this comment!

def hide_row_by_regex(xlsx_path, column_name, regex, out_file_suffix='_cols_hidden'):
    """
    Hides rows in an XLSX file based on the values in certain cells.
    :param xlsx_path: path of XLSX file to be formatted
    :param column_name: header name of the column that should be checked for cell values
    :param regex: regular expression to check cell values with
    :param out_file_suffix: suffix added to the output file name before saving
    :return: None
    """
    target_col = None
    hidden_rows = list()
    workbook = openpyxl.load_workbook(xlsx_path)
    for worksheet in workbook:
        rows = worksheet.rows
        header_row = worksheet[1]
        for cell in header_row:
            if cell.value == column_name:
                target_col = cell.column
        for row_index, row in enumerate(rows):
            for cell in row:
                cell_column = cell.column
                cell_value = str(cell.value)
                if not cell_value:
                    continue
                if cell_column == target_col and re.search(regex, cell_value):
                    hidden_rows.append(cell.row)
        for row_index in hidden_rows:
            worksheet.row_dimensions[row_index].hidden = True
    hidden_out_dir = os.path.dirname(xlsx_path)
    hidden_out_file = Path(xlsx_path).stem + out_file_suffix + '.xlsx'
    hidden_out_path = os.path.join(hidden_out_dir, hidden_out_file)
    workbook.save(hidden_out_path)


# TASK 2
# The file "sample_translation.xlsx" contains a column "Creation Date"
# It contains information about when the translation was made
# During data review we have discovered, that some of the older translations are not up to standard
# We know want to hide all translations that have been Created before 2022
# Use your function "hide_row_by_regex" to hide all rows with creation dates not from 2022!
# Hint: openpyxl will parse dates in the format YYYY-MM-DD HH:MM:SS

# TODO: Write your code here! Feel free to delete this comment!

hide_row_by_regex(sample_file, 'Creation Date', r'^2022')
