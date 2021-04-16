# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 23:51:20 2021

@author: orkun
"""
import pandas as pd
import numpy as np
from PyQt5.QtGui import QStandardItem, QBrush
from PyQt5.QtCore import Qt


class File_GET(object):
    def __init__(self, model, file_path, separator, miss_formats):
        self.model = model
        self.file_path = file_path
        self.miss_formats = miss_formats
        self.separator = separator

    def file_import_csv(self):
        self.model.clear()
        try:
            if self.file_path:
                df = pd.read_csv(self.file_path, na_values=list(self.miss_formats.split(",")),
                                 delimiter=self.separator, decimal=",")
                # self.model.appendRow([QStandardItem(field) for field in df.columns])
                items = []
                for field in df.columns:
                    item = QStandardItem(str(field))
                    item.setBackground(QBrush(Qt.green))
                    items.append(item)
                self.model.appendRow(items)

                for i in range(len(df)):
                    items = []
                    for field in df.iloc[i, :]:
                        item = QStandardItem(str(field))
                        if str(field) in self.miss_formats:
                            item.setBackground(QBrush(Qt.red))
                        items.append(item)
                    self.model.appendRow(items)
            return df

        except FileNotFoundError:
            print("file {} does not exist".format(self.file_path))
            return None
