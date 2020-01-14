# -*- coding: utf-8 -*-
from __future__ import division
import json
import requests
import datetime


class API:

    def __init__(self, **kwargs):  # default color is wh     ite
        # Initialized common attributes
        self.variables = kwargs

    # These set and get methods allow scalability
    def set_variable(self, k, v):  # k=key, v=value
        self.variables[k] = v

    def get_variable(self, k):
        return self.variables.get(k, None)  # default of get_variable is none

    def getDeviceStatus(self):

        try:

            self.get_variable('url')
            self.get_variable('client_id')
            self.get_variable('username')
            self.get_variable('password')
            self.get_variable('client_secret')

            scope = 'read_station'
            grant_type = 'password'
            content = 'application/x-www-form-urlencoded;charset=UTF-8'

            r = requests.post(
                url=self.get_variable('url'),
                headers={
                    "Content-Type": content,
                },
                data={
                    "client_id": self.get_variable('client_id'),
                    "username": self.get_variable('username'),
                    "password": self.get_variable('password'),
                    "scope": scope,
                    "client_secret": self.get_variable('client_secret'),
                    "grant_type": grant_type,
                    "device_type": self.get_variable('device_type')

                },
                verify=False
            )

            print
            "{0} Agent is querying its current status (status:{1}) at {2} please wait ...".format(
                self.variables.get('agent_id', None),
                r.status_code,
                datetime.datetime.now())
            if r.status_code == 200:  # 200 means successfully
                self.getAccessTokenJson(r.content)  # convert string data to JSON object
                # My API (3) (GET https://api.netatmo.net/api/devicelist)
                try:
                    r = requests.get(
                        url="https://api.netatmo.net/api/devicelist",
                        params={
                            "access_token": self.get_variable("access_token"),
                        },
                        verify=False
                    )

                    self.getDeviceStatusJson(r.content)
                    self.printDeviceStatus()
                except requests.exceptions.RequestException as e:
                    print('HTTP Request failed')
            else:
                print
                " Received an error from server, cannot retrieve results {}".format(r.status_code)
        except requests.exceptions.RequestException as e:
            print('HTTP Request failed')

    def getAccessTokenJson(self, data):

        _theJSON = json.loads(data)
        try:
            self.set_variable("access_token", _theJSON["access_token"])
            self.set_variable("refresh_token", _theJSON["access_token"])
            self.set_variable("scope", _theJSON["scope"][0])
            self.set_variable("expire_in", _theJSON["expire_in"])
        except:
            print
            "Error! Netatmo @getAccessTokenJson"

    def getDeviceStatusJson(self, data):

        _theJSON = json.loads(data)
        try:
            # print data
            print
            _theJSON["body"]["devices"][0]["_id"]
            self.set_variable("noise", _theJSON["body"]["devices"][0]["dashboard_data"]["Noise"])  # dB
            _temperature = float(_theJSON["body"]["devices"][0]["dashboard_data"]["Temperature"])
            self.set_variable("temperature", _temperature)  # C
            self.set_variable("humidity", _theJSON["body"]["devices"][0]["dashboard_data"]["Humidity"])  # %
            _pressure = float(_theJSON["body"]["devices"][0]["dashboard_data"]["Pressure"]) * 0.02953
            self.set_variable("pressure", _pressure)  # inHg
            self.set_variable("co2", _theJSON["body"]["devices"][0]["dashboard_data"]["CO2"])  # ppm
            self.set_variable("date_max_temp", _theJSON["body"]["devices"][0]["dashboard_data"]["date_max_temp"])
            self.set_variable("date_min_temp", _theJSON["body"]["devices"][0]["dashboard_data"]["date_min_temp"])
            _max_temperature = float(_theJSON["body"]["devices"][0]["dashboard_data"]["max_temp"])
            self.set_variable("max_temp", _max_temperature)  # C
            _min_temperature = float(_theJSON["body"]["devices"][0]["dashboard_data"]["min_temp"])
            self.set_variable("min_temp", _min_temperature)  # C
            self.set_variable("device_type", 'weather station')  # C
        except:
            print
            "Error! Netatmo Indoor @getDeviceStatusJson"

        try:
            _outdoor_temperature = float(_theJSON["body"]["modules"][0]["dashboard_data"]["Temperature"])
            self.set_variable("outdoor_temperature", _outdoor_temperature)  # C
            self.set_variable("outdoor_humidity", _theJSON["body"]["modules"][0]["dashboard_data"]["Humidity"])  # %
            self.set_variable("outdoor_date_max_temp",
                              _theJSON["body"]["modules"][0]["dashboard_data"]["date_max_temp"])
            self.set_variable("outdoor_date_min_temp",
                              _theJSON["body"]["modules"][0]["dashboard_data"]["date_min_temp"])
            _outdoor_max_temperature = float(_theJSON["body"]["modules"][0]["dashboard_data"]["max_temp"])
            self.set_variable("outdoor_max_temp", _outdoor_max_temperature)  # C
            _outdoor_min_temperature = float(_theJSON["body"]["modules"][0]["dashboard_data"]["min_temp"])
            self.set_variable("outdoor_min_temp", _outdoor_min_temperature)  # C
        except:
            print
            "Error! Netatmo Outdoor @getDeviceStatusJson"

    def printDeviceStatus(self):
        print
        " Netatmo indoor device"
        print("     noise = {} dB".format(self.get_variable('noise')).upper())
        print("     temperature = {} C".format(self.get_variable('temperature')).upper())
        print("     humidity = {} %".format(self.get_variable('humidity')).upper())
        print("     pressure = {} inHg".format(self.get_variable('pressure')).upper())
        print("     co2 = {} ppm".format(self.get_variable('co2')).upper())
        print("     date_max_temp = {} unix timestamp".format(self.get_variable('date_max_temp')).upper())
        print("     date_min_temp = {} unix timestamp".format(self.get_variable('date_min_temp')).upper())
        print("     max_temp = {} C".format(self.get_variable('max_temp')).upper())
        print("     min_temp = {} C".format(self.get_variable('min_temp')).upper())
        print("     outdoor_temperature = {} C".format(self.get_variable('outdoor_temperature')).upper())
        print("     outdoor_humidity = {} %".format(self.get_variable('outdoor_humidity')).upper())
        print("     outdoor_date_max_temp = {} unix timestamp".format(self.get_variable('outdoor_date_max_temp')).upper())
        print("     outdoor_date_min_temp = {} unix timestamp".format(self.get_variable('outdoor_date_min_temp')).upper())
        print("     outdoor_max_temp = {} C".format(self.get_variable('outdoor_max_temp')).upper())
        print("     outdoor_min_temp = {} C".format(self.get_variable('outdoor_min_temp')).upper())
        print("     device_type = {} ".format(self.get_variable('device_type')).upper())


def main():
    Netatmo = API(address='https://api.netatmo.net/api/devicelist',
                  url="https://api.netatmo.net/oauth2/token", client_id="592fc89f743c360b3a8b53e9",
                  username='smarthome.pea@gmail.com', password='28Sep1960',client_secret='nPoa7wZfyq7VbCbF7Gqzo5bI1V5')
    print("{0} agent is initialzed for {1} using API={2} at {3}".format(Netatmo.get_variable('agent_id'),
                                                                        Netatmo.get_variable('model'),
                                                                        Netatmo.get_variable('api'),
                                                                        Netatmo.get_variable('address'),
                                                                        Netatmo.get_variable('url'),
                                                                        Netatmo.get_variable('client_id'),
                                                                        Netatmo.get_variable('username'),
                                                                        Netatmo.get_variable('scope'),
                                                                        Netatmo.get_variable('client_secret'),
                                                                        Netatmo.get_variable('grant_type'),
                                                                        Netatmo.get_variable('content')))

    Netatmo.getDeviceStatus()
if __name__ == "__main__": main()
