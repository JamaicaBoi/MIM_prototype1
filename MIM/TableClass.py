import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt,pyqtSignal
from datetime import datetime
import numpy as np
import pandas as pd
import datetime


## Table for Examination page ##
class TableModel(QtCore.QAbstractTableModel):

    df_updated = pyqtSignal(pd.DataFrame)
    Wrong_Prescript = pyqtSignal()
    Complete_Exam = pyqtSignal()
    Send_Medication = pyqtSignal(str)

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        ##############Data type Handler###################
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            if isinstance(value, str):
                return '%s' % value
            if isinstance(value, np.int64):
                return int(value)
        #################Text Alignment####################
        if role == Qt.TextAlignmentRole:
            value = self._data.iloc[index.row(), index.column()]

            if isinstance(value, np.int64) or isinstance(value, float):
                return Qt.AlignVCenter + Qt.AlignHCenter
            
            if isinstance(value,str):
                return Qt.AlignVCenter + Qt.AlignHCenter
        ###############Blackground Gradient##############
        if role == Qt.BackgroundRole:
            value = self._data.iloc[index.row(), index.column()]
            if self._data.iloc[index.row(),0] == "Waiting":
                return QtGui.QColor('#DCDCDC') #gray
            if self._data.iloc[index.row(),0] == "Complete":
                return QtGui.QColor('#00D4AE') #green
            if self._data.iloc[index.row(),0] == "Incorrect":
                return QtGui.QColor('#F35A5A') #red
            if self._data.iloc[index.row(),0] == "Exceed":
                return QtGui.QColor('#ffee93') #ryellow
        ################ADD ICON#############################
        if role == Qt.DecorationRole:
            value = self._data.iloc[index.row(), index.column()]
            if value == "Waiting":
                return QtGui.QIcon('Icon/clock-select-remain.png')
            if value == "Complete":
                return QtGui.QIcon('Icon/tick.png')
            if value == "Incorrect":
                return QtGui.QIcon('Icon/cross.png')
            if value == "Exceed":
                return QtGui.QIcon('Icon/exclamation.png')

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])
    
    def Update_Detect_Data(self,Class_index,Class_nm):
        ###### Update Quentity ######
        for i in Class_index:
            Medicine_name = Class_nm[i]
            if Medicine_name in self._data['Medication'].tolist():
                index =  self._data.index.get_loc(self._data.loc[self._data['Medication'] == Medicine_name].index[0])
                self._data['Detected'][index] = self._data['Detected'][index] + 1
                ###### Check Goal #######
                if self._data['Detected'][index] == self._data['  Goal  '][index]:
                    self._data[' Status '][index] = "Complete"
                elif self._data['Detected'][index] > self._data['  Goal  '][index] and  self._data[' Status '][index] != 'Incorrect':
                    self._data[' Status '][index] = "Exceed"
                    self.Wrong_Prescript.emit()
            else:
                self._data.loc[self._data.shape[0]] = ['Incorrect', Medicine_name, 1,0]
                self.Wrong_Prescript.emit()
        
        if (self._data[" Status "] == "Complete").all():
            self.Complete_Exam.emit()
        
        self.df_updated.emit(self._data)
    
    def Selected_Medication(self, Selected_row):
        Medication_nm =  self._data.iloc[Selected_row,1]
        self.Send_Medication.emit(Medication_nm)


## Table for Examination page ##
class Examlist_TableModel(QtCore.QAbstractTableModel):

    df_updated = pyqtSignal(pd.DataFrame)
    Send_Exam_id = pyqtSignal(str)

    def __init__(self, data):
        super(Examlist_TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        ##############Data type Handler###################
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            if isinstance(value, str):
                return '%s' % value
            if isinstance(value, np.int64):
                return int(value)
            if isinstance(value, datetime.date):
                return str(value)
            if isinstance(value, datetime.timedelta):
                time = str(value)
                return time[7:15]
        #################Text Alignment####################
        if role == Qt.TextAlignmentRole:
            value = self._data.iloc[index.row(), index.column()]
            if isinstance(value, np.int64) or isinstance(value, float):
                return Qt.AlignVCenter + Qt.AlignHCenter
            if isinstance(value,str):
                return Qt.AlignVCenter + Qt.AlignHCenter
            if isinstance(value, datetime.date):
                return Qt.AlignVCenter + Qt.AlignHCenter
            if isinstance(value, datetime.timedelta):
                return Qt.AlignVCenter + Qt.AlignHCenter
        ###############Blackground Gradient##############
        if role == Qt.BackgroundRole:
            value = self._data.iloc[index.row(), index.column()]
            if self._data.iloc[index.row(),1] == "Accepted" and value == self._data.iloc[index.row(),1]:
                return QtGui.QColor('#00D4AE') #green
            elif self._data.iloc[index.row(),1] == "Denied" and value == self._data.iloc[index.row(),1]:
                return QtGui.QColor('#F35A5A') #red
            else:
                return QtGui.QColor('#DCDCDC') #gray
        ################ADD ICON#############################
        if role == Qt.DecorationRole:
            value = self._data.iloc[index.row(), index.column()]
            if value == "Waiting":
                return QtGui.QIcon('Icon/clock-select-remain.png')
            if value == "Complete":
                return QtGui.QIcon('Icon/tick.png')
            if value == "Incorrect":
                return QtGui.QIcon('Icon/cross.png')
            if value == "Exceed":
                return QtGui.QIcon('Icon/exclamation.png')
            
    def Selected_Exam_ID(self, Selected_row):
        Exam_id =  self._data.iloc[Selected_row,0]
        self.Send_Exam_id.emit(Exam_id)
    
    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])
    