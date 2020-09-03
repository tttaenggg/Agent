# -*- coding: utf-8 -*-
import time
import json
import requests
import socket
from struct import pack
from bs4 import BeautifulSoup

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
        import requests
        url = 'http://'+self.get_variable("ip") + "/cgi-bin/egauge?inst&tot"
        response = urllib.request.urlopen(url)
        data = response.read()  # a `bytes` object
        text = data.decode('utf-8')  # a `str`;
        soup = BeautifulSoup(text, 'xml')
        # print(soup)

        try:
            for h in soup.find_all(n="Total Usage"):
                mdb_text = h.find('i')

            try:
                mdb = abs(float(mdb_text.text))
            except:
                print("error")
        except:
            print ("error no mdb i data")

        try:
            for h in soup.find_all(n="1 Floor Plug"):
                floor1plug_text = h.find('i')
            floor1plug = abs(float(floor1plug_text.text))
        except:
            print("error no 1floorplug i data")

        try:
            for h in soup.find_all(n="1 Floor Light"):
                floor1light_text = h.find('i')
            floor1light = abs(float(floor1light_text.text))
        except:
            print("error no 1floorlight i data")

            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        try:
            for h in soup.find_all(n="1 Floor Air"):
                floor1air_text = h.find('i')
            floor1air = abs(float(floor1air_text.text))
        except:
            print("error no 1floorlight i data")

        try:
            for h in soup.find_all(n="2 Floor Plug"):
                floor2plug_text = h.find('i')
            floor2plug = abs(float(floor2plug_text.text))
        except:
            print("error no 2floorplug i data")

        try:
            for h in soup.find_all(n="2 Floor Light"):
                floor2light_text = h.find('i')
            floor2light = abs(float(floor2light_text.text))
        except:
            print("error no 2floorlight i data")

            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        try:
            for h in soup.find_all(n="2 Floor Air"):
                floor2air_text = h.find('i')
            floor2air = abs(float(floor2air_text.text))
        except:
            print("error no 2floorlight i data")


        try:
            for h in soup.find_all(n="EBD"):
                edb_text = h.find('i')
            edb = abs(float(edb_text.text))
        except:
            print("error no 2floorlight i data")

        try:
            for h in soup.find_all(n="EO Room  Air"):
                eo_room_text = h.find('i')
            eo_room = abs(float(eo_room_text.text))
        except:
            print("error no eo_room_text data")

        try:
            for h in soup.find_all(n="PV GENERTION"):
                PV_GENERTION_text = h.find('i')
            PV_GENERTION = abs(float(PV_GENERTION_text.text))
        except:
            print("error no eo_room_text data")

        try:
            for h in soup.find_all(n="Grid Import"):
                Grid_Import_text = h.find('i')
            Grid_Import = abs(float(Grid_Import_text.text))
        except:
            print("error no eo_room_text data")

        self.set_variable('mdb', str(mdb))
        self.set_variable('floor1plug', str(floor1plug))
        self.set_variable('floor1light', str(floor1light))
        self.set_variable('floor1air', str(floor1air))
        self.set_variable('floor2plug', str(floor2plug))
        self.set_variable('floor2light', str(floor2light))
        self.set_variable('floor2air', str(floor2air))
        self.set_variable('edb', str(edb))
        self.set_variable('eoroom_air', str(eo_room))
        self.set_variable('PV_GENERTION', str(PV_GENERTION))
        self.set_variable('Grid_Import', str(Grid_Import))
        self.printDeviceStatus()

    def printDeviceStatus(self):
        # now we can access the contents of the JSON like any other Python object
        print(" the current status is as follows:")
        print(" mdb = {}".format(self.get_variable('mdb')))
        print(" floor1plug = {}".format(self.get_variable('floor1plug')))
        print(" floor1light = {}".format(self.get_variable('floor1light')))
        print(" floor1air = {}".format(self.get_variable('floor1air')))
        print(" floor2plug = {}".format(self.get_variable('floor2plug')))
        print(" floor2light = {}".format(self.get_variable('floor2light')))
        print(" floor2air = {}".format(self.get_variable('floor2air')))
        print(" floor2air = {}".format(self.get_variable('floor2air')))
        print(" eoroom_air = {}".format(self.get_variable('eoroom_air')))
        print(" edb = {}".format(self.get_variable('edb')))
        print(" PV_GENERTION = {}".format(self.get_variable('PV_GENERTION')))
        print(" Grid_Import = {}".format(self.get_variable('Grid_Import')))


    # ----------------------------------------------------------------------


# This main method will not be executed when this class is used as a module
def main():
    # -------------Kittchen----------------
    meter = API(model='eGauge', api='API3', agent_id='05EGA010101', types='imeter', device='egauge50040',
                ip='192.168.10.21', port=82)

    meter.getDeviceStatus()
    # time.sleep(3)


if __name__ == "__main__": main()
