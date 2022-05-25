from bs4 import BeautifulSoup
import os.path
import sys
import io
import urllib.request as req
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QKeySequence, QIcon
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QUrl, Qt
from PyQt5 import uic
from PIL import Image
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from smtplib import SMTP_SSL
import re
import datetime
from lib.TestLayout2 import Ui_MainWindow
from lib.AuthDialog import AuthDialog


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initAuthLock()
        self.initSignal()

        #로그인
        #self.user_id='test'
        #self.user_pw=None
        self.is_on=False
        self.home=None

    #기본 ui 비활성화
    def initAuthLock(self):
        self.comboBox.setEnabled(False)
        self.comboBox_2.setEnabled(False)
        self.calendarWidget.setEnabled(False)
        self.plainTextEdit.setEnabled(False)
        self.plainTextEdit_3.setEnabled(False)
        self.pushButton_2.setEnabled(False)
        self.pushButton_3.setEnabled(False)
        self.pushButton_4.setEnabled(False)
        self.pushButton_5.setEnabled(False)
        self.showStatusMsg('인증안됨')

    #기본 ui 활성화
    def initAuthActive(self):
        self.comboBox.setEnabled(True)
        self.comboBox_2.setEnabled(True)
        self.calendarWidget.setEnabled(True)
        self.plainTextEdit.setEnabled(True)
        self.plainTextEdit_3.setEnabled(True)
        self.pushButton_2.setEnabled(True)
        self.pushButton_3.setEnabled(True)
        self.pushButton_4.setEnabled(True)
        self.pushButton_5.setEnabled(True)
        self.showStatusMsg('인증 완료')

    def showStatusMsg(self,msg):
        self.statusbar.showMessage(msg)

    def initSignal(self):
        self.loginButton.clicked.connect(self.authCheck)
        #self.comboBox.clicked.connect(self.travelinfo)
        self.calendarWidget.clicked.connect(self.append_date)
        self.pushButton_3.clicked.connect(self.travelinfo)
        self.comboBox.currentIndexChanged.connect(self.extractPlace)
        self.pushButton_2.clicked.connect(self.new)
        self.plainTextEdit_2.setReadOnly(True)
        self.plainTextEdit_3.setReadOnly(True)
        self.pushButton_4.clicked.connect(self.sendEmail)
        self.pushButton_5.clicked.connect(self.clearMemo)


    @pyqtSlot()
    def clearMemo(self):
        self.plainTextEdit.clear()
        self.plainTextEdit.setFocus(True)


    @pyqtSlot()
    def sendEmail(self):
        email = EmailSender()
        email.exec_()


    @pyqtSlot()
    def new(self):
        form=Form()
        form.show()
        app.exec_()


    def closeEvent(self, QCloseEvent):
        ans = QMessageBox.question(self, "종료 확인", "종료하시겠습니까?",
                             QMessageBox.Yes|QMessageBox.No, QMessageBox.Yes)
        if ans == QMessageBox.Yes:
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore()



    @pyqtSlot()
    def authCheck(self):
        dlg = AuthDialog()
        dlg.exec_()
        self.user_id=dlg.user_id
        self.user_pw=dlg.user_pw
        print("id: %s password: %s" %(self.user_id,self.user_pw))
        if True:
            self.initAuthActive()
            self.loginButton.setText("인증 완료")
            self.loginButton.setEnabled(False)
            self.append_log_msg("login Success")
        else:
            QMessageBox.about(self, "인증오류", "아이디 또는 비밀번호를 확인해주세요")


    @pyqtSlot()
    def travelinfo(self):
        sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

        url1 = "http://api.visitkorea.or.kr/openapi/service/rest/GreenTourService/areaBasedList?serviceKey=QrLj7VbQShOJrUXBZpBkKF7hD5P8AixlwRQDy4QklL0m%2F1%2B57y4Q3QJzORuAne7sGPITPaEQtFPH5htq8cWXNQ%3D%3D&numOfRows=20&pageSize=20&pageNo=1& arrange=C&MobileOS=ETC&MobileApp=AppTest&areaCode=1"
        url2 = "http://api.visitkorea.or.kr/openapi/service/rest/GreenTourService/areaBasedList?serviceKey=QrLj7VbQShOJrUXBZpBkKF7hD5P8AixlwRQDy4QklL0m%2F1%2B57y4Q3QJzORuAne7sGPITPaEQtFPH5htq8cWXNQ%3D%3D&numOfRows=20&pageSize=20&pageNo=1& arrange=C&MobileOS=ETC&MobileApp=AppTest&areaCode=2"
        url3 = "http://api.visitkorea.or.kr/openapi/service/rest/GreenTourService/areaBasedList?serviceKey=QrLj7VbQShOJrUXBZpBkKF7hD5P8AixlwRQDy4QklL0m%2F1%2B57y4Q3QJzORuAne7sGPITPaEQtFPH5htq8cWXNQ%3D%3D&numOfRows=20&pageSize=20&pageNo=1& arrange=C&MobileOS=ETC&MobileApp=AppTest&areaCode=3"
        url4 = "http://api.visitkorea.or.kr/openapi/service/rest/GreenTourService/areaBasedList?serviceKey=QrLj7VbQShOJrUXBZpBkKF7hD5P8AixlwRQDy4QklL0m%2F1%2B57y4Q3QJzORuAne7sGPITPaEQtFPH5htq8cWXNQ%3D%3D&numOfRows=20&pageSize=20&pageNo=1& arrange=C&MobileOS=ETC&MobileApp=AppTest&areaCode=4"
        url6 = "http://api.visitkorea.or.kr/openapi/service/rest/GreenTourService/areaBasedList?serviceKey=QrLj7VbQShOJrUXBZpBkKF7hD5P8AixlwRQDy4QklL0m%2F1%2B57y4Q3QJzORuAne7sGPITPaEQtFPH5htq8cWXNQ%3D%3D&numOfRows=20&pageSize=20&pageNo=1& arrange=C&MobileOS=ETC&MobileApp=AppTest&areaCode=6"
        url7 = "http://api.visitkorea.or.kr/openapi/service/rest/GreenTourService/areaBasedList?serviceKey=QrLj7VbQShOJrUXBZpBkKF7hD5P8AixlwRQDy4QklL0m%2F1%2B57y4Q3QJzORuAne7sGPITPaEQtFPH5htq8cWXNQ%3D%3D&numOfRows=20&pageSize=20&pageNo=1& arrange=C&MobileOS=ETC&MobileApp=AppTest&areaCode=7"
        url31 = "http://api.visitkorea.or.kr/openapi/service/rest/GreenTourService/areaBasedList?serviceKey=QrLj7VbQShOJrUXBZpBkKF7hD5P8AixlwRQDy4QklL0m%2F1%2B57y4Q3QJzORuAne7sGPITPaEQtFPH5htq8cWXNQ%3D%3D&numOfRows=20&pageSize=20&pageNo=1& arrange=C&MobileOS=ETC&MobileApp=AppTest&areaCode=31"
        url32 = "http://api.visitkorea.or.kr/openapi/service/rest/GreenTourService/areaBasedList?serviceKey=QrLj7VbQShOJrUXBZpBkKF7hD5P8AixlwRQDy4QklL0m%2F1%2B57y4Q3QJzORuAne7sGPITPaEQtFPH5htq8cWXNQ%3D%3D&numOfRows=20&pageSize=20&pageNo=1& arrange=C&MobileOS=ETC&MobileApp=AppTest&areaCode=32"
        url33 = "http://api.visitkorea.or.kr/openapi/service/rest/GreenTourService/areaBasedList?serviceKey=QrLj7VbQShOJrUXBZpBkKF7hD5P8AixlwRQDy4QklL0m%2F1%2B57y4Q3QJzORuAne7sGPITPaEQtFPH5htq8cWXNQ%3D%3D&numOfRows=20&pageSize=20&pageNo=1& arrange=C&MobileOS=ETC&MobileApp=AppTest&areaCode=33"
        url34 = "http://api.visitkorea.or.kr/openapi/service/rest/GreenTourService/areaBasedList?serviceKey=QrLj7VbQShOJrUXBZpBkKF7hD5P8AixlwRQDy4QklL0m%2F1%2B57y4Q3QJzORuAne7sGPITPaEQtFPH5htq8cWXNQ%3D%3D&numOfRows=20&pageSize=20&pageNo=1& arrange=C&MobileOS=ETC&MobileApp=AppTest&areaCode=34"
        url35 = "http://api.visitkorea.or.kr/openapi/service/rest/GreenTourService/areaBasedList?serviceKey=QrLj7VbQShOJrUXBZpBkKF7hD5P8AixlwRQDy4QklL0m%2F1%2B57y4Q3QJzORuAne7sGPITPaEQtFPH5htq8cWXNQ%3D%3D&numOfRows=20&pageSize=20&pageNo=1& arrange=C&MobileOS=ETC&MobileApp=AppTest&areaCode=35"
        url36 = "http://api.visitkorea.or.kr/openapi/service/rest/GreenTourService/areaBasedList?serviceKey=QrLj7VbQShOJrUXBZpBkKF7hD5P8AixlwRQDy4QklL0m%2F1%2B57y4Q3QJzORuAne7sGPITPaEQtFPH5htq8cWXNQ%3D%3D&numOfRows=20&pageSize=20&pageNo=1& arrange=C&MobileOS=ETC&MobileApp=AppTest&areaCode=36"
        url37 = "http://api.visitkorea.or.kr/openapi/service/rest/GreenTourService/areaBasedList?serviceKey=QrLj7VbQShOJrUXBZpBkKF7hD5P8AixlwRQDy4QklL0m%2F1%2B57y4Q3QJzORuAne7sGPITPaEQtFPH5htq8cWXNQ%3D%3D&numOfRows=20&pageSize=20&pageNo=1& arrange=C&MobileOS=ETC&MobileApp=AppTest&areaCode=37"
        url38 = "http://api.visitkorea.or.kr/openapi/service/rest/GreenTourService/areaBasedList?serviceKey=QrLj7VbQShOJrUXBZpBkKF7hD5P8AixlwRQDy4QklL0m%2F1%2B57y4Q3QJzORuAne7sGPITPaEQtFPH5htq8cWXNQ%3D%3D&numOfRows=20&pageSize=20&pageNo=1& arrange=C&MobileOS=ETC&MobileApp=AppTest&areaCode=38"
        url39 = "http://api.visitkorea.or.kr/openapi/service/rest/GreenTourService/areaBasedList?serviceKey=QrLj7VbQShOJrUXBZpBkKF7hD5P8AixlwRQDy4QklL0m%2F1%2B57y4Q3QJzORuAne7sGPITPaEQtFPH5htq8cWXNQ%3D%3D&numOfRows=20&pageSize=20&pageNo=1& arrange=C&MobileOS=ETC&MobileApp=AppTest&areaCode=39"


        savename1="../TermProject/TourService2-1.xml"
        savename2="../TermProject/TourService2-2.xml"
        savename3="../TermProject/TourService2-3.xml"
        savename4="../TermProject/TourService2-4.xml"
        savename6="../TermProject/TourService2-6.xml"
        savename7="../TermProject/TourService2-7.xml"
        savename31="../TermProject/TourService2-31.xml"
        savename32="../TermProject/TourService2-32.xml"
        savename33="../TermProject/TourService2-33.xml"
        savename34="../TermProject/TourService2-34.xml"
        savename35="../TermProject/TourService2-35.xml"
        savename36="../TermProject/TourService2-36.xml"
        savename37="../TermProject/TourService2-37.xml"
        savename38="../TermProject/TourService2-38.xml"
        savename39="../TermProject/TourService2-39.xml"


        if not os.path.exists(savename1):
            req.urlretrieve(url1, savename1)
        if not os.path.exists(savename2):
            req.urlretrieve(url2, savename2)
        if not os.path.exists(savename3):
            req.urlretrieve(url3, savename3)
        if not os.path.exists(savename4):
            req.urlretrieve(url4, savename4)
        if not os.path.exists(savename6):
            req.urlretrieve(url6, savename6)
        if not os.path.exists(savename7):
            req.urlretrieve(url7, savename7)
        if not os.path.exists(savename31):
            req.urlretrieve(url31, savename31)
        if not os.path.exists(savename32):
            req.urlretrieve(url32, savename32)
        if not os.path.exists(savename33):
            req.urlretrieve(url33, savename33)
        if not os.path.exists(savename34):
            req.urlretrieve(url34, savename34)
        if not os.path.exists(savename35):
            req.urlretrieve(url35, savename35)
        if not os.path.exists(savename36):
            req.urlretrieve(url36, savename36)
        if not os.path.exists(savename37):
            req.urlretrieve(url37, savename37)
        if not os.path.exists(savename38):
            req.urlretrieve(url38, savename38)
        if not os.path.exists(savename39):
            req.urlretrieve(url39, savename39)

        #BeautifulSoup 파싱
        xml1=open(savename1, 'r', encoding="utf-8").read()
        soup1 = BeautifulSoup(xml1, 'html.parser')
        xml2=open(savename2, 'r', encoding="utf-8").read()
        soup2 = BeautifulSoup(xml2, 'html.parser')
        xml3=open(savename3, 'r', encoding="utf-8").read()
        soup3 = BeautifulSoup(xml3, 'html.parser')
        xml4=open(savename4, 'r', encoding="utf-8").read()
        soup4 = BeautifulSoup(xml4, 'html.parser')
        xml6=open(savename6, 'r', encoding="utf-8").read()
        soup6 = BeautifulSoup(xml6, 'html.parser')
        xml7=open(savename7, 'r', encoding="utf-8").read()
        soup7 = BeautifulSoup(xml7, 'html.parser')
        xml31=open(savename31, 'r', encoding="utf-8").read()
        soup31 = BeautifulSoup(xml31, 'html.parser')
        xml32=open(savename32, 'r', encoding="utf-8").read()
        soup32 = BeautifulSoup(xml32, 'html.parser')
        xml33=open(savename33, 'r', encoding="utf-8").read()
        soup33 = BeautifulSoup(xml33, 'html.parser')
        xml34=open(savename34, 'r', encoding="utf-8").read()
        soup34 = BeautifulSoup(xml34, 'html.parser')
        xml35=open(savename35, 'r', encoding="utf-8").read()
        soup35 = BeautifulSoup(xml35, 'html.parser')
        xml36=open(savename36, 'r', encoding="utf-8").read()
        soup36 = BeautifulSoup(xml36, 'html.parser')
        xml37=open(savename37, 'r', encoding="utf-8").read()
        soup37 = BeautifulSoup(xml37, 'html.parser')
        xml38=open(savename38, 'r', encoding="utf-8").read()
        soup38 = BeautifulSoup(xml38, 'html.parser')
        xml39=open(savename39, 'r', encoding="utf-8").read()
        soup39 = BeautifulSoup(xml39, 'html.parser')


        if self.comboBox.currentIndex()==1:
            for i in soup1.find_all('item'):
                title=i.find("title").string
                addr=i.find("addr").string
                summary=i.find("summary").string
                tel=i.find("tel").string
                telname=i.find("telname").string
                mainimage=i.find("mainimage")
                mainimage=str(mainimage)
                if len(mainimage) is not 4:
                    mainimage=mainimage[11:]
                    mainimage=mainimage[:-12]


                if self.comboBox_2.currentText()==title:
                    self.plainTextEdit_3.appendPlainText("-----------------------------------")
                    self.plainTextEdit_3.appendPlainText("<"+title+">")
                    self.plainTextEdit_3.appendPlainText(addr)
                    self.plainTextEdit_3.appendPlainText(summary)
                    self.plainTextEdit_3.appendPlainText(tel)
                    self.plainTextEdit_3.appendPlainText(telname)
                    self.plainTextEdit_3.appendPlainText(mainimage)
                    self.plainTextEdit_3.appendPlainText("-----------------------------------")
                    self.plainTextEdit_3.appendPlainText("\n")
                    self.comboBox_2.currentIndexChanged.connect(self.clearInfo)
                    if len(mainimage) is not 4:
                        req.urlretrieve(mainimage,'../TermProject/resource/image.jpg')
                        self.label_5.setPixmap(QPixmap('../TermProject/resource/image.jpg').scaled(341,281,Qt.KeepAspectRatio, Qt.FastTransformation))
                    else:
                        self.label_5.setPixmap(QPixmap('../TermProject/resource/no_image.png'))



        if self.comboBox.currentIndex()==2:
            for i in soup2.find_all('item'):
                title=i.find("title").string
                addr=i.find("addr").string
                summary=i.find("summary").string
                tel=i.find("tel").string
                telname=i.find("telname").string
                mainimage=i.find("mainimage")
                mainimage=str(mainimage)
                if len(mainimage) is not 4:
                    mainimage=mainimage[11:]
                    mainimage=mainimage[:-12]

                if self.comboBox_2.currentText()==title:
                    self.plainTextEdit_3.appendPlainText("-----------------------------------")
                    self.plainTextEdit_3.appendPlainText("<"+title+">")
                    self.plainTextEdit_3.appendPlainText(addr)
                    self.plainTextEdit_3.appendPlainText(summary)
                    self.plainTextEdit_3.appendPlainText(tel)
                    self.plainTextEdit_3.appendPlainText(telname)
                    self.plainTextEdit_3.appendPlainText(mainimage)
                    self.plainTextEdit_3.appendPlainText("-----------------------------------")
                    self.plainTextEdit_3.appendPlainText("\n")
                    self.comboBox_2.currentIndexChanged.connect(self.clearInfo)
                    if len(mainimage) is not 4:
                        req.urlretrieve(mainimage,'../TermProject/resource/image.jpg')
                        self.label_5.setPixmap(QPixmap('../TermProject/resource/image.jpg').scaled(341,281,Qt.KeepAspectRatio, Qt.FastTransformation))
                    else:
                        self.label_5.setPixmap(QPixmap('../TermProject/resource/no_image.png'))


        if self.comboBox.currentIndex()==3:
            for i in soup3.find_all('item'):
                title=i.find("title").string
                addr=i.find("addr").string
                summary=i.find("summary").string
                tel=i.find("tel").string
                telname=i.find("telname").string
                mainimage=i.find("mainimage")
                mainimage=str(mainimage)
                if len(mainimage) is not 4:
                    mainimage=mainimage[11:]
                    mainimage=mainimage[:-12]

                if self.comboBox_2.currentText()==title:
                    self.plainTextEdit_3.appendPlainText("-----------------------------------")
                    self.plainTextEdit_3.appendPlainText("<"+title+">")
                    self.plainTextEdit_3.appendPlainText(addr)
                    self.plainTextEdit_3.appendPlainText(summary)
                    self.plainTextEdit_3.appendPlainText(tel)
                    self.plainTextEdit_3.appendPlainText(telname)
                    self.plainTextEdit_3.appendPlainText(mainimage)
                    self.plainTextEdit_3.appendPlainText("-----------------------------------")
                    self.plainTextEdit_3.appendPlainText("\n")
                    self.comboBox_2.currentIndexChanged.connect(self.clearInfo)
                    if len(mainimage) is not 4:
                        req.urlretrieve(mainimage,'../TermProject/resource/image.jpg')
                        self.label_5.setPixmap(QPixmap('../TermProject/resource/image.jpg').scaled(341,281,Qt.KeepAspectRatio, Qt.FastTransformation))
                    else:
                        self.label_5.setPixmap(QPixmap('../TermProject/resource/no_image.png'))



        if self.comboBox.currentIndex()==4:
            for i in soup4.find_all('item'):
                title=i.find("title").string
                addr=i.find("addr").string
                summary=i.find("summary").string
                tel=i.find("tel").string
                telname=i.find("telname").string
                mainimage=i.find("mainimage")
                mainimage=str(mainimage)
                if len(mainimage) is not 4:
                    mainimage=mainimage[11:]
                    mainimage=mainimage[:-12]

                if self.comboBox_2.currentText()==title:
                    self.plainTextEdit_3.appendPlainText("-----------------------------------")
                    self.plainTextEdit_3.appendPlainText("<"+title+">")
                    self.plainTextEdit_3.appendPlainText(addr)
                    self.plainTextEdit_3.appendPlainText(summary)
                    self.plainTextEdit_3.appendPlainText(tel)
                    self.plainTextEdit_3.appendPlainText(telname)
                    self.plainTextEdit_3.appendPlainText(mainimage)
                    self.plainTextEdit_3.appendPlainText("-----------------------------------")
                    self.plainTextEdit_3.appendPlainText("\n")
                    self.comboBox_2.currentIndexChanged.connect(self.clearInfo)
                    if len(mainimage) is not 4:
                        req.urlretrieve(mainimage,'../TermProject/resource/image.jpg')
                        self.label_5.setPixmap(QPixmap('../TermProject/resource/image.jpg').scaled(341,281,Qt.KeepAspectRatio, Qt.FastTransformation))
                    else:
                        self.label_5.setPixmap(QPixmap('../TermProject/resource/no_image.png'))


        if self.comboBox.currentIndex()==5:
            for i in soup6.find_all('item'):
                title=i.find("title").string
                addr=i.find("addr").string
                summary=i.find("summary").string
                tel=i.find("tel").string
                telname=i.find("telname").string
                mainimage=i.find("mainimage")
                mainimage=str(mainimage)
                if len(mainimage) is not 4:
                    mainimage=mainimage[11:]
                    mainimage=mainimage[:-12]

                if self.comboBox_2.currentText()==title:
                    self.plainTextEdit_3.appendPlainText("-----------------------------------")
                    self.plainTextEdit_3.appendPlainText("<"+title+">")
                    self.plainTextEdit_3.appendPlainText(addr)
                    self.plainTextEdit_3.appendPlainText(summary)
                    self.plainTextEdit_3.appendPlainText(tel)
                    self.plainTextEdit_3.appendPlainText(telname)
                    self.plainTextEdit_3.appendPlainText(mainimage)
                    self.plainTextEdit_3.appendPlainText("-----------------------------------")
                    self.plainTextEdit_3.appendPlainText("\n")
                    self.comboBox_2.currentIndexChanged.connect(self.clearInfo)
                    if len(mainimage) is not 4:
                        req.urlretrieve(mainimage,'../TermProject/resource/image.jpg')
                        self.label_5.setPixmap(QPixmap('../TermProject/resource/image.jpg').scaled(341,281,Qt.KeepAspectRatio, Qt.FastTransformation))
                    else:
                        self.label_5.setPixmap(QPixmap('../TermProject/resource/no_image.png'))



        if self.comboBox.currentIndex()==6:
            for i in soup7.find_all('item'):
                title=i.find("title").string
                addr=i.find("addr").string
                summary=i.find("summary").string
                tel=i.find("tel").string
                telname=i.find("telname").string
                mainimage=i.find("mainimage")
                mainimage=str(mainimage)
                if len(mainimage) is not 4:
                    mainimage=mainimage[11:]
                    mainimage=mainimage[:-12]

                if self.comboBox_2.currentText()==title:
                    self.plainTextEdit_3.appendPlainText("-----------------------------------")
                    self.plainTextEdit_3.appendPlainText("<"+title+">")
                    self.plainTextEdit_3.appendPlainText(addr)
                    self.plainTextEdit_3.appendPlainText(summary)
                    self.plainTextEdit_3.appendPlainText(tel)
                    self.plainTextEdit_3.appendPlainText(telname)
                    self.plainTextEdit_3.appendPlainText(mainimage)
                    self.plainTextEdit_3.appendPlainText("-----------------------------------")
                    self.plainTextEdit_3.appendPlainText("\n")
                    self.comboBox_2.currentIndexChanged.connect(self.clearInfo)
                    if len(mainimage) is not 4:
                        req.urlretrieve(mainimage,'../TermProject/resource/image.jpg')
                        self.label_5.setPixmap(QPixmap('../TermProject/resource/image.jpg').scaled(341,281,Qt.KeepAspectRatio, Qt.FastTransformation))
                    else:
                        self.label_5.setPixmap(QPixmap('../TermProject/resource/no_image.png'))


        if self.comboBox.currentIndex()==7:
            for i in soup31.find_all('item'):
                title=i.find("title").string
                addr=i.find("addr").string
                summary=i.find("summary").string
                tel=i.find("tel")
                tel=str(tel)
                telname=i.find("telname")
                telname=str(telname)
                mainimage=i.find("mainimage")
                mainimage=str(mainimage)
                if len(mainimage) is not 4:
                    mainimage=mainimage[11:]
                    mainimage=mainimage[:-12]

                if self.comboBox_2.currentText()==title:
                    self.plainTextEdit_3.appendPlainText("-----------------------------------")
                    self.plainTextEdit_3.appendPlainText("<"+title+">")
                    self.plainTextEdit_3.appendPlainText(addr)
                    self.plainTextEdit_3.appendPlainText(summary)
                    self.plainTextEdit_3.appendPlainText(tel)
                    self.plainTextEdit_3.appendPlainText(telname)
                    self.plainTextEdit_3.appendPlainText(mainimage)
                    self.plainTextEdit_3.appendPlainText("-----------------------------------")
                    self.plainTextEdit_3.appendPlainText("\n")
                    self.comboBox_2.currentIndexChanged.connect(self.clearInfo)
                    if len(mainimage) is not 4:
                        req.urlretrieve(mainimage,'../TermProject/resource/image.jpg')
                        self.label_5.setPixmap(QPixmap('../TermProject/resource/image.jpg').scaled(341,281,Qt.KeepAspectRatio, Qt.FastTransformation))
                    else:
                        self.label_5.setPixmap(QPixmap('../TermProject/resource/no_image.png'))



        if self.comboBox.currentIndex()==8:
            for i in soup32.find_all('item'):
                title=i.find("title").string
                addr=i.find("addr").string
                summary=i.find("summary").string
                tel=i.find("tel").string
                telname=i.find("telname").string
                mainimage=i.find("mainimage")
                mainimage=str(mainimage)
                if len(mainimage) is not 4:
                    mainimage=mainimage[11:]
                    mainimage=mainimage[:-12]

                if self.comboBox_2.currentText()==title:
                    self.plainTextEdit_3.appendPlainText("-----------------------------------")
                    self.plainTextEdit_3.appendPlainText("<"+title+">")
                    self.plainTextEdit_3.appendPlainText(addr)
                    self.plainTextEdit_3.appendPlainText(summary)
                    self.plainTextEdit_3.appendPlainText(tel)
                    self.plainTextEdit_3.appendPlainText(telname)
                    self.plainTextEdit_3.appendPlainText(mainimage)
                    self.plainTextEdit_3.appendPlainText("-----------------------------------")
                    self.plainTextEdit_3.appendPlainText("\n")
                    self.comboBox_2.currentIndexChanged.connect(self.clearInfo)
                    if len(mainimage) is not 4:
                        req.urlretrieve(mainimage,'../TermProject/resource/image.jpg')
                        self.label_5.setPixmap(QPixmap('../TermProject/resource/image.jpg').scaled(341,281,Qt.KeepAspectRatio, Qt.FastTransformation))
                    else:
                        self.label_5.setPixmap(QPixmap('../TermProject/resource/no_image.png'))


        if self.comboBox.currentIndex()==9:
            for i in soup33.find_all('item'):
                title=i.find("title").string
                addr=i.find("addr").string
                summary=i.find("summary").string
                tel=i.find("tel").string
                telname=i.find("telname").string
                mainimage=i.find("mainimage")
                mainimage=str(mainimage)
                if len(mainimage) is not 4:
                    mainimage=mainimage[11:]
                    mainimage=mainimage[:-12]

                if self.comboBox_2.currentText()==title:
                    self.plainTextEdit_3.appendPlainText("-----------------------------------")
                    self.plainTextEdit_3.appendPlainText("<"+title+">")
                    self.plainTextEdit_3.appendPlainText(addr)
                    self.plainTextEdit_3.appendPlainText(summary)
                    self.plainTextEdit_3.appendPlainText(tel)
                    self.plainTextEdit_3.appendPlainText(telname)
                    self.plainTextEdit_3.appendPlainText(mainimage)
                    self.plainTextEdit_3.appendPlainText("-----------------------------------")
                    self.plainTextEdit_3.appendPlainText("\n")
                    self.comboBox_2.currentIndexChanged.connect(self.clearInfo)
                    if len(mainimage) is not 4:
                        req.urlretrieve(mainimage,'../TermProject/resource/image.jpg')
                        self.label_5.setPixmap(QPixmap('../TermProject/resource/image.jpg').scaled(341,281,Qt.KeepAspectRatio, Qt.FastTransformation))
                    else:
                        self.label_5.setPixmap(QPixmap('../TermProject/resource/no_image.png'))



        if self.comboBox.currentIndex()==10:
            for i in soup34.find_all('item'):
                title=i.find("title").string
                addr=i.find("addr").string
                summary=i.find("summary").string
                tel=i.find("tel").string
                telname=i.find("telname").string
                mainimage=i.find("mainimage")
                mainimage=str(mainimage)
                if len(mainimage) is not 4:
                    mainimage=mainimage[11:]
                    mainimage=mainimage[:-12]

                if self.comboBox_2.currentText()==title:
                    self.plainTextEdit_3.appendPlainText("-----------------------------------")
                    self.plainTextEdit_3.appendPlainText("<"+title+">")
                    self.plainTextEdit_3.appendPlainText(addr)
                    self.plainTextEdit_3.appendPlainText(summary)
                    self.plainTextEdit_3.appendPlainText(tel)
                    self.plainTextEdit_3.appendPlainText(telname)
                    self.plainTextEdit_3.appendPlainText(mainimage)
                    self.plainTextEdit_3.appendPlainText("-----------------------------------")
                    self.plainTextEdit_3.appendPlainText("\n")
                    self.comboBox_2.currentIndexChanged.connect(self.clearInfo)
                    if len(mainimage) is not 4:
                        req.urlretrieve(mainimage,'../TermProject/resource/image.jpg')
                        self.label_5.setPixmap(QPixmap('../TermProject/resource/image.jpg').scaled(341,281,Qt.KeepAspectRatio, Qt.FastTransformation))
                    else:
                        self.label_5.setPixmap(QPixmap('../TermProject/resource/no_image.png'))



        if self.comboBox.currentIndex()==11:
            for i in soup35.find_all('item'):
                title=i.find("title").string
                addr=i.find("addr").string
                summary=i.find("summary").string
                tel=i.find("tel")
                tel=str(tel)
                telname=i.find("telname")
                telname=str(telname)
                mainimage=i.find("mainimage")
                mainimage=str(mainimage)
                if len(mainimage) is not 4:
                    mainimage=mainimage[11:]
                    mainimage=mainimage[:-12]

                if self.comboBox_2.currentText()==title:
                    self.plainTextEdit_3.appendPlainText("-----------------------------------")
                    self.plainTextEdit_3.appendPlainText("<"+title+">")
                    self.plainTextEdit_3.appendPlainText(addr)
                    self.plainTextEdit_3.appendPlainText(summary)
                    self.plainTextEdit_3.appendPlainText(tel)
                    self.plainTextEdit_3.appendPlainText(telname)
                    self.plainTextEdit_3.appendPlainText(mainimage)
                    self.plainTextEdit_3.appendPlainText("-----------------------------------")
                    self.plainTextEdit_3.appendPlainText("\n")
                    self.comboBox_2.currentIndexChanged.connect(self.clearInfo)
                    if len(mainimage) is not 4:
                        req.urlretrieve(mainimage,'../TermProject/resource/image.jpg')
                        self.label_5.setPixmap(QPixmap('../TermProject/resource/image.jpg').scaled(341,281,Qt.KeepAspectRatio, Qt.FastTransformation))
                    else:
                        self.label_5.setPixmap(QPixmap('../TermProject/resource/no_image.png'))



        if self.comboBox.currentIndex()==12:
            for i in soup36.find_all('item'):
                title=i.find("title").string
                addr=i.find("addr").string
                summary=i.find("summary").string
                tel=i.find("tel").string
                telname=i.find("telname").string
                mainimage=i.find("mainimage")
                mainimage=str(mainimage)
                if len(mainimage) is not 4:
                    mainimage=mainimage[11:]
                    mainimage=mainimage[:-12]

                if self.comboBox_2.currentText()==title:
                    self.plainTextEdit_3.appendPlainText("-----------------------------------")
                    self.plainTextEdit_3.appendPlainText("<"+title+">")
                    self.plainTextEdit_3.appendPlainText(addr)
                    self.plainTextEdit_3.appendPlainText(summary)
                    self.plainTextEdit_3.appendPlainText(tel)
                    self.plainTextEdit_3.appendPlainText(telname)
                    self.plainTextEdit_3.appendPlainText(mainimage)
                    self.plainTextEdit_3.appendPlainText("-----------------------------------")
                    self.plainTextEdit_3.appendPlainText("\n")
                    self.comboBox_2.currentIndexChanged.connect(self.clearInfo)
                    if len(mainimage) is not 4:
                        req.urlretrieve(mainimage,'../TermProject/resource/image.jpg')
                        self.label_5.setPixmap(QPixmap('../TermProject/resource/image.jpg').scaled(341,281,Qt.KeepAspectRatio, Qt.FastTransformation))
                    else:
                        self.label_5.setPixmap(QPixmap('../TermProject/resource/no_image.png'))



        if self.comboBox.currentIndex()==13:
            for i in soup37.find_all('item'):
                title=i.find("title").string
                addr=i.find("addr").string
                summary=i.find("summary").string
                tel=i.find("tel").string
                telname=i.find("telname").string
                mainimage=i.find("mainimage")
                mainimage=str(mainimage)
                if len(mainimage) is not 4:
                    mainimage=mainimage[11:]
                    mainimage=mainimage[:-12]

                if self.comboBox_2.currentText()==title:
                    self.plainTextEdit_3.appendPlainText("-----------------------------------")
                    self.plainTextEdit_3.appendPlainText("<"+title+">")
                    self.plainTextEdit_3.appendPlainText(addr)
                    self.plainTextEdit_3.appendPlainText(summary)
                    self.plainTextEdit_3.appendPlainText(tel)
                    self.plainTextEdit_3.appendPlainText(telname)
                    self.plainTextEdit_3.appendPlainText(mainimage)
                    self.plainTextEdit_3.appendPlainText("-----------------------------------")
                    self.plainTextEdit_3.appendPlainText("\n")
                    self.comboBox_2.currentIndexChanged.connect(self.clearInfo)
                    if len(mainimage) is not 4:
                        req.urlretrieve(mainimage,'../TermProject/resource/image.jpg')
                        self.label_5.setPixmap(QPixmap('../TermProject/resource/image.jpg').scaled(341,281,Qt.KeepAspectRatio, Qt.FastTransformation))
                    else:
                        self.label_5.setPixmap(QPixmap('../TermProject/resource/no_image.png'))



        if self.comboBox.currentIndex()==14:
            for i in soup38.find_all('item'):
                title=i.find("title").string
                addr=i.find("addr").string
                summary=i.find("summary").string
                tel=i.find("tel").string
                telname=i.find("telname").string
                mainimage=i.find("mainimage")
                mainimage=str(mainimage)
                if len(mainimage) is not 4:
                    mainimage=mainimage[11:]
                    mainimage=mainimage[:-12]

                if self.comboBox_2.currentText()==title:
                    self.plainTextEdit_3.appendPlainText("-----------------------------------")
                    self.plainTextEdit_3.appendPlainText("<"+title+">")
                    self.plainTextEdit_3.appendPlainText(addr)
                    self.plainTextEdit_3.appendPlainText(summary)
                    self.plainTextEdit_3.appendPlainText(tel)
                    self.plainTextEdit_3.appendPlainText(telname)
                    self.plainTextEdit_3.appendPlainText(mainimage)
                    self.plainTextEdit_3.appendPlainText("-----------------------------------")
                    self.plainTextEdit_3.appendPlainText("\n")
                    self.comboBox_2.currentIndexChanged.connect(self.clearInfo)
                    if len(mainimage) is not 4:
                        req.urlretrieve(mainimage,'../TermProject/resource/image.jpg')
                        self.label_5.setPixmap(QPixmap('../TermProject/resource/image.jpg').scaled(341,281,Qt.KeepAspectRatio, Qt.FastTransformation))
                    else:
                        self.label_5.setPixmap(QPixmap('../TermProject/resource/no_image.png'))



        if self.comboBox.currentIndex()==15:
            for i in soup39.find_all('item'):
                title=i.find("title").string
                addr=i.find("addr").string
                summary=i.find("summary").string
                tel=i.find("tel").string
                telname=i.find("telname").string
                mainimage=i.find("mainimage")
                mainimage=str(mainimage)
                if len(mainimage) is not 4:
                    mainimage=mainimage[11:]
                    mainimage=mainimage[:-12]

                if self.comboBox_2.currentText()==title:
                    self.plainTextEdit_3.appendPlainText("-----------------------------------")
                    self.plainTextEdit_3.appendPlainText("<"+title+">")
                    self.plainTextEdit_3.appendPlainText(addr)
                    self.plainTextEdit_3.appendPlainText(summary)
                    self.plainTextEdit_3.appendPlainText(tel)
                    self.plainTextEdit_3.appendPlainText(telname)
                    self.plainTextEdit_3.appendPlainText(mainimage)
                    self.plainTextEdit_3.appendPlainText("-----------------------------------")
                    self.plainTextEdit_3.appendPlainText("\n")
                    self.comboBox_2.currentIndexChanged.connect(self.clearInfo)
                    if len(mainimage) is not 4:
                        req.urlretrieve(mainimage,'../TermProject/resource/image.jpg')
                        self.label_5.setPixmap(QPixmap('../TermProject/resource/image.jpg').scaled(341,281,Qt.KeepAspectRatio, Qt.FastTransformation))
                    else:
                        self.label_5.setPixmap(QPixmap('../TermProject/resource/no_image.png'))



    def clearInfo(self):
        self.plainTextEdit_3.clear()
        self.label_5.clear()


    @pyqtSlot()
    def extractPlace(self):
        sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

        url1 = "http://api.visitkorea.or.kr/openapi/service/rest/GreenTourService/areaBasedList?serviceKey=QrLj7VbQShOJrUXBZpBkKF7hD5P8AixlwRQDy4QklL0m%2F1%2B57y4Q3QJzORuAne7sGPITPaEQtFPH5htq8cWXNQ%3D%3D&numOfRows=20&pageSize=20&pageNo=1& arrange=C&MobileOS=ETC&MobileApp=AppTest&areaCode=1"
        url2 = "http://api.visitkorea.or.kr/openapi/service/rest/GreenTourService/areaBasedList?serviceKey=QrLj7VbQShOJrUXBZpBkKF7hD5P8AixlwRQDy4QklL0m%2F1%2B57y4Q3QJzORuAne7sGPITPaEQtFPH5htq8cWXNQ%3D%3D&numOfRows=20&pageSize=20&pageNo=1& arrange=C&MobileOS=ETC&MobileApp=AppTest&areaCode=2"
        url3 = "http://api.visitkorea.or.kr/openapi/service/rest/GreenTourService/areaBasedList?serviceKey=QrLj7VbQShOJrUXBZpBkKF7hD5P8AixlwRQDy4QklL0m%2F1%2B57y4Q3QJzORuAne7sGPITPaEQtFPH5htq8cWXNQ%3D%3D&numOfRows=20&pageSize=20&pageNo=1& arrange=C&MobileOS=ETC&MobileApp=AppTest&areaCode=3"
        url4 = "http://api.visitkorea.or.kr/openapi/service/rest/GreenTourService/areaBasedList?serviceKey=QrLj7VbQShOJrUXBZpBkKF7hD5P8AixlwRQDy4QklL0m%2F1%2B57y4Q3QJzORuAne7sGPITPaEQtFPH5htq8cWXNQ%3D%3D&numOfRows=20&pageSize=20&pageNo=1& arrange=C&MobileOS=ETC&MobileApp=AppTest&areaCode=4"
        url6 = "http://api.visitkorea.or.kr/openapi/service/rest/GreenTourService/areaBasedList?serviceKey=QrLj7VbQShOJrUXBZpBkKF7hD5P8AixlwRQDy4QklL0m%2F1%2B57y4Q3QJzORuAne7sGPITPaEQtFPH5htq8cWXNQ%3D%3D&numOfRows=20&pageSize=20&pageNo=1& arrange=C&MobileOS=ETC&MobileApp=AppTest&areaCode=6"
        url7 = "http://api.visitkorea.or.kr/openapi/service/rest/GreenTourService/areaBasedList?serviceKey=QrLj7VbQShOJrUXBZpBkKF7hD5P8AixlwRQDy4QklL0m%2F1%2B57y4Q3QJzORuAne7sGPITPaEQtFPH5htq8cWXNQ%3D%3D&numOfRows=20&pageSize=20&pageNo=1& arrange=C&MobileOS=ETC&MobileApp=AppTest&areaCode=7"
        url31 = "http://api.visitkorea.or.kr/openapi/service/rest/GreenTourService/areaBasedList?serviceKey=QrLj7VbQShOJrUXBZpBkKF7hD5P8AixlwRQDy4QklL0m%2F1%2B57y4Q3QJzORuAne7sGPITPaEQtFPH5htq8cWXNQ%3D%3D&numOfRows=20&pageSize=20&pageNo=1& arrange=C&MobileOS=ETC&MobileApp=AppTest&areaCode=31"
        url32 = "http://api.visitkorea.or.kr/openapi/service/rest/GreenTourService/areaBasedList?serviceKey=QrLj7VbQShOJrUXBZpBkKF7hD5P8AixlwRQDy4QklL0m%2F1%2B57y4Q3QJzORuAne7sGPITPaEQtFPH5htq8cWXNQ%3D%3D&numOfRows=20&pageSize=20&pageNo=1& arrange=C&MobileOS=ETC&MobileApp=AppTest&areaCode=32"
        url33 = "http://api.visitkorea.or.kr/openapi/service/rest/GreenTourService/areaBasedList?serviceKey=QrLj7VbQShOJrUXBZpBkKF7hD5P8AixlwRQDy4QklL0m%2F1%2B57y4Q3QJzORuAne7sGPITPaEQtFPH5htq8cWXNQ%3D%3D&numOfRows=20&pageSize=20&pageNo=1& arrange=C&MobileOS=ETC&MobileApp=AppTest&areaCode=33"
        url34 = "http://api.visitkorea.or.kr/openapi/service/rest/GreenTourService/areaBasedList?serviceKey=QrLj7VbQShOJrUXBZpBkKF7hD5P8AixlwRQDy4QklL0m%2F1%2B57y4Q3QJzORuAne7sGPITPaEQtFPH5htq8cWXNQ%3D%3D&numOfRows=20&pageSize=20&pageNo=1& arrange=C&MobileOS=ETC&MobileApp=AppTest&areaCode=34"
        url35 = "http://api.visitkorea.or.kr/openapi/service/rest/GreenTourService/areaBasedList?serviceKey=QrLj7VbQShOJrUXBZpBkKF7hD5P8AixlwRQDy4QklL0m%2F1%2B57y4Q3QJzORuAne7sGPITPaEQtFPH5htq8cWXNQ%3D%3D&numOfRows=20&pageSize=20&pageNo=1& arrange=C&MobileOS=ETC&MobileApp=AppTest&areaCode=35"
        url36 = "http://api.visitkorea.or.kr/openapi/service/rest/GreenTourService/areaBasedList?serviceKey=QrLj7VbQShOJrUXBZpBkKF7hD5P8AixlwRQDy4QklL0m%2F1%2B57y4Q3QJzORuAne7sGPITPaEQtFPH5htq8cWXNQ%3D%3D&numOfRows=20&pageSize=20&pageNo=1& arrange=C&MobileOS=ETC&MobileApp=AppTest&areaCode=36"
        url37 = "http://api.visitkorea.or.kr/openapi/service/rest/GreenTourService/areaBasedList?serviceKey=QrLj7VbQShOJrUXBZpBkKF7hD5P8AixlwRQDy4QklL0m%2F1%2B57y4Q3QJzORuAne7sGPITPaEQtFPH5htq8cWXNQ%3D%3D&numOfRows=20&pageSize=20&pageNo=1& arrange=C&MobileOS=ETC&MobileApp=AppTest&areaCode=37"
        url38 = "http://api.visitkorea.or.kr/openapi/service/rest/GreenTourService/areaBasedList?serviceKey=QrLj7VbQShOJrUXBZpBkKF7hD5P8AixlwRQDy4QklL0m%2F1%2B57y4Q3QJzORuAne7sGPITPaEQtFPH5htq8cWXNQ%3D%3D&numOfRows=20&pageSize=20&pageNo=1& arrange=C&MobileOS=ETC&MobileApp=AppTest&areaCode=38"
        url39 = "http://api.visitkorea.or.kr/openapi/service/rest/GreenTourService/areaBasedList?serviceKey=QrLj7VbQShOJrUXBZpBkKF7hD5P8AixlwRQDy4QklL0m%2F1%2B57y4Q3QJzORuAne7sGPITPaEQtFPH5htq8cWXNQ%3D%3D&numOfRows=20&pageSize=20&pageNo=1& arrange=C&MobileOS=ETC&MobileApp=AppTest&areaCode=39"


        savename1="../TermProject/TourService2-1.xml"
        savename2="../TermProject/TourService2-2.xml"
        savename3="../TermProject/TourService2-3.xml"
        savename4="../TermProject/TourService2-4.xml"
        savename6="../TermProject/TourService2-6.xml"
        savename7="../TermProject/TourService2-7.xml"
        savename31="../TermProject/TourService2-31.xml"
        savename32="../TermProject/TourService2-32.xml"
        savename33="../TermProject/TourService2-33.xml"
        savename34="../TermProject/TourService2-34.xml"
        savename35="../TermProject/TourService2-35.xml"
        savename36="../TermProject/TourService2-36.xml"
        savename37="../TermProject/TourService2-37.xml"
        savename38="../TermProject/TourService2-38.xml"
        savename39="../TermProject/TourService2-39.xml"


        if not os.path.exists(savename1):
            req.urlretrieve(url1, savename1)
        if not os.path.exists(savename2):
            req.urlretrieve(url2, savename2)
        if not os.path.exists(savename3):
            req.urlretrieve(url3, savename3)
        if not os.path.exists(savename4):
            req.urlretrieve(url4, savename4)
        if not os.path.exists(savename6):
            req.urlretrieve(url6, savename6)
        if not os.path.exists(savename7):
            req.urlretrieve(url7, savename7)
        if not os.path.exists(savename31):
            req.urlretrieve(url31, savename31)
        if not os.path.exists(savename32):
            req.urlretrieve(url32, savename32)
        if not os.path.exists(savename33):
            req.urlretrieve(url33, savename33)
        if not os.path.exists(savename34):
            req.urlretrieve(url34, savename34)
        if not os.path.exists(savename35):
            req.urlretrieve(url35, savename35)
        if not os.path.exists(savename36):
            req.urlretrieve(url36, savename36)
        if not os.path.exists(savename37):
            req.urlretrieve(url37, savename37)
        if not os.path.exists(savename38):
            req.urlretrieve(url38, savename38)
        if not os.path.exists(savename39):
            req.urlretrieve(url39, savename39)

        #BeautifulSoup 파싱
        xml1=open(savename1, 'r', encoding="utf-8").read()
        soup1 = BeautifulSoup(xml1, 'html.parser')
        xml2=open(savename2, 'r', encoding="utf-8").read()
        soup2 = BeautifulSoup(xml2, 'html.parser')
        xml3=open(savename3, 'r', encoding="utf-8").read()
        soup3 = BeautifulSoup(xml3, 'html.parser')
        xml4=open(savename4, 'r', encoding="utf-8").read()
        soup4 = BeautifulSoup(xml4, 'html.parser')

        xml6=open(savename6, 'r', encoding="utf-8").read()
        soup6 = BeautifulSoup(xml6, 'html.parser')
        xml7=open(savename7, 'r', encoding="utf-8").read()
        soup7 = BeautifulSoup(xml7, 'html.parser')

        xml31=open(savename31, 'r', encoding="utf-8").read()
        soup31 = BeautifulSoup(xml31, 'html.parser')
        xml32=open(savename32, 'r', encoding="utf-8").read()
        soup32 = BeautifulSoup(xml32, 'html.parser')
        xml33=open(savename33, 'r', encoding="utf-8").read()
        soup33 = BeautifulSoup(xml33, 'html.parser')
        xml34=open(savename34, 'r', encoding="utf-8").read()
        soup34 = BeautifulSoup(xml34, 'html.parser')
        xml35=open(savename35, 'r', encoding="utf-8").read()
        soup35 = BeautifulSoup(xml35, 'html.parser')
        xml36=open(savename36, 'r', encoding="utf-8").read()
        soup36 = BeautifulSoup(xml36, 'html.parser')
        xml37=open(savename37, 'r', encoding="utf-8").read()
        soup37 = BeautifulSoup(xml37, 'html.parser')
        xml38=open(savename38, 'r', encoding="utf-8").read()
        soup38 = BeautifulSoup(xml38, 'html.parser')
        xml39=open(savename39, 'r', encoding="utf-8").read()
        soup39 = BeautifulSoup(xml39, 'html.parser')

        self.comboBox_2.clear()
        if self.comboBox.currentIndex()==1:
            for i in soup1.find_all('item'):
                title=i.find("title").string
                self.comboBox_2.addItem(title)

        if self.comboBox.currentIndex()==2:
            for i in soup2.find_all('item'):
                title=i.find("title").string
                self.comboBox_2.addItem(title)

        if self.comboBox.currentIndex()==3:
            for i in soup3.find_all('item'):
                title=i.find("title").string
                self.comboBox_2.addItem(title)

        if self.comboBox.currentIndex()==4:
            for i in soup4.find_all('item'):
                title=i.find("title").string
                self.comboBox_2.addItem(title)

        if self.comboBox.currentIndex()==5:
            for i in soup6.find_all('item'):
                title=i.find("title").string
                self.comboBox_2.addItem(title)

        if self.comboBox.currentIndex()==6:
            for i in soup7.find_all('item'):
                title=i.find("title").string
                self.comboBox_2.addItem(title)


        if self.comboBox.currentIndex()==7:
            for i in soup31.find_all('item'):
                title=i.find("title").string
                self.comboBox_2.addItem(title)

        if self.comboBox.currentIndex()==8:
            for i in soup32.find_all('item'):
                title=i.find("title").string
                self.comboBox_2.addItem(title)

        if self.comboBox.currentIndex()==9:
            for i in soup33.find_all('item'):
                title=i.find("title").string
                self.comboBox_2.addItem(title)

        if self.comboBox.currentIndex()==10:
            for i in soup34.find_all('item'):
                title=i.find("title").string
                self.comboBox_2.addItem(title)

        if self.comboBox.currentIndex()==11:
            for i in soup35.find_all('item'):
                title=i.find("title").string
                self.comboBox_2.addItem(title)

        if self.comboBox.currentIndex()==12:
            for i in soup36.find_all('item'):
                title=i.find("title").string
                self.comboBox_2.addItem(title)

        if self.comboBox.currentIndex()==13:
            for i in soup37.find_all('item'):
                title=i.find("title").string
                self.comboBox_2.addItem(title)

        if self.comboBox.currentIndex()==14:
            for i in soup38.find_all('item'):
                title=i.find("title").string
                self.comboBox_2.addItem(title)

        if self.comboBox.currentIndex()==15:
            for i in soup39.find_all('item'):
                title=i.find("title").string
                self.comboBox_2.addItem(title)


    def append_log_msg(self,act):
        now = datetime.datetime.now()
        nowDatetime = now.strftime("%Y-%m-%d %H:%S")
        app_msg = self.user_id + ' : ' + act + ' - (' + nowDatetime + ')'
        print(app_msg)
        self.plainTextEdit_2.appendPlainText(app_msg)

        #활동 로그 저장
        with open('../TermProject/log/log.txt','a') as f:
            f.write(app_msg+'\n')

    @pyqtSlot()
    def append_date(self):
        cur_date=self.calendarWidget.selectedDate()
        #print('click date', self.calendarWidget.selectedDate().toString())
        print(str(cur_date.year())+'-'+str(cur_date.month())+'-'+str(cur_date.day()))
        self.append_log_msg('Calender Click')

