from PyQt5.QtCore import QThreadPool, pyqtSignal
from PyQt5 import QtWidgets,uic,QtGui
from PyQt5.QtWidgets import (
    QFileDialog,
    QMessageBox,
    QLineEdit
)
import pandas as pd
import os
import sys
import datetime
import mysql.connector

class PageWindow(QtWidgets.QMainWindow):
    gotoSignal = pyqtSignal(str)

    def goto(self, name):
        self.gotoSignal.emit(name)


class Login_Page(PageWindow):

    def __init__(self, *args, **kwargs):
        super(Login_Page, self).__init__(*args, **kwargs)

        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Debsirin_135",
            database="software_onboard"
        )

        self.db_cursor = self.connection.cursor()
        #Load the UI Page
        uic.loadUi('UI/LoginPage.ui', self)
        self.setWindowTitle("Medicine Inspection Machine")

        self.UserEdit_Login = self.Username_edit_login

        self.PasswordEdit_Login = self.Password_edit_login
        self.PasswordEdit_Login.setEchoMode(QLineEdit.Password)

        self.Show_psw_btn = self.ShowPassword_btn
        self.Show_psw_btn.setCheckable(True)
        self.Show_psw_btn.clicked.connect(self.PasswordLogin_Toggle)

        self.Loginbtn = self.Login_btn
        self.Loginbtn.clicked.connect(self.Login)

        self.loginLabel = self.Login_status
        self.loginLabel.setText("")
        

        self.UserEdit_Signup = self.Username_edit_signup

        self.PasswordEdit_Signup = self.Password_edit_signup
        self.PasswordEdit_Signup.setEchoMode(QLineEdit.Password)

        self.Show_psw_signup_btn = self.ShowPassword_signin_btn
        self.Show_psw_signup_btn.setCheckable(True)
        self.Show_psw_signup_btn.clicked.connect(self.PasswordLogin_Toggle)

        self.CF_PasswordEdit_Signup = self.ConfirmPassword_edit_signup
        self.CF_PasswordEdit_Signup.setEchoMode(QLineEdit.Password)

        self.show_CFpsw_signup_btn = self.ShowCFPassword_signin_btn
        self.show_CFpsw_signup_btn.setCheckable(True)
        self.show_CFpsw_signup_btn.clicked.connect(self.PasswordLogin_Toggle)

        self.AuthorizedEdit = self.Authorized_edit

        self.Signupbtn = self.Signup_btn
        self.Signupbtn.clicked.connect(self.Signup)

        self.SignupLabel = self.Signin_status
        self.SignupLabel.setText("")

    def Login(self):
        Username = self.UserEdit_Login.text()
        Password = self.PasswordEdit_Login.text()
        query_useraccount = "SELECT Password FROM useraccount WHERE Username = %(Username)s" 
        query_data_useraccount = {
            'Username': Username
        }

        self.db_cursor.execute(query_useraccount,query_data_useraccount)
        DB_Password = self.db_cursor.fetchone()
        if DB_Password != None:
            if Password == DB_Password[0]:
                self.UserEdit_Login.setText("")
                self.PasswordEdit_Login.setText("")
                self.loginLabel.setText("")

                self.PasswordEdit_Signup.setText("")
                self.CF_PasswordEdit_Signup.setText("")
                self.AuthorizedEdit.setText("")
                self.UserEdit_Signup.setText("")
                self.SignupLabel.setText("")
                self.goto("Main")
            else:
                self.loginLabel.setText("Wrong Password or Username!!")
        else :
            self.loginLabel.setText("Username not found")
    
    def Signup(self):
        Username = self.UserEdit_Signup.text()
        Password = self.PasswordEdit_Signup.text()
        CF_password = self.CF_PasswordEdit_Signup.text()
        Autho = self.AuthorizedEdit.text()
        query_useraccount = "SELECT Username FROM useraccount WHERE Username = %(Username)s" 
        query_data_useraccount = {
            'Username': Username
        }

        self.db_cursor.execute(query_useraccount,query_data_useraccount)
        DB_Username = self.db_cursor.fetchone()
        if DB_Username != None:
            self.SignupLabel.setText("This Username already use")
        elif Password != CF_password:
            self.SignupLabel.setText("Confirm Pasword is incorrect")
        elif Autho != "Hello1234":
            self.SignupLabel.setText("Wrong Authorized Code")
        elif len(Password) < 5:
            self.SignupLabel.setText("Password is too short")
        else :
            self.SignupLabel.setText("Created Account Complete")
            add_Useracount = "INSERT INTO useraccount (Username,Password) VALUES (%(U)s, %(P)s)"
            data_add_Useracount = {
                'U': Username,
                'P': Password
            }
            self.db_cursor.execute(add_Useracount,data_add_Useracount)
            self.connection.commit()

            self.PasswordEdit_Signup.setText("")
            self.CF_PasswordEdit_Signup.setText("")
            self.AuthorizedEdit.setText("")
            self.UserEdit_Signup.setText("")
            



    def PasswordLogin_Toggle(self):
        if self.Show_psw_btn.isChecked() == True:
            self.PasswordEdit_Login.setEchoMode(QLineEdit.Normal)
        else :
            self.PasswordEdit_Login.setEchoMode(QLineEdit.Password)

        if self.Show_psw_signup_btn.isChecked() == True:
            self.PasswordEdit_Signup.setEchoMode(QLineEdit.Normal)
        else :
            self.PasswordEdit_Signup.setEchoMode(QLineEdit.Password)

        if self.show_CFpsw_signup_btn.isChecked() == True:
            self.CF_PasswordEdit_Signup.setEchoMode(QLineEdit.Normal)
        else :
            self.CF_PasswordEdit_Signup.setEchoMode(QLineEdit.Password)
        


# def main():
#     app = QtWidgets.QApplication(sys.argv)
#     main = Login_Page()
#     main.show()
#     sys.exit(app.exec_())

# if __name__ == '__main__':
#     main()