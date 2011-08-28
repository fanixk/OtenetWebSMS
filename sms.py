#!/usr/bin/env python

#############################################################################
#									    #				
#    This program is free software: you can redistribute it and/or modify   #
#    it under the terms of the GNU General Public License as published by   #
#    the Free Software Foundation, either version 3 of the License, or	    #
#    (at your option) any later version.				    #
#									    #
#    This program is distributed in the hope that it will be useful,	    #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of	    #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the	    #
#    GNU General Public License for more details.			    #
#									    #
#    You should have received a copy of the GNU General Public License	    #
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.  #
#								 	    #
#############################################################################

from mechanize import Browser
from PyQt4 import QtCore, QtGui
import sys
import re

msg = Browser()

class OtenetForm(QtGui.QWidget):
    """
      Main PyQT Form
    """
    def __init__(self, parent=None):
        super(OtenetForm, self).__init__(parent)

        self.message = ''
        self.number = ''
        self.content = self.parser()

        try:
            dailyLabel = QtGui.QLabel("Daily: " + self.getDailyRemaining(self.content) + "/5")
            monthlyLabel = QtGui.QLabel("Monthly: " + self.getMonthlyRemaining(self.content) + "/100")
        except:
            QtGui.QMessageBox.critical(self, "Login Error", "Invalid Login Information.")
            sys.exit(1)
            
        phoneLabel = QtGui.QLabel("Phone:")
        self.phoneLine = QtGui.QLineEdit()

        msgLabel = QtGui.QLabel("Message:")
        self.msgText = QtGui.QTextEdit()

        self.sendButton = QtGui.QPushButton("&Send")
        self.sendButton.show()
        self.exitButton = QtGui.QPushButton("&Exit")
        self.exitButton.show()
          
        self.sendButton.clicked.connect(self.checkSMS)	
        self.exitButton.clicked.connect(self.exit_app)

        buttonLayout1 = QtGui.QHBoxLayout()
        buttonLayout1.addWidget(self.sendButton)
        buttonLayout1.addWidget(self.exitButton)
        
        labelLayout1 = QtGui.QHBoxLayout()
        labelLayout1.addWidget(dailyLabel)
        labelLayout1.addWidget(monthlyLabel)

        mainLayout = QtGui.QGridLayout()
        mainLayout.addWidget(phoneLabel, 0, 0)
        mainLayout.addWidget(self.phoneLine, 0, 1)
        mainLayout.addWidget(msgLabel, 1, 0, QtCore.Qt.AlignTop)
        mainLayout.addWidget(self.msgText, 1 ,1)
        mainLayout.addLayout(buttonLayout1, 3, 1)
        mainLayout.addLayout(labelLayout1, 2 ,1, QtCore.Qt.AlignCenter)

        self.setLayout(mainLayout)
        self.setWindowTitle("OtenetWebSMS Sender")

    def exit_app(self):
        """
            Exit Application
        """
        sys.exit(1)
        
    def checkSMS(self):
        """
	  Validation of data
	  (add message encoding for greek characters)
        """
        self.number = self.phoneLine.text()
        self.message = self.msgText.toPlainText()
        self.number = str(self.number)  	#QString-->String
        self.message = str(self.message)	#################

        passed = True
        
        if not self.number.startswith("69") or len(self.number) > 10 or not self.number:
            passed = False
            QtGui.QMessageBox.information(self, "Invalid Number", "Enter a valid phone number.")
            return
        
        if len(self.message) > 137:
            passed = False
            QtGui.QMessageBox.information(self, "Limit", "Limit 137 chars.")
            return
        
        if not self.message:
            passed = False
            QtGui.QMessageBox.information(self, "Empty", "Enter a message.")
            return
        
        if passed == True:
            self.sendSMS()
        
    def sendSMS(self):
        """
	  Send SMS
	  (add error handling)
        """
        
        msg.set_handle_robots(False)
        msg.open("http://tools.otenet.gr/tools/tiles/web2sms.do?showPage=smsSend&mnu=smenu23")
        msg.select_form(name="sendform")
        msg["phone"] = self.number
        msg["message"] = self.message
        msg.submit()
        
        QtGui.QMessageBox.information(self, "Sent!", "Message was successfully sent.")
        
        self.dailyLabel.setText(self, "Daily: " + self.getDailyRemaining(self.content) + "/5")
        self.monthlyLabel.setText(self, "Monthly: " + self.getMonthlyRemaining(self.content) + "/100")
        
    def parser(self):
        """
        WebPage Parser
        """
        resp = msg.open("http://tools.otenet.gr/tools/tiles/web2sms.do?showPage=smsSend&mnu=smenu23")
        content = str(resp.read())
        return content
        
    def getDailyRemaining(self,content):
        content = re.search(r'<input type="hidden" name="todaySMS" value="(\d+)">', content)
        return content.group(1)
        
    def getMonthlyRemaining(self,content):
        content = re.search(r'<input type="hidden" name="monthSMS" value="(\d+)">', content)
        return content.group(1)

def login_ote(user, password):
    """
      Login
      (add error handling)
    """
    msg.set_handle_robots(False)
    msg.open("http://tools.otenet.gr/tools/index.do")
    msg.select_form(name="loginform")
    msg["username"] = user
    msg["password"] = password
    msg.submit()
    
if __name__ == '__main__':
    login_ote('***','***')		#login(username, password)
    app = QtGui.QApplication(sys.argv)
    otenet_form = OtenetForm()
    otenet_form.show()
    sys.exit(app.exec_())
