#!/usr/bin/env python3
# -- coding: utf-8 --

import sys, os, subprocess, time
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QImageReader, QImage, QPainter, QPen, QTransform, QIcon
from PyQt5.QtWidgets import ( QApplication, QDialog, QFileDialog, QButtonGroup, QMessageBox,
    QTableWidgetItem, QHeaderView, QVBoxLayout, QLabel
)
sys.path.append(os.path.dirname(__file__)) # A workout for enabling python 2 like import
from ui_window import Ui_Dialog

class Window(QDialog, Ui_Dialog):
    thumbnailLoadRequested1 = QtCore.pyqtSignal(list, list)
    thumbnailLoadRequested2 = QtCore.pyqtSignal(list, list)
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tableWidget.itemSelectionChanged.connect(self.onSelectionChange)
        # manage threads
        self.thread1 = QtCore.QThread(self)
        self.thread2 = QtCore.QThread(self)
        self.loader1 = Loader()                 # TODO : delete loader on close
        self.loader1.moveToThread(self.thread1)
        self.loader2 = Loader()
        self.loader2.moveToThread(self.thread2)
        self.thumbnailLoadRequested1.connect(self.loader1.load)
        self.thumbnailLoadRequested2.connect(self.loader2.load)
        self.loader1.thumbnailLoaded.connect(self.setThumbnail)
        self.loader2.thumbnailLoaded.connect(self.setThumbnail)
        # Connect Signals
        self.closeBtn.clicked.connect(self.close)
        self.createPdfBtn.clicked.connect(self.createPdf)
        self.addFilesBtn.clicked.connect(self.addFiles)
        self.removeFileBtn.clicked.connect(self.removeFile)
        self.clearListBtn.clicked.connect(self.clearList)
        self.moveUpBtn.clicked.connect(self.moveUp)
        self.moveDownBtn.clicked.connect(self.moveDown)
        self.rotateLeftBtn.clicked.connect(self.rotateLeft)
        self.rotateRightBtn.clicked.connect(self.rotateRight)
        # start threads
        self.thread1.start()
        self.thread2.start()
        # Add files
        filenames = []
        if len(sys.argv)>1 :
            for each in sys.argv[1:]:
                if os.path.exists(each):
                    filenames.append(each)
        self.addFilesFromList(filenames)

    def getThumbnails(self, filenames):
        rows = self.tableWidget.rowCount()
        index_list = [i for i in range(rows-len(filenames), rows)]
        midpoint = len(filenames)//2
        self.thumbnailLoadRequested1.emit(filenames[:midpoint], index_list[:midpoint])
        self.thumbnailLoadRequested2.emit(filenames[midpoint:], index_list[midpoint:])

    def setThumbnail(self, image, index, img_width, img_height):
        self.verticalLayout2.itemAt(index).widget().setImage(image)
        self.tableWidget.item(index, 0).width = img_width
        self.tableWidget.item(index, 0).height = img_height

    def onThumbnailClick(self):
        row = self.verticalLayout2.indexOf(self.sender())
        self.tableWidget.selectRow(row)

    def onSelectionChange(self):
        rows = self.tableWidget.selectionModel().selectedRows()
        if len(rows)==0 : return
        row = rows[0].row()
        for i in range(self.tableWidget.rowCount()):
            thumbnail = self.verticalLayout2.itemAt(i).widget()
            thumbnail.select(False)
        thumbnail = self.verticalLayout2.itemAt(row).widget()
        thumbnail.select(True)

    def addFiles(self):
        filenames, format = QFileDialog.getOpenFileNames(self, "Select Files to Open", '', 'JPEG Images (*.jpg *.jpeg);;All Files (*)')
        self.addFilesFromList(filenames)

    def addFilesFromList(self, filenames):
        output_name = time.strftime('PDF Doc %Y-%m-%d %H:%M:%S')
        self.filenameEdit.setText(output_name)
        pm = QPixmap(100,100)
        pm.fill()
        row = self.tableWidget.rowCount()
        for filename in filenames:
            item = FileItem(filename)
            self.tableWidget.insertRow(row)
            self.tableWidget.setItem(row,0, item)
            thumb = Thumbnail(self.scrollAreaWidgetContents, pm)
            self.verticalLayout2.addWidget(thumb, 0, QtCore.Qt.AlignHCenter)
            thumb.clicked.connect(self.onThumbnailClick)
            row += 1
        self.getThumbnails(filenames)

    def removeFile(self):
        rows = self.tableWidget.selectionModel().selectedRows()
        for row in rows:
            self.tableWidget.removeRow(row.row())
            self.verticalLayout2.takeAt(row.row()).widget().deleteLater()

    def clearList(self):
        for i in range(self.tableWidget.rowCount()):
            self.verticalLayout2.takeAt(0).widget().deleteLater()
        self.tableWidget.clear()
        self.tableWidget.setRowCount(0)

    def moveUp(self):
        row = self.tableWidget.selectionModel().selectedRows()[0].row()
        if row == 0: return
        item_up = self.tableWidget.takeItem(row-1, 0)
        item_down = self.tableWidget.takeItem(row, 0)
        self.tableWidget.setItem(row-1, 0, item_down)
        self.tableWidget.setItem(row, 0, item_up)
        thumb1 = self.verticalLayout2.itemAt(row).widget()
        thumb2 = self.verticalLayout2.itemAt(row-1).widget()
        thumb1.pm, thumb2.pm = thumb2.pm, thumb1.pm
        thumb1.updatePixmap()
        thumb2.updatePixmap()
        self.tableWidget.selectRow(row-1)

    def moveDown(self):
        row = self.tableWidget.selectionModel().selectedRows()[0].row()
        if row == self.tableWidget.rowCount()-1: return
        item_up = self.tableWidget.takeItem(row, 0)
        item_down = self.tableWidget.takeItem(row+1, 0)
        self.tableWidget.setItem(row, 0, item_down)
        self.tableWidget.setItem(row+1, 0, item_up)
        thumb1 = self.verticalLayout2.itemAt(row).widget()
        thumb2 = self.verticalLayout2.itemAt(row+1).widget()
        thumb1.pm, thumb2.pm = thumb2.pm, thumb1.pm
        thumb1.updatePixmap()
        thumb2.updatePixmap()
        self.tableWidget.selectRow(row+1)

    def rotateLeft(self):
        row = self.tableWidget.selectionModel().selectedRows()[0].row()
        self.tableWidget.item(row, 0).rotate(-90)
        self.verticalLayout2.itemAt(row).widget().rotate(270)

    def rotateRight(self):
        row = self.tableWidget.selectionModel().selectedRows()[0].row()
        self.tableWidget.item(row, 0).rotate(90)
        self.verticalLayout2.itemAt(row).widget().rotate(90)

    def createPdf(self):
        tmpfiles = []
        for i in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(i, 0)
            filename = item.filename
            output_file = 'ebkmkr%i.pdf'%i
            if self.clearBgBtn.isChecked():
                process_options = ['-colorspace', 'gray', '-lat', '15x15-5%', '-compress', 'Group4']
            else:
                process_options = ['-compress', 'JPEG']
            dpi = str(item.width*25.4/210)
            cmd = ['convert', filename, '-rotate', str(item.rotation)] + process_options + [
                    '-units', 'pixelsperinch', '-density', dpi, output_file]
            p = subprocess.Popen(cmd)
            p.wait()
            tmpfiles.append(output_file)
        cmd = ['pdfunite'] + tmpfiles + ['%s.pdf'%self.filenameEdit.text()]
        p = subprocess.Popen(cmd)
        p.wait()
        for each in tmpfiles:
            os.remove(each)

