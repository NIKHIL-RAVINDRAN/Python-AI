import datetime
import sys
import webbrowser
import pyttsx3
import speech_recognition as sr
import wikipedia
import pywhatkit
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QTimer, QTime, QDate, Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import * 
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from newgui import Ui_myAI_GUI



engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
print(voices)
engine.setProperty('voice', voices[2].id)
engine.setProperty('rate', 180)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishes():
    hour = int(datetime.datetime.now().hour)
    if hour >=0 and hour < 12:
        speak("GOOD MORNING SIR")
    elif hour >=12 and hour<16:
        speak("GOOD AFTERNOON SIR")
    else:
        speak("GOOD EVENING SIR")
    
    speak("aaJ AAPKI KYA HELP KARU")

class MainThread(QThread):
    def __init__(self):
        super(MainThread,self).__init__()

    def run(self):
        self.taskExecution()
         

    
    def takeCommand(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening....")
            r.pause_threshold = 1
            audio = r.listen(source)

        try:
            print("Recognizing")
            query = r.recognize_google(audio,language = 'en-in')
            print(f"User said:{query}\n")

        except Exception as e:
            print("Say that again please")
            speak("SIR, please though-baara boliye")
            return "None"
        return query


    def taskExecution(self):

        while True:
            self.query = self.takeCommand().lower()
            
            if 'friday' in self.query:
                wishes()
            
            while True:
                  
                self.query = self.takeCommand().lower()

                if 'wikipedia' in self.query:
                    speak('searching wikipedia....')
                    results = wikipedia.summary(self.query, sentences = 3)
                    speak("According to Wikipedia")
                    print(results)
                    speak(results)
                
                elif 'youtube' in self.query:
                    webbrowser.open("youtube.com")

                elif 'google' in self.query:
                    webbrowser.open("google.com")

                elif 'gfg' in self.query:
                    webbrowser.open("geeksforgeeks.org")
                
                elif  'leetcode' in self.query:
                    webbrowser.open("leetcode.com")

                elif 'time' in self.query:
                    strtime = datetime.datetime.now().strftime("%H:%M")
                    speak(f" time abhi {strtime} hua hai")
                
                elif 'go to sleep friday' in self.query:
                    speak("ok sir, have a good time ahead")

startExecution = MainThread()

class Main(QMainWindow): 
    def __init__(self):
        super().__init__()
        self.ui = Ui_myAI_GUI()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)

    def startTask(self):
        self.ui.movie = QtGui.QMovie("../../Downloads/aig.gif")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("../../Downloads/init.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(20000)
        startExecution.start()

    def showTime(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        label_time = current_time.toString('hh:mm:ss')
        label_date = current_date.toString(Qt.ISODate)
        self.ui.textBrowser.setText(label_date)
        self.ui.textBrowser.setText(label_time)


app = QApplication(sys.argv)
myai = Main()
myai.show()
exit(app.exec_())