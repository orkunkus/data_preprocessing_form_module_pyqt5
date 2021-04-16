# -*- coding: utf-8 -*-
"""
Created on Fri Apr 16 00:27:20 2021

@author: orkun
"""
import pyqtgraph as pg
import pyqtgraph.exporters
import numpy as np 
import sys 

class graphics(object):
        
    def out_graph_show(self, col_name, process, lower, upper, df_old, df_new):
        self.win = pg.GraphicsLayoutWidget(show=True)
        self.win.resize(1200,760)
        self.win.setWindowTitle(col_name + " " + str(process))
        plt1 = self.win.addPlot(title='Before ')
        plt2 = self.win.addPlot(title='Processed ' )
        
        s1 = pg.ScatterPlotItem(pen=pg.mkPen(None), brush=pg.mkBrush(255, 255, 255, 120))
        pos = df_old[col_name]
        s1.addPoints(x=pos.index, y=pos[:])
        plt1.addItem(s1)

        lr_low = pg.LinearRegionItem([lower,df_old[col_name].min()],movable=False,brush=(150,0,0,150), orientation = 'horizontal')
        lr_low.setZValue(-10)
        plt1.addItem(lr_low)
        lr_upper = pg.LinearRegionItem([upper,df_old[col_name].max()],movable=False,brush=(150,0,0,150), orientation = 'horizontal')
        lr_upper.setZValue(-10)
        plt1.addItem(lr_upper)    
        
        s2 = pg.ScatterPlotItem(pen=pg.mkPen(None), brush=pg.mkBrush(255, 255, 255, 120))
        pos2 = df_new[col_name]
        s2.addPoints(x=pos2.index, y=pos2[:])
        plt2.addItem(s2)
        
        sys.displayhook(self.win)

    def scale_graph_show(self, col_name, process, df_old, df_new):
        self.win = pg.GraphicsLayoutWidget(show=True)
        self.win.resize(1200,760)
        self.win.setWindowTitle(col_name + " " + str(process))
        plt1 = self.win.addPlot(title='Before ')
        plt2 = self.win.addPlot(title='Processed ' )
        
        s1 = pg.ScatterPlotItem(pen=pg.mkPen(None), brush=pg.mkBrush(255, 255, 255, 120))
        pos = df_old[col_name]
        s1.addPoints(x=pos.index, y=pos[:])
        plt1.addItem(s1) 
        
        s2 = pg.ScatterPlotItem(pen=pg.mkPen(None), brush=pg.mkBrush(255, 255, 255, 120))
        pos2 = df_new[col_name]
        s2.addPoints(x=pos2.index, y=pos2[:])
        plt2.addItem(s2)
        
        sys.displayhook(self.win)                
                