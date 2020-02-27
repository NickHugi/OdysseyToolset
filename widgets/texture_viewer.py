import io

from PIL import Image
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QWidget
from pykotor.globals import resource_types

from pykotor.formats.tpc import TPC
from ui import texture_viewer


class TextureViewer(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)

        self.ui = texture_viewer.Ui_Form()
        self.ui.setupUi(self)

    @staticmethod
    def open_resource(parent, res_ref, res_type, res_data, txi=""):
        widget = TextureViewer(parent)

        if res_type == resource_types["tpc"]:
            tpc = TPC.from_data(res_data)
            qimage = QImage(tpc.width, tpc.height, QImage.Format_RGBA8888)

            pixels = tpc.get_rgba()
            for x in range(tpc.width):
                for y in range(tpc.height):
                    index = x + y * tpc.width
                    qimage.setPixel(x, y, pixels[index])

            widget.ui.texture_label.setPixmap(QPixmap.fromImage(qimage))
            widget.ui.txi_edit.setPlainText(txi)
        else:
            image = Image.open(io.BytesIO(res_data))
            image = image.convert('RGBA')

            qimage = QImage(image.width, image.height, QImage.Format_RGBA8888)
            for y in range(image.height):
                for x in range(image.width):
                    pixel = image.getpixel((x, y))
                    rgba = (pixel[2]) + (pixel[1] << 8) + (pixel[0] << 16) + (pixel[3] << 24)
                    qimage.setPixel(x, y, rgba)

            widget.ui.texture_label.setPixmap(QPixmap.fromImage(qimage))
            widget.ui.txi_edit.setPlainText(txi)

        return widget


