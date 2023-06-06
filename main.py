from tabula import read_pdf
from tabulate import tabulate
import pandas as pd
import io

#TODO:
# Have an area selector to create accurate tables 
# Figure out how to handle tables that leak through multiple pages
#    - Creating two tables first and have an option to combine?
#    - Find a feature in tabula that does the first - for me.
#    - Use Tabula API if exists?
#    - Figure a way to make table into notion.

def create_checklist_table(dataframe):
    table = [[f"<input type='checkbox' disabled {'checked' if status else ''}>"] + row.tolist() for status, row in zip(dataframe['Status'], dataframe.iloc[:, 1:].itertuples(index=False))]
    headers = ["Status"] + list(dataframe.columns)[1:]
    return tabulate(table, headers=headers, tablefmt="html")

# Example usage


def main():
    # Read the only the page 3 of the file
    quizzes = read_pdf('./SylLink/Test_Syllabus.pdf',pages = [3], 
                            multiple_tables = False, lattice = True, stream=True)

    # print(quizzes)

    df = quizzes[0]
    df = df[df["Quiz"].str.contains("Quiz") == True]
    # print(df)
    
    df = pd.DataFrame(df)
    check_list = create_checklist_table(df)
    print(check_list)

if __name__ == "__main__":
    main()

# Transform the result into a string table format
# table = tabulate(df)

# print(table)


# Transform the table into dataframe
# df = pd.read_fwf(io.StringIO(table))



# # Save the final result as excel file
# df.to_excel("./SylLink/Test_Syallbus.xlsx")