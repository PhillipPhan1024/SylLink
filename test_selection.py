import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import tabula
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import fitz

class PDFSelectionTool:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.selected_areas = []
        self.fig, self.ax = plt.subplots()
        self.page_number = 1
        self.image = self.extract_page_image(self.page_number)
        self.ax.imshow(self.image)
        self.rect = Rectangle((0, 0), 0, 0, linewidth=1, edgecolor='r', facecolor='none')
        self.ax.add_patch(self.rect)
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_move)
        plt.show()

 

    def extract_page_image(self, page_number):
        doc = fitz.open(self.pdf_path)
        page = doc.load_page(page_number - 1)
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        image = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)
        return pixmap

    def on_click(self, event):
        if event.button == 1:
            self.selected_areas.append((event.xdata, event.ydata))
            self.update_plot()

    def on_move(self, event):
        if event.button == 1:
            self.rect.set_width(event.xdata - self.rect.get_x())
            self.rect.set_height(event.ydata - self.rect.get_y())
            self.update_plot()

    def update_plot(self):
        self.ax.clear()
        self.ax.imshow(self.image)
        for x, y in self.selected_areas:
            self.ax.add_patch(Rectangle((x, y), 10, 10, linewidth=1, edgecolor='r', facecolor='none'))
        self.ax.add_patch(self.rect)
        plt.draw()

    def generate_pdf(self):
        output_filename = "selected_areas.pdf"
        c = canvas.Canvas(output_filename, pagesize=letter)
        for x, y in self.selected_areas:
            c.rect(x, y, 10, 10, stroke=1, fill=0)
        c.save()
        print(f"PDF file '{output_filename}' generated successfully.")

if __name__ == "__main__":
    pdf_path = "path_to_your_pdf_file.pdf"
    selection_tool = PDFSelectionTool(pdf_path)
    selection_tool.generate_pdf()
