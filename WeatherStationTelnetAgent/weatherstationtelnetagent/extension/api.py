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
            print("Get Status Telnet - Weather Station")
            # open connection
            tn = telnetlib.Telnet(self.get_variable("ip"), self.get_variable("port"))
            print(tn)

            raw_data = {}

            # ambient temp
            send_mess = b'\x01\x03\x00\x00\x00\x01\x84\x0A'
            tn.write(send_mess)
            raw_data['ambienttemp'] = int((tn.read_some().hex())[6:-4], 16) / 10

            # radiation
            send_mess = b'\x01\x03\x00\x0E\x00\x01\xE5\xC9'
            tn.write(send_mess)
            raw_data['radiation'] = int((tn.read_some().hex())[6:-4], 16)

            # wind speed
            send_mess = b'\x01\x03\x00\x16\x00\x01\x65\xCE'
            tn.write(send_mess)
            raw_data['windspeed'] = int((tn.read_some().hex())[6:-4], 16) / 10

            # wind direction
            send_mess = b'\x01\x03\x00\x15\x00\x01\x95\xCE'
            tn.write(send_mess)
            raw_data['winddir'] = int((tn.read_some().hex())[6:-4], 16)

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
            print('ERROR: classAPI_Telnet_Wisco failed to getDeviceStatus')

    def getDeviceStatusJson(self, data):

        # conve_json = json.loads(data)
        print(data)

        self.set_variable('ambienttemp', data['ambienttemp'])
        self.set_variable('radiation', data['radiation'])
        self.set_variable('windspeed', data['windspeed'])
        self.set_variable('winddir', data['winddir'])

    def printDeviceStatus(self):
        # now we can access the contents of the JSON like any other Python object
        print(" the current status is as follows:")
        print(" ambient temp = {}".format(self.get_variable('ambienttemp')))
        print(" radiation = {}".format(self.get_variable('radiation')))
        print(" wind speed = {}".format(self.get_variable('windspeed')))
        print(" wind direction = {}".format(self.get_variable('winddir')))

    # ----------------------------------------------------------------------


# This main method will not be executed when this class is used as a module
def main():
    # -------------Kittchen----------------
    weatherstation = API(model='Wisco', api='API3', agent_id='27WIS010101', types='sensor', ip='192.168.10.11', port=93)

    weatherstation.getDeviceStatus()
    # weatherstation.sleep(3)


if __name__ == "__main__": main()
