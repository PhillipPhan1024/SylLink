from tabula import read_pdf
from tabulate import tabulate
import pandas as pd
import io

#TODO:
# Have an area selector to create accurate tables 
# Figure out how to handle tables that leak through multiple pages
#    - Creating two tables first and have an option to combine?
#    - Find a feature in tabula that does the first - for me.


# Read the only the page 3 of the file
quizzes = read_pdf('./SylLink/Test_Syllabus.pdf',pages = [3], 
                         multiple_tables = False, lattice = True, stream=True, area=[])

print(quizzes)

# Transform the result into a string table format
# table = tabulate(quizzes)

# Transform the table into dataframe
# df = pd.read_fwf(io.StringIO(table))



# Save the final result as excel file
# df.to_excel("./SylLink/Test_Syallbus.xlsx")