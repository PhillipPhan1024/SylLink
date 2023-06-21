from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QComboBox
from PyQt5.QtGui import QPixmap, QPainter, QPen, QImage
from PyQt5.QtCore import Qt, QRect, QSize
import fitz
import sys

coords = []  # Global coords that changes after a selection is made

class PdfWidget(QWidget):
    def __init__(self, page_combobox, parent=None):
        super().__init__(parent)
        self.pdf_path = ""
        self.page_index = 0
        self.roi_start_pos = None
        self.roi_end_pos = None
        self.setMinimumSize(QSize(800, 600))  # Set a minimum size
        self.page_combobox = page_combobox  # Store the page_combobox

    def load_pdf(self, pdf_path):
        self.pdf_path = pdf_path
        doc = fitz.open(self.pdf_path)
        page = doc[self.page_index]
        pixmap = self.get_page_pixmap(page)
        self.setFixedSize(pixmap.size())  # Adjust the size of the PdfWidget to match the pixmap
        self.update()

    def paintEvent(self, event):
        if not self.pdf_path:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        doc = fitz.open(self.pdf_path)
        page = doc[self.page_index]
        pixmap = self.get_page_pixmap(page)
        painter.drawPixmap(self.rect(), pixmap)

        if self.roi_start_pos and self.roi_end_pos:
            painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
            painter.drawRect(self.get_roi_rectangle())

    def get_roi_rectangle(self):
        if self.roi_start_pos and self.roi_end_pos:
            x = min(self.roi_start_pos.x(), self.roi_end_pos.x())
            y = min(self.roi_start_pos.y(), self.roi_end_pos.y())
            width = abs(self.roi_end_pos.x() - self.roi_start_pos.x())
            height = abs(self.roi_end_pos.y() - self.roi_start_pos.y())
            return QRect(x, y, width, height)
        return QRect()

    def get_page_pixmap(self, page):
        zoom = 1.0
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        img = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(img)
        return pixmap

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.roi_start_pos = event.pos()
            self.roi_end_pos = None
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.roi_start_pos:
            self.roi_end_pos = event.pos()
            coordinates = self.print_rectangle_coordinates()
            if coordinates:
                coords.clear()
                coords.append(coordinates)
            self.page_combobox.setCurrentIndex(self.page_index)  # Update the combobox selection
            self.update()

    def print_rectangle_coordinates(self):
        if self.roi_start_pos and self.roi_end_pos:
            y = self.roi_start_pos.y()
            x = self.roi_start_pos.x()
            height = abs(self.roi_end_pos.y() - self.roi_start_pos.y())
            width = abs(self.roi_end_pos.x() - self.roi_start_pos.x())
            return y, x, height, width
        return None

    def next_page(self):
        if not self.pdf_path:
            return

        doc = fitz.open(self.pdf_path)
        if self.page_index + 1 < doc.page_count:
            self.page_index += 1
            self.update()
            self.page_combobox.setCurrentIndex(self.page_index)  # Update the combobox selection

    def previous_page(self):
        if not self.pdf_path:
            return

        if self.page_index > 0:
            self.page_index -= 1
            self.update()
            self.page_combobox.setCurrentIndex(self.page_index)  # Update the combobox selection


class PdfViewer(QMainWindow):
    def __init__(self, pdf_path):
        super().__init__()
        self.pdf_path = pdf_path
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("PDF Viewer")

        self.page_combobox = QComboBox(self)
        self.page_combobox.currentIndexChanged.connect(self.change_page)
        self.page_combobox.setMinimumWidth(100)
        self.page_combobox.setFocusPolicy(Qt.NoFocus)

        self.pdf_widget = PdfWidget(self.page_combobox, self)

        self.next_page_button = QPushButton("Next Page")
        self.next_page_button.clicked.connect(self.pdf_widget.next_page)

        self.previous_page_button = QPushButton("Previous Page")
        self.previous_page_button.clicked.connect(self.pdf_widget.previous_page)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.page_combobox)
        main_layout.addWidget(self.pdf_widget)
        main_layout.addWidget(self.previous_page_button)
        main_layout.addWidget(self.next_page_button)

        central_widget = QWidget(self)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.update_page_combobox()

    def update_page_combobox(self):
        doc = fitz.open(self.pdf_path)
        self.page_combobox.clear()
        for i in range(doc.page_count):
            self.page_combobox.addItem(f"Page {i + 1}")

        self.change_page(0)  # Load the first page

    def change_page(self, index):
        self.pdf_widget.page_index = index
        self.pdf_widget.load_pdf(self.pdf_path)  # Reload the PDF with the new page index
        self.pdf_widget.update()
        self.page_combobox.setCurrentIndex(index)  # Update the combobox selection

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_D:
            self.pdf_widget.next_page()
        elif event.key() == Qt.Key_A:
            self.pdf_widget.previous_page()
