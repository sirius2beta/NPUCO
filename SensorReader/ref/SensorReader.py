from PySide2.QtWidgets import QApplication
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile, QTimer
from PySide2.QtGui import QImage, QPixmap
from PySide2 import QtCore
import cv2

class Stats:
    def __init__(self):
        self.ui = QUiLoader().load("ui/AquaPlayerUI.ui")
        self.isCapturing = False
        self.cap = cv2.VideoCapture(0)
        
        self.timer = QTimer(self.ui)
        self.timer.timeout.connect(self.updateFrame)
        self.ui.btnStrVideo0.clicked.connect(self.toggleCamera)

    def updateFrame(self):
        ret, frame = self.cap.read()  
        if ret:
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgbImage.shape
            bytesPerLine = ch * w
            convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
            
            quality = self.ui.cbxQuality.currentText()
            if(quality == "1920*1080"):
                w = 1920
                h = 1080
            elif(quality == "1280*1024"):
                w = 1280
                h = 1024
            elif(quality == "640*480"):
                w = 640
                h = 480
            elif(quality == "320*240"):
                w = 320
                h = 240
            
            p = convertToQtFormat.scaled(w, h, aspectRatioMode=QtCore.Qt.KeepAspectRatio)
            self.ui.labVideo0.setPixmap(QPixmap.fromImage(p))
    
    def toggleCamera(self):
        if self.isCapturing:
            self.timer.stop()
            self.isCapturing = False
            self.ui.labVideo0.setText("video0")
            self.ui.btnStrVideo0.setText("開始")
        else:
            self.timer.start(20)
            self.isCapturing = True
            self.ui.btnStrVideo0.setText("關閉")

    """def connMod(self):"""
        

app = QApplication([])
stats = Stats()
stats.ui.show()
app.exec_()
