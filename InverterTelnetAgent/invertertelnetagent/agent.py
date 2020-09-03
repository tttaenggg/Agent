"""
Agent documentation goes here.
"""

__docformat__ = 'reStructuredText'

import logging
import sys, os
from volttron.platform.agent import utils
from volttron.platform.vip.agent import Agent, Core, RPC, PubSub
from volttron.platform.scheduling import periodic
from pprint import pformat
import json
import socket
from .extension import api
from multiprocessing import Process
from Agent import settings
import pyrebase
from datetime import datetime

import time
import socket
from threading import Thread

_log = logging.getLogger(__name__)
utils.setup_logging()
__version__ = "0.1"

DEFAULT_MESSAGE = 'I am a Inverter Agent'
DEFAULT_AGENTID = "InverterTelnetAgent"
DEFAULT_HEARTBEAT_PERIOD = 5

gateway_id = settings.gateway_id

conn = ('', 1033)
info_data = {'batt_P': '1',
             'batt_percen': '2',
             'load_act_P': '3',
             'PV_total_P': '1',
             'output_P': '1',
             'SOH': '2'}


# firebase config
try:
    config = {
        "apiKey": settings.FIREBASE['apiKeyLight'],
        "authDomain": settings.FIREBASE['authLight'],
        "databaseURL": settings.FIREBASE['databaseLight'],
        "storageBucket": settings.FIREBASE['storageLight']
    }
    firebase = pyrebase.initialize_app(config)
    db =firebase.database()

except Exception as er:
    _log.debug(er)



class Invertertelnetagent(Agent):
    """
    Document agent constructor here.
    """

    def polling_data(self, cmd, command_type):
        def sendData(cmd):
            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

                addr = ("192.168.10.11", 1032)

                # check case
                if cmd == 'batt_P':
                    client_socket.sendto(b"\x02\x04\x00\x11\x00\x01\x61\xFC", addr)

                elif cmd == 'batt_percen':
                    client_socket.sendto(b"\x02\x04\x00\x2F\x00\x01\x00\x30", addr)

                elif cmd == 'load_act_P':
                    client_socket.sendto(b"\x02\x04\x00\x31\x00\x01\x60\x36", addr)

                elif cmd == 'PV_total_P':
                    client_socket.sendto(b"\x02\x04\x00\x6C\x00\x01\xF1\xE4", addr)

                elif cmd == 'output_P':
                    client_socket.sendto(b"\x02\x04\x00\x71\x00\x01\x61\xE2", addr)

                elif cmd == 'SOH':
                    client_socket.sendto(b"\x02\x04\x00\xA6\x00\x01\xD1\xDA", addr)

                else:
                    pass

                print("Send")
            except socket.timeout:
                print('REQUEST TIMED OUT')

        def recvData(command_type):
            print(">>>> {}".format(command_type))
            ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            ss.bind(conn)
            while 1:
                message, address = ss.recvfrom(1024)
                hexmsg = message.hex()
                print(hexmsg)
                rawdata = ('0' * ((int(hexmsg[4:6]) * 2) - len(hexmsg[6:-4]))) + hexmsg[6:-4]
                data = ''

                # check case
                if command_type == '1':
                    data = str((((int(rawdata, 16) + 0x8000) & 0xFFFF) - 0x8000) / 10)

                elif command_type == '2':
                    data = str(int(rawdata, 16))

                elif command_type == '3':
                    data = str(int(rawdata, 16) / 10)

                else:
                    pass

                print(data)

                break

            return data

        t1 = Thread(target=sendData, args=(cmd,))
        t2 = Thread(target=recvData, args=(command_type,))

        t1.start()
        t2.start()

        t1.join()
        t2.join()


    def update_firebase(self, all_data):

        # TODO : Update Firebase with _status variable
        try:

            # db.child(gateway_id).child('devicetype').child('inverter').child(devices[0]).child('BATTERY_PERCENTAGE').set(inverter.variables['batt_percen'])
            # db.child(gateway_id).child('devicetype').child('inverter').child(devices[0]).child('LOAD_ACTIVE_POWER').set(inverter.variables['load_act_P'])
            # db.child(gateway_id).child('devicetype').child('inverter').child(devices[0]).child('PV_DAILY_POWER_GEN').set(inverter.variables['PV_daily_P_gen'])
            # db.child(gateway_id).child('devicetype').child('inverter').child(devices[0]).child('PV_TOTAL_POWER_GEN').set(inverter.variables['PV_total_P_gen'])
            # db.child(gateway_id).child('devicetype').child('inverter').child(devices[0]).child('DAILY_LOAD_CONSUMPTION').set(inverter.variables['daily_load_con'])
            # db.child(gateway_id).child('devicetype').child('inverter').child(devices[0]).child('DAILY_POWER_INTAKE_FROM_GRID').set(inverter.variables['daily_P_intake_grid'])
            # db.child(gateway_id).child('devicetype').child('inverter').child(devices[0]).child('TOTAL_POWER_INTAKE_FROM_GRID').set(inverter.variables['total_P_intake_grid'])
            # db.child(gateway_id).child('devicetype').child('inverter').child(devices[0]).child('DAILY_POWER_FED_TO_GRID').set(inverter.variables['daily_P_fed_grid'])
            # db.child(gateway_id).child('devicetype').child('inverter').child(devices[0]).child('TOTAL_POWER_FED_TO_GRID').set(inverter.variables['total_P_fed_grid'])
            # db.child(gateway_id).child('devicetype').child('inverter').child(devices[0]).child('OUTPUT_POWER').set(inverter.variables['output_P'])
            # db.child(gateway_id).child('devicetype').child('inverter').child(devices[0]).child('SOH').set(inverter.variables['SOH'])
            # db.child(gateway_id).child('devicetype').child('inverter').child(devices[0]).child('BMS_BATTERY_STATUS').set(inverter.variables['BMS_batt_status'])

            db.child(gateway_id).child('devicetype').child('inverter').child('IN202001').child('DT').set(datetime.now().replace(microsecond=0).isoformat())
            db.child(gateway_id).child('devicetype').child('inverter').child('IN202001').child('BATTERY_POWER').set(all_data['batt_P'])
            db.child(gateway_id).child('devicetype').child('inverter').child('IN202001').child('PV_TOTAL_POWER').set(all_data['PV_total_P'])
            db.child(gateway_id).child('devicetype').child('inverter').child('IN202001').child('batt_percen').set(all_data['batt_percen'])
            db.child(gateway_id).child('devicetype').child('inverter').child('IN202001').child('load_act_P').set(all_data['load_act_P'])
            db.child(gateway_id).child('devicetype').child('inverter').child('IN202001').child('grid_P').set(all_data['output_P'])
            db.child(gateway_id).child('devicetype').child('inverter').child('IN202001').child('SOH').set(all_data['SOH'])


        except Exception as err:
            print("ERROR firebase: {}".format(err))
            pass


    def __init__(self, config_path,
                 **kwargs):
        super().__init__(**kwargs)

        self.config = utils.load_config(config_path)
        self._agent_id = self.config.get('agentid', DEFAULT_AGENTID)
        self._message = self.config.get('message', DEFAULT_MESSAGE)
        self._heartbeat_period = self.config.get('heartbeat_period',
                                                 DEFAULT_HEARTBEAT_PERIOD)

        self.iplist_path = self.config.get('pathconf')
        self.members = json.load(open(os.environ['VOLTTRON_ROOT']+self.iplist_path))

        _log.debug("IP List : {}".format(self.members))

        try:
            self._heartbeat_period = int(self._heartbeat_period)
        except:
            _log.warning('Invalid heartbeat period specified setting to default')
            self._heartbeat_period = DEFAULT_HEARTBEAT_PERIOD
        log_level = self.config.get('log-level', 'INFO')
        if log_level == 'ERROR':
            self._logfn = _log.error
        elif log_level == 'WARN':
            self._logfn = _log.warn
        elif log_level == 'DEBUG':
            self._logfn = _log.debug
        else:
            self._logfn = _log.info

    @Core.receiver("onstart")
    def onstart(self, sender, **kwargs):
        # TODO :  Start Server Listener Here

        pass

    @Core.schedule(periodic(300))
    def updatestatus(self):
        _log.info(msg="Get Current Status")

        data_list = {}

        for k, v in info_data.items():
            print("{} --- {}".format(k, v))
            data_list[k] = self.polling_data(k, v)

        # firebase
        self.update_firebase(data_list)





def main():
    """Main method called to start the agent."""
    from gevent import monkey

    monkey.patch_all()
    utils.vip_main(Invertertelnetagent,
                   version=__version__)


if __name__ == '__main__':
    # Entry point for script
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        pass
