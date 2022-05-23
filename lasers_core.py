# -*- coding: utf-8 -*-
"""
Created on Mon July 24 16:35:13 2017

@author: Maxime PINSARD
@edits for Vanguard full control : Arjun David RAO
"""
import sys

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.uic import loadUiType
from PyQt5.QtCore import pyqtSignal, pyqtSlot

print('Importing VISA ...')

import pyvisa as visa

print('VISA ok ok.')

Ui_lasersWindow, QlasersWindow = loadUiType('lasers_gui.ui')  # loading the dialog box for jobs


class Lasers_GUI(QlasersWindow, Ui_lasersWindow):
    """
    pyqtsginals go here 
    """

    vanguard_get_param_status_signal = pyqtSignal()

    def __init__(self, parent=None):
        """
        var init go here 
        """

        super(Lasers_GUI, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)

        # when you want to destroy the dialog set this to True
        self._want_to_close = False
        self.close_gui_push.clicked.connect(self.quit_gui_lasers_meth)
        self.wrn_msg_lbl.setVisible(False)

        self.first_read = 1
        self.val_wrmup_current = 0  # init

        self.vanguard_connect_button.clicked.connect(self.connect_vanguard_meth)
        self.vanguard_param_status_query_push.clicked.connect(self.get_param_status_vanguard_meth)
        self.vanguard_get_param_status_signal.connect(self.get_param_status_vanguard_meth)

        self.on_vanguard_push.clicked.connect(self.turn_on_vanguard_meth)
        self.off_vanguard_push.clicked.connect(self.turn_off_vanguard_meth)

        self.autotune_start.clicked.connect(self.thg_autotune_start)
        self.autotune_stop.clicked.connect(self.thg_autotune_stop)

        self.temp_diode_max_vg = 30  # °C

        self.shutter_open_vg_radio.clicked.connect(self.shutter_vanguard_meth)
        self.shutter_close_vg_radio.clicked.connect(self.shutter_vanguard_meth)

        self.THG_change_position.clicked.connect(self.thg_change)
        self.SESAM_change_position.clicked.connect(self.SESAM_change)

        self.vg_gb_shutter.setEnabled(False)
        self.on_vanguard_push.setEnabled(False)
        self.autotune_start.setEnabled(False)
        self.autotune_stop.setEnabled(False)
        self.off_vanguard_push.setEnabled(False)
        self.vanguard_param_status_query_push.setEnabled(False)

        self.vg_chck.stateChanged.connect(self.vg_chck_meth)
        self.vg_chck_meth()  # hide the buttons

        self.vg_expert_chck.stateChanged.connect(self.vg_expert_meth)
        self.vg_autotune_chck.stateChanged.connect(self.vg_autotune_meth)

    @pyqtSlot()
    def quit_gui_lasers_meth(self):

        if QtWidgets.QMessageBox.question(None, '', "Are you sure you want to quit?",
                                          QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                          QtWidgets.QMessageBox.No) == QtWidgets.QMessageBox.Yes:
            print("User chose to close ...")
            # QApplication.quit()

            if hasattr(self, 'vanguard'):
                self.vanguard.close()



            print('Terminating  ...')

            # time.sleep(2)
            sys.exit()
            self.close()
            print('terminated.')

    def closeEvent(self,
                   event):  # method to overwrite the close event, because otherwise the object is no longer available
        # self.deleteLater()
        if self._want_to_close:

            super(Lasers_GUI, self).closeEvent(event)
        else:
            event.ignore()
            self.setWindowState(QtCore.Qt.WindowMinimized)

    ## Vanguard

    @pyqtSlot()
    def connect_vanguard_meth(self):

        baud_rate_vanguard = 9600
        bits_vanguard = 8
        parity_vanguard = visa.constants.Parity.none
        stop_bit_vanguard = visa.constants.StopBits.one
        flow_control_vanguard = 0  # hardware control ?
        timeout_vanguard = 2000  # ms
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

        if bool(bb):  # True if is detected

            self.terminal_log_2_edt.append(bb)

            # activate buttons
            self.vg_gb_shutter.setEnabled(True)
            self.on_vanguard_push.setEnabled(True)
            self.off_vanguard_push.setEnabled(True)
            self.vanguard_param_status_query_push.setEnabled(True)
            self.thg_autotune_stop.setEnabled(True)
            self.thg_autotune_start.setEnabled(True)
            # self.thg_autotune_start.setEnab
            self.vanguard_get_param_status_signal.emit()

        else:
            self.terminal_log_2_edt.append(bb)

            # activate buttons
            self.vg_gb_shutter.setEnabled(True)
            self.on_vanguard_push.setEnabled(True)
            self.off_vanguard_push.setEnabled(True)
            self.vanguard_param_status_query_push.setEnabled(True)
            # self.thg_autotune_start.setEnab
            self.vanguard_get_param_status_signal.emit()
            print('Vanguard not detected')

    @pyqtSlot()
    def get_param_status_vanguard_meth(self):

        # shutter

        stat_shutter = self.vanguard.query('SHUTter?')

        # print('stat_shutter = ', stat_shutter)

        if int(stat_shutter):
            self.shutter_open_vg_radio.setChecked(True)  # shutter open)
            print('shutter is open')
        else:
            self.shutter_open_vg_radio.setChecked(False)  # shutter closed)
            print('shutter is closed')

        # diode 0 does not work

        # diode 1
        bb = self.vanguard.query('READ:DIODE1:CURRent?')

        stat_diode1 = float(bb[0:len(bb) - 3])  # ex is '0.12A1\n' for 1 if OFF

        self.vanguard_diode1_LCD.display(stat_diode1)

        # diode 2
        bb = self.vanguard.query('READ:DIODE2:CURRent?')

        stat_diode2 = float(bb[0:len(bb) - 3])  # ex is  for 0

        self.vanguard_diode2_LCD.display(stat_diode2)

        current_min = 0.15  # A
        current_threshold = 13  # A

        if (stat_diode1 < current_min and stat_diode2 < current_min):
            self.vanguard_status_edt.setText('Laser is OFF')
        elif stat_diode1 > current_threshold:
            self.vanguard_status_edt.setText('Laser is ON at full power')
        else:
            self.vanguard_status_edt.setText('Laser is turning on ...')

        bb = self.vanguard.query('READ:DIODE1:TEMPerature?')
        temp_diode1 = float(bb[0:len(bb) - 3])  #

        self.vanguard_diode1_temp_LCD.display(temp_diode1)

        bb = self.vanguard.query('READ:DIODE2:TEMPerature?')
        temp_diode2 = float(bb[0:len(bb) - 3])  #

        self.vanguard_diode2_temp_LCD.display(temp_diode2)

        if (temp_diode1 > self.temp_diode_max_vg or temp_diode2 > self.temp_diode_max_vg):
            self.terminal_log_2_edt.setTextColor(QtGui.QColor('red'))
            self.terminal_log_2_edt.append('WARNING : temperature too high !')

        # heatsinks

        bb = self.vanguard.query('READ:DIODE1:HeatSINK?')
        hs_diode1 = float(bb[0:len(bb) - 3])  #

        self.vanguard_HS1_LCD.display(hs_diode1)

        bb = self.vanguard.query('READ:DIODE2:HeatSINK?')
        hs_diode2 = float(bb[0:len(bb) - 3])  #

        self.vanguard_HS2_LCD.display(hs_diode2)

        # duration 
        bb = self.vanguard.query('READ:DIODE1:HOURs?')
        self.vanguard_duration_edt.setText('Control unit ON for %s now' % bb[0:len(bb) - 3])

        # thg duration
        bb = self.vanguard.query('READ:THG:HOURs?')
        self.thg_position_duration.setText('THG spot used for %s' % bb[0:len(bb) - 3])

        # thg spot position
        bb = self.vanguard.query('READ:THG:SPOT?')
        spot = float(bb[0:len(bb) - 3])  #
        self.vanguard_thg_spot_position.display(spot)

        # thg x position
        bb = self.vanguard.query('READ:THG:XPOS?')
        xpos = float(bb[0:len(bb) - 3])  #
        self.vanguard_thg_x_position.display(xpos)

        # thg y position
        bb = self.vanguard.query('READ:THG:YPOS?')
        ypos = float(bb[0:len(bb) - 3])  #
        self.vanguard_thg_y_position.display(ypos)

        # sesam position
        bb = self.vanguard.query('READ:QW:XPOS?')
        sesam = float(bb[0:len(bb) - 3])  #
        self.sesam_position.display(sesam)

        # sesam duration
        bb = self.vanguard.query('READ:QW:HOUR?')
        self.thg_position_duration.setText('SESAM spot used for %s' % bb[0:len(bb) - 3])

        # PCT warmed up ? 
        bb = self.vanguard.query('READ:PCTW?')
        val_wrmup = round(float(bb[0:len(bb) - 2]))
        self.vanguard_heatup_progressBar.setValue(val_wrmup)

    @pyqtSlot()
    def turn_on_vanguard_meth(self):

        if QtWidgets.QMessageBox.question(None, '', "Are you sure you want to turn Vanguard ON?",
                                          QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                          QtWidgets.QMessageBox.No) == QtWidgets.QMessageBox.Yes:
            self.vanguard.write('ON')  # turn on the vanguard

            self.vanguard_status_edt.setText('Laser turned on : query the actual current...')

    @pyqtSlot()
    def turn_off_vanguard_meth(self):

        if QtWidgets.QMessageBox.question(None, '', "Are you sure you want to turn Vanguard OFF?",
                                          QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                          QtWidgets.QMessageBox.No) == QtWidgets.QMessageBox.Yes:
            self.shutter_open_vg_radio.setChecked(False)  # shutter open is checked

            self.vanguard.write('OFF')  # turn off the vanguard

            self.vanguard_status_edt.setText('Laser turned OFF')

            self.shutter_vanguard_meth()

    @pyqtSlot()
    def thg_autotune_start(self):

        if QtWidgets.QMessageBox.question(None, '', "Are you sure you want to autotune the THG?",
                                          QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                          QtWidgets.QMessageBox.No) == QtWidgets.QMessageBox.Yes:
            if QtWidgets.QMessageBox.question(None, '', "Has the laser been operating for 5 mins?",
                                              QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                              QtWidgets.QMessageBox.No) == QtWidgets.QMessageBox.Yes:
                # self.shutter_open_vg_radio.setChecked(False)  # shutter open is checked
                if self.shutter_open_vg_radio.isChecked():
                    # self.vanguard.write('CONT:THG:AUTO 1')  # start autotune process # TODO test without sending query..

                    self.vanguard_status_edt.setText('Vanguard autotune in progress\n')
                else:
                    self.terminal_log_2_edt.setText('ERR: Vanguard shutter is closed.\n')
                upd = self.vanguard.query('CONT:THG:AUTO?')

                print(f'vanguard autotune query {upd}')

    @pyqtSlot()
    def thg_autotune_stop(self):

        if QtWidgets.QMessageBox.question(None, '', "STOP autotune?",
                                          QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                          QtWidgets.QMessageBox.No) == QtWidgets.QMessageBox.Yes:
            # self.vanguard.write('CONT:THG:AUTO 0')  # end autotune process # TODO test without running to check scripting works then uncomment

            self.vanguard_status_edt.setText('Vanguard autotune terminated...\n')
        upd = self.vanguard.query('CONT:THG:AUTO?')

        print(f'vanguard autotune ? query returns : {upd}')

    @pyqtSlot()
    def shutter_vanguard_meth(self):

        if self.shutter_open_vg_radio.isChecked():  # shutter open is checked

            self.vanguard.write('SHUTter:1')  # open shutter
            print('shutter open')
        else:  # shutter closed is checked

            self.vanguard.write('SHUTter:0')  # close the shutter
            print('shutter closed')

    @pyqtSlot()
    def thg_change(self):
        if QtWidgets.QMessageBox.question(None, '', "Change THG crystal position?",
                                          QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                          QtWidgets.QMessageBox.No) == QtWidgets.QMessageBox.Yes:
            new_x_pos = str(self.vanguard_change_THG_1.currentText())
            new_y_pos = str(self.vanguard_change_THG_2.currentText())
            old_x_pos = self.vanguard_thg_x_position.value()
            old_y_pos = self.vanguard_thg_y_position.value()

            if not new_x_pos == old_x_pos:
                # self.vanguard.query(f'CONT:THG:xPOS {int(new_x_pos)}') # TODO insert query code for changing crystal
                print(f'THG crystal changed to X={new_X_pos}')
            if not new_y_pos == old_y_pos:
                # self.vanguard.query(f'CONT:THG:YPOS {int(new_y_pos)}') # TODO uncheck query code for changing crystal
                print(f'THG crystal changed to Y={new_Y_pos}')

            else:
                print(
                    f'new x pos = {new_x_pos} and old x pos = {old_x_pos}\n new y pos = {new_y_pos} and old y pos = {old_y_pos}')
                pass

    @pyqtSlot()
    def SESAM_change(self):
        if QtWidgets.QMessageBox.question(None, '', "Change SESAM position?",
                                          QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                          QtWidgets.QMessageBox.No) == QtWidgets.QMessageBox.Yes:
            new_SESAM_pos = str(self.vanguard_change_SESAM.currentText())
            bb = self.vanguard.query('READ:QW:XPOS?')
            old_SESAM_pos = str(bb[0:len(bb) - 3])
            print(f'new_SESAM_pos = {new_SESAM_pos}, old_SESAM_pos = {old_SESAM_pos}')

            if not old_SESAM_pos == new_SESAM_pos:
                # self.vanguard.query(f'CONT:QW:XPOS {int(new_SESAM_pos)}')
                print(f'SESAM crystal changed to Y={new_SESAM_pos}')

    @pyqtSlot()
    def vg_chck_meth(self):

        if self.vg_chck.isChecked():  # Vanguard menus

            self.on_vanguard_push.setVisible(True)
            self.off_vanguard_push.setVisible(True)
            self.vg_gb_shutter.setVisible(True)
            self.vanguard_param_status_query_push.setVisible(True)
            self.vg_dur_lbl.setVisible(True)
            self.vanguard_duration_edt.setVisible(True)
            self.vanguard_connect_button.setVisible(True)
            self.vg_stat_lbl.setVisible(True)
            self.vanguard_com_combo.setVisible(True)

        else:  # no Vanguard menus

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
            self.vg_autotune_chck.setChecked(False)

        self.vg_expert_meth()  # hide some buttons
        self.vg_autotune_meth()

    @pyqtSlot()
    def vg_expert_meth(self):

        if self.vg_expert_chck.isChecked():  # expert mode

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


        else:  # no expert mode

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

    @pyqtSlot()
    # thg autotune part of vanguard window
    def vg_autotune_meth(self):

        if self.vg_autotune_chck.isChecked():  # thg autotune mode

            self.thg_dur_lbl.setVisible(True)
            self.thg_position_duration.setVisible(True)
            self.vanguard_thg_spot_position.setVisible(True)
            self.vanguard_thg_x_position.setVisible(True)
            self.vanguard_thg_y_position.setVisible(True)
            self.vg_thg_lbl_9.setVisible(True)
            self.vg_thg_lbl_5.setVisible(True)
            self.vg_thg_lbl_6.setVisible(True)
            self.vg_thg_lbl_3.setVisible(True)
            self.vg_thg_lbl_4.setVisible(True)
            self.vg_thg_lbl_2.setVisible(True)
            self.sesam_position.setVisible(True)
            self.sesam_position_duration.setVisible(True)
            self.thg_dur_lbl.setVisible(True)
            self.thg_position_duration.setVisible(True)
            self.thg_dur_lbl_2.setVisible(True)
            self.vanguard_change_THG_1.setVisible(True)
            self.vanguard_change_THG_2.setVisible(True)
            self.SESAM_change_position.setVisible(True)
            self.vg_thg_lbl_7.setVisible(True)
            self.vg_thg_lbl_8.setVisible(True)
            self.autotune_start.setVisible(True)
            self.autotune_stop.setVisible(True)
            self.vanguard_change_SESAM.setVisible(True)
            self.vg_sesam_lbl_3.setVisible(True)
            self.THG_change_position.setVisible(True)



        else:  # no autotune mode

            self.thg_dur_lbl.setVisible(False)
            self.thg_position_duration.setVisible(False)
            self.vanguard_thg_spot_position.setVisible(False)
            self.vanguard_thg_x_position.setVisible(False)
            self.vanguard_thg_y_position.setVisible(False)
            self.vg_thg_lbl_9.setVisible(False)
            self.vg_thg_lbl_5.setVisible(False)
            self.vg_thg_lbl_6.setVisible(False)
            self.vg_thg_lbl_3.setVisible(False)
            self.vg_thg_lbl_4.setVisible(False)
            self.vg_thg_lbl_2.setVisible(False)
            self.sesam_position.setVisible(False)
            self.sesam_position_duration.setVisible(False)
            self.thg_dur_lbl.setVisible(False)
            self.thg_position_duration.setVisible(False)
            self.thg_dur_lbl_2.setVisible(False)
            self.vanguard_change_THG_1.setVisible(False)
            self.vanguard_change_THG_2.setVisible(False)
            self.SESAM_change_position.setVisible(False)
            self.vg_thg_lbl_7.setVisible(False)
            self.vg_thg_lbl_8.setVisible(False)
            self.autotune_start.setVisible(False)
            self.autotune_stop.setVisible(False)
            self.vanguard_change_SESAM.setVisible(False)
            self.vg_sesam_lbl_3.setVisible(False)
            self.THG_change_position.setVisible(False)
