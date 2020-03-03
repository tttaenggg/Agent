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
        try:
            print("Get Status Interact Lighting")
            # open connection
            # tn = telnetlib.Telnet(self.get_variable("ip"), self.get_variable("port"))
            # print(tn)

            # tn.set_debuglevel(100)

            # read data
            # data = tn.read_all()
            # print("Data: {}".format(data))

            # closed connection
            # tn.close()

        except Exception as err:
            print("Error: cannot connect host/port")

    def printDeviceStatus(self):
        # now we can access the contents of the JSON like any other Python object
        print(" the current status is as follows:")
        print(" label = {}".format(self.get_variable('label')))

    # setDeviceStatus(postmsg), isPostmsgValid(postmsg), convertPostMsg(postmsg)
    def setDeviceStatus(self, postmsg):
        setDeviceStatusResult = True

        if self.isPostMsgValid(postmsg) == True:  # check if the data is valid

            # _data = json.dumps(self.convertPostMsg(postmsg))
            # _data = _data.encode(encoding='utf_8')
            _data = self.convertPostMsg(postmsg)
            print("DATA status = {}".format(_data))

            # get access token
            access_token = self.get_token()

            # send data
            try:
                url = "https://api.interact-lighting.com/interact/api/v1/officeCloud/lightingSpaces/" + self.get_variable('uuid') + "/lightState"
                header = {"Content-Type": "application/json",
                           "Authorization": "Bearer " + access_token}

                response = requests.put(url, data=json.dumps(_data), headers=header)
                print("Status Code = {}".format(response.content))
                self.set_variable('status', _data)

            except Exception as err:
                print("ERROR: {}".format(err))
                print("ERROR: classAPI_Interact_Lighting connection failure! @ setDeviceStatus")
                setDeviceStatusResult = False
        else:
            print("The POST message is invalid, try again\n")

        return setDeviceStatusResult

    def isPostMsgValid(self, postmsg):  # check validity of postmsg
        dataValidity = True
        # TODO algo to check whether postmsg is valid
        return dataValidity

    def convertPostMsg(self, postmsg):
        msgToDevice = {}

        for k, v in postmsg.items():
            if str(k) == 'status':
                msgToDevice['state'] = postmsg['status'].upper()  # off, on, automatic, dim
            elif str(k) == 'level':
                msgToDevice['level'] = postmsg['level']
            else:
                msgToDevice[k] = v

        return msgToDevice

    def get_token(self):
        try:
            url = "https://api.interact-lighting.com/oauth/accesstoken"
            header = {"Content-Type": "application/x-www-form-urlencoded"}
            auth = ('phanumat.saa@pea.co.th', 'Pea2534+')
            data = {"app_key": "Bq0kEixitmZx4rfIEalsU4BZItpxcvbQ",
                    "app_secret": "GEBks337G8hXeoOC",
                    "service": "cb"}
            response = requests.post(url, auth=auth, data=data, headers=header)
            result = json.loads(response.text)
            return result["token"]
        except Exception as err:
            print(err)

    # ----------------------------------------------------------------------


# This main method will not be executed when this class is used as a module
def main():

    interact = API(model='Interact', api='API3', agent_id='25INTF73D39F6', types='lighting',
                   uuid='f73d39f6-432c-4593-91ca-db836c45d1e0')

    # interact.setDeviceStatus({"status": "on"})
    # interact.setDeviceStatus({"status": "off"})
    interact.setDeviceStatus({"status": "automatic"})
    # interact.setDeviceStatus({"status": "dim", "level": 10})
    # time.sleep(3)


if __name__ == "__main__": main()
