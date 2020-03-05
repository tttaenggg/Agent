# -*- coding: utf-8 -*-
import time
import json
import requests
import socket
from struct import pack

import telnetlib

info_on_off = {0:'Off', 1:'On'}

info_mode_section = {0:'load priority', 1: 'Battery priority', 2:'Economic mode', 3:'peak shaving',
                     4:'multi period charging and discharging', 5:'manual dispatching', 6:'battery protection',
                     7:'backup power management', 8:'constant power discharge', 9:'forced charging mode'}

info_BMS_batt_status = {0:'Hold', 1: 'Charging and discharging disable', 2:'Charging disable', 3:'Discharging disable',
                        4:'Charging', 5:'Discharging'}


class API:
    def __init__(self, **kwargs):
        # Initialized common attributes
        self.variables = kwargs
        self.debug = True
        self.set_variable('offline_count', 0)
        self.set_variable('connection_renew_interval', 6000)

    def renewConnection(self):
        pass

    def set_variable(self, k, v):  # k=key, v=value
        self.variables[k] = v

    def get_variable(self, k):
        return self.variables.get(k, None)  # default of get_variable is none

    '''
    Attributes:
     ------------------------------------------------------------------------------------------
    label            GET          label in string
    status           GET          status
    unitTime         GET          time
    type             GET          type      
     ------------------------------------------------------------------------------------------
    '''

    '''
    API3 available methods:
    1. getDeviceStatus() GET
    2. setDeviceStatus() SET
    '''

    # ----------------------------------------------------------------------
    # getDeviceStatus(), printDeviceStatus()
    def getDeviceStatus(self):

        getDeviceStatusResult = True

        try:
            # open connection
            tn = telnetlib.Telnet(self.get_variable("ip"), self.get_variable("port"))
            print(tn)

            raw_data = {}

            # # FUNCTION CODE: 03
            # # Register:0-0x0000 ===== on/off (2b)
            # send_mess = b"\x02\x03\x00\x00\x00\x01\x84\x39"
            # tn.write(send_mess)
            # raw_data['on_off'] = (tn.read_some().hex())
            #
            # # Register:26-0x0058 ===== Mode selection (2b)
            # send_mess = b"\x02\x03\x00\x1A\x00\x01\xA5\xFE"
            # tn.write(send_mess)
            # raw_data['mode_select'] = (tn.read_some().hex())
            #
            # # Register:50-0x0032 ===== Maximum DC voltage（PV) (2b)
            # send_mess = b"\x02\x03\x00\x32\x00\x01\x25\xF6"
            # tn.write(send_mess)
            # raw_data['max_DC_volt_PV'] = (tn.read_some().hex())
            #
            # # Register:58-0x003A ===== Maximum Output power (2b)
            # send_mess = b"\x02\x03\x00\x3A\x00\x01\xA4\x34"
            # tn.write(send_mess)
            # raw_data['max_output_P'] = (tn.read_some().hex())
            #
            # # Register:74-0x004A ===== Voltage reference (2b)
            # send_mess = b"\x02\x03\x00\x4A\x00\x01\xA5\xEF"
            # tn.write(send_mess)
            # raw_data['volt_ref'] = (tn.read_some().hex())


            # -----------------------------------------------
            # FUNCTION CODE: 04
            # Register:0-0x0000 ===== PV1 Voltage (2b+-)
            # send_mess = b"\x02\x04\x00\x00\x00\x01\x31\xF9"
            # tn.write(send_mess)
            # raw_data['PV1_volt'] = (tn.read_some().hex())
            #
            # # Register:3-0x0003 ===== PV1 DC current (2b+-)
            # send_mess = b"\x02\x04\x00\x03\x00\x01\xC1\xF9"
            # tn.write(send_mess)
            # raw_data['PV1_DC_cur'] = (tn.read_some().hex())
            #
            # # Register:4-0x0004 ===== Output voltage UV (2b+-)
            # send_mess = b"\x02\x04\x00\x04\x00\x01\x70\x38"
            # tn.write(send_mess)
            # raw_data['output_volt_UV'] = (tn.read_some().hex())
            #
            # # Register:5-0x0005 ===== Output voltage VW (2b+-)
            # send_mess = b"\x02\x04\x00\x05\x00\x01\x21\xF8"
            # tn.write(send_mess)
            # raw_data['output_volt_VW'] = (tn.read_some().hex())
            #
            # # Register:6-0x0006 ===== Output voltage WU (2b+-)
            # send_mess = b"\x02\x04\x00\x06\x00\x01\xD1\xF8"
            # tn.write(send_mess)
            # raw_data['output_volt_WU'] = (tn.read_some().hex())
            #
            # # Register:16-0x0010 ===== Output frequency (2b+-)
            # send_mess = b"\x02\x04\x00\x10\x00\x01\x30\x3C"
            # tn.write(send_mess)
            # raw_data['output_freq'] = (tn.read_some().hex())

            # Register:17-0x0011 ===== Battery power (2b+-)
            send_mess = b"\x02\x04\x00\x11\x00\x01\x61\xFC"
            tn.write(send_mess)
            raw_data['batt_P'] = (tn.read_some().hex())

            # Register:21-0x0015 ===== Power grid frequency (2b+-)
            # send_mess = b"\x02\x04\x00\x15\x00\x01\x20\x3D"
            # tn.write(send_mess)
            # raw_data['P_grid_freq'] = (tn.read_some().hex())
            #
            # # Register:22-0x0016 ===== Power factor symbol (screen none) (2b+-)
            # send_mess = b"\x02\x04\x00\x16\x00\x01\xD0\x3D"
            # tn.write(send_mess)
            # raw_data['PF_symbol'] = (tn.read_some().hex())
            #
            # # Register:23-0x0017 ===== Power factor (2b+-)
            # send_mess = b"\x02\x04\x00\x17\x00\x01\x81\xFD"
            # tn.write(send_mess)
            # raw_data['PF'] = (tn.read_some().hex())
            #
            # # Register:47-0x002F ===== Battery percentage (2b+)
            # send_mess = b"\x02\x04\x00\x2F\x00\x01\x00\x30"
            # tn.write(send_mess)
            # raw_data['batt_percen'] = (tn.read_some().hex())
            #
            # # Register:49-0x0031 ===== Load active power (2b+)
            # send_mess = b"\x02\x04\x00\x31\x00\x01\x60\x36"
            # tn.write(send_mess)
            # raw_data['load_act_P'] = (tn.read_some().hex())
            #
            # # Register:51-0x0033 ===== PV1 power (2b+-)
            # send_mess = b"\x02\x04\x00\x33\x00\x01\xC1\xF6"
            # tn.write(send_mess)
            # raw_data['PV1_P'] = (tn.read_some().hex())
            #
            # # Register:53-0x0035 ===== Load current A (2b+-)
            # send_mess = b"\x02\x04\x00\x35\x00\x01\x21\xF7"
            # tn.write(send_mess)
            # raw_data['load_cur_A'] = (tn.read_some().hex())
            #
            # # Register:54-0x0036 ===== Load current B (2b+-)
            # send_mess = b"\x02\x04\x00\x36\x00\x01\xD1\xF7"
            # tn.write(send_mess)
            # raw_data['load_cur_B'] = (tn.read_some().hex())
            #
            # # Register:55-0x0037 ===== Load current C (2b+-)
            # send_mess = b"\x02\x04\x00\x37\x00\x01\x80\x37"
            # tn.write(send_mess)
            # raw_data['load_cur_C'] = (tn.read_some().hex())
            #
            # # Register:62-0x003E ===== PV daily power generation (2b+)
            # send_mess = b"\x02\x04\x00\x3E\x00\x01\x50\x35"
            # tn.write(send_mess)
            # raw_data['PV_daily_P_gen'] = (tn.read_some().hex())
            #
            # # Register:64-0x0040 ===== PV total power generation High (2b+)
            # # Register:65-0x0041 ===== PV total power generation Low (2b+)
            # send_mess = b"\x02\x04\x00\x40\x00\x02\x70\x2C"
            # tn.write(send_mess)
            # raw_data['PV_total_P_gen'] = (tn.read_some().hex())
            #
            # # Register:80-0x0050 ===== Output reactive power (2b+-)
            # send_mess = b"\x02\x04\x00\x50\x00\x01\x31\xE8"
            # tn.write(send_mess)
            # raw_data['output_react_P'] = (tn.read_some().hex())
            #
            # # Register:82-0x0052 ===== Daily load consumption (2b+)
            # send_mess = b"\x02\x04\x00\x52\x00\x01\x90\x28"
            # tn.write(send_mess)
            # raw_data['daily_load_con'] = (tn.read_some().hex())
            #
            # # Register:88-0x0058 ===== Daily power intake from grid (2b+)
            # send_mess = b"\x02\x04\x00\x58\x00\x01\xB0\x2A"
            # tn.write(send_mess)
            # raw_data['daily_P_intake_grid'] = (tn.read_some().hex())
            #
            # # Register:90-0x005A ===== Total power intake from grid High (2b+)
            # # Register:91-0x005B ===== Total power intake from grid Low (2b+)
            # send_mess = b"\x02\x04\x00\x5A\x00\x02\x51\xEB"
            # tn.write(send_mess)
            # raw_data['total_P_intake_grid'] = (tn.read_some().hex())
            #
            # # Register:94-0x005E ===== Daily power fed to grid
            # send_mess = b"\x02\x04\x00\x5E\x00\x01\x50\x2B"
            # tn.write(send_mess)
            # raw_data['daily_P_fed_grid'] = (tn.read_some().hex())
            #
            # # Register:96-0x0060 ===== Total power fed to grid High (2b+)
            # # Register:97-0x0061 ===== Total power fed to grid Low (2b+)
            # send_mess = b"\x02\x04\x00\x60\x00\x02\x71\xE6"
            # tn.write(send_mess)
            # raw_data['total_P_fed_grid'] = (tn.read_some().hex())

            # Register:108-0x006C ===== PV total power (2b+-)
            send_mess = b"\x02\x04\x00\x6C\x00\x01\xF1\xE4"
            tn.write(send_mess)
            raw_data['PV_total_P'] = (tn.read_some().hex())

            # Register:113-0x0071 ===== Output power (2b+-)
            # send_mess = b"\x02\x04\x00\x71\x00\x01\x61\xE2"
            # tn.write(send_mess)
            # raw_data['output_P'] = (tn.read_some().hex())
            #
            # # Register:166-0x00A6 ===== SOH (2b+)
            # send_mess = b"\x02\x04\x00\xA6\x00\x01\xD1\xDA"
            # tn.write(send_mess)
            # raw_data['SOH'] = (tn.read_some().hex())
            #
            # # Register:176-0x00B0 ===== BMS battery status (1b)
            # send_mess = b"\x02\x04\x00\xB0\x00\x01\x30\x1E"
            # tn.write(send_mess)
            # raw_data['BMS_batt_status'] = (tn.read_some().hex())

            for k,v in raw_data.items():
                raw_data[k] = ('0'*((int(v[4:6])*2) - len(v[6:-4]))) + v[6:-4]

            # closed connection
            tn.close()

            self.getDeviceStatusJson(raw_data)
            self.printDeviceStatus()

            if getDeviceStatusResult==True:
                self.set_variable('offline_count', 0)
            else:
                self.set_variable('offline_count', self.get_variable('offline_count')+1)
        except Exception as er:
            print (er)
            print('ERROR: classAPI_Telnet_Inverter failed to getDeviceStatus')

    def getDeviceStatusJson(self, data):

        # conve_json = json.loads(data)
        # print("data: {}".format(data))

        # self.set_variable('on_off', str(info_on_off[int(data["on_off"], 16)]))
        # self.set_variable('mode_select', str(info_mode_section[int(data["mode_select"], 16)]))
        # self.set_variable('max_DC_volt_PV', str(int(data["max_DC_volt_PV"], 16) / 10))
        # self.set_variable('max_output_P', str(int(data["max_output_P"], 16)))
        # self.set_variable('volt_ref', str(int(data["max_output_P"], 16)))

        # self.set_variable('PV1_volt', str((((int(data["PV1_volt"], 16) + 0x8000) & 0xFFFF) - 0x8000) / 10))
        # self.set_variable('PV1_DC_cur', str((((int(data["PV1_DC_cur"], 16) + 0x8000) & 0xFFFF) - 0x8000) / 10))
        # self.set_variable('output_volt_UV', str(int(data["output_volt_UV"], 16) / 10))
        # self.set_variable('output_volt_VW', str(int(data["output_volt_VW"], 16) / 10))
        # self.set_variable('output_volt_WU', str(int(data["output_volt_WU"], 16) / 10))
        # self.set_variable('output_freq', str(int(data["output_freq"], 16) / 100))
        self.set_variable('batt_P', str((((int(data["batt_P"], 16) + 0x8000) & 0xFFFF) - 0x8000) / 10))
        # self.set_variable('P_grid_freq', str(int(data["P_grid_freq"], 16) / 100))
        # self.set_variable('PF_symbol', str(int(data["PF_symbol"], 16)))
        # self.set_variable('PF', str(int(data["PF"], 16) / 1000))
        # self.set_variable('batt_percen', str(int(data["batt_percen"], 16)))
        # self.set_variable('load_act_P', str(int(data["load_act_P"], 16) / 10))
        # self.set_variable('PV1_P', str(int(data["PV1_P"], 16) / 10))
        # self.set_variable('load_cur_A', str((((int(data["load_cur_A"], 16) + 0x8000) & 0xFFFF) - 0x8000) / 10))
        # self.set_variable('load_cur_B', str((((int(data["load_cur_B"], 16) + 0x8000) & 0xFFFF) - 0x8000) / 10))
        # self.set_variable('load_cur_C', str((((int(data["load_cur_C"], 16) + 0x8000) & 0xFFFF) - 0x8000) / 10))
        # self.set_variable('PV_daily_P_gen', str(int(data["PV_daily_P_gen"], 16) / 10))
        # self.set_variable('PV_total_P_gen', str(int(data["PV_total_P_gen"], 16) / 10))
        # self.set_variable('output_react_P', str((((int(data["output_react_P"], 16) + 0x8000) & 0xFFFF) - 0x8000) / 10))
        # self.set_variable('daily_load_con', str(int(data["daily_load_con"],16)/10))
        # self.set_variable('daily_P_intake_grid', str(int(data["daily_P_intake_grid"],16)/10))
        # self.set_variable('total_P_intake_grid', str(int(data["total_P_intake_grid"],16)/10))
        # self.set_variable('daily_P_fed_grid', str(int(data["daily_P_fed_grid"],16)/10))
        # self.set_variable('total_P_fed_grid', str(int(data["total_P_fed_grid"],16)/10))
        self.set_variable('PV_total_P', str((((int(data["PV_total_P"], 16) + 0x8000) & 0xFFFF) - 0x8000)/10))
        # self.set_variable('output_P', str((((int(data["output_P"], 16) + 0x8000) & 0xFFFF) - 0x8000)/10))
        # self.set_variable('SOH', str(int(data["SOH"],16)))
        # self.set_variable('BMS_batt_status', str(info_BMS_batt_status[int(data["BMS_batt_status"][:2],16)]))


    def printDeviceStatus(self):
        # now we can access the contents of the JSON like any other Python object
        print(" the current status is as follows:")
        # print(" ON/OFF = {}".format(self.get_variable('on_off')))
        # print(" Mode selection = {}".format(self.get_variable('mode_select')))
        # print(" Maximum DC voltage（PV) = {}".format(self.get_variable('max_DC_volt_PV')))
        # print(" Maximum Output power = {}".format(self.get_variable('max_output_P')))
        # print(" Voltage reference = {}".format(self.get_variable('volt_ref')))

        # print(" PV1 Voltage = {}".format(self.get_variable('PV1_volt')))
        # print(" PV1 DC current = {}".format(self.get_variable('PV1_DC_cur')))
        # print(" Output voltage UV = {}".format(self.get_variable('output_volt_UV')))
        # print(" Output voltage VW = {}".format(self.get_variable('output_volt_VW')))
        # print(" Output voltage WU = {}".format(self.get_variable('output_volt_WU')))
        # print(" Output frequency = {}".format(self.get_variable('output_freq')))
        print(" Battery power = {}".format(self.get_variable('batt_P')))
        # print(" Power grid frequency = {}".format(self.get_variable('P_grid_freq')))
        # print(" Power factor symbol (screen none) = {}".format(self.get_variable('PF_symbol')))
        # print(" Power factor = {}".format(self.get_variable('PF')))
        # print(" Battery percentage = {}".format(self.get_variable('batt_percen')))
        # print(" Load active power = {}".format(self.get_variable('load_act_P')))
        # print(" PV1 power = {}".format(self.get_variable('PV1_P')))
        # print(" Load current A = {}".format(self.get_variable('load_cur_A')))
        # print(" Load current B = {}".format(self.get_variable('load_cur_B')))
        # print(" Load current C = {}".format(self.get_variable('load_cur_C')))
        # print(" PV daily power generation = {}".format(self.get_variable('PV_daily_P_gen')))
        # print(" PV total power generation = {}".format(self.get_variable('PV_total_P_gen')))
        # print(" Output reactive power = {}".format(self.get_variable('output_react_P')))
        # print(" Daily load consumption = {}".format(self.get_variable('daily_load_con')))
        # print(" Daily power intake from grid = {}".format(self.get_variable('daily_P_intake_grid')))
        # print(" Total power intake from grid = {}".format(self.get_variable('total_P_intake_grid')))
        # print(" Daily power fed to grid = {}".format(self.get_variable('daily_P_fed_grid')))
        # print(" Total power fed to grid = {}".format(self.get_variable('total_P_fed_grid')))
        print(" PV total power = {}".format(self.get_variable('PV_total_P')))
        # print(" Output power = {}".format(self.get_variable('output_P')))
        # print(" SOH = {}".format(self.get_variable('SOH')))
        # print(" BMS battery status = {}".format(self.get_variable('BMS_batt_status')))

    # ----------------------------------------------------------------------


# This main method will not be executed when this class is used as a module
def main():
    # -------------Kittchen----------------
    inverter = API(model='Growatt', api='API3', agent_id='28INVIN202001', types='inverter', ip='192.168.10.11', port=94)

    inverter.getDeviceStatus()
    # time.sleep(3)


if __name__ == "__main__": main()
