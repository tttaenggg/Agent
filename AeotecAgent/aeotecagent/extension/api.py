# -*- coding: utf-8 -*-
import json
import requests

class API:

    def __init__(self,**kwargs):

        self.variables = kwargs
        self.debug = True
        self.set_variable('offline_count',0)
        self.set_variable('connection_renew_interval',6000)
        self.only_white_bulb = None

    def renewConnection(self):
        pass

    def set_variable(self,k,v):
        self.variables[k] = v

    def get_variable(self,k):
        return self.variables.get(k, None)

    '''
    Attributes:
     ------------------------------------------------------------------------------------------
    label            GET          label in string
    type             GET          type
    unitTime         GET          time
    motion           GET          
    temperature      GET          
    battery          GET          
    tamper           GET          
    humidity         GET          
    illuminance      GET          
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
            r = requests.get(url,
                             headers=headers, timeout=20);
            print(" {0}Agent is querying its current status (status:{1}) please wait ...")
            format(self.variables.get('agent_id', None), str(r.status_code))
            print(r.status_code)
            if r.status_code == 200:
                getDeviceStatusResult = False
                self.getDeviceStatusJson(r.text)
                if self.debug is True:
                    self.printDeviceStatus()
            else:
                print (" Received an error from server, cannot retrieve results")
                getDeviceStatusResult = False

            if getDeviceStatusResult==True:
                self.set_variable('offline_count', 0)
            else:
                self.set_variable('offline_count', self.get_variable('offline_count')+1)
        except Exception as er:
            print (er)
            print('ERROR: classAPI_FirstAlert failed to getDeviceStatus')

    def getDeviceStatusJson(self, data):

        conve_json = json.loads(data)
        print(conve_json)

        self.set_variable('device_type', str(conve_json["type"]).upper())
        self.set_variable('unitTime', str(conve_json["unitTime"]))
        self.set_variable('device_label', str(conve_json["label"]).upper())
        self.set_variable('motion', str(conve_json["motion"]).upper())
        self.set_variable('temperature', str(conve_json["temperature"]).upper())
        self.set_variable('battery', str(conve_json["battery"]).upper())
        self.set_variable('tamper', str(conve_json["tamper"]).upper())
        self.set_variable('humidity', str(conve_json["humidity"]).upper())
        self.set_variable('illuminance', str(conve_json["illuminance"]).upper())

    def printDeviceStatus(self):
        print(" the current status is as follows:")
        print(" unitTime = {}".format(self.get_variable('unitTime')))
        print(" device_type = {}".format(self.get_variable('device_type')))
        print(" device_label = {}".format(self.get_variable('device_label')))
        print(" motion = {}".format(self.get_variable('motion')))
        print(" temperature = {}".format(self.get_variable('temperature')))
        print(" battery = {}".format(self.get_variable('battery')))
        print(" tamper = {}".format(self.get_variable('tamper')))
        print(" humidity = {}".format(self.get_variable('humidity')))
        print(" illuminance = {}".format(self.get_variable('illuminance')))
        print("---------------------------------------------")

def main():


    Sensor = API(model='Sensor',types='illuminances',api='API3', agent_id='18ORC_OpenCloseAgent',
                 url = 'https://graph-ap02-apnortheast2.api.smartthings.com/api/smartapps/installations/9c0d73e3-b80b-4cbc-bc7c-b36de7d36f79/illuminances/',
                 bearer = 'Bearer cfe2264b-aa9e-4983-9881-3c041f3abbb1',
                 device = 'fde4cb0d-9200-4a39-a293-7aac47daf9ea')
    Sensor.getDeviceStatus()


if __name__ == "__main__": main()
