from tabula import read_pdf
import sys
from test_selection import coords as cds
from test_selection import QApplication, PdfViewer
import tkinter as tk
from tkinter import filedialog
from notion import create_database

#TODO:
# Create a GUI system to select page
#    - Ask if selection is good, if so, close app.
#    - Ask if need for multiple pages
# Figure out how to handle tables that leak through multiple pages
#    - Have a feature saying need to select over multiple pages, then combine after selection

file_path = None

import csv

def generate_csv_file(dataframe, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(dataframe.columns)  # Write the column headers
        for row in dataframe.values:
            cleaned_row = [str(cell).encode('utf-8', 'replace').decode('utf-8') for cell in row]
            writer.writerow(cleaned_row)  # Write the data rows

def main():
    # Read only page 3 of the file
    print(coords)
    quizzes = read_pdf(file_path, pages=[3], multiple_tables=False, lattice=True, stream=True, area=coords, encoding='latin-1')
    df = quizzes[0]
    generate_csv_file(df, "checklist.csv")
    create_database() # from notion.py


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    root = tk.Tk()
    root.withdraw()
    
    # open the file dialog box
    file_path = filedialog.askopenfilename()
    
    # pdf_path = 'T:\VsCode\SylLink\SylLink\Test_Syllabus.pdf'
    viewer = PdfViewer(file_path)
    coords = cds
    app.aboutToQuit.connect(main)
    sys.exit(app.exec_())
    