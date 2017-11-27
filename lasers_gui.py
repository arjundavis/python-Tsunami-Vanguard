# -*- coding: utf-8 -*-
"""
Created on Mon July 24 16:35:13 2017

@author: Maxime PINSARD
"""
import os, sys
os.chdir('C:/Users/admin/Documents/Python/Lasers GUI standalone')

from PyQt5 import QtWidgets

import lasers_core
        

if __name__=='__main__':
    
    # just to avoid pyqt5 to quit when an error is raised
    def my_excepthook(type, value, tback):
        # log the exception here
    
        # then call the default handler
        sys.__excepthook__(type, value, tback)
    sys.excepthook = my_excepthook
    
    app = QtWidgets.QApplication(sys.argv)
    lasers_window = lasers_core.Lasers_GUI()
    lasers_window.show()
    sys.exit(app.exec_())