#!/usr/bin/env python3
# -- coding: utf-8 --

import sys, os, subprocess, time
from ctypes import *
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QImageReader, QImage, QPainter, QPen, QTransform, QIcon
from PyQt5.QtWidgets import ( QApplication, QDialog, QFileDialog, QMessageBox,
    QTableWidgetItem, QHeaderView, QLabel, QSystemTrayIcon
)
sys.path.append(os.path.dirname(__file__)) # A workout for enabling python 2 like import
from ui_window import Ui_Dialog
from pdfwriter import *

lib = CDLL(os.path.dirname(__file__) +"/filters.so")
def adaptiveThresh(image):
    data_ptr = c_void_p(image.bits().__int__())
    w,h,BPL = image.width(), image.height(), image.bytesPerLine()
    lib.adaptiveIntegralThresh(data_ptr, w, h, BPL)


class Window(QDialog, Ui_Dialog):
    thumbnailLoadRequested = QtCore.pyqtSignal(int, list, list)
    imgProcRequested = QtCore.pyqtSignal(int, str, int)
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tableWidget.itemSelectionChanged.connect(self.onSelectionChange)
        self.tableWidget.cellClicked.connect(self.onItemClick)
        self.compressBtn.setEnabled(False)
        # manage threads, (must delete threads and loader on close)
        self.threads = []
        self.workers = []
        for i in range(3):
            thread = QtCore.QThread(self)
            worker = Worker(i)
            worker.moveToThread(thread)
            self.thumbnailLoadRequested.connect(worker.load)
            worker.thumbnailLoaded.connect(self.setThumbnail)
            self.imgProcRequested.connect(worker.processImage)
            worker.imageReady.connect(self.onImageReady)
            self.threads.append(thread)
            self.workers.append(worker)
            thread.start()
        # Connect Signals
        self.closeBtn.clicked.connect(self.close)
        self.clearBgBtn.toggled.connect(self.onClearBgBtnClick)
        self.createPdfBtn.clicked.connect(self.createPdf)
        self.addFilesBtn.clicked.connect(self.addFiles)
        self.removeFileBtn.clicked.connect(self.removeFile)
        self.clearListBtn.clicked.connect(self.clearList)
        self.moveUpBtn.clicked.connect(self.moveUp)
        self.moveDownBtn.clicked.connect(self.moveDown)
        self.rotateLeftBtn.clicked.connect(self.rotateLeft)
        self.rotateRightBtn.clicked.connect(self.rotateRight)
        # Add files
        filenames = []
        if len(sys.argv)>1 :
            for each in sys.argv[1:]:
                if os.path.exists(each):
                    filenames.append(each)
        self.addFilesFromList(filenames)
        # init some variables


    def getThumbnails(self, filenames):
        rows = self.tableWidget.rowCount()
        index_list = [i for i in range(rows-len(filenames), rows)]
        midpoint = len(filenames)//2
        self.thumbnailLoadRequested.emit(0, filenames[:midpoint], index_list[:midpoint])
        self.thumbnailLoadRequested.emit(1, filenames[midpoint:], index_list[midpoint:])

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

    def onItemClick(self, row, col):
        scrolbar_pos = self.verticalLayout2.itemAt(row).widget().pos().y()
        self.scrollArea.verticalScrollBar().setValue(scrolbar_pos)

    def addFiles(self):
        filenames, format = QFileDialog.getOpenFileNames(self, "Select Files to Open", '', 'JPEG Images (*.jpg *.jpeg);;All Files (*)')
        self.addFilesFromList(filenames)

    def addFilesFromList(self, filenames):
        if filenames == [] : return
        pm = QPixmap(150,200)
        pm.fill()
        row = self.tableWidget.rowCount()
        for filename in filenames:
            item = FileItem(filename)
            if not os.path.exists(item.filename) : continue
            self.tableWidget.insertRow(row)
            self.tableWidget.setItem(row,0, item)
            thumb = Thumbnail(self.scrollAreaWidgetContents, pm)
            self.verticalLayout2.addWidget(thumb, 0, QtCore.Qt.AlignHCenter)
            thumb.clicked.connect(self.onThumbnailClick)
            row += 1
        self.getThumbnails(filenames)
        self.tableWidget.selectRow(0)
        # get valid output filename
        first_file = self.tableWidget.item(0, 0).filename
        self.output_dir = os.path.dirname(first_file) + '/'
        output_file = time.strftime('Doc %b%d.pdf') # 'Doc May21.pdf' like format
        output_file = autoRename(output_file, self.output_dir)
        self.filenameEdit.setText(os.path.basename(output_file)[:-4])

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
        self.filenameEdit.clear()

    def moveUp(self):
        rows = self.tableWidget.selectionModel().selectedRows()
        if len(rows) == 0 : return
        row = rows[0].row()
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
        rows = self.tableWidget.selectionModel().selectedRows()
        if len(rows) == 0 : return
        row = rows[0].row()
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
        rows = self.tableWidget.selectionModel().selectedRows()
        if len(rows) == 0 : return
        row = rows[0].row()
        self.tableWidget.item(row, 0).rotate(-90)
        self.verticalLayout2.itemAt(row).widget().rotate(270)

    def rotateRight(self):
        rows = self.tableWidget.selectionModel().selectedRows()
        if len(rows) == 0 : return
        row = rows[0].row()
        self.tableWidget.item(row, 0).rotate(90)
        self.verticalLayout2.itemAt(row).widget().rotate(90)

    def createPdf(self):
        '''start processing'''
        if self.tableWidget.rowCount() == 0 : return
        self.filenames = []
        for i in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(i, 0)
            filename = item.filename
            self.filenames.append(filename)
        self.writer = PdfWriter()
        self.writer.begin(self.output_dir+self.filenameEdit.text()+".pdf")
        # Directly embed the image file without processing
        if not self.clearBgBtn.isChecked() and not self.compressBtn.isChecked():
            for i, filename in enumerate(self.filenames):
                item = self.tableWidget.item(i, 0)
                img = PdfObj(Type='/XObject', Subtype='/Image',
                        Width=item.width, Height=item.height, ColorSpace='/DeviceRGB')
                img['BitsPerComponent'] = 8
                img['Filter'] = '/DCTDecode'
                self.writer.addObj(img, stream=readFile(filename))
                cont = PdfObj()
                pg_w, pg_h, matrix = pageMatrix(item.width, item.height, item.rotation)
                cont_strm = 'q %s /img0 Do Q'% matrix
                self.writer.addObj(cont, stream=cont_strm)
                page = self.writer.createPage(w=pg_w, h=pg_h, Contents=cont)
                page['Resources'] = PdfDict(XObject=PdfDict(img0=img))
                self.writer.addPage(page)
            self.writer.finish()
            trayIcon = Notifier(self)
            trayIcon.notify("Finished !", "Conversion has been finished")
        else:
            # process image for black & white and compress
            self.proc_mode = 1 if self.clearBgBtn.isChecked() else 0
            self.current_index = 0
            self.processedImages = {}
            self.beginProcessing()

    def beginProcessing(self):
        # check if all images has been processed
        if self.current_index == len(self.filenames):
            #save pdf and return
            self.writer.finish()
            trayIcon = Notifier(self)
            trayIcon.notify("Finished !", "Conversion has been finished")
            return
        # request for processing
        for i in range(3):
            if self.current_index+i >= len(self.filenames): break
            filename = self.filenames[self.current_index+i]
            self.imgProcRequested.emit(i, filename, self.proc_mode)

    def onImageReady(self, filename, image):
        self.processedImages[self.filenames.index(filename)] = image
        remaining = len(self.filenames)-self.current_index
        if len(self.processedImages) == min(3, remaining):
            #here save images as pdf
            for index, image in self.processedImages.items():
                rotation = self.tableWidget.item(index, 0).rotation
                # create buffer for saving image in memory
                buff = QtCore.QBuffer(self)
                buff.open(QtCore.QIODevice.ReadWrite)
                img = PdfObj(Type='/XObject', Subtype='/Image',
                            Width=image.width(), Height=image.height())

                if self.clearBgBtn.isChecked(): # Embed as monochrome png image
                    #image = image.convertToFormat(QImage.Format_Mono)
                    image.save(buff, "PNG")
                    idat, palette, bpc = parse_png(buff.data().data())
                    #img['ColorSpace'] = '/DeviceGray'
                    img['Filter'] = '/FlateDecode'
                    img['BitsPerComponent'] = bpc
                    img['ColorSpace'] = '[/Indexed /DeviceRGB 1 <ffffff000000>]'
                    decode_parms = PdfDict(BitsPerComponent=bpc, Predictor=15, Colors=1,
                                    Columns=image.width())
                    img['DecodeParms'] = decode_parms
                    imgdat = idat
                else:                           # embed as jpeg image
                    img['ColorSpace'] = '/DeviceRGB'
                    img['BitsPerComponent'] = 8
                    img['Filter'] = '/DCTDecode'
                    image.save(buff, "JPG")
                    imgdat=buff.data().data()
                self.writer.addObj(img, stream=imgdat)
                cont = PdfObj()
                pg_w, pg_h, matrix = pageMatrix(image.width(),image.height(), rotation)
                cont_strm = 'q %s /img0 Do Q'% matrix
                self.writer.addObj(cont, stream=cont_strm)
                page = self.writer.createPage(w=pg_w, h=pg_h, Contents=cont)
                page['Resources'] = PdfDict(XObject=PdfDict(img0=img))
                self.writer.addPage(page)
                buff.data().clear()     # clear buffer to free memory
                buff.close()

            self.processedImages.clear()
            self.current_index += min(3,remaining)
            self.beginProcessing()

    def onClearBgBtnClick(self, checked):
        self.compressBtn.setEnabled(not checked)

    def closeEvent(self, ev):
        for i, thread in enumerate(self.threads):
            self.workers[i].deleteLater()
            thread.quit()
        self.reject()
        QDialog.closeEvent(self, ev)

    def reject(self):
        QDialog.reject(self)


