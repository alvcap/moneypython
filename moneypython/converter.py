import sys
import json
from copy import copy
from datetime import date
from pkg_resources import resource_string

import requests

from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QPushButton, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QGridLayout

URL = "https://www.currency-api.com/rates?base={0}&date={1}&symbols={2}"

json_string = resource_string(__name__, "currencies.json").decode("utf-8")
CURRENCIES = json.loads(json_string)['currencies']

class ConverterGUI(QWidget):

    def __init__(self):

        super().__init__()
        self.lands = [curr['land'] for curr in CURRENCIES]

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
        self.lbl_result1.setFont(fnt1)
        self.lbl_result2.setFont(fnt1)
        # Combo boxes
        self.cb_fr = QComboBox(self)
        self.cb_to = QComboBox(self)
        self.set_combo_boxes()
        # Line edit
        self.le = QLineEdit(self)
        self.le.setFocus()
        self.le.returnPressed.connect(self.convert)
        # Button 
        btn_cnvrt = QPushButton('Convert', self)
        btn_cnvrt.clicked.connect(self.convert)

        vlayout = QVBoxLayout()
        hlayout1 = QHBoxLayout()
        hlayout2 = QHBoxLayout()

        hlayout1.addWidget(lbl_fr)
        hlayout1.addWidget(lbl_to)
        hlayout2.addWidget(self.cb_fr)
        hlayout2.addWidget(self.cb_to)

        vlayout.addLayout(hlayout1)
        vlayout.addLayout(hlayout2)
        vlayout.addWidget(lbl_it)
        vlayout.addWidget(self.le)
        vlayout.addWidget(btn_cnvrt)
        vlayout.addWidget(self.lbl_result1)
        vlayout.addWidget(self.lbl_result2)

        self.setLayout(vlayout)
        self.setGeometry(300, 200, 270, 200)
        self.setWindowTitle('moneypython')

        self.show()

    def convert(self):

        frm_land = self.cb_fr.currentText()
        to_land = self.cb_to.currentText()

        for curr in CURRENCIES:
            if frm_land == curr['land']:
                frm = curr['currency']
            if to_land == curr['land']:
                to = curr['currency']

        try:
            amount = float(self.le.text())
        except:
            self.lbl_result1.setText("Introduce number")
            return

        rate = float(getrate(frm, to))

        converted = amount*rate

        self.lbl_result1.setText('%.2f'%amount + ' ' + frm)
        self.lbl_result2.setText('%.2f'%converted + ' ' + to)

    def set_combo_boxes(self):

        self.cb_fr.addItems(self.lands)
        to_lands = copy(self.lands)
        to_lands.remove(self.cb_fr.currentText())
        self.cb_to.addItems(to_lands)
        self.cb_fr.activated.connect(self.update_cb)

    def update_cb(self):
        """
        If item at one CB is changed, update the other so that it is not repeated
        """
        tochange = self.cb_to

        remove = self.cb_fr.currentText()
        new_lands = copy(self.lands)
        new_lands.remove(remove)
        self.cb_to.clear()
        self.cb_to.addItems(new_lands)

def getrate(frm, to):
    today = date.today().isoformat()

    r = requests.get(URL.format(frm, today, to))
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
