import sys

import requests

from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QPushButton, QLabel, QLineEdit

url = "http://api.fixer.io/latest?symbols={0},{1}"

currencies = ["EUR", "NOK", "USD", "MXN"]

class ConverterGUI(QWidget):

    def __init__(self):

        super().__init__()

        self.initUI()

    def initUI(self):

        # Font
        fnt1 = QtGui.QFont("Helvetica", 20)
        fnt1.setBold(True)

        # Labels
        lbl_fr = QLabel("From", self)
        lbl_to = QLabel("To", self)
        lbl_it = QLabel("Introduce amount", self)
        self.lbl_result1 = QLabel(self)
        self.lbl_result2 = QLabel(self)
        # Combo boxes
        self.cb_fr = QComboBox(self)
        self.cb_fr.addItems(currencies)
        self.cb_to = QComboBox(self)
        self.cb_to.addItems(currencies)
        # Line edit
        self.le = QLineEdit(self)
        self.le.setFocus()
        self.le.returnPressed.connect(self.convert)
        # Button 
        btn_cnvrt = QPushButton('Convert', self)
        btn_cnvrt.clicked.connect(self.convert)

        lbl_fr.move(20, 20)
        self.cb_fr.move(20, 35)
        lbl_to.move(20, 70)
        self.cb_to.move(20, 85)
        lbl_it.move(100, 20)
        self.le.move(100, 35)
        btn_cnvrt.move(100, 85)
        self.lbl_result1.move(30, 140)
        self.lbl_result2.move(30, 170)

        self.lbl_result1.resize(150, 20)
        self.lbl_result1.setFont(fnt1)
        self.lbl_result2.resize(150, 20)
        self.lbl_result2.setFont(fnt1)

        self.setGeometry(300, 200, 250, 200)
        self.setWindowTitle('Currency converter')

        self.show()

    def convert(self):

        frm = self.cb_fr.currentText()
        to = self.cb_to.currentText()

        amount = float(self.le.text())
        rate = float(getrate(frm, to))

        converted = amount*rate

        self.lbl_result1.setText('%.2f'%amount + ' ' + frm)
        self.lbl_result2.setText('%.2f'%converted + ' ' + to)

def getrate(frm, to):

    r = requests.get(url.format(frm, to))
    base = r.json()['base']

    if base == frm:
        rate = float(r.json()['rates'][to])
    elif base == to:
        rate = 1/float(r.json()['rates'][frm])
    else:
        base2frm = float(r.json()['rates'][frm])
        base2to = float(r.json()['rates'][to])
        rate = base2to/base2frm

    return rate

def main():

    app = QApplication(sys.argv)
    gui = ConverterGUI()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
