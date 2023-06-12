import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QPainter, QPen, QImage
from PyQt5.QtCore import Qt
import fitz


class PdfViewer(QMainWindow):
    def __init__(self, pdf_path):
        super().__init__()
        self.pdf_path = pdf_path
        self.page_index = 0
        self.roi_start_pos = None
        self.roi_end_pos = None

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('PDF Viewer')
        self.pdf_widget = QLabel(self)
        self.setCentralWidget(self.pdf_widget)

        self.load_pdf()
        self.show()

    def load_pdf(self):
        doc = fitz.open(self.pdf_path)
        page = doc[self.page_index]
        pixmap = self.get_page_pixmap(page)
        self.pdf_widget.setPixmap(pixmap)

    def get_page_pixmap(self, page):
        zoom = 1.0
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        img = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(img)
        return pixmap

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))

        if self.roi_start_pos and self.roi_end_pos:
            painter.drawRect(self.roi_start_pos.x(), self.roi_start_pos.y(),
                             self.roi_end_pos.x() - self.roi_start_pos.x(),
                             self.roi_end_pos.y() - self.roi_start_pos.y())

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.roi_start_pos = event.pos()
            self.roi_end_pos = None
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.roi_start_pos:
            self.roi_end_pos = event.pos()
            self.update()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Right:
            self.next_page()
        elif event.key() == Qt.Key_Left:
            self.previous_page()

    def next_page(self):
        doc = fitz.open(self.pdf_path)
        if self.page_index + 1 < doc.page_count:
            self.page_index += 1
            self.load_pdf()

    def previous_page(self):
        if self.page_index > 0:
            self.page_index -= 1
            self.load_pdf()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    pdf_path = 'Test_Syllabus.pdf'
    viewer = PdfViewer(pdf_path)
    sys.exit(app.exec_())