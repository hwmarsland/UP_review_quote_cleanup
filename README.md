# University Press Review Quote and Blurb Cleanup Programs
DESCRIPTION
- The review quote program takes an excel file from a custom university press database, cleans up the raw quote data, splits that data into the text, the source, and the author of the quote, then places the split data into sperate columns. The result has greatly improved readability, makes the quotes sortable by author or source, and allows the data to be input into new databases more easily.
- The blurb program is a modification of the review quote program that parses a similar data set into just the text and author (no source).

USAGE
- Review Quote Program:
  - This program is run through the command line with the line "python review_text_cleanup_v2_0.py &lt;filename&gt;" but has a reminder of proper usage if this line is not input properly.
  - The filename portion is to be filled with the name of the excel file that the user has pulled from the database.
- Blurb Program:
  - This program is run through the command line with the line "python blurb_cleanup_v1_0.py &lt;filename&gt;" but has a reminder of proper usage if this line is not input properly.
  - The filename portion is to be filled with the name of the excel file that the user has pulled from the database.

PROGRAM STEPS (Review Quote)
- Collect the information from the command line call

My program that takes an excel file exported from a university press database and cleans up the raw quote data, then splits it into the text, the source, and the author of the quote.

The additional blurb programs are modifications of the review quote programs to parse a similar file into the text and author.
