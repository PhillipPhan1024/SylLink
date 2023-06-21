from tabula import read_pdf
from tabulate import tabulate
import pandas as pd
import sys
from test_selection import coords as cds
from test_selection import QApplication, PdfViewer, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog

#TODO:
# Create a GUI system to select page
#    - Ask if selection is good, if so, close app.
#    - Ask if need for multiple pages
# Figure out how to handle tables that leak through multiple pages
#    - Have a feature saying need to select over multiple pages, then combine after selection
# CSS
# Customizable table

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

def read_custom_css(css_file):
    with open(css_file, "r") as file:
        css_content = file.read()
    return css_content

def generate_html_file(dataframe, filename, css_file="checklist.css"):
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
            {read_custom_css(css_file) if css_file else ''}
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

def select_pdf_file():
    file_path, _ = QFileDialog.getOpenFileName(None, "Select PDF File", "", "PDF Files (*.pdf)")
    if file_path:
        viewer = PdfViewer(file_path)
        viewer.setWindowTitle("SylLnk")
        viewer.setGeometry(100, 100, 800, 600)  # Set the window size
        viewer.show()
        return viewer
    return None


def main():
    viewer = select_pdf_file()
    if viewer:
        app.aboutToQuit.connect(
            lambda: generate_html_file(viewer.pdf_widget.get_dataframe(), "checklist.html")
        )
    else:
        sys.exit()

    app.exec_()

    if coords:
        print("ROI Coordinates:")
        for coord in coords:
            print(coord)
    else:
        print("No ROI coordinates selected.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("SylLnk")  # Set the program title

    coords = []

    window = QWidget()
    window.setWindowTitle("SylLnk")  # Set the window title
    window.setGeometry(100, 100, 600, 400)  # Set the window size
    layout = QVBoxLayout()

    button = QPushButton("Select PDF File")
    button.clicked.connect(select_pdf_file)
    layout.addWidget(button)

    window.setLayout(layout)
    window.show()

    app.aboutToQuit.connect(main)
    sys.exit(app.exec_())

    