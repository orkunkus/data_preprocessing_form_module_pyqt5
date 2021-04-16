# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 23:32:46 2021

@author: orkun
"""
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtGui import QStandardItemModel
from import_file import File_GET
from process_steps import processes
import random


class pre_process_ui(QMainWindow):
    def __init__(self, *args):
        QMainWindow.__init__(self, *args)
        uic.loadUi('design/PreProcess.ui', self)
        self.model = QStandardItemModel(self)
        self.tview.setModel(self.model)
        self.selectmodel = self.tview.selectionModel()
        self.btnPrev.setEnabled(False)
        self.tabWidget.currentChanged.connect(self.tab_change)
        self.btnLoad.clicked.connect(self.open_filename)
        self.btnNext.clicked.connect(self.next_tab)
        self.btnPrev.clicked.connect(self.prev_tab)
        self.btndata.clicked.connect(self.load_data)

        self.delimeter = ";"
        self.cmblist = [";", ",", ":", "-"]
        self.cbSep.addItems(self.cmblist)
        self.cbSep.currentTextChanged.connect(self.on_combobox_changed)

        self.miss_formats = 'n.a.,NA,na,--,NAN,nan'
        self.leMissing.setText(self.miss_formats)
        self.leMissing.textChanged.connect(self.on_label_changed)

        self.selectmodel.selectionChanged.connect(self.on_selectionChanged)

        self.btnProcess.clicked.connect(self.do_process)

        self.show()

    def open_filename(self):
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Select (.csv) File", "", "All Files (*);;csv Files (*.csv)")
        if fileName:
            self.leFileName.setText(fileName)

    def next_tab(self):
        cur_index = self.tabWidget.currentIndex()
        if cur_index < len(self.tabWidget)-1:
            self.tabWidget.setCurrentIndex(cur_index+1)

    def prev_tab(self):
        cur_index = self.tabWidget.currentIndex()
        if cur_index > 0:
            self.tabWidget.setCurrentIndex(cur_index-1)

    def tab_change(self):
        cur_index = self.tabWidget.currentIndex()

        if cur_index == len(self.tabWidget)-1:
            self.btnNext.setEnabled(False)
            self.btnPrev.setEnabled(True)
        elif cur_index < len(self.tabWidget)-1 and cur_index > 0:
            self.btnNext.setEnabled(True)
            self.btnPrev.setEnabled(True)
        elif cur_index == 0:
            self.btnPrev.setEnabled(False)
            self.btnNext.setEnabled(True)

    def on_combobox_changed(self):
        self.delimeter = self.cbSep.currentText()

    def on_label_changed(self):
        self.miss_formats = self.leMissing.text()

    def on_selectionChanged(self):
        self.lblcolhead.setText("Selected Columns :" + str([col.data() for col in self.selectmodel.selectedColumns()]))
        self.col_list = list(col.data() for col in self.selectmodel.selectedColumns())

    def load_data(self):
        file_class = File_GET(self.model, self.leFileName.text(), self.delimeter, self.miss_formats)
        self.df = file_class.file_import_csv()

    def do_process(self):
        process_list = [self.chkmiss.isChecked(), self.chkoutlier.isChecked(), self.chkscale.isChecked()]
        export_list = [self.chkfile.isChecked(), self.chkgraph.isChecked()]
        if any(export_list):
            process_class = processes(process_list, export_list, self.df, self.col_list, self.miss_formats)
            data_get = process_class.process_steps()
            
            if export_list[0]:
                
                if data_get is not None:
                    # ----Export File
                    try:
                        fileName, selectedFilter = QFileDialog.getSaveFileName(self, "Save File",
                                                                               str(random.randint(0, 10000)) + "_documentView", "CSV Files (*.csv)")
                        if fileName:
                            data_get.to_csv(fileName, index=False, header=True)
                            # return True
    
                    except IOError:
                        print("Write Error:", fileName)
                        # return False
                        
if __name__ == "__main__":
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    window = pre_process_ui()
    sys.exit(app.exec_())
