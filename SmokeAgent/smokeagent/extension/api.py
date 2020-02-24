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
    smoke            GET          clear/alarm
    carbonMonoxide   GET          clear/alarm
    battery          GET          battery
    alarmState       GET          clear/alarm
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
        self.set_variable('smoke', str(conve_json["smoke"]).upper())
        self.set_variable('carbonMonoxide', str(conve_json["carbonMonoxide"]).upper())
        self.set_variable('battery', str(conve_json["battery"]).upper())
        self.set_variable('alarmState', str(conve_json["alarmState"]).upper())

    def printDeviceStatus(self):
        print(" the current status is as follows:")
        print(" unitTime = {}".format(self.get_variable('unitTime')))
        print(" device_type = {}".format(self.get_variable('device_type')))
        print(" device_label = {}".format(self.get_variable('device_label')))
        print(" smoke = {}".format(self.get_variable('smoke')))
        print(" carbonMonoxide = {}".format(self.get_variable('carbonMonoxide')))
        print(" battery = {}".format(self.get_variable('battery')))
        print(" alarmState = {}".format(self.get_variable('alarmState')))
        print("---------------------------------------------")

def main():


    FirstAlert = API(model='Smoke',types='smoke',api='API3', agent_id='18ORC_OpenCloseAgent',
                     url = 'https://graph-ap02-apnortheast2.api.smartthings.com/api/smartapps/installations/9c0d73e3-b80b-4cbc-bc7c-b36de7d36f79/smoke/',
                     bearer = 'Bearer cfe2264b-aa9e-4983-9881-3c041f3abbb1',
                     device = 'ffc7f6ee-0594-4ec4-960e-0afae4bd315c')
    FirstAlert.getDeviceStatus()


if __name__ == "__main__": main()
