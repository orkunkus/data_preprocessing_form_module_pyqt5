# -*- coding: utf-8 -*-
"""
Created on Sun Apr 11 22:34:12 2021

@author: orkun
"""
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from pandas.api.types import is_numeric_dtype
from sklearn import preprocessing
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QSize
from graph_view import graphics

class processes(object):
    def __init__(self, process_list, export_list, dataframe, col_list, miss_list):
        self.process_list = process_list
        self.export_list = export_list
        self.dataframe = dataframe
        self.col_list = col_list
        self.miss_list = miss_list

    def process_steps(self):
        self.procs_dic = {0: self.imput_data_get, 1: self.out_iqr_get, 2: self.scale_data_get}
        
        if self.export_list[1]:
            self.graph_class=graphics()
        
        for index, item in enumerate(self.process_list):
            if item:
                processed_data = self.procs_dic[index]()
                if processed_data is not None:
                    self.dataframe = processed_data
                else:
                    return None    
        return self.dataframe

    def imput_data_get(self):
        num_imp = SimpleImputer(missing_values=np.nan, strategy='mean')
        cat_imp = SimpleImputer(missing_values=np.nan, strategy='most_frequent')

        imputed_data = self.dataframe.copy()

        for col_name in self.col_list:
            if is_numeric_dtype(self.dataframe[col_name].dtypes):
                imputer = num_imp.fit_transform(pd.DataFrame(self.dataframe[col_name]))
                imputed_data[col_name] = pd.DataFrame(data=imputer)
            else:
                imputer = cat_imp.fit_transform(pd.DataFrame(self.dataframe[col_name]))
                imputed_data[col_name] = pd.DataFrame(data=imputer)

        return imputed_data

    def out_iqr_get(self):
        self.out_frame = self.dataframe.copy()
        for col_name in self.col_list:
            if any(str(elem) in self.miss_list for elem in self.dataframe[col_name]):
                self.error_catch("Please ensure the missing value detection first", "Missing Values Detection!")
                return None
            if is_numeric_dtype(self.dataframe[col_name].dtypes):
                out_data = self.dataframe[col_name]
                q25, q75 = np.quantile(out_data, 0.25), np.quantile(out_data, 0.75)
                iqr = q75 - q25
                cut_off = iqr * 1.5
                lower, upper = q25 - cut_off, q75 + cut_off
                
                self.out_frame = self.dataframe[(out_data < upper) & (out_data > lower)].copy()
                
                if self.export_list[1]:
                    self.graph_class.out_graph_show(col_name, "Outlier Process", lower, upper, self.dataframe, self.out_frame)
                    

        return self.out_frame

    def scale_data_get(self):
        self.scale_frame = self.dataframe.copy()
        for col_name in self.col_list:
            if any(str(elem) in self.miss_list for elem in self.dataframe[col_name]):
                self.error_catch("Please ensure the missing value detection first", "Missing Values Detection!")
                return None
            if is_numeric_dtype(self.dataframe[col_name].dtypes):
                scaler = preprocessing.StandardScaler()
                
                self.scale_frame[col_name] = scaler.fit_transform(np.reshape(self.dataframe[col_name].values, (-1, 1)))
    
                if self.export_list[1]:
                    self.graph_class.scale_graph_show(col_name, "Scale Process", self.dataframe, self.scale_frame)

        return self.scale_frame

    def error_catch(self, info_text, message_text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(message_text)
        msg.setInformativeText(info_text)
        msg.setWindowTitle("Error")
        msg.setBaseSize(QSize(500, 100))
        msg.exec_()        
