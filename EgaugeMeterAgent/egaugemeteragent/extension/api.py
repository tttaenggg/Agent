# -*- coding: utf-8 -*-
import time
import json
import requests
import socket
from struct import pack

import urllib, datetime
from xml.etree import ElementTree as ET


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
            print("Get Status eGauge Power Meter")

            # Get XML from eGauge device
            url = "http://" + self.get_variable("bearer") + ".egaug.es/cgi-bin/egauge?noteam"

            # Parse the results
            raw_data = ET.parse(urllib.urlopen(url)).getroot()
            print(raw_data)

            self.getDeviceStatusJson(raw_data)
            self.printDeviceStatus()

            if getDeviceStatusResult==True:
                self.set_variable('offline_count', 0)
            else:
                self.set_variable('offline_count', self.get_variable('offline_count')+1)
        except Exception as er:
            print (er)
            print('ERROR: classAPI_Egauge_PowerMeter failed to getDeviceStatus')

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
    meter = API(model='eGauge', api='API3', agent_id='05EGA010101', types='powermeter', device='egauge50040',
                ip='192.168.1.8', port=82)

    meter.getDeviceStatus()
    time.sleep(3)


if __name__ == "__main__": main()
