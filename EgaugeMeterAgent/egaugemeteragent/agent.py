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
import os
_log = logging.getLogger(__name__)
utils.setup_logging()
__version__ = "0.1"

DEFAULT_MESSAGE = 'I am a Egauge Meter Agent'
DEFAULT_AGENTID = "EgaugemeterAgent"
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



class Egaugemeteragent(Agent):
    """
    Document agent constructor here.
    """

    # TODO -- Need Revise again
    def getstatus_proc(self, devices):  # Function for MultiProcess

        # Devices is tuple index 0 is Devices ID , 1 is IPADDRESS

        _log.info(msg="Start Get Status from {}".format(devices[1]))

        # try:

        meter = api.API(model='eGauge', api='API3', agent_id='05EGA010101', types='powermeter',
                        device=(devices[1])['meter_id'], ip=(devices[1])['ip'], port=(devices[1])['port'])

        meter.getDeviceStatus()
        # TODO : Update Firebase with _status variable
        db.child(gateway_id).child('devicetype').child('powermeter').child('mdb').set(meter.variables['mdb'])
        db.child(gateway_id).child('devicetype').child('powermeter').child('floor1plug').set(meter.variables['floor1plug'])
        db.child(gateway_id).child('devicetype').child('powermeter').child('floor1light').set(meter.variables['floor1light'])
        db.child(gateway_id).child('devicetype').child('powermeter').child('floor1air').set(meter.variables['floor1air'])
        db.child(gateway_id).child('devicetype').child('powermeter').child('floor2plug').set(meter.variables['floor2plug'])
        db.child(gateway_id).child('devicetype').child('powermeter').child('floor2light').set(meter.variables['floor2light'])
        db.child(gateway_id).child('devicetype').child('powermeter').child('floor2air').set(meter.variables['floor2air'])
        db.child(gateway_id).child('devicetype').child('powermeter').child('edb').set(meter.variables['edb'])

        # except Exception as err:
        #     pass


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

    @Core.schedule(periodic(5))
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
    utils.vip_main(Egaugemeteragent,
                   version=__version__)


if __name__ == '__main__':
    # Entry point for script
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        pass
