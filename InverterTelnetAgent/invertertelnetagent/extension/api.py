# -*- coding: utf-8 -*-
import time
import json
import requests
import socket
from struct import pack

import telnetlib


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
            print("Get Status Telnet - Growatt Inverter")
            # open connection
            tn = telnetlib.Telnet(self.get_variable("ip"), self.get_variable("port"))
            print(tn)
            send_mess = '\x02\x04\x00\x00\x00\x01\x31\xF9'                                            # EDIT !!!!!!!!
            tn.write(send_mess)

            tn.set_debuglevel(100)

            # read data
            raw_data = tn.read_all()
            print("Data: {}".format(raw_data))

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
        print(data)

        # self.set_variable('device_label', str(conve_json["label"]))
        # self.set_variable('device_type', str(conve_json["type"]).upper())
        # self.set_variable('unitTime', str(conve_json["unitTime"]))
        # self.set_variable('status', str(conve_json["contact"]).upper())

    def printDeviceStatus(self):
        # now we can access the contents of the JSON like any other Python object
        print(" the current status is as follows:")
        # print(" label = {}".format(self.get_variable('label')))

    # ----------------------------------------------------------------------


# This main method will not be executed when this class is used as a module
def main():
    # -------------Kittchen----------------
    inverter = API(model='Growatt', api='API3', agent_id='28INVIN202001', types='inverter', ip='192.168.10.11', port=93)

    inverter.getDeviceStatus()
    # curtain.setDeviceStatus({"status": "p1"})
    # time.sleep(3)


if __name__ == "__main__": main()