class FileItem(QTableWidgetItem):
    def __init__(self, filename):
        QTableWidgetItem.__init__(self, filename)
        self.filename = filename
        self.rotation = 0
        self.width, self.height = 0, 0

    def rotate(self, deg):
        self.rotation += deg
        self.width, self.height = self.height, self.width


class Loader(QtCore.QObject):
    thumbnailLoaded = QtCore.pyqtSignal(QImage, int, int, int)
    def __init__(self, parent=None):
        QtCore.QObject.__init__(self, parent)

    def load(self, files, index_list):
        #print('files', files)
        for i in range(len(files)):
            image_reader = QImageReader(files[i])
            image_reader.setAutoTransform(True)
            image = image_reader.read()
            if not image.isNull() :
                width, height = image.width(), image.height()
                image = image.scaledToWidth(150)
                self.thumbnailLoaded.emit(image, index_list[i], width, height)

class Thumbnail(QLabel):
    clicked = QtCore.pyqtSignal()
    def __init__(self, parent, pm):
        QLabel.__init__(self, parent)
        self.setMouseTracking(True)
        self.setSizePolicy(0,0)
        self.setPixmap(pm)
        self.selected = False

    def mousePressEvent(self, ev):
        self.clicked.emit()

    def select(self, select):
        if select == self.selected : return
        self.selected = select
        self.updatePixmap()

    def updatePixmap(self):
        if self.selected:
            pm = self.pm.copy()
            painter = QPainter(pm)
            pen = QPen(QtCore.Qt.blue)
            pen.setWidth(4)
            painter.setPen(pen)
            painter.drawRect(2, 2, pm.width()-4, pm.height()-4)
            painter.end()
            self.setPixmap(pm)
        else:
            self.setPixmap(self.pm)

    def setImage(self, image):
        self.pm = QPixmap.fromImage(image)
        self.setPixmap(self.pm)
        self.updatePixmap()

    def rotate(self, degree):
        transform = QTransform()
        transform.rotate(degree)
        self.pm = self.pm.transformed(transform)
        self.updatePixmap()

def main():
    app = QApplication(sys.argv)
    app.setOrganizationName("ebook-maker")
    app.setApplicationName("ebook-maker")
    win = Window()
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

