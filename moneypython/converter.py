import sys
from copy import copy

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
        fnt2 = QtGui.QFont("Helvetica", 15)

        # Labels
        lbl_fr = QLabel("From", self)
        lbl_fr.setFont(fnt2)
        lbl_to = QLabel("To", self)
        lbl_to.setFont(fnt2)
        lbl_it = QLabel("Introduce amount", self)
        lbl_it.setFont(fnt2)
        self.lbl_result1 = QLabel(self)
        self.lbl_result2 = QLabel(self)
        # Combo boxes
        self.cb_fr = QComboBox(self)
        self.cb_to = QComboBox(self)
        self.cb_fr.addItems(currencies)
        to_currencies = copy(currencies)
        to_currencies.remove(self.cb_fr.currentText())
        self.cb_to.addItems(to_currencies)
        self.cb_fr.activated.connect(self.update_cb)
        # Line edit
        self.le = QLineEdit(self)
        self.le.setFocus()
        self.le.returnPressed.connect(self.convert)
        # Button 
        btn_cnvrt = QPushButton('Convert', self)
        btn_cnvrt.clicked.connect(self.convert)

        lbl_fr.move(20, 15)
        self.cb_fr.move(20, 30)
        lbl_to.move(150, 15)
        self.cb_to.move(150, 30)
        lbl_it.move(20, 60)
        self.le.move(20, 80)
        btn_cnvrt.move(150, 75)
        self.lbl_result1.move(30, 130)
        self.lbl_result2.move(30, 160)

        self.lbl_result1.resize(250, 20)
        self.lbl_result1.setFont(fnt1)
        self.lbl_result2.resize(250, 20)
        self.lbl_result2.setFont(fnt1)

        self.setGeometry(300, 200, 270, 200)
        self.setWindowTitle('Currency converter')

        self.show()

    def convert(self):

        frm = self.cb_fr.currentText()
        to = self.cb_to.currentText()

        try:
            amount = float(self.le.text())
        except:
            self.lbl_result1.setText("Introduce number")
            return

        rate = float(getrate(frm, to))

        converted = amount*rate

        self.lbl_result1.setText('%.2f'%amount + ' ' + frm)
        self.lbl_result2.setText('%.2f'%converted + ' ' + to)

    def update_cb(self):
        """
        If item at one CB is changed, update the other so that it is not repeated
        """
        tochange = self.cb_to

        remove = self.cb_fr.currentText()
        new_currencies = copy(currencies)
        new_currencies.remove(remove)
        self.cb_to.clear()
        self.cb_to.addItems(new_currencies)

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
