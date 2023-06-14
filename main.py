from tabula import read_pdf
from tabulate import tabulate
import pandas as pd
import io

#TODO:
# Have an area selector to create accurate tables 
# Figure out how to handle tables that leak through multiple pages
#    - Have a feature saying need to select over multiple pages, then combine after selection
# Find a feature in tabula that does the first - for me.
# Use Tabula API if exists? (this is in order to make more accurate selection of table)
# Figure a way to make table into notion (Done but need to figure out better way)

def generate_checklist_table(dataframe):
    # Generate the HTML table
    checklist_table = ""
    for index, row in dataframe.iterrows():
        checklist_table += "<tr>"
        checklist_table += f"<td><input type='checkbox' onclick='toggleRow(this, {index})'></td>"
        for value in row.values[0:]:
            checklist_table += f"<td>{value}</td>"
        checklist_table += "</tr>"

    return checklist_table


def generate_html_file(dataframe, filename):
    checklist_table = generate_checklist_table(dataframe)
    headers = "\n".join([f"<th>{header}</th>" for header in dataframe.columns])

    html_content = f"""
    <html>
    <head>
        <title>Checklist Table</title>
        <style>
            table {{
                border-collapse: collapse;
                width: 100%;
            }}
            th, td {{
                padding: 8px;
                text-align: left;
            }}
            th {{
                background-color: #f2f2f2;
            }}
            .completed {{
                background-color: green;
            }}
        </style>
        <script>
            function toggleRow(checkbox, row) {{
                var table = checkbox.closest('table');
                var rows = table.getElementsByTagName('tr');
                if (checkbox.checked) {{
                    rows[row + 1].classList.add('completed');
                }} else {{
                    rows[row + 1].classList.remove('completed');
                }}
            }}
        </script>
    </head>
    <body>
        <h1>Checklist Table</h1>
        <table>
            <thead>
                <tr>
                    <th>Complete</th>
                    {headers}
                </tr>
            </thead>
            <tbody>
                {checklist_table}
            </tbody>
        </table>
    </body>
    </html>
    """

    with open(filename, "w") as file:
        file.write(html_content)


def main():
    # Read only page 3 of the file
    quizzes = read_pdf('Test_Syllabus.pdf', pages=[5], multiple_tables=False, lattice=True, stream=True)
    df = quizzes[0]
    # df = df[df["Quiz"].str.contains("Quiz")]
    generate_html_file(df, "checklist.html")


if __name__ == "__main__":
    main()


# Transform the result into a string table format
# table = tabulate(df)

# print(table)


# Transform the table into dataframe
# df = pd.read_fwf(io.StringIO(table))



# # Save the final result as excel file
# df.to_excel("./SylLink/Test_Syallbus.xlsx")