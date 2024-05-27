from PyQt5.QtWidgets import QWidget
from PyQt5 import uic,QtCore
import mysql.connector

class SelectPresciption_Window(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    ID_summit = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Debsirin_135",
            database="software_onboard"
        )

        self.db_cursor = self.connection.cursor()

        uic.loadUi('UI/Select_Exam_Presciption_Widget.ui', self)
        self.LineEdit = self.Searchbar
        self.LineEdit.textChanged.connect(self.Search)

        self.ConfirmSelection_btn = self.Confirm_btn
        self.ConfirmSelection_btn.clicked.connect(self.Confirm)
        self.ConfirmSelection_btn.setEnabled(False)

        self.CancelSelection_btn = self.Cancel_btn
        self.CancelSelection_btn.clicked.connect(self.Cancel)

        self.IDList = self.PresciptionList

        self.Import_ID_list()
        self.IDList.currentTextChanged.connect(self.Selected_ID)
    
    def Import_ID_list(self):
        query = "SELECT ID FROM pre_exam_list"
        self.db_cursor.execute(query)
        ID_List = self.db_cursor.fetchall()
        List = []
        for i in range(len(ID_List)):
            List.append(ID_List[i][0])
        
        self.IDList.addItems(List)
    
    def Search(self,s):
        self.IDList.clear()
        query = "SELECT ID FROM pre_exam_list WHERE ID LIKE %(Search)s "
        Query_data_ID = {
            'Search': '%'+s+'%'
        }
        self.db_cursor.execute(query,Query_data_ID)
        ID_List = self.db_cursor.fetchall()
        List = []
        for i in range(len(ID_List)):
            List.append(ID_List[i][0])
        
        self.IDList.addItems(List)
    

    def Selected_ID(self,S):
        self.ID = S
        self.ConfirmSelection_btn.setEnabled(True)

    def Confirm(self):
        self.ID_summit.emit(self.ID)
        self.hide()

    def Cancel(self):
        self.hide()