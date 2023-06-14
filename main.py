from tabula import read_pdf
from tabulate import tabulate
import pandas as pd
import sys
import io
from test_selection import coords as cds
from test_selection import QApplication, PdfViewer

#TODO:
# Create a GUI system to select page and other features
# Figure out how to handle tables that leak through multiple pages
#    - Have a feature saying need to select over multiple pages, then combine after selection

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
    print(coords)
    quizzes = read_pdf('Test_Syllabus.pdf', pages=[3], multiple_tables=False, lattice=True, stream=True, area=coords)
    df = quizzes[0]
    # df = df[df["Quiz"].str.contains("Quiz")]
    generate_html_file(df, "checklist.html")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pdf_path = 'Test_Syllabus.pdf'
    viewer = PdfViewer(pdf_path)
    coords = cds
    app.aboutToQuit.connect(main)
    sys.exit(app.exec_())
    