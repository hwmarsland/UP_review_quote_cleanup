# University Press Review Quote and Blurb Cleanup Programs
DESCRIPTION
- The review quote program takes an excel file from a custom university press database, cleans up the raw quote data, splits that data into the text, the source, and the author of the quote, marks what type of review the quotes is, then places the split data into sperate columns. The result has greatly improved readability, makes the quotes sortable by author or source, and allows the data to be input into new databases more easily.
- The blurb program is a modification of the review quote program that parses a similar data set into just the text and source (no author).

USAGE
- Review Quote Program:
  - This program is run through the command line with the line "python review_text_cleanup_v2_0.py &lt;filename&gt;" but has a reminder of proper usage if this line is not input properly.
  - The filename portion is to be filled with the name of the excel file that the user has pulled from the database.
- Blurb Program:
  - This program is run through the command line with the line "python blurb_cleanup_v1_0.py &lt;filename&gt;" but has a reminder of proper usage if this line is not input properly.
  - The filename portion is to be filled with the name of the excel file that the user has pulled from the database.

PROGRAM STEPS (Review Quote)
- Collect the information from the command line call
- Using pd.read_excel(), reads the contents of the provided excel file
- Create a temporary column (aka temp) that can be sliced apart to fill the new columns respectively
- Resets the index for the dataset to basic increasing integers
- Preforms a nearly identical cleanup as the University Press Data Cleanup program (see UP_data_cleanup repository) on the data in the temp column
- Iterates through the temp column, copying all of the text between the quotes and placing it in the text column in the same row
- Performs a cleanup of the text column, removing all unnecessary punctuation, extra spacing, and cells without text.
- Iterates through the temp column, removing the quotes and all text between them
- Iterates through the temp column, pulling the sources of the quotes and placing them in the source column in the same row or skipping the cell if the quote doesn't contain a source
- Performs a cleanup of the source column, removing all unnecessary punctuation, extra spacing, and cells without text.
- Iterates through the temp column, marking some quotes as endorsements if they contain specific strings and removing the sources
- Performs a cleanup of the temp column, removing any leftover punctuation not related to the author of the review
- Iterates through the temp column, copying the relavent leftover text into the text author column
- Iterates through the text author column, cleaning up spacing and formatting
- Iterates through the text type column, filling in the relavent unfilled slots with "Review Quote"
- Deletes the temp column
- Resets the index for the dataset to the original index
- Minor text cleanup overall
- Using pd.ExcelWriter(), write the edited data into a new excel file
- Save that file
- Print "Finished"

PROGRAM STEPS (Blurb)
- Collect the information from the command line call
- Using pd.read_excel(), reads the contents of the provided excel file
- Create a temporary column (aka temp) that can be sliced apart to fill the new columns respectively
- Resets the index for the dataset to basic increasing integers
- Preforms a nearly identical cleanup as the first half of the University Press Data Cleanup program (see UP_data_cleanup repository) on the data in the temp column
- Iterates through the temp column, copying all of the text between the quotes and placing it in the text column in the same row
- Performs a cleanup of the text column, removing all unnecessary punctuation, extra spacing, and cells without text.
- Iterates through the temp column, removing the quotes and all text between them
- Iterates through the temp column, copying the relavent leftover text into the source column
- Performs a minor cleanup of the source column data's spacing
- Iterates through the source column, checking for errors in the remaining data
- Preforms a nearly identical cleanup as the second half of the University Press Data Cleanup program (see UP_data_cleanup repository) on the data in the temp column
- Iterates through the text column doing a minor cleanup of punctuation
- Delets the temp column
- Replaces some formatting changes made during the parsing process for ease of conversion
- Using pd.ExcelWriter(), write the edited data into a new excel file
- Save that file
- Print "Finished"
