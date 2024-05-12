from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from ultralytics import YOLO

import traceback, sys
import os


class MLSignals(QObject):
    finished = pyqtSignal(tuple)
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    # progress = pyqtSignal(int)


class MLThread(QRunnable):
    def __init__(self,Pic = None,*args, **kwargs):
        super(MLThread, self).__init__()

        self.model = YOLO('best.pt')
        
        self.pic = Pic
        self.args = args
        self.kwargs = kwargs
        self.signals = MLSignals()

    @pyqtSlot()
    def run(self):
        try:
            self.Split_path = os.path.split(self.pic)
            self.result = self.model(source=self.pic,save=True, project='Examinated_Label',name=self.Split_path[1])
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        finally:
            self.signals.finished.emit((self.result[0].boxes.cls.tolist(),self.result[0].names))  # Done