class StatusBar(QStatusBar):
    def __init__(self):
        QStatusBar.__init__(self)
        self.progress_bar = QProgressBar()
        self.addWidget(self.progress_bar)

    @pyqtSlot(int, name="setProgressValue")
    def set_progress_value(self,v):
        self.progress_bar.setValue(v)

class Form(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.init_widget()

    def init_widget(self):
        self.setWindowTitle("Korea Travel Info Homepage")
        self.toolbar=ToolBar()
        self.statusbar=StatusBar()
        self.addToolBar(self.toolbar)
        self.web=QWebEngineView()
        self.web.setUrl(QUrl("https://www.kpu.ac.kr"))
        self.setCentralWidget(self.web)
        self.web.loadProgress.connect(self.statusbar.setProgressValue)
        self.web.loadProgress.connect(lambda v: self.toolbar.changeStopReload(bool(0<=v>=100)))
        self.toolbar.backClicked.connect(self.web.back)
        self.toolbar.forwardClicked.connect(self.web.forward)
        self.toolbar.stopReloadClicked.connect(lambda v:self.web.triggerPageAction(v))
        self.toolbar.addressChanged.connect(lambda v: self.web.setUrl(QUrl(v)))
        self.setStatusBar(self.statusbar)



class ToolBar(QToolBar):
        back_button_clicked = pyqtSignal(name="backClicked")
        forward_button_clicked = pyqtSignal(name="forwardClicked")
        stop_reload_button_clicked = pyqtSignal(int, name="stopReloadClicked")
        address_changed = pyqtSignal(str, name="addressChanged")

        def __init__(self):
            QToolBar.__init__(self)
            self.setMovable(False)
            self.toggleViewAction().setEnabled(False)
            back_action=QAction(self)
            back_action.setShortcut(QKeySequence(Qt.Key_Back))
            back_action.setIcon(QIcon("../TermProject/resource/go-previous.png"))

            self.addAction(back_action)
            back_action.triggered.connect(self.back_button_clicked)

            forward_action=QAction(self)
            forward_action.setShortcut(QKeySequence(Qt.Key_Forward))
            forward_action.setIcon(QIcon("../TermProject/resource/go-next.png"))
            self.addAction(forward_action)
            forward_action.triggered.connect(self.forward_button_clicked)

            self.stop_reload_action=QAction(self)
            self.stop_reload_action.setShortcut(QKeySequence(Qt.Key_F5))
            self.stop_reload_action.setIcon(QIcon("../TermProject/resource/refresh.png"))
            self.stop_reload_action.setData(QWebEnginePage.Reload)
            self.addAction(self.stop_reload_action)
            self.stop_reload_action.triggered.connect(
            lambda: self.stop_reload_button_clicked.emit(
            QWebEnginePage.WebAction(self.stop_reload_action.data())))

            self.le = QLineEdit()
            fav_action = QAction(self)
            self.le.addAction(fav_action, QLineEdit.LeadingPosition)
            self.le.setText("http://")
            self.le.setClearButtonEnabled(True)
            self.addWidget(self.le)
            self.le.editingFinished.connect(lambda: self.address_changed.emit(self.le.text()))

        @pyqtSlot(bool, name="changeStopReload")
        def change_stop_reload(self, state):
            if state:
                self.stop_reload_action.setShortcut(QKeySequence(Qt.Key_F5))
                self.stop_reload_action.setIcon(QIcon("../TermProject/resource/refresh.png"))
                self.stop_reload_action.setData(QWebEnginePage.Reload)
            else:
                self.stop_reload_action.setShortcut(QKeySequence(Qt.Key_Escape))
                self.stop_reload_action.setIcon(QIcon("../TermProject/resource/process-stop.png"))
                self.stop_reload_action.setData(QWebEnginePage.Stop)

class EmailSender(QDialog):
    def __init__(self):
        super().__init__()
        self.setupUI()
        self.server="smtp.gmail.com"
        self.port=465
        self.id = "jjyp1108@gmail.com"
        self.pw = "ihjjlibwbpovrmrw"
        self.address=None
        self.title=None


    def setupUI(self):
        self.setGeometry(800,400,400,200)
        self.setWindowTitle("Send an E-mail")
        self.setFixedSize(400,200)

        label1 = QLabel("받는이")
        label2 = QLabel("제목")

        self.txtTo = QLineEdit() #보낼 주소 입력창
        self.txtTitle = QLineEdit() #메일 제목 입력창

        self.sendButton=QPushButton("전송")
        self.sendButton.clicked.connect(self.confirm)

        layout=QGridLayout()
        layout.addWidget(label1,0,0)
        layout.addWidget(self.txtTo,0,1)
        layout.addWidget(label2,1,0)
        layout.addWidget(self.txtTitle,1,1)
        layout.addWidget(self.sendButton,2,2)

        self.setLayout(layout)

    def confirm(self):
        self.address=self.txtTo.text()
        self.title=self.txtTitle.text()
        if self.address == ''or self.address is None or not self.address:
            QMessageBox.about(self, "전송 오류", "주소를 입력하세요.")
            self.txtTo.setFocus(True)
            return None
        if self.title == ''or self.title is None or not self.title:
            QMessageBox.about(self, "전송 오류", "제목을 입력하세요.")
            self.txtTitle.setFocus(True)
            return None
        else:
            self.address=self.txtTo.text()
            self.title=self.txtTitle.text()
            self.content = tour_main.plainTextEdit.toPlainText()

            msg = MIMEText(self.content, _charset='euc-kr')
            msg['Subject'] = self.title
            msg['From'] = self.id
            msg['To'] = self.address

            smtp1 = SMTP_SSL(self.server, self.port)
            smtp1.login(self.id, self.pw)

            smtp1.sendmail(self.id, self.address, msg.as_string())
            smtp1.quit()
            QMessageBox.about(self, "메일 전송", "전송 완료!")
            self.close()
            tour_main.append_log_msg("e-mail was sent")




if __name__ == "__main__":
    app=QApplication(sys.argv)
    tour_main=Main()
    tour_main.show()
    app.exec_()
