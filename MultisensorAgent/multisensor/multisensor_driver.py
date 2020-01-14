# -*- coding: utf-8 -*-

import json
import requests

class API:

    def __init__(self,**kwargs):
        # Initialized common attributes
        self.variables = kwargs
        self.debug = True
        self.set_variable('offline_count',0)
        self.set_variable('connection_renew_interval', 6000) # nothing to renew, right now
        self.only_white_bulb = None

    def renewConnection(self):
        pass

    def set_variable(self,k,v):  # k=key, v=value
        self.variables[k] = v

    def get_variable(self,k):
        return self.variables.get(k, None)  # default of get_variable is none

    '''
    Attributes:
     ------------------------------------------------------------------------------------------
    label            GET          label in string
    illuminance      GET          illuminance
    temperature      GET          temporary target heat setpoint (floating point in deg F)
    battery          GET          percent battery of Multisensor censor
    motion           GET          motion  status (active/inactive)
    tamper           GET          tamper  status (active/inactive)
    unitTime         GET          Hue light effect 'none' or 'colorloop'
    type             GET          type
     ------------------------------------------------------------------------------------------

    '''

    '''
    API3 available methods:
    1. getDeviceStatus() GET
    '''

    # ----------------------------------------------------------------------
    # getDeviceStatus(), getDeviceStatusJson(data), printDeviceStatus()
    def getDeviceStatus(self):
        try:
            headers = {"Authorization": self.get_variable("bearer")}
            url = str(self.get_variable("url") + self.get_variable("device"))
            url = 'https://graph-ap02-apnortheast2.api.smartthings.com/api/smartapps/installations/7833689d-a39e-40e3-bf80-67253469cd65/illuminances/6fa190f7-9349-49c3-b132-ca7d52c3773e'
            data = {'Authorization': 'Bearer c654f55b-a254-4800-b536-0fbb354ee800'}

            from urllib import request, parse
            req = request.Request(url, headers=data)  # this will make the method "POST"
            resp = request.urlopen(req)
            msg = resp.read()
            print(msg)
            self.getDeviceStatusJson(msg)
            self.printDeviceStatus()
        except Exception as er:
            print(er)
            print('ERROR: classAPI_Multisensor failed to getDeviceStatus')

    def getDeviceStatusJson(self, data):
        conve_json = json.loads(data)
        self.set_variable('label', str(conve_json["label"]).lower())
        self.set_variable('illuminance', str(conve_json["illuminance"]))
        self.set_variable('temperature', str(conve_json["temperature"]))
        self.set_variable('battery', str(conve_json["battery"]))
        self.set_variable('status', str(conve_json["motion"]).lower())
        self.set_variable('motion', str(conve_json["motion"]).lower())
        self.set_variable('tamper', str(conve_json["tamper"]).lower())
        self.set_variable('humidity', str(conve_json["humidity"]).lower())
        self.set_variable('unitTime', conve_json["unitTime"])
        self.set_variable('device_type', str(conve_json["type"]).lower())

    def printDeviceStatus(self):
        # now we can access the contents of the JSON like any other Python object
        print(" the current status is as follows:")
        print(" label = {}".format(self.get_variable('label')))
        print(" illuminance = {}".format(self.get_variable('ILLUMINANCE')))
        print(" temperature = {}".format(self.get_variable('TEMPERATURE')))
        print(" battery = {}".format(self.get_variable('BATTERY')))
        print(" STATUS = {}".format(self.get_variable('STATUS')))
        print(" MOTION = {}".format(self.get_variable('MOTION')))
        print(" tamper = {}".format(self.get_variable('TAMPER')))
        print(" humidity = {}".format(self.get_variable('HUMIDITY')))
        print(" unitTime = {}".format(self.get_variable('unitTime')))
        print(" device_type= {}".format(self.get_variable('device_type')))
        print("---------------------------------------------")

    # ----------------------------------------------------------------------

def main():

    Multisensor = API(url='https://graph-ap02-apnortheast2.api.smartthings.com/api/smartapps/installations/7833689d-a39e-40e3-bf80-67253469cd65/illuminances/',
                 bearer='Bearer c654f55b-a254-4800-b536-0fbb354ee800', device='6fa190f7-9349-49c3-b132-ca7d52c3773e')
    Multisensor.getDeviceStatus()

if __name__ == "__main__": main()
