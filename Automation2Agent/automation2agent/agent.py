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
import asyncio, concurrent.futures

_log = logging.getLogger(__name__)
utils.setup_logging()
__version__ = "0.1"

DEFAULT_MESSAGE = 'I am a Automation2 Agent'
DEFAULT_AGENTID = "Automation2Agent"
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



class Automation2agent(Agent):
    """
    Document agent constructor here.
    """

    def __init__(self, config_path,
                 **kwargs):
        super().__init__(**kwargs)

        self.config = utils.load_config(config_path)
        self._agent_id = self.config.get('agentid', DEFAULT_AGENTID)
        self._message = self.config.get('message', DEFAULT_MESSAGE)
        self._heartbeat_period = self.config.get('heartbeat_period',
                                                 DEFAULT_HEARTBEAT_PERIOD)

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
        _log.info(msg="Check ac data from firebase")

        ac_status = db.child(gateway_id).child('devicetype').child('ac').child('AC104001').child('STATUS').get().val()
        print("ac status: {}".format(ac_status))

        plug_status = db.child(gateway_id).child('devicetype').child('plug').child('SP101002').child('STATUS').get().val()
        print("plug status: {}".format(plug_status))

        if (ac_status != plug_status): # same status!
            self.plug = api.API(model='TPlinkPlug', api='API3',
                                agent_id='TPlinkPlugAgent', types='plug',
                                ip='192.168.10.128', port=9999)

            self.plug.setDeviceStatus({"status": ac_status})
            del self.plug

        else:
            pass


        # TODO : if you want to wait the process completed Uncomment code below
        # for proc in procs:
        #     proc.join()



def main():
    """"Main method called to start the agent."""
    from gevent import monkey

    monkey.patch_all()
    utils.vip_main(Automation2agent,
                   version=__version__)


if __name__ == '__main__':
    # Entry point for script
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        pass
