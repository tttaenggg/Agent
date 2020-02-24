# -*- coding: utf-8 -*-
import json
import requests

class API:
    def __init__(self,**kwargs):
        # Initialized common attributes
        self.variables = kwargs
        self.debug = True
        self.set_variable('offline_count',0)
        self.set_variable('connection_renew_interval', 6000)
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
    status           GET          status
    unitTime         GET          time
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
            print('ERROR: classAPI_OpenClose failed to getDeviceStatus')

    def getDeviceStatusJson(self, data):

        conve_json = json.loads(data)
        print(conve_json)

        self.set_variable('device_label', str(conve_json["label"]))
        self.set_variable('device_type', str(conve_json["type"]).upper())
        self.set_variable('unitTime', str(conve_json["unitTime"]))
        self.set_variable('status', str(conve_json["contact"]).upper())

    def printDeviceStatus(self):
        # now we can access the contents of the JSON like any other Python object
        print(" the current status is as follows:")
        print(" device label = {}".format(self.get_variable('device_label')))
        print(" device type = {}".format(self.get_variable('device_type')))
        print(" on_time = {}".format(self.get_variable('unitTime')))
        print(" status = {}".format(self.get_variable('status')))
        print("---------------------------------------------")

    # ----------------------------------------------------------------------

# This main method will not be executed when this class is used as a module
def main():


    OpenClosed = API(model='OpenClose', types='contactSensors', api='API3', agent_id='18ORC_OpenCloseAgent',
                    url="https://graph-ap02-apnortheast2.api.smartthings.com/api/smartapps/installations/9c0d73e3-b80b-4cbc-bc7c-b36de7d36f79/contactSensors/",
                    bearer="Bearer cfe2264b-aa9e-4983-9881-3c041f3abbb1",
                    device="83b90785-a2ed-4b5b-b119-c670eace2feb")

    OpenClosed.getDeviceStatus()

if __name__ == "__main__": main()
