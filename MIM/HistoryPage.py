from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5 import QtWidgets,uic,QtGui
from TableClass import TableModel,Examlist_TableModel
import pandas as pd
import mysql.connector
import base64
from PIL import Image
from io import BytesIO

class PageWindow(QtWidgets.QMainWindow):
    gotoSignal = pyqtSignal(str)

    def goto(self, name):
        self.gotoSignal.emit(name)

class History_Page(PageWindow):

    def __init__(self, *args, **kwargs):
        super(History_Page, self).__init__(*args, **kwargs)

        self.Selected_Flag = False

        #Define Database Connection
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Debsirin_135",
            database="software_onboard"
        )

        self.db_cursor = self.connection.cursor()

        uic.loadUi('UI\HistoryPage2.ui', self)
        self.setWindowTitle("HistoryPage")

        self.DateEdit = self.dateEdit
        self.Init_timeEdit = self.Init_TimeEdit
        self.Final_timeEdit = self.Final_TimeEdit

        self.PrescriptID_LineEdit = self.lineEdit
        self.PrescriptID_LineEdit.textChanged.connect(self.SearchExamID)
        
    
        self.btn_toExamPage = self.To_exampage_btn
        self.btn_toExamPage.clicked.connect(self.GotoExam)

        self.btn_1 = self.Datetime_search_btn
        self.btn_1.clicked.connect(self.Filter_Examlist)

        self.Medication_Image_Label = self.Select_Medication_Label
        self.Medication_Image_Label.hide()

        self.Medication_Detail_Label = self.Select_Medication_Detail_Label
        self.Medication_Detail_Label.hide()

        self.Exam_list_table = self.Exam_List_Table
        self.Exam_list_table.setModel(None)
        self.Exam_list_table.clicked.connect(self.Select_Exam_ID)

        self.Exam_result_table = self.Exam_Result_Table
        self.Exam_result_table.setModel(None)
        self.Exam_result_table.clicked.connect(self.Select_Medication)

        self.Import_Examlist_table()
    
    def Import_Examlist_table(self):
        query_Examination_List = "SELECT ID,Status,DecisionDay,DecisionTime FROM exam_list" 
        self.db_cursor.execute(query_Examination_List)
        data = self.db_cursor.fetchall()

        self.connection.commit()

        data_df = pd.DataFrame(data,columns = ['ID','Status','DecisionDay','DecisionTime'])
        data_df = data_df.sort_values(by=['DecisionDay', 'DecisionTime'])
        self.Examlist_table(data_df)
    
    def Import_Exam_Result(self,Select_exam_id):
        self.Medication_Image_Label.hide()
        self.Medication_Detail_Label.hide()

        query_Examination_Result = "SELECT Status,MedicineName,ExamQuentity,SetQuentity FROM exam_prescript WHERE exam_ID = %(exam_ID)s" 
        query_data_Examination_Result = {
            'exam_ID': Select_exam_id
        }
        self.db_cursor.execute(query_Examination_Result,query_data_Examination_Result)
        data = self.db_cursor.fetchall()

        self.connection.commit()

        data_df = pd.DataFrame(data,columns = ['  Status  ','MedicineName','Detected','  Goal  '])
        self.Examresult_table(data_df)

    def Examlist_table(self,Exam_info):
        model = Examlist_TableModel(Exam_info)
        self.Exam_list_table.setModel(model)
        self.Exam_list_table.resizeColumnToContents(1)
        self.Exam_list_table.resizeColumnToContents(2)
        self.Exam_list_table.resizeColumnToContents(3)
        self.Exam_list_table.model().Send_Exam_id.connect(self.Import_Exam_Result)
    
    def Examresult_table(self,Exam_info):
        model = TableModel(Exam_info)
        self.Exam_result_table.setModel(model)
        self.Exam_result_table.resizeColumnToContents(0)
        self.Exam_result_table.resizeColumnToContents(2)
        self.Exam_result_table.resizeColumnToContents(3)
        self.Exam_result_table.model().Send_Medication.connect(self.Import_Medication_info)

        for i in range(len(self.Exam_result_table.model()._data)):
            self.Exam_result_table.showRow(i)

    def Select_Exam_ID(self,Select_index):
        self.Exam_list_table.model().Selected_Exam_ID(Select_index.row())

    def Select_Medication(self,Select_index):
        self.Exam_result_table.model().Selected_Medication(Select_index.row())

    def Import_Medication_info(self,s):
        query_Medicine_Info = "SELECT Picture,Info FROM medicine_info WHERE MedicineName = %(MedNAme)s" 
        query_data_Medicine_Info = {
            'MedNAme': s
        }
        self.db_cursor.execute(query_Medicine_Info,query_data_Medicine_Info)
        data = self.db_cursor.fetchall()

        self.connection.commit()

        im = Image.open(BytesIO(data[0][0]))
        resize_img = im.resize((303, 150))
        rotated_img = resize_img.rotate(180) 
        rotated_img.save('Icon\MedicationLabel.{im_format}'.format(im_format=im.format))

        self.Medication_Image_Label.setPixmap(QtGui.QPixmap("Icon\MedicationLabel.JPEG"))
        self.Medication_Image_Label.show()
        self.Medication_Detail_Label.setText(data[0][1])
        self.Medication_Detail_Label.show()


    def Filter_Examlist(self):
        self.Date = self.DateEdit.dateTime()
        self.init_time = self.Init_timeEdit.dateTime()
        self.final_time = self.Final_timeEdit.dateTime()

        timefilter_query_Examination_List = "SELECT ID,Status,DecisionDay,DecisionTime FROM exam_list WHERE DecisionDay = %(Date)s AND DecisionTime Between %(InitTime)s AND %(FinalTime)s" 
        timefilter_query_data_Examination_List = {
            'Date': self.DateEdit.date().toString("yyyy-MM-dd"),
            'InitTime': self.init_time.time().toString("HH:mm:ss"),
            'FinalTime': self.final_time.time().toString("HH:mm:ss")
        }

        self.db_cursor.execute(timefilter_query_Examination_List,timefilter_query_data_Examination_List)
        data = self.db_cursor.fetchall()

        self.connection.commit()

        data_df = pd.DataFrame(data,columns = ['ID','Status','DecisionDay','DecisionTime'])
        data_df = data_df.sort_values(by=['DecisionDay', 'DecisionTime'])

        if self.Exam_result_table.model() != None:
            for i in range(len(self.Exam_result_table.model()._data)):
                self.Exam_result_table.hideRow(i)

        self.Examlist_table(data_df)

    def SearchExamID(self,s):
        query_Examination_List = "SELECT ID,Status,DecisionDay,DecisionTime FROM exam_list WHERE ID LIKE %(ID)s"
        query_Data_Examination_List = {
            'ID':'%'+s+'%'
        }
        self.db_cursor.execute(query_Examination_List,query_Data_Examination_List)
        data = self.db_cursor.fetchall()

        self.connection.commit()

        data_df = pd.DataFrame(data,columns = ['ID','Status','DecisionDay','DecisionTime'])
        data_df = data_df.sort_values(by=['DecisionDay', 'DecisionTime'])

        if self.Exam_result_table.model() != None:
            for i in range(len(self.Exam_result_table.model()._data)):
                self.Exam_result_table.hideRow(i)

        self.Examlist_table(data_df)

    def GotoExam(self):
        if self.Exam_result_table.model() != None:
            for i in range(len(self.Exam_result_table.model()._data)):
                self.Exam_result_table.hideRow(i)
        
        self.Medication_Image_Label.hide()
        self.Medication_Detail_Label.hide()
        self.PrescriptID_LineEdit.clear()
        self.goto("Main")
        