class FileItem(QTableWidgetItem):
    def __init__(self, filename):
        QTableWidgetItem.__init__(self, os.path.basename(filename))
        self.filename = os.path.abspath(filename)
        self.rotation = 0
        self.width, self.height = 0, 0

    def rotate(self, deg):
        self.rotation += deg


class Worker(QtCore.QObject):
    ''' Loads images and converts them to thumbnails'''
    thumbnailLoaded = QtCore.pyqtSignal(QImage, int, int, int)
    imageReady = QtCore.pyqtSignal(str, QImage)
    def __init__(self, i, parent=None):
        QtCore.QObject.__init__(self, parent)
        self.index = i

    def load(self, i, files, index_list):
        if self.index != i : return
        #print('files', files)
        for i in range(len(files)):
            image_reader = QImageReader(files[i])
            image_reader.setAutoTransform(True)
            image = image_reader.read()
            if not image.isNull() :
                width, height = image.width(), image.height()
                image = image.scaledToWidth(150)
                self.thumbnailLoaded.emit(image, index_list[i], width, height)

    def processImage(self, i, filename, mode):
        if self.index != i : return
        image_reader = QImageReader(filename)
        image_reader.setAutoTransform(True)
        image = image_reader.read()
        #if image.isNull() : return image
        if image.width() > 1600:
            image = image.scaledToWidth(1600)
        if mode==1:
            adaptiveThresh(image)
            image = image.convertToFormat(QImage.Format_Mono)
        self.imageReady.emit(filename, image)


class Thumbnail(QLabel):
    clicked = QtCore.pyqtSignal()
    def __init__(self, parent, pm):
        QLabel.__init__(self, parent)
        self.setMouseTracking(True)
        self.setSizePolicy(0,0)
        self.setPixmap(pm)
        self.selected = False
        self.pm = pm

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


class Notifier(QSystemTrayIcon):
    def __init__(self, parent):
        QSystemTrayIcon.__init__(self, QIcon(':/quartz.png'), parent)
        self.messageClicked.connect(self.deleteLater)
        self.activated.connect(self.deleteLater)

    def notify(self, title, message):
        self.show()
        # Wait for 200ms, otherwise notification bubble will showup in wrong position.
        wait(200)
        self.showMessage(title, message)
        QtCore.QTimer.singleShot(3000, self.deleteLater)

def wait(millisec):
    loop = QtCore.QEventLoop()
    QtCore.QTimer.singleShot(millisec, loop.quit)
    loop.exec_()

def autoRename(filename, directory=None):
    if directory: filename = directory + filename
    name, ext = os.path.splitext(filename)
    i = 1
    while 1:
        if not os.path.exists(filename) : return filename
        filename = '%s %d%s' % (name, i, ext)
        i+=1


def main():
    app = QApplication(sys.argv)
    app.setOrganizationName("ebook-maker")
    app.setApplicationName("ebook-maker")
    win = Window()
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

