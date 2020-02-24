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
import settings
import pyrebase
from datetime import datetime

_log = logging.getLogger(__name__)
utils.setup_logging()
__version__ = "0.1"

DEFAULT_MESSAGE = 'I am a Aeotec Agent'
DEFAULT_AGENTID = "AeotecAgent"
DEFAULT_HEARTBEAT_PERIOD = 60

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



class Aeotecagent(Agent):
    """
    Document agent constructor here.
    """

    # TODO -- Need Revise again
    def getstatus_proc(self, devices):  # Function for MultiProcess

        # Devices is tuple index 0 is Devices ID , 1 is IPADDRESS

        _log.info(msg="Start Get Status from {}".format(devices[1]))

        try:
            multisensor = api.API(model='Sensor', types='illuminances', api='API3', agent_id='18ORC_OpenCloseAgent',
                                  url=(devices[1])['url'], bearer=(devices[1])['bearer'], device=(devices[1])['device'])

            multisensor.getDeviceStatus()

            # TODO : Update Firebase with _status variable
            db.child(gateway_id).child('devicetype').child('multisensor').child(devices[0]).child('DT').set(multisensor.variables['unitTime'])
            db.child(gateway_id).child('devicetype').child('multisensor').child(devices[0]).child('HUMIDITY').set(multisensor.variables['humidity'])
            db.child(gateway_id).child('devicetype').child('multisensor').child(devices[0]).child('ILLUMINANCE').set(multisensor.variables['illuminance'])
            db.child(gateway_id).child('devicetype').child('multisensor').child(devices[0]).child('MOTION').set(multisensor.variables['motion'])
            db.child(gateway_id).child('devicetype').child('multisensor').child(devices[0]).child('TAMPER').set(multisensor.variables['tamper'])
            db.child(gateway_id).child('devicetype').child('multisensor').child(devices[0]).child('TEMPERATURE').set(multisensor.variables['temperature'])

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
        self.members = json.load(open(self.iplist_path))

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

    @Core.schedule(periodic(20))
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
    utils.vip_main(Aeotecagent,
                   version=__version__)


if __name__ == '__main__':
    # Entry point for script
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        pass
