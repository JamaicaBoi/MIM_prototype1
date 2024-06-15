from PyQt5.QtCore import QThreadPool, pyqtSignal
from PyQt5 import QtWidgets,uic,QtGui
from PyQt5.QtWidgets import (
    QFileDialog,
    QMessageBox
)
from qt_material import apply_stylesheet
from TableClass import TableModel
from SelectPresciption_Widget import SelectPresciption_Window
from ML_Thread import MLThread
import pandas as pd
import os
import datetime
import mysql.connector
import time

class PageWindow(QtWidgets.QMainWindow):
    gotoSignal = pyqtSignal(str)

    def goto(self, name):
        self.gotoSignal.emit(name)


class MainWindow(PageWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.Selected_Image_Flag = False

        #Define Database Connection
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Debsirin_135",
            database="software_onboard"
        )

        self.db_cursor = self.connection.cursor()

        #Load the UI Page
        uic.loadUi('UI/Mainwindow.ui', self)
        os.mkdir("Examinated_Label")
        self.setWindowTitle("MainWindow")

        self.SelectWindow = SelectPresciption_Window()
        apply_stylesheet(self.SelectWindow,theme="light_blue.xml",css_file='UI/style.qss')
        self.SelectWindow.hide()

        self.Examtable = self.Exam_prescript_table

        # self.btn_1 = self.Select_prescript_btn
        self.btn_1 = self.findChild(QtWidgets.QPushButton,"Select_prescript_btn")
        self.btn_1.clicked.connect(self.Show_SelectPrescription_window)

        self.btn_2 = self.Upload_btn
        self.btn_2.clicked.connect(self.Upload_Exam_Image)

        self.btn_3 = self.Accepted_btn
        self.btn_3.setEnabled(False)
        self.btn_3.clicked.connect(lambda checked: self.Exam_Decision_action("Accepted")) 

        self.btn_4 = self.Denied_btn
        self.btn_4.setEnabled(False)
        self.btn_4.clicked.connect(lambda checked: self.Exam_Decision_action("Denied"))

        self.btn_toHistoryPage = self.To_recordedpage_btn
        self.btn_toHistoryPage.clicked.connect(self.GotoHistory)

        self.Exam_img_label = self.Exam_pic_display

        self.PrescripID_label = self.Prescrip_id_label

        self.Status_label = self.Status_display
        self.Status_label.setText('Select Prescription')

        self.LogOut_btn = self.Logout_btn
        self.LogOut_btn.clicked.connect(self.GotoLogin)

        self.threadpool = QThreadPool()
        self.Model = MLThread("Icon\clock-select-remain.png") ## dummy path
        self.threadpool.start(self.Model)

        #### test #####
        self.classify_time = []

    def Upload_Exam_Image(self):
        if self.Selected_Image_Flag == True:
            Filter = "Image Files (*.jpg *.png);;All Files (*)"
            fileName, _ = QFileDialog.getOpenFileName(self,"Select Image to Examination", "",Filter)
            if fileName:
                self.LogOut_btn.setEnabled(False)
                self.btn_toHistoryPage.setEnabled(False)
                self.btn_2.setEnabled(False)

                self.Exam_img_path = fileName
                self.Exam_img_label.setPixmap(QtGui.QPixmap(self.Exam_img_path))
                self.Status_label.setText("Loading ...")
                self.btn_1.setEnabled(False)
                self.btn_4.setEnabled(False)
                self.Classification(self.Exam_img_path)
        else:
            QMessageBox.warning(self, 'WARNING', "The prescription to be examinate has not been selected.")
    
    def Classification(self,path):
        self.Model = MLThread(path)
        self.Model.signals.finished.connect(self.Finished_Classify)
        self.threadpool.start(self.Model)
        self.start_time = time.time()

    def Show_SelectPrescription_window(self):
        self.SelectWindow.show()
        self.SelectWindow.ID_summit.connect(self.Select_Prescription)

    def Select_Prescription(self,ID):
        self.Current_ID = ID
        self.PrescripID_label.setText(self.Current_ID)
        query_Examination = "SELECT MedicineName,SetQuentity FROM pre_exam_prescript WHERE Pre_exam_ID = %(Query_index)s" 
        Query_data_Pres_exam_ID = {
            'Query_index': ID
        }

        self.db_cursor.execute(query_Examination,Query_data_Pres_exam_ID)
        data = self.db_cursor.fetchall()

        self.connection.commit()

        status_data = ["Waiting"]*len(data)
        detected_data = [0] * len(data)

        data_df = pd.DataFrame(data,columns = ['Medication','  Goal  '])
        data_df.insert(0,' Status ',status_data)
        data_df.insert(2,"Detected",detected_data)
        self.Examination_table(data_df)

        self.Selected_Image_Flag = True
        self.btn_3.setEnabled(False) ## Accept
        self.btn_4.setEnabled(True) ## Denied
        self.btn_1.setEnabled(True) ## Select_Prescipt
        self.Status_label.setText("Select Image to Examination")

    def Examination_table(self,Medicine_info):
        model = TableModel(Medicine_info)
        self.Current_df = Medicine_info
        self.Examtable.setModel(model)
        self.Examtable.resizeColumnToContents(0)
        self.Examtable.resizeColumnToContents(2)
        self.Examtable.resizeColumnToContents(3)
        for i in range(len(self.Examtable.model()._data)):
            self.Examtable.showRow(i)
    
    def Finished_Classify(self,t):
        self.end_time = time.time()
        self.classify_time.append(self.end_time-self.start_time)

        self.btn_4.setEnabled(True)
        self.Status_label.setText("Complete")
        Fullpath = str(self.Exam_img_path)
        head_tail = os.path.split(Fullpath)
        folder_path = 'Examinated_Label'

        Label_path = os.path.join(folder_path,head_tail[1],head_tail[1])
        self.Exam_img_label.setPixmap(QtGui.QPixmap(Label_path))
        self.btn_2.setEnabled(True)

        class_index = t[0]
        class_name = t[1]

        self.Examtable.model().df_updated.connect(self.Examination_table)
        self.Examtable.model().Wrong_Prescript.connect(self.Wrong_Medication_Found)
        self.Examtable.model().Complete_Exam.connect(self.Complete_Examination)
        self.Examtable.model().Update_Detect_Data(class_index,class_name)
    
    def Wrong_Medication_Found(self):
        self.btn_3.setEnabled(False)

    def Complete_Examination(self):
        self.btn_3.setEnabled(True)

    def Exam_Decision_action(self,Decision = str):
        if Decision == "Accepted":
            delete_pre_exam_prescipt = "DELETE FROM pre_exam_prescript WHERE Pre_exam_ID = %(ID)s"
            delete_data_pre_exam_prescipt = {
                'ID': self.Current_ID
            }
            delete_pre_exam_list = "DELETE FROM pre_exam_list WHERE ID = %(ID)s"
            delete_data_pre_exam_list = {
                'ID': self.Current_ID
            }
            self.db_cursor.execute(delete_pre_exam_prescipt,delete_data_pre_exam_prescipt)
            self.db_cursor.execute(delete_pre_exam_list,delete_data_pre_exam_list)
            self.connection.commit()

        for i in range(len(self.Examtable.model()._data)):
            self.Examtable.hideRow(i)

        self.Insert_Examination_Result(Decision)
        self.Exam_img_label.setPixmap(QtGui.QPixmap("Icon\Screenshot 2024-04-08 203400.png"))
        self.Status_label.setText('Select Prescription')
        self.PrescripID_label.clear()
        self.btn_1.setEnabled(True)
        self.btn_3.setEnabled(False)
        self.btn_4.setEnabled(False)
        self.LogOut_btn.setEnabled(True)
        self.btn_toHistoryPage.setEnabled(True)
        self.Selected_Image_Flag = False

    def Insert_Examination_Result(self,Decision=str):
        prescript_id_timestamp = self.Current_ID + '_' + str(datetime.datetime.now().strftime("%H:%M:%S"))
        add_exam_list = "INSERT INTO exam_list (ID,Status,DecisionDay,DecisionTime) VALUES (%(ID)s, %(Status)s, %(DecisionDay)s, %(DecisionTime)s)"
        data_exam_list = {
            'ID': prescript_id_timestamp,
            'Status': Decision,
            'DecisionDay': datetime.date.today(),
            'DecisionTime': datetime.datetime.now().time()
        }
        self.db_cursor.execute(add_exam_list,data_exam_list)

        add_exam_pres = "INSERT INTO exam_Prescript (exam_ID,Status,MedicineName,ExamQuentity,SetQuentity) VALUES (%(exam_ID)s, %(Status)s, %(MedicineName)s, %(ExamQuentity)s, %(SetQuentity)s)"
        Status_list_pres = self.Current_df[' Status '].tolist()
        Medicine_list_pres = self.Current_df["Medication"].tolist()
        DetectedQuentity_list = self.Current_df["Detected"].tolist()
        SetQuentity_list = self.Current_df["  Goal  "].tolist()

        for i in range(len(Medicine_list_pres)):
          data_exam_pres = {
            'exam_ID': prescript_id_timestamp,
            'Status': Status_list_pres[i],
            'MedicineName': Medicine_list_pres[i],
            'ExamQuentity': DetectedQuentity_list[i],
            'SetQuentity': SetQuentity_list[i]
          }
          self.db_cursor.execute(add_exam_pres,data_exam_pres)
        self.connection.commit()

    def GotoHistory(self):
        self.SelectWindow.hide()
        self.goto("History")
    
    def GotoLogin(self):
        dlg = QMessageBox.question(self,'Confirm Logout', "Do you want to log out?.")
        if dlg == QMessageBox.Yes:
            if self.Examtable.model() != None:
                for i in range(len(self.Examtable.model()._data)):
                    self.Examtable.hideRow(i)

            self.SelectWindow.hide()
            self.Exam_img_label.setPixmap(QtGui.QPixmap("Icon\Screenshot 2024-04-08 203400.png"))
            self.Status_label.setText('Select Prescription')
            self.PrescripID_label.clear()
            self.btn_1.setEnabled(True)
            self.btn_3.setEnabled(False)
            self.btn_4.setEnabled(False)
            self.Selected_Image_Flag = False
            self.goto("Login")
        else:
            None