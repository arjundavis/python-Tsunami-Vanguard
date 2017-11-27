# -*- coding: utf-8 -*-
"""
Created on Mon July 24 16:35:13 2017

@author: Maxime PINSARD
"""
import sys

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.uic import loadUiType
from PyQt5.QtCore import pyqtSignal, pyqtSlot

print('Importing VISA ...')

import visa

print('VISA ok ok.')


Ui_lasersWindow, QlasersWindow = loadUiType('lasers_gui.ui') # loading the dialog box for jobs 

class Lasers_GUI(QlasersWindow, Ui_lasersWindow):
    """
    pyqtsginals go here 
    """
    
    read_command_millenia_signal = pyqtSignal()
    query_last_pwr_cmd_millenia_signal = pyqtSignal()
    millenia_get_param_status_signal = pyqtSignal()
    vanguard_get_param_status_signal = pyqtSignal()
    lktoclock_get_param_status_signal = pyqtSignal()

    
    def __init__(self, parent=None):
        """
        var init go here 
        """
        
        super(Lasers_GUI, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)
        
        # when you want to destroy the dialog set this to True
        self._want_to_close = False
        
        self.wrn_msg_lbl.setVisible(False)
        
        self.millenia_connect_push.clicked.connect(self.connect_millenia_meth)
        self.on_millenia_push.clicked.connect(self.turn_on_millenia_meth)
        self.off_millenia_push.clicked.connect(self.turn_off_millenia_meth)
        self.millenia_shutter_open_radio.clicked.connect(self.shutter_millenia_meth)
        self.millenia_shutter_close_radio.clicked.connect(self.shutter_millenia_meth)
        self.close_gui_push.clicked.connect(self.quit_gui_lasers_meth)
        self.millenia_lst_pwr_cmd_query_push.clicked.connect(self.query_last_pwr_cmd_millenia_meth)
        self.millenia_set_pwr_push.clicked.connect(self.set_pwr_prof_millenia_meth)
        self.millenia_power_prof_combo.activated.connect(self.ctl_prof_combobx_meth)
        
        self.millenia_param_status_query_push.clicked.connect(self.get_param_status_millenia_meth)
        # self.millenia_get_diodes_temp_push.clicked.connect(self.get_diodes_temp_millenia_meth)
        # self.millenia_curr_pwr_query_push.clicked.connect(self.get_pwr_laser_millenia_meth)
        # self.millenia_duration_query_push.clicked.connect(self.get_duration_millenia_meth)
        # self.millenia_ctl_warmup_push.clicked.connect(self.ctl_wrmup_millenia_meth)
        
        self.on_millenia_push.setEnabled(False)
        self.off_millenia_push.setEnabled(False)
        self.millenia_shutter_bx.setEnabled(False)
        self.millenia_param_status_query_push.setEnabled(False)
        self.millenia_ctl_warmup_push.setEnabled(False)
        self.millenia_lst_pwr_cmd_query_push.setEnabled(False)
        self.millenia_set_pwr_push.setEnabled(False)
        
        self.read_command_millenia_signal.connect(self.read_command_millenia_meth)
        self.query_last_pwr_cmd_millenia_signal.connect(self.query_last_pwr_cmd_millenia_meth)
        
        self.millenia_get_param_status_signal.connect(self.get_param_status_millenia_meth)
        # self.get_pwr_laser_millenia_signal.connect(self.get_pwr_laser_millenia_meth)
        # self.millenia_get_diodes_signal.connect(self.get_diodes_millenia_push_meth)
        # self.millenia_get_diodes_temp_signal.connect(self.get_diodes_temp_millenia_meth)
        # self.millenia_duration_query_signal.connect(self.get_duration_millenia_meth)
        # self.ctl_wrmup_millenia_signal.connect(self.ctl_wrmup_millenia_meth)

        
        self.pwr_millenia_low = 0.05 # W
        self.pwr_millenia_high = 12.00 # W
        
        self.temp_diode_max = 30 # °C
        
        self.first_read = 1
        self.val_wrmup_current = 0 # init
        
        self.vanguard_connect_button.clicked.connect(self.connect_vanguard_meth)
        self.vanguard_param_status_query_push.clicked.connect(self.get_param_status_vanguard_meth)
        self.vanguard_get_param_status_signal.connect(self.get_param_status_vanguard_meth)
        
        self.on_vanguard_push.clicked.connect(self.turn_on_vanguard_meth)
        self.off_vanguard_push.clicked.connect(self.turn_off_vanguard_meth)
        
        self.temp_diode_max_vg = 30 # °C
        
        self.shutter_open_vg_radio.clicked.connect(self.shutter_vanguard_meth)
        self.shutter_close_vg_radio.clicked.connect(self.shutter_vanguard_meth)
        
        self.vg_gb_shutter.setEnabled(False)
        self.on_vanguard_push.setEnabled(False)
        self.off_vanguard_push.setEnabled(False)
        self.vanguard_param_status_query_push.setEnabled(False)
        
        # self.wrn_msg_lbl_vg.setVisible(False)
        self.lktoclock_get_param_status_signal.connect(self.get_param_status_lktoclock_meth)
        
        self.lktoclock_param_status_query_push.clicked.connect(self.get_param_status_lktoclock_meth)
    
        self.lktoclock_delay_spnbx.valueChanged.connect(self.lktoclock_after_change_dly_spnbx_meth)
        self.lktoclock_delay_spnbx.editingFinished.connect(self.lktoclock_query_delay_meth)
        # editingFinished not responsive enough
        # self.lktoclock_dial.sliderMoved.connect(self.lktoclock_after_change_dly_dial_meth)
        self.lktoclock_dial.valueChanged.connect(self.lktoclock_after_change_dly_dial_meth)
        self.lktoclock_dial.sliderReleased.connect(self.lktoclock_query_delay_meth)
        # vqlueChqnged reacts also when another function change it, unless you block signals
        # sliderMoved does not react to clicks
        
        self.lktoclock_connect_push.clicked.connect(self.connect_lktoclock_meth)
        
        self.lktoclock_lock_on_radio.setEnabled(False)
        #self.lktoclock_delay_spnbx.setEnabled(False)
        # self.lktoclock_dial.setEnabled(False)
        self.lktoclock_param_status_query_push.setEnabled(False)
        self.lktoclock_disconnect_push.setEnabled(False)
        
        self.lktoclock_lock_on_radio.clicked.connect(self.lktoclock_lock_meth)
        self.lktoclock_lock_off_radio.clicked.connect(self.lktoclock_lock_meth)
        
        self.lktoclock_disconnect_push.clicked.connect(self.lktoclock_disconn_meth)
        
        self.lktoclock_delayposstep_push.clicked.connect(self.lktoclock_delayposstep_meth)
        self.lktoclock_delaynegstep_push.clicked.connect(self.lktoclock_delaynegstep_meth)
        
        self.millenia_chck.stateChanged.connect(self.millenia_chck_meth)
        self.millenia_expert_chck.stateChanged.connect(self.millenia_expert_chck_meth)
        self.millenia_chck_meth() # hide the buttons
        
        self.lk2clk_chck.stateChanged.connect(self.lktoclock_chck_meth)
        self.lktoclock_chck_meth() # hide the buttons
        
        self.vg_chck.stateChanged.connect(self.vg_chck_meth)
        self.vg_chck_meth() # hide the buttons
        
        self.vg_expert_chck.stateChanged.connect(self.vg_expert_meth)
        
        self.max_bit_lktoclck_delay = 4095
        self.max_ns_lktoclck_delay = 2 # ns
        self.lktoclock_pzt_dc_max = 1000
        self.lktoclock_lmon_dc_max = 100
        
        # self.list_STB_lktoclock = ['ACQ 1 if the system is in acquisition mode'
        
    @pyqtSlot()    
    def quit_gui_lasers_meth(self):
        
        if QtWidgets.QMessageBox.question(None, '', "Are you sure you want to quit?",
                            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                            QtWidgets.QMessageBox.No) == QtWidgets.QMessageBox.Yes:
            print("User chose to close ...")
            # QApplication.quit()
            
            # (x.close() for x in ['self.millenia', 'self.vanguard', 'self.lktoclock'] if x in locals())
            if hasattr(self,'millenia'):
                self.millenia.close()
                
            if hasattr(self,'vanguard'):
                self.vanguard.close()
                
            if hasattr(self,'lktoclock'):
                self.lktoclock.close()

            
            print('Terminating  ...')
            
            # time.sleep(2)
            sys.exit()
            self.close()
            print('terminated.')
        
    def closeEvent(self, event): # method to overwrite the close event, because otherwise the object is no longer available
        # self.deleteLater()
        if self._want_to_close:
            
            super(Lasers_GUI, self).closeEvent(event)
        else:
            event.ignore()
            self.setWindowState(QtCore.Qt.WindowMinimized)
            
    @pyqtSlot()        
    def read_command_millenia_meth(self):
        
        bb =  self.millenia.read()

        if bool(bb): # True if is detected
        
            self.terminal_log_1_edt.append(bb)
            
            if self.first_read:
                
                self.millenia_shutter_bx.setEnabled(True)
            
            self.first_read = 0
            
            # activate buttons
            self.millenia_param_status_query_push.setEnabled(True)
            self.millenia_ctl_warmup_push.setEnabled(True)
            self.millenia_lst_pwr_cmd_query_push.setEnabled(True)
            self.millenia_set_pwr_push.setEnabled(True)
            
            self.query_last_pwr_cmd_millenia_signal.emit()
            self.millenia_get_param_status_signal.emit()
        
        else:
            
            print('Millenia not detected')

        
    @pyqtSlot()        
    def connect_millenia_meth(self):
        
        baud_rate_millenia= 9600
        bits_millenia = 8
        parity_millenia = visa.constants.Parity.none
        stop_bit_millenia = visa.constants.StopBits.one
        flow_control_millenia= 0 # hardware control ?
        timeout_millenia = 2000
        read_termination_millenia  = '\n'
        write_termination_millenia = read_termination_millenia
        
        current_txt = self.millenia_com_combo.currentText()
        # for pyvisa and not pyvisa-py
        # if current_txt[6] == '(':
        #     current_txt = current_txt[0:6]
        # else:
        #     current_txt = current_txt[0:7]
        
        ressource_millenia = '%s' % current_txt
        print('ressource_millenia =', ressource_millenia)
        
        rm = visa.ResourceManager('@py')
        self.millenia = rm.open_resource(ressource_millenia)
        
        self.millenia.baud_rate = baud_rate_millenia 
        self.millenia.data_bits = bits_millenia 
        self.millenia.parity = parity_millenia 
        self.millenia.stop_bits = stop_bit_millenia 
        self.millenia.flow_control = flow_control_millenia 
        self.millenia.timeout = timeout_millenia 
        self.millenia.read_termination  = read_termination_millenia 
        self.millenia.write_termination = write_termination_millenia
        
        self.millenia_heatup_progressBar.setValue(0)
        
        self.query_ID_millenia_meth()
        
          
    def query_ID_millenia_meth(self):
        
        b = self.millenia.write('*IDN?')
        
        self.read_command_millenia_signal.emit()
    
    @pyqtSlot()        
    def query_last_pwr_cmd_millenia_meth(self):
        
        bb = self.millenia.query('?PSET')
        
        val_last_pwr_cmd = float(bb[0:len(bb)-1])
        
        if val_last_pwr_cmd == self.pwr_millenia_low:
            self.millenia_power_prof_combo.setCurrentIndex(0)
        elif val_last_pwr_cmd == self.pwr_millenia_high:
            self.millenia_power_prof_combo.setCurrentIndex(1)
        
    @pyqtSlot()        
    def turn_on_millenia_meth(self):
        
        if QtWidgets.QMessageBox.question(None, '', "Are you sure you want to turn Millenia ON?",
                            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                            QtWidgets.QMessageBox.No) == QtWidgets.QMessageBox.Yes:
            self.millenia.write('ON') # turn on the Millenia
            
            self.millenia_status_edt.setText('Laser turned on : query the actual power...')
        
    @pyqtSlot()        
    def turn_off_millenia_meth(self):
        
        if QtWidgets.QMessageBox.question(None, '', "Are you sure you want to turn Millenia OFF?",
                            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                            QtWidgets.QMessageBox.No) == QtWidgets.QMessageBox.Yes:
            self.millenia.write('OFF') # turn off the Millenia
            
            self.millenia_status_edt.setText('Laser turned OFF')
        
    @pyqtSlot()        
    def shutter_millenia_meth(self):
        
        if self.millenia_shutter_open_radio.isChecked(): # shutter open is checked
        
            self.millenia.write('SHUTTER:1') # open shutter
            
        else: # shutter closed is checked
            
            self.millenia.write('SHUTTER:0') # close the shutter
            
            
    @pyqtSlot()        
    def set_pwr_prof_millenia_meth(self):
        
        if self.millenia_power_prof_combo.currentIndex() == 0: # low power profile
            val_pwr = self.pwr_millenia_low # W
        elif self.millenia_power_prof_combo.currentIndex() == 1: # high power profile
            val_pwr = self.pwr_millenia_high # W
            
        self.millenia.write('P:%.2f' % val_pwr)
        
        self.millenia_status_edt.setText('Laser power set to %fW : query the actual power ...' % val_pwr)
    
    @pyqtSlot()        
    def get_param_status_millenia_meth(self):  
    
    # @pyqtSlot()        
    # def ctl_wrmup_millenia_meth(self):
        
        bb = self.millenia.query('?WARMUP%')
        val_wrmup = round(float(bb[0:len(bb)-1]))
        
        self.millenia_heatup_progressBar.setValue(val_wrmup)
        
        if (val_wrmup == 100 and val_wrmup != self.val_wrmup_current): # first time it reaches 100
            self.on_millenia_push.setEnabled(True)
            self.off_millenia_push.setEnabled(True)
            
        self.val_wrmup_current = val_wrmup  
    
    # @pyqtSlot()        
    # def get_pwr_laser_millenia_meth(self):
        
        bb = self.millenia.query('?P')
        val_pwr = round(float(bb[0:len(bb)-1]))
        
        self.millenia_power_LCD.display(val_pwr)
        
        if self.millenia_power_prof_combo.currentIndex() == 0: # low power profile
            val_ref_pwr = self.pwr_millenia_low # W
        elif self.millenia_power_prof_combo.currentIndex() == 1: # high power profile
            val_ref_pwr = self.pwr_millenia_high # W
        
        if val_pwr == val_ref_pwr: # val max is reached
            self.millenia_status_edt.setText('Laser at full power')
        else:
            self.millenia_status_edt.setText('Laser power increasing...')
        
        
    # @pyqtSlot()        
    # def get_shutter_status_millenia_meth(self):
        
        stat_shutter = self.millenia.query('?SHUTTER')
        
        print('stat_shutter = ', stat_shutter)
        
        if int(stat_shutter): 
            self.millenia_shutter_open_radio.setChecked(True) # shutter open)
        else:
            self.millenia_shutter_open_radio.setChecked(False) # shutter closed)
            
    # @pyqtSlot()        
    # def get_diodes_millenia_push_meth(self):
        
        bb = self.millenia.query('?C1')
        stat_diode1 = float(bb[0:len(bb)-2]) # ex is 25.36A1 for 1
        
        self.millenia_diode1_LCD.display(stat_diode1)
        
        bb = self.millenia.query('?C2')
        stat_diode2 = float(bb[0:len(bb)-2]) # ex is 25.36A1 for 1
        
        self.millenia_diode2_LCD.display(stat_diode2)
        
        current_min = 1.0 # A
        if (stat_diode1 < current_min and stat_diode2 < current_min):
            self.millenia_status_edt.setText('Laser is OFF')
        
    # @pyqtSlot()        
    # def get_diodes_temp_millenia_meth(self):
        
        bb = self.millenia.query('?HS1')
        temp_diode1 = float(bb[0:len(bb)-2]) # ex is 25.36A1 for 1
        
        self.millenia_diode1_temp_LCD.display(temp_diode1)
        
        bb = self.millenia.query('?HS2')
        temp_diode2 = float(bb[0:len(bb)-2]) # ex is 25.36A1 for 1
        
        self.millenia_diode2_temp_LCD.display(temp_diode2)
        
        if (temp_diode1 > self.temp_diode_max or temp_diode2 > self.temp_diode_max):
            self.wrn_msg_lbl.setVisible(True)
        else:
            self.wrn_msg_lbl.setVisible(False)
            
    # @pyqtSlot()        
    # def get_duration_millenia_meth(self):
        
        self.millenia_duration_edt.setText(self.millenia.query('?ONHRS'))
        
    @pyqtSlot()        
    def ctl_prof_combobx_meth(self):
        
        print('self.millenia_power_prof_combo.currentIndex()', self.millenia_power_prof_combo.currentIndex())
        # err
    
    @pyqtSlot()        
    def millenia_chck_meth(self): 
       
        if self.millenia_chck.isChecked():
            
            self.millenia_connect_push.setVisible(True)
            self.millenia_com_combo.setVisible(True)
            self.on_millenia_push.setVisible(True)
            self.off_millenia_push.setVisible(True)
            self.millenia_shutter_bx.setVisible(True)
            self.millenia_shutter_bx.setVisible(True)
            self.millenia_param_status_query_push.setVisible(True)
            self.millenia_status_edt.setVisible(True)
            # label_12
            self.millenia_diode1_LCD.setVisible(True)
            self.millenia_duration_edt.setVisible(True)
            self.millenia_expert_chck.setVisible(True)
            self.mill_stat_lbl.setVisible(True)
            self.mill_dur_lbl.setVisible(True)
            
            
        else: # no Milennia menus
        
            self.millenia_connect_push.setVisible(False)
            self.millenia_com_combo.setVisible(False)
            self.on_millenia_push.setVisible(False)
            self.off_millenia_push.setVisible(False)
            self.millenia_shutter_bx.setVisible(False)
            self.millenia_shutter_bx.setVisible(False)
            self.millenia_param_status_query_push.setVisible(False)
            self.millenia_status_edt.setVisible(False)
            # label_12
            self.millenia_diode1_LCD.setVisible(False)
            self.millenia_duration_edt.setVisible(False)
            self.millenia_expert_chck.setVisible(False)
            self.mill_stat_lbl.setVisible(False)
            self.mill_dur_lbl.setVisible(False)
            
            self.millenia_expert_chck.setChecked(False)
            
                            
        self.millenia_expert_chck_meth()
            
    @pyqtSlot()        
    def millenia_expert_chck_meth(self):
        
            if self.millenia_expert_chck.isChecked(): # expert_mode
                
                self.millenia_heatup_progressBar.setVisible(True)
                self.millenia_ctl_warmup_push.setVisible(True)
                self.millenia_diode1_LCD.setVisible(True)
                self.millenia_diode2_LCD.setVisible(True)
                self.millenia_diode1_temp_LCD.setVisible(True)
                self.millenia_diode2_temp_LCD.setVisible(True)
                self.millenia_lst_pwr_cmd_query_push.setVisible(True)
                self.millenia_set_pwr_push.setVisible(True)
                self.millenia_power_prof_combo.setVisible(True)
                self.millenia_power_LCD.setVisible(True)
                self.millenia_power_prof_lbl.setVisible(True)
                self.millenia_power_lbl.setVisible(True)
                self.mill_d1_amp_lbl.setVisible(True)
                self.mill_d2_amp_lbl.setVisible(True)
                self.mill_ex1_amp_lbl.setVisible(True)
                self.mill_ex2_amp_lbl.setVisible(True)
                self.mill_ex1_temp_lbl.setVisible(True)
                self.mill_ex2_temp_lbl.setVisible(True)
                self.mill_ex3_temp_lbl.setVisible(True)
                self.mill_ex4_temp_lbl.setVisible(True)
                
            else: # user mode
        
                self.millenia_heatup_progressBar.setVisible(False)
                self.millenia_ctl_warmup_push.setVisible(False)
                self.millenia_diode1_LCD.setVisible(False)
                self.millenia_diode2_LCD.setVisible(False)
                self.millenia_diode1_temp_LCD.setVisible(False)
                self.millenia_diode2_temp_LCD.setVisible(False)
                self.millenia_lst_pwr_cmd_query_push.setVisible(False)
                self.millenia_set_pwr_push.setVisible(False)
                self.millenia_power_prof_combo.setVisible(False)
                self.millenia_power_LCD.setVisible(False)
                self.millenia_power_prof_lbl.setVisible(False)
                self.millenia_power_lbl.setVisible(False)
                self.mill_d1_amp_lbl.setVisible(False)
                self.mill_d2_amp_lbl.setVisible(False)
                self.mill_ex1_amp_lbl.setVisible(False)
                self.mill_ex2_amp_lbl.setVisible(False)
                self.mill_ex1_temp_lbl.setVisible(False)
                self.mill_ex2_temp_lbl.setVisible(False)
                self.mill_ex3_temp_lbl.setVisible(False)
                self.mill_ex4_temp_lbl.setVisible(False)
        
            
    ## lok to clock 3930
    
    @pyqtSlot()        
    def connect_lktoclock_meth(self):
        
        baud_rate_lktoclock= 9600
        bits_lktoclock = 8
        parity_lktoclock = visa.constants.Parity.none
        stop_bit_lktoclock = visa.constants.StopBits.one
        flow_control_lktoclock= 0 # hardware control ?
        timeout_lktoclock = 500 # ms
        # read_termination_lktoclock  = '\n'
        # write_termination_lktoclock = read_termination_lktoclock
        
        current_txt = self.lktoclock_com_combo.currentText()
        # for pyvisa and not pyvisa-py
        # if current_txt[6] == '(':
        #     current_txt = current_txt[0:6]
        # else:
        #     current_txt = current_txt[0:7]
        
        ressource_lktoclock = '%s' % current_txt
        print('ressource_lktoclock =', ressource_lktoclock)
        
        rm = visa.ResourceManager('@py')
        self.lktoclock = rm.open_resource(ressource_lktoclock)
        
        self.lktoclock.baud_rate = baud_rate_lktoclock 
        self.lktoclock.data_bits = bits_lktoclock 
        self.lktoclock.parity = parity_lktoclock 
        self.lktoclock.stop_bits = stop_bit_lktoclock 
        self.lktoclock.flow_control = flow_control_lktoclock 
        self.lktoclock.timeout = timeout_lktoclock 
        # self.lktoclock.read_termination  = read_termination_lktoclock 
        # self.lktoclock.write_termination = write_termination_lktoclock

        self.query_ID_lktoclock_meth()
    
    def query_ID_lktoclock_meth(self):
        
        bb = self.lktoclock.query('*IDN?')
        
        if bool(bb): # True if is detected
        
            self.terminal_log_3_edt.append(bb)
            
            # activate buttons
            self.lktoclock_lock_on_radio.setEnabled(True)
            self.lktoclock_param_status_query_push.setEnabled(True)
            self.lktoclock_disconnect_push.setEnabled(True)
            
            self.lktoclock_get_param_status_signal.emit()
            
        else:
            
            print('loktoclock not detected')
    
    @pyqtSlot()     
    def get_param_status_lktoclock_meth(self):
        
        stat_loop_lock = self.lktoclock.query('LOOP?') # is locked or not
        
        if int(stat_loop_lock) == 1: # servo loop on 
        
            self.lktoclock_delay_spnbx.setEnabled(True)
            self.lktoclock_dial.setEnabled(True)
        
            self.lktoclock_status_edt.setText('ON')
            self.lktoclock_lock_on_radio.setChecked(True) # allows to put OFF
            
            # delay 
            
            dly_raw = self.lktoclock.query('DLY?') # delay set by DLY command
            # gives a value between 0 and 4095 and max is 2ns
            
            if bool(dly_raw): # is not ''
                dly_ps = int(dly_raw)/self.max_bit_lktoclck_delay*self.max_ns_lktoclck_delay*1000 # in ns
                
                dly_dial = int(dly_raw)/self.max_bit_lktoclck_delay*99 # for dial widget, max is 99
                
                self.lktoclock_delay_spnbx.setValue(dly_ps)
                self.lktoclock_dial.setValue(dly_dial)
            else:
                print('Delay can`t be read')
            
            
            # Monitor signal
            
            LMON_DC = self.lktoclock.query('LMON:DC?')
            LMON_AC = self.lktoclock.query('LMON:AC?')
            
            PZT_DC = self.lktoclock.query('PZT:DC?')
            PZT_AC = self.lktoclock.query('PZT:AC?')
            
            print('Loop signal DC : %s (normally abs<40), AC : %s (normally < 5)' % (LMON_DC, LMON_AC))
            print('PZT signal DC : %s (normally abs<400), AC : %s (normally < 10)' % (PZT_DC, PZT_AC))
            
            self.lktoclock_pzDC_edt.setText(str(PZT_DC))
            self.lktoclock_pzAC_edt.setText(str(PZT_AC))
            
            self.lktoclock_lmonDC_edt.setText(str(LMON_DC))
            self.lktoclock_lmonAC_edt.setText(str(LMON_AC))

            if bool(LMON_DC): # is not ''
                self.lktoclock_lpsign_vslider.setValue(round((int(LMON_DC) + self.lktoclock_lmon_dc_max)/(2*self.lktoclock_lmon_dc_max)*99))
            
            if bool(PZT_DC): # is not ''
                self.lktoclock_pzt_vslider.setValue(round((int(PZT_DC)+self.lktoclock_pzt_dc_max)/(2*self.lktoclock_pzt_dc_max)*99))
            
            self.lktoclock_query_delay_meth()
        
        elif int(stat_loop_lock) == 0: # servo loop OFF
        
            self.lktoclock_delay_spnbx.setEnabled(False)
            self.lktoclock_dial.setEnabled(False)
            
            self.lktoclock_status_edt.setText('OFF')
            
            self.lktoclock_lock_on_radio.setChecked(False) # allows to put ON
            
        else:
            print('Retry to update, device was not available')
    
    @pyqtSlot()        
    def lktoclock_after_change_dly_spnbx_meth(self):
        
        dly_to_write = round(self.lktoclock_delay_spnbx.value()/1000/self.max_ns_lktoclck_delay*(self.max_bit_lktoclck_delay+1))
        
        self.lktoclock.write('DLY %d' % dly_to_write)
        
        dly_to_set = round(self.lktoclock_delay_spnbx.value()/1000/self.max_ns_lktoclck_delay*99)
        # print('dly_to_set sbx', dly_to_set)
        self.lktoclock_dial.blockSignals(True) # block the widget signals : it will just move without doing his function
        self.lktoclock_dial.setValue(dly_to_set)
        self.lktoclock_dial.blockSignals(False) # re-enable the signals
        
        # self.lktoclock_query_delay_meth()
            
        
    @pyqtSlot()        
    def lktoclock_after_change_dly_dial_meth(self):
        
        dly_to_write = round(self.lktoclock_dial.value()/99*(self.max_bit_lktoclck_delay+1))
        # print('dly_to_write ', dly_to_write)
        self.lktoclock.write('DLY %d' % dly_to_write)
        
        dly_to_set = self.lktoclock_dial.value()/99*self.max_ns_lktoclck_delay*1000
        # print('dly_to_set dial', dly_to_set)
        self.lktoclock_delay_spnbx.blockSignals(True) # block the widget signals : it will just move without doing his function
        self.lktoclock_delay_spnbx.setValue(dly_to_set)
        self.lktoclock_delay_spnbx.blockSignals(False) # re-enable the signals
           
        # # self.lktoclock_query_delay_meth()
                    
    def lktoclock_query_delay_meth(self):
        
        dly_raw = self.lktoclock.query('DLY?') # delay set by DLY command
        # gives a value between 0 and 4095 and max is 2ns
        
        # print('dly_raw %s' % dly_raw)
        if bool(dly_raw): # is not ''
            dly_ps_str = ('%.1f' % (int(dly_raw)/self.max_bit_lktoclck_delay*self.max_ns_lktoclck_delay*1000)) # in ps
            self.lktoclock_delay_edt.setText(dly_ps_str)
        else:
            print('Delay can`t be read')
            
    @pyqtSlot()        
    def lktoclock_lock_meth(self):
        
        if self.lktoclock_lock_on_radio.isChecked(): # lock on is checked
        
            b = self.lktoclock.write('LOOP 1') # lock
            
            if b[0] == 6: # no success
                print('Error while prompting to lock : ', b)
            
        else: # lock OFF is checked
                
            b = self.lktoclock.write('LOOP 0') # unlock
            
            if b[0] == 6: # no success
                print('Error while prompting to unlock : ', b)
        
        self.get_param_status_lktoclock_meth() # update status
        
    @pyqtSlot()        
    def lktoclock_delayposstep_meth(self):
        
        dly_to_write = round((self.lktoclock_delay_spnbx.value()+5)/1000/self.max_ns_lktoclck_delay*(self.max_bit_lktoclck_delay+1))
        
        self.lktoclock.write('DLY %d' % dly_to_write)
        
        dly_to_set_sp = self.lktoclock_delay_spnbx.value()+5
        dly_to_set_dial = round((self.lktoclock_delay_spnbx.value()+5)/1000/self.max_ns_lktoclck_delay*99)

        self.lktoclock_delay_spnbx.blockSignals(True) # block the widget signals : it will just move without doing his function
        self.lktoclock_dial.blockSignals(True) # block the widget signals : it will just move without doing his function
        self.lktoclock_delay_spnbx.setValue(dly_to_set_sp)
        self.lktoclock_dial.setValue(dly_to_set_dial)
        self.lktoclock_delay_spnbx.blockSignals(False) # re-enable the signals
        self.lktoclock_dial.blockSignals(False) # re-enable the signals

        self.lktoclock_query_delay_meth()
        
    @pyqtSlot()        
    def lktoclock_delaynegstep_meth(self):
        
        dly_to_write = round((self.lktoclock_delay_spnbx.value()-5)/1000/self.max_ns_lktoclck_delay*(self.max_bit_lktoclck_delay+1))
        
        self.lktoclock.write('DLY %d' % dly_to_write)
        
        dly_to_set_sp = self.lktoclock_delay_spnbx.value()-5
        dly_to_set_dial = round((self.lktoclock_delay_spnbx.value()-5)/1000/self.max_ns_lktoclck_delay*99)

        self.lktoclock_delay_spnbx.blockSignals(True) # block the widget signals : it will just move without doing his function
        self.lktoclock_dial.blockSignals(True) # block the widget signals : it will just move without doing his function
        self.lktoclock_delay_spnbx.setValue(dly_to_set_sp)
        self.lktoclock_dial.setValue(dly_to_set_dial)
        self.lktoclock_delay_spnbx.blockSignals(False) # re-enable the signals
        self.lktoclock_dial.blockSignals(False) # re-enable the signals

        self.lktoclock_query_delay_meth()
        
        
    @pyqtSlot()        
    def lktoclock_disconn_meth(self):
        
        # print('lktoclock' in locals())
        # print('self.lktoclock' in locals())
        # print('self.lktoclock' in vars())
        # print('self.lktoclock' in globals())
        # print(hasattr(self,'lktoclock'))
        
        if hasattr(self,'lktoclock'):
            self.lktoclock.close()
            print('loktoclock terminated')
            
            self.lktoclock_lock_on_radio.setEnabled(False)
            self.lktoclock_delay_spnbx.setEnabled(False)
            self.lktoclock_dial.setEnabled(False)
            self.lktoclock_param_status_query_push.setEnabled(False)
            self.lktoclock_disconnect_push.setEnabled(False)
            
        else:
            print('loktoclock not present')
            
    
    @pyqtSlot()        
    def lktoclock_chck_meth(self): 
       
        if self.lk2clk_chck.isChecked():
            
            self.lktoclock_dial.setVisible(True)
            self.lktoclock_pzt_vslider.setVisible(True)
            self.lktoclock_lpsign_vslider.setVisible(True)
            self.lktoclock_connect_push.setVisible(True)
            self.lktoclock_com_combo.setVisible(True)
            self.lktoclock_shutter_bx.setVisible(True)
            self.lk_stat_lbl.setVisible(True)
            self.lktoclock_status_edt.setVisible(True)
            self.tl_log_lkck_lbl.setVisible(True)
            self.lktoclock_disconnect_push.setVisible(True)
            self.lkck_delay_lbl.setVisible(True)
            self.lkck_read_lbl.setVisible(True)
            self.lktoclock_delay_spnbx.setVisible(True)
            self.lktoclock_delayposstep_push.setVisible(True)
            self.lktoclock_delaynegstep_push.setVisible(True)
            self.lktoclock_delay_edt.setVisible(True)
            self.lkck_ps1_lbl.setVisible(True)
            self.lkck_ps2_lbl.setVisible(True)
            self.lkck_slider1_lbl.setVisible(True)
            self.lkck_slider2_lbl.setVisible(True)
            self.lktoclock_param_status_query_push.setVisible(True)
            self.lkck_freq_lbl.setVisible(True)
            self.lktoclock_freqdiff_LCD.setVisible(True)
            self.lkck_hz_lbl.setVisible(True)
            self.lktoclock_pzDC_edt.setVisible(True)
            self.lktoclock_pzAC_edt.setVisible(True)
            self.lktoclock_lmonDC_edt.setVisible(True)
            self.lktoclock_lmonAC_edt.setVisible(True)
            self.lkck_ac1_lbl.setVisible(True)
            self.lkck_ac2_lbl.setVisible(True)
            self.lkck_ac3_lbl.setVisible(True)
            self.lkck_ac4_lbl.setVisible(True)
            self.lkck_dc1_lbl.setVisible(True)
            self.lkck_dc2_lbl.setVisible(True)
            self.lkck_dc3_lbl.setVisible(True)
            self.lkck_dc4_lbl.setVisible(True)
            self.lkck_dial1_lbl.setVisible(True)
            self.lkck_dial2_lbl.setVisible(True)
            self.lkck_dial3_lbl.setVisible(True)
            self.lkck_dial4_lbl.setVisible(True)
            self.lkck_dial5_lbl.setVisible(True)
            self.lkck_dial6_lbl.setVisible(True)
            
        else: # no lktoclock menus
        
            self.lktoclock_dial.setVisible(False)
            self.lktoclock_pzt_vslider.setVisible(False)
            self.lktoclock_lpsign_vslider.setVisible(False)
            self.lktoclock_connect_push.setVisible(False)
            self.lktoclock_com_combo.setVisible(False)
            self.lktoclock_shutter_bx.setVisible(False)
            self.lk_stat_lbl.setVisible(False)
            self.lktoclock_status_edt.setVisible(False)
            self.tl_log_lkck_lbl.setVisible(False)
            self.lktoclock_disconnect_push.setVisible(False)
            self.lkck_delay_lbl.setVisible(False)
            self.lkck_read_lbl.setVisible(False)
            self.lktoclock_delay_spnbx.setVisible(False)
            self.lktoclock_delayposstep_push.setVisible(False)
            self.lktoclock_delaynegstep_push.setVisible(False)
            self.lktoclock_delay_edt.setVisible(False)
            self.lkck_ps1_lbl.setVisible(False)
            self.lkck_ps2_lbl.setVisible(False)
            self.lkck_slider1_lbl.setVisible(False)
            self.lkck_slider2_lbl.setVisible(False)
            self.lktoclock_param_status_query_push.setVisible(False)
            self.lkck_freq_lbl.setVisible(False)
            self.lktoclock_freqdiff_LCD.setVisible(False)
            self.lkck_hz_lbl.setVisible(False)
            self.lktoclock_pzDC_edt.setVisible(False)
            self.lktoclock_pzAC_edt.setVisible(False)
            self.lktoclock_lmonDC_edt.setVisible(False)
            self.lktoclock_lmonAC_edt.setVisible(False)
            self.lkck_ac1_lbl.setVisible(False)
            self.lkck_ac2_lbl.setVisible(False)
            self.lkck_ac3_lbl.setVisible(False)
            self.lkck_ac4_lbl.setVisible(False)
            self.lkck_dc1_lbl.setVisible(False)
            self.lkck_dc2_lbl.setVisible(False)
            self.lkck_dc3_lbl.setVisible(False)
            self.lkck_dc4_lbl.setVisible(False)
            self.lkck_dial1_lbl.setVisible(False)
            self.lkck_dial2_lbl.setVisible(False)
            self.lkck_dial3_lbl.setVisible(False)
            self.lkck_dial4_lbl.setVisible(False)
            self.lkck_dial5_lbl.setVisible(False)
            self.lkck_dial6_lbl.setVisible(False)
        
    ## Vanguard
        
    @pyqtSlot()        
    def connect_vanguard_meth(self):
        
        baud_rate_vanguard= 9600
        bits_vanguard = 8
        parity_vanguard = visa.constants.Parity.none
        stop_bit_vanguard = visa.constants.StopBits.one
        flow_control_vanguard= 0 # hardware control ?
        timeout_vanguard = 2000 # ms
        # read_termination_vanguard  = '\n'
        # write_termination_vanguard = read_termination_vanguard
        
        current_txt = self.vanguard_com_combo.currentText()
        # for pyvisa and not pyvisa-py
        # if current_txt[6] == '(':
        #     current_txt = current_txt[0:6]
        # else:
        #     current_txt = current_txt[0:7]
        
        ressource_vanguard = '%s' % current_txt
        print('ressource_vanguard =', ressource_vanguard)
        
        rm = visa.ResourceManager('@py')
        self.vanguard = rm.open_resource(ressource_vanguard)
        
        self.vanguard.baud_rate = baud_rate_vanguard 
        self.vanguard.data_bits = bits_vanguard 
        self.vanguard.parity = parity_vanguard 
        self.vanguard.stop_bits = stop_bit_vanguard 
        self.vanguard.flow_control = flow_control_vanguard 
        self.vanguard.timeout = timeout_vanguard 
        # self.vanguard.read_termination  = read_termination_vanguard 
        # self.vanguard.write_termination = write_termination_vanguard
        # 
        # self.vanguard_heatup_progressBar.setValue(0)
        # 
        # self.query_last_pwr_cmd_vanguard_signal.emit()
        # self.vanguard_get_param_status_signal.emit()
        
        self.vanguard_heatup_progressBar.setValue(0)
        
        self.query_ID_vanguard_meth()
              
    def query_ID_vanguard_meth(self):
        
        bb = self.vanguard.query('*IDN?')

        if bool(bb): # True if is detected
        
            self.terminal_log_2_edt.append(bb)
            
            # activate buttons
            self.vg_gb_shutter.setEnabled(True)
            self.on_vanguard_push.setEnabled(True)
            self.off_vanguard_push.setEnabled(True)
            self.vanguard_param_status_query_push.setEnabled(True)
            
            self.vanguard_get_param_status_signal.emit()
        
        else:
            
            print('Vanguard not detected')
        
    @pyqtSlot()        
    def get_param_status_vanguard_meth(self):  
    
        # shutter
        
        stat_shutter = self.vanguard.query('SHUTter?')
        
        # print('stat_shutter = ', stat_shutter)
        
        if int(stat_shutter): 
            self.shutter_open_vg_radio.setChecked(True) # shutter open)
            print('shutter is open')
        else:
            self.shutter_open_vg_radio.setChecked(False) # shutter closed)
            print('shutter is closed')
        
        # diode 0 does not work

        # diode 1
        bb = self.vanguard.query('READ:DIODE1:CURRent?')
        
        stat_diode1 = float(bb[0:len(bb)-3]) # ex is '0.12A1\n' for 1 if OFF
        
        self.vanguard_diode1_LCD.display(stat_diode1)
        
        # diode 2
        bb = self.vanguard.query('READ:DIODE2:CURRent?')
        
        stat_diode2 = float(bb[0:len(bb)-3]) # ex is  for 0
        
        self.vanguard_diode2_LCD.display(stat_diode2)
        
        current_min = 0.15 # A
        current_threshold = 13 #A
        
        if (stat_diode1 < current_min and stat_diode2 < current_min):
            self.vanguard_status_edt.setText('Laser is OFF')
        elif stat_diode1 > current_threshold:
            self.vanguard_status_edt.setText('Laser is ON at full power')
        else:
            self.vanguard_status_edt.setText('Laser is turning on ...')
        
    # @pyqtSlot()        
    # def get_diodes_temp_millenia_meth(self):
        
        bb = self.vanguard.query('READ:DIODE1:TEMPerature?')
        temp_diode1 = float(bb[0:len(bb)-3]) # 
        
        self.vanguard_diode1_temp_LCD.display(temp_diode1)
        
        bb = self.vanguard.query('READ:DIODE2:TEMPerature?')
        temp_diode2 = float(bb[0:len(bb)-3]) # 
        
        self.vanguard_diode2_temp_LCD.display(temp_diode2)
        
        
        if (temp_diode1 > self.temp_diode_max_vg or temp_diode2 > self.temp_diode_max_vg):
            self.terminal_log_2_edt.setTextColor(QtGui.QColor('red'))
            self.terminal_log_2_edt.append('WARNING : temperature too high !')
     
    # heatsinks
    
        bb = self.vanguard.query('READ:DIODE1:HeatSINK?')
        hs_diode1 = float(bb[0:len(bb)-3]) # 
        
        self.vanguard_HS1_LCD.display(hs_diode1)
        
        bb = self.vanguard.query('READ:DIODE2:HeatSINK?')
        hs_diode2 = float(bb[0:len(bb)-3]) # 
        
        self.vanguard_HS2_LCD.display(hs_diode2)
        
        # duration 
        bb = self.vanguard.query('READ:DIODE1:HOURs?')
        self.vanguard_duration_edt.setText('Control unit ON for %s now' % bb[0:len(bb)-3])
        
        # PCT warmed up ? 
        bb = self.vanguard.query('READ:PCTWarmedup?')
        val_wrmup = round(float(bb[0:len(bb)-2]))
        self.vanguard_heatup_progressBar.setValue(val_wrmup)
    
        
    @pyqtSlot()        
    def turn_on_vanguard_meth(self):
        
        if QtWidgets.QMessageBox.question(None, '', "Are you sure you want to turn Vanguard ON?",
                            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                            QtWidgets.QMessageBox.No) == QtWidgets.QMessageBox.Yes:
            self.vanguard.write('ON') # turn on the vanguard
            
            self.vanguard_status_edt.setText('Laser turned on : query the actual current...')
        
    @pyqtSlot()        
    def turn_off_vanguard_meth(self):
        
        if QtWidgets.QMessageBox.question(None, '', "Are you sure you want to turn Vanguard OFF?",
                            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                            QtWidgets.QMessageBox.No) == QtWidgets.QMessageBox.Yes:
            
            self.shutter_open_vg_radio.setChecked(False) # shutter open is checked
            
            self.vanguard.write('OFF') # turn off the vanguard
            
            self.vanguard_status_edt.setText('Laser turned OFF')
            
            self.shutter_vanguard_meth()
    
    @pyqtSlot()        
    def shutter_vanguard_meth(self):
        
        if self.shutter_open_vg_radio.isChecked(): # shutter open is checked
        
            self.vanguard.write('SHUTter:1') # open shutter
            print('shutter open')
        else: # shutter closed is checked
            
            self.vanguard.write('SHUTter:0') # close the shutter
            print('shutter closed')
            
    @pyqtSlot()        
    def vg_chck_meth(self):
               
        if self.vg_chck.isChecked(): # Vanguard menus
            
            self.on_vanguard_push.setVisible(True)
            self.off_vanguard_push.setVisible(True)
            self.vg_gb_shutter.setVisible(True)
            self.vanguard_param_status_query_push.setVisible(True)
            self.vg_dur_lbl.setVisible(True)
            self.vanguard_duration_edt.setVisible(True)
            self.vanguard_connect_button.setVisible(True)
            self.vg_stat_lbl.setVisible(True)
            self.vanguard_com_combo.setVisible(True)
    
        else: # no Vanguard menus
        
            self.on_vanguard_push.setVisible(False)
            self.off_vanguard_push.setVisible(False)
            self.vg_gb_shutter.setVisible(False)
            self.vanguard_param_status_query_push.setVisible(False)
            self.vg_dur_lbl.setVisible(False)
            self.vanguard_duration_edt.setVisible(False)
            self.vanguard_connect_button.setVisible(False)
            self.vg_stat_lbl.setVisible(False)
            self.vanguard_com_combo.setVisible(False)
            self.vg_expert_chck.setChecked(False)
            
        self.vg_expert_meth() # hide some buttons
     
    @pyqtSlot()        
    def vg_expert_meth(self):  
         
        if self.vg_expert_chck.isChecked(): # expert mode
            
            self.vanguard_diode1_LCD.setVisible(True)
            self.vanguard_diode2_LCD.setVisible(True)
            self.vg_amp1_lbl.setVisible(True)
            self.vg_amp2_lbl.setVisible(True)
            self.vg_amp3_lbl.setVisible(True)
            self.vg_amp4_lbl.setVisible(True)
            self.vg_amp5_lbl.setVisible(True)
            self.vg_amp6_lbl.setVisible(True)
            self.vg_amp7_lbl.setVisible(True)
            self.vg_amp8_lbl.setVisible(True)
            self.vg_temp1_lbl.setVisible(True)
            self.vg_temp2_lbl.setVisible(True)
            self.vg_temp3_lbl.setVisible(True)
            self.vg_temp4_lbl.setVisible(True)
            self.vg_temp5_lbl.setVisible(True)
            self.vg_temp6_lbl.setVisible(True)
            self.vanguard_diode1_temp_LCD.setVisible(True)
            self.vanguard_diode2_temp_LCD.setVisible(True)
            self.vanguard_HS1_LCD.setVisible(True)
            self.vanguard_HS2_LCD.setVisible(True)
            self.vg_pct_lbl.setVisible(True)
            self.vanguard_heatup_progressBar.setVisible(True)
 
            
        else: # no expert mode
        
            self.vanguard_diode1_LCD.setVisible(False)
            self.vanguard_diode2_LCD.setVisible(False)
            self.vg_amp1_lbl.setVisible(False)
            self.vg_amp2_lbl.setVisible(False)
            self.vg_amp3_lbl.setVisible(False)
            self.vg_amp4_lbl.setVisible(False)
            self.vg_amp5_lbl.setVisible(False)
            self.vg_amp6_lbl.setVisible(False)
            self.vg_amp7_lbl.setVisible(False)
            self.vg_amp8_lbl.setVisible(False)
            self.vg_temp1_lbl.setVisible(False)
            self.vg_temp2_lbl.setVisible(False)
            self.vg_temp3_lbl.setVisible(False)
            self.vg_temp4_lbl.setVisible(False)
            self.vg_temp5_lbl.setVisible(False)
            self.vg_temp6_lbl.setVisible(False)
            self.vanguard_diode1_temp_LCD.setVisible(False)
            self.vanguard_diode2_temp_LCD.setVisible(False)
            self.vanguard_HS1_LCD.setVisible(False)
            self.vanguard_HS2_LCD.setVisible(False)
            self.vg_pct_lbl.setVisible(False)
            self.vanguard_heatup_progressBar.setVisible(False)
