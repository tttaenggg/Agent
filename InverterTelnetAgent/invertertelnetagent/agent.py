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

_log = logging.getLogger(__name__)
utils.setup_logging()
__version__ = "0.1"

DEFAULT_MESSAGE = 'I am a Inverter Agent'
DEFAULT_AGENTID = "InverterTelnetAgent"
DEFAULT_HEARTBEAT_PERIOD = 5

gateway_id = settings.gateway_id

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

    # TODO -- Need Revise again
    def getstatus_proc(self, devices):  # Function for MultiProcess

        # Devices is tuple index 0 is Devices ID , 1 is IPADDRESS

        _log.info(msg="Start Get Status from {}".format(devices[1]))

        try:
            inverter = api.API(model = 'Growatt', api = 'API3', agent_id = '28INVIN202001', types = 'inverter',
                               ip=(devices[1])['ip'], port=(devices[1])['port'])

            inverter.getDeviceStatus()


            # TODO : Update Firebase with _status variable
            try:
                db.child(gateway_id).child('devicetype').child('inverter').child(devices[0]).child('DT').set(datetime.now().replace(microsecond=0).isoformat())
                # db.child(gateway_id).child('devicetype').child('inverter').child(devices[0]).child('MODE_SELECTION').set(inverter.variables['mode_select'])
                db.child(gateway_id).child('devicetype').child('inverter').child(devices[0]).child('BATTERY_POWER').set(inverter.variables['batt_P'])
                # db.child(gateway_id).child('devicetype').child('inverter').child(devices[0]).child('BATTERY_PERCENTAGE').set(inverter.variables['batt_percen'])
                # db.child(gateway_id).child('devicetype').child('inverter').child(devices[0]).child('LOAD_ACTIVE_POWER').set(inverter.variables['load_act_P'])
                # db.child(gateway_id).child('devicetype').child('inverter').child(devices[0]).child('PV_DAILY_POWER_GEN').set(inverter.variables['PV_daily_P_gen'])
                # db.child(gateway_id).child('devicetype').child('inverter').child(devices[0]).child('PV_TOTAL_POWER_GEN').set(inverter.variables['PV_total_P_gen'])
                # db.child(gateway_id).child('devicetype').child('inverter').child(devices[0]).child('DAILY_LOAD_CONSUMPTION').set(inverter.variables['daily_load_con'])
                # db.child(gateway_id).child('devicetype').child('inverter').child(devices[0]).child('DAILY_POWER_INTAKE_FROM_GRID').set(inverter.variables['daily_P_intake_grid'])
                # db.child(gateway_id).child('devicetype').child('inverter').child(devices[0]).child('TOTAL_POWER_INTAKE_FROM_GRID').set(inverter.variables['total_P_intake_grid'])
                # db.child(gateway_id).child('devicetype').child('inverter').child(devices[0]).child('DAILY_POWER_FED_TO_GRID').set(inverter.variables['daily_P_fed_grid'])
                # db.child(gateway_id).child('devicetype').child('inverter').child(devices[0]).child('TOTAL_POWER_FED_TO_GRID').set(inverter.variables['total_P_fed_grid'])
                db.child(gateway_id).child('devicetype').child('inverter').child(devices[0]).child('PV_TOTAL_POWER').set(inverter.variables['PV_total_P'])
                # db.child(gateway_id).child('devicetype').child('inverter').child(devices[0]).child('OUTPUT_POWER').set(inverter.variables['output_P'])
                # db.child(gateway_id).child('devicetype').child('inverter').child(devices[0]).child('SOH').set(inverter.variables['SOH'])
                # db.child(gateway_id).child('devicetype').child('inverter').child(devices[0]).child('BMS_BATTERY_STATUS').set(inverter.variables['BMS_batt_status'])
                #


            except Exception as err:
                print("ERROR firebase: {}".format(err))
                pass


        except Exception as err:
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

    @Core.schedule(periodic(120))
    def updatestatus(self):
        _log.info(msg="Get Current Status")
        procs = []

        for k, v in self.members.items():
            devices = (k, v)
            proc = Process(target=self.getstatus_proc, args=(devices,))
            procs.append(proc)
            proc.start()

        # TODO : if you want to wait the process completed Uncomment code below
        # for proc in procs:
        #     proc.join()



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
