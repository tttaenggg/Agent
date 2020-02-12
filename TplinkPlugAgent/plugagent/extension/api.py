# -*- coding: utf-8 -*-
import time
import json
import requests
import socket
from struct import pack

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

    def encrypt(self, string):
        key = 171
        result = pack('>I', len(string))
        print(result)
        print(string)
        print(len(string))

        for i in string:

            a = key ^ i  #ord()
            key = a

            result += bytes(a)

        return str(result).encode('utf-8')

    def decrypt(self,string):
        key = 171
        result = ""
        for i in string:
            a = key ^ ord(i)
            key = ord(i)
            result += chr(a)
        return result



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
    # getDeviceStatus(), getDeviceStatusJson(data), printDeviceStatus()
    def getDeviceStatus(self):

        getDeviceStatusResult = True
        try:

            ip = self.get_variable("ip")
            port = self.get_variable("port")
            r = '{"system":{"get_sysinfo":{}}, "emeter":{"get_realtime":{}}}'
            sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock_tcp.connect((ip, port))
            sock_tcp.send(self.encrypt(r))
            da = sock_tcp.recv(2048)
            sock_tcp.close()

            energy_data = json.loads(self.decrypt(da[4:]))
            self.getDeviceStatusJson(energy_data)
            self.printDeviceStatus()

            if getDeviceStatusResult==True:
                self.set_variable('offline_count', 0)
            else:
                self.set_variable('offline_count', self.get_variable('offline_count')+1)
        except Exception as er:
            print(er)
            print('ERROR: classAPI_Tplink failed to getDeviceStatus')
            self.set_variable('offline_count', self.get_variable('offline_count')+1)

    def getDeviceStatusJson(self, data):

        conve_json = data # now we get both sysinfo + energy

        # from system data
        self.set_variable('label', str(conve_json["system"]['get_sysinfo']['dev_name']))
        self.set_variable('alias', str(conve_json["system"]['get_sysinfo']['alias']))
        self.set_variable('macaddr', ''.join(conve_json["system"]['get_sysinfo']['mac'].split(':')))
        self.set_variable('deviceId', str(conve_json["system"]['get_sysinfo']['deviceId']))
        self.set_variable('model', str(conve_json["system"]['get_sysinfo']['model']))
        if str(conve_json["system"]['get_sysinfo']['relay_state']) == '0':
            self.set_variable('status', 'OFF')
        elif str(conve_json["system"]['get_sysinfo']['relay_state']) == '1':
            self.set_variable('status', 'ON')
        else:
            print('error')
        self.set_variable('device_type', str(conve_json["system"]['get_sysinfo']['type']))
        self.set_variable('on_time', str(conve_json["system"]['get_sysinfo']['on_time']))

        # from energy data
        self.set_variable('current', conve_json['emeter']['get_realtime']['current'])
        self.set_variable('total', conve_json['emeter']['get_realtime']['total'])
        self.set_variable('voltage', conve_json['emeter']['get_realtime']['voltage'])
        self.set_variable('power', conve_json['emeter']['get_realtime']['power'])
        self.set_variable('err_code', conve_json['emeter']['get_realtime']['err_code'])

    def printDeviceStatus(self):
        # now we can access the contents of the JSON like any other Python object
        print(" the current status is as follows:")
        print(" label = {}".format(self.get_variable('label')))
        print(" alias = {}".format(self.get_variable('alias')))
        print(" macaddr = {}".format(self.get_variable('macaddr')))
        print(" deviceId = {}".format(self.get_variable('deviceId')))
        print(" model = {}".format(self.get_variable('model')))
        print(" status = {}".format(self.get_variable('status')))
        print(" on_time = {}".format(self.get_variable('on_time')))
        print(" device_type = {}".format(self.get_variable('device_type')))
        print(" current = {}".format(self.get_variable('current')))
        print(" total = {}".format(self.get_variable('total')))
        print(" voltage = {}".format(self.get_variable('voltage')))
        print(" power = {}".format(self.get_variable('power')))
        print(" err_code= {}".format(self.get_variable('err_code')))
        print("---------------------------------------------")

    # setDeviceStatus(postmsg), isPostmsgValid(postmsg), convertPostMsg(postmsg)
    def setDeviceStatus(self, postmsg):
        setDeviceStatusResult = True

        ip = self.get_variable("ip")
        port = self.get_variable("port")
        print(">>>> {}".format(ip))
        print(">>>> {}".format(port))
        print(postmsg)
        print("===============================================")
        if self.isPostMsgValid(postmsg) == True:  # check if the data is valid
            # _data = json.dumps(self.convertPostMsg(postmsg))
            _data = (self.convertPostMsg(postmsg))
            print(_data)

            _data = _data.encode(encoding='utf_8')
            print(_data)
            try:
                print("sending command")
                sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock_tcp.connect((ip, port))
                print(">>>>>>  Connected")
                print(type(_data))
                print(self.encrypt(_data))
                #
                sock_tcp.send(self.encrypt(_data))
                sock_tcp.send(_data)
                da = sock_tcp.recv(2048)
                sock_tcp.close()
                # print "Sent:     ", _data
                # print "Received: ", self.decrypt(da[4:])
                print("Successful")
            except Exception as err:
                print("ERROR: classAPI_Tplink connection failure! @ setDeviceStatus")
                print("error fail: {}".format(err))
                setDeviceStatusResult = False
        else:
            print("The POST message is invalid, try again\n")
        return setDeviceStatusResult

    def isPostMsgValid(self, postmsg):  # check validity of postmsg
        dataValidity = True
        # TODO algo to check whether postmsg is valid
        return dataValidity

    def convertPostMsg(self, postmsg):
        commands = {
            'info': '{"system":{"get_sysinfo":{}}}',
            'on': '{"system":{"set_relay_state":{"state":1}}}',
            'off': '{"system":{"set_relay_state":{"state":0}}}',
            'cloudinfo': '{"cnCloud":{"get_info":{}}}',
            'wlanscan': '{"netif":{"get_scaninfo":{"refresh":0}}}',
            'time': '{"time":{"get_time":{}}}',
            'schedule': '{"schedule":{"get_rules":{}}}',
            'countdown': '{"count_down":{"get_rules":{}}}',
            'antitheft': '{"anti_theft":{"get_rules":{}}}',
            'reboot': '{"system":{"reboot":{"delay":1}}}',
            'reset': '{"system":{"reset":{"delay":1}}}',
            'energy': '{"emeter":{"get_realtime":{}}}'
        }
        msgToDevice = {}
        if ('status' in postmsg.keys()):
            msgToDevice = commands[(postmsg['status'].lower())]
            # print postmsg['status']
            print(msgToDevice)
        # if 'STATUS' in postmsg.keys():
        #     msgToDevice['command'] = str(postmsg['STATUS'].lower().capitalize())
        #     print msgToDevice
        return msgToDevice

    # ----------------------------------------------------------------------

# This main method will not be executed when this class is used as a module
def main():

    # -------------Kittchen----------------
    TpG = API(model='TPlinkPlug', api='API3', agent_id='TPlinkPlugAgent',types='plug', ip='192.168.1.106',
                  port=9999)

    # TpG.getDeviceStatus()
    #TpG.setDeviceStatus({"status": "OFF"})
    # time.sleep(3)
    # TpG.getDeviceStatus()
    # TpG.setDeviceStatus({"status": "OFF"})
    # time.sleep(3)
    # TpG.getDeviceStatus()
    # TpG.setDeviceStatus({"status": "ON"})
    # time.sleep(3)
    # TpG.getDeviceStatus()

if __name__ == "__main__": main()
