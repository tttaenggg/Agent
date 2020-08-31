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

DEFAULT_MESSAGE = 'I am a Automation1 Agent'
DEFAULT_AGENTID = "Automation1Agent"
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



class Automation1agent(Agent):
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

    @Core.schedule(periodic(600))
    def updatestatus(self):
        _log.info(msg="Check multisensor data from firebase")

        multi_temp = float(db.child(gateway_id).child('devicetype').child('multisensor').child('MS202001').child('TEMPERATURE').get().val())
        # print("multi_temp: {}".format(multi_temp))

        ac_status = db.child(gateway_id).child('devicetype').child('ac').child('AC202001').child('STATUS').get().val()
        # ac_status = db.child(gateway_id).child('devicetype').child('ac').child('AC101001').child('STATUS').get().val()
        # print("ac status: {}".format(ac_status))

        try:
            auto_time = datetime.strptime(db.child(gateway_id).child('time_automation1').get().val(), "%Y-%m-%dT%H:%M:%S")
            # print("time_now-try: {}".format(auto_time))

        except:
            auto_time = datetime.now()
            # print("time_now-except: {}".format(auto_time))
            pass

        time_now = datetime.now()
        # print("time_now: {}".format(time_now))
        duration = time_now - auto_time
        # print("diff time: {}".format(duration))
        duration_in_s = duration.total_seconds()
        # print("diff second: {}".format(duration_in_s))
        diff_min = divmod(duration_in_s, 60)[0]
        # print("diff min: {}".format(diff_min))

        if (multi_temp >= 25) and (ac_status == 'OFF'):
            self.daikin = api.API(model='daikin', type='AC', api='API', agent_id='ACAgent',
                                  url='http://192.168.10.238', port=502,
                                  parity='E', baudrate=9600,
                                  startregis=2006, startregisr=2012)

            self.daikin.setDeviceStatus({"status": "ON", "mode": "COLD", "stemp":"18"})
            # self.daikin.getDeviceStatus()
            del self.daikin
            db.child(gateway_id).child('time_automation1').set(datetime.now().replace(microsecond=0).isoformat())
            print("automation-on")

        elif (multi_temp < 25) and (diff_min >= 120) and (ac_status == 'ON'):
            self.daikin = api.API(model='daikin', type='AC', api='API', agent_id='ACAgent',
                                  url='http://192.168.10.238', port=502,
                                  parity='E', baudrate=9600,
                                  startregis=2006, startregisr=2012)

            self.daikin.setDeviceStatus({"status": "OFF"})
            # self.daikin.getDeviceStatus()
            del self.daikin
            print("automation-off")

        else:
            pass


        # TODO : if you want to wait the process completed Uncomment code below
        # for proc in procs:
        #     proc.join()



def main():
    """"Main method called to start the agent."""
    from gevent import monkey

    monkey.patch_all()
    utils.vip_main(Automation1agent,
                   version=__version__)


if __name__ == '__main__':
    # Entry point for script
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        pass
