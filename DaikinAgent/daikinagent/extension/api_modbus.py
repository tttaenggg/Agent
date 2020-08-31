# -*- coding: utf-8 -*-


import requests
import json
import time
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.constants import Defaults
class API:
    # 1. constructor : gets call every time when create a new class
    # requirements for instantiation1. model, 2.type, 3.api, 4. address
    def __init__(self,**kwargs):
        # Initialized common attributes
        self.variables = kwargs
        self.debug = True


    def set_variable(self,k,v):  # k=key, v=value
        self.variables[k] = v

    def get_variable(self,k):
        return self.variables.get(k, None)  # default of get_variable is none

    # 2. Attributes from Attributes table

    '''
    Attributes:
     ------------------------------------------------------------------------------------------
    status               GET,SET      open/close airconditioner
    set_temperature      GET,SET      change set temperature
    current_temperature  GET          show current temperature
    mode                 GET,SET      represents the operating mode
    set_humidity         GET          represents the target humidity
     ------------------------------------------------------------------------------------------

    '''
    # 3. Capabilites (methods) from Capabilities table
    '''
    API3 available methods:
    1. getDeviceStatus() GET
    2. setDeviceStatus() SET
    '''

    # ----------------------------------------------------------------------
    # getDeviceStatus(), getDeviceStatusJson(data), printDeviceStatus()
    def getDeviceStatus(self):
        url = str(self.get_variable("url"))

        Defaults.Parity = 'E'
        Defaults.Baudrate = 9600
        # read temp
        client = ModbusTcpClient(url, port=502)
        client.connect()
        print(client.connect())
        result = client.read_holding_registers(2000, 5, unit=1)

        status = (str(hex(result.registers[0])))
        statusraw = status[-1:]
        stemp = result.registers[1]
        client.close()

        if statusraw == "1":
            status = "ON"
        elif statusraw == "0":
            status = "OFF"
        else:
            status = "ON"

        set_temperature = int(stemp/10)

        if set_temperature > 30:
            set_temperature = 26
        set_humidity = '70'

        if set_temperature == '--':
            set_temperature = '20'

        if set_humidity == '--':
            set_humidity = '70'


        mode = '1'

        if mode == '1':
            strmode = 'COLD'
        if mode == '2':
            strmode = 'DEHUMDIFICATOR'
        if mode == '4':
            strmode = 'HOT'
        if mode == '0':
            strmode = 'FAN'



        fan = '5'

        if fan == '3':
            fan = '1'

        if fan == '4':
            fan = '2'

        if fan == '5':
            fan = '3'

        if fan == '6':
            fan = '4'

        if fan == '7':
            fan = '5'

        if fan == 'A':
            fan = 'AUTO'

        if fan == 'B':
            fan = 'SILENT'

        swing = '3'
        if swing == '0':
            swing = 'silent'

        if swing == '1':
            swing = 'vertical'

        if swing == '2':
            swing = 'horizontal'

        if swing == '3':
            swing = 'VH'
        self.set_variable('status', status)
        self.set_variable('current_temperature', (set_temperature))
        self.set_variable('set_temperature', set_temperature)
        self.set_variable('set_humidity', set_humidity)
        self.set_variable('mode', strmode)
        self.set_variable('fan', fan)
        self.set_variable('swing', swing)
        self.printDeviceStatus()


    def printDeviceStatus(self):

        # now we can access the contents of the JSON like any other Python object
        print(" the current status is as follows:")
        print(" status = {}".format(self.get_variable('STATUS')))
        print(" current_temperature = {}".format(self.get_variable('TEMPERATURE')))
        print(" set_temperature = {}".format(self.get_variable('SET_TEMPERATURE')))
        print(" set_humidity = {}".format(self.get_variable('SET_HUMIDITY')))
        print(" mode = {}".format(self.get_variable('MODE')))
        print(" fan = {}".format(self.get_variable('FAN_SPEED')))
        # print(" swing = {}".format(self.get_variable('swing')))
        print("---------------------------------------------")

    # setDeviceStatus(postmsg), isPostmsgValid(postmsg), convertPostMsg(postmsg)
    def setDeviceStatus(self, postmsg):
        url = str(self.get_variable("url"))
        # postmsg = str(postmsg)

        Defaults.Parity = 'E'
        Defaults.Baudrate = 9600
        # read temp

        for k, v in postmsg.items():
            if k == 'status':
                if (postmsg['status']) == "ON":

                    # seton
                    client = ModbusTcpClient(url, port=502)
                    client.connect()
                    print(client.connect())
                    result = client.write_register(2000, 1101, unit=1)  # open /close
                    print("on")
                    client.close()


                elif (postmsg['status']) == "OFF":
                    # set off
                    client = ModbusTcpClient(url, port=502)
                    client.connect()
                    print(client.connect())
                    result = client.write_register(2000, 1100, unit=1)  # open /close
                    print("off")
                    client.close()

            if k == 'mode':

                if (postmsg['mode']) == "COOL":
                    print("mode")


                elif (postmsg['mode']) == "DEHUMDIFICATOR":
                    print("mode")





                elif (postmsg['mode']) == "FAN":
                    print("mode")

            if k == 'fan':
                if (postmsg['fan']) == "1":
                    print("fan")

                elif (postmsg['fan']) == "2":
                    print("fan")

                elif (postmsg['fan']) == "3":
                    print("fan")

                elif (postmsg['fan']) == "4":
                    print("fan")

                elif (postmsg['fan']) == "5":
                    print("fan")

                elif (postmsg['fan']) == "AUTO":
                    print("fan")

                elif (postmsg['fan']) == "SILENT":
                    print("fan")

            if k == 'swing':
                if (postmsg['swing']) == "ON":
                    print("fan")

                elif (postmsg['swing']) == "OFF":
                    print("fan")

            if k == 'stemp':
                print ('start settemp')
                stemp = postmsg['stemp']
                client = ModbusTcpClient(url, port=502)
                client.connect()
                print(client.connect())
                settemp=  (int(stemp)*10)
                result = client.write_register(2001, settemp, unit=1)  # open /close
                print ("settemp")
                client.close()

        client.close()

    def isPostMsgValid(self, postmsg):  # check validity of postmsg
        dataValidity = True
        # TODO algo to check whether postmsg is valid
        return dataValidity


# This main method will not be executed when this class is used as a module
def main():
    # create an object with initialized data from DeviceDiscovery Agent
    # requirements for instantiation1. model, 2.type, 3.api, 4. address
    AC = API(model='daikin', type='AC', api='API', agent_id='ACAgent', url='192.168.10.239',
                                     port=502, parity='E', baudrate=9600, startregis=2006, startregisr=2012)

    # example>>>>>>>>>>>>>>>
    # AC.setDeviceStatus({"status": "ON","username": "hive5"})
    # time.sleep(2)
    # AC.setDeviceStatus({'stemp':'22'})
    # AC.setDeviceStatus({"status": "OFF"})

    # AC.setDeviceStatus({'status': 'ON', 'mode': 'COLD', 'device': '1DAIK1200138'})
    # AC.setDeviceStatus({'status': 'ON', 'device': '1DAIK1200138'})
    # time.sleep(6)
    # time.sleep(3)
    AC.getDeviceStatus()
    # AC.setDeviceStatus({'stemp':'25'})
    # time.sleep(3)
    # AC.getDeviceStatus()
    # AC.setDeviceStatus({'swing':'ON','device': '1DAIK1200138'})
if __name__ == "__main__": main()

