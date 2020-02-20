"""
Agent documentation goes here.
"""

__docformat__ = 'reStructuredText'

import logging
import sys
from volttron.platform.agent import utils
from volttron.platform.vip.agent import Agent, Core, RPC, PubSub
from pprint import pformat
import json
import socket
from .extension import api
from volttron.platform.scheduling import periodic
from multiprocessing import Process

_log = logging.getLogger(__name__)
utils.setup_logging()
__version__ = "0.1"

DEFAULT_MESSAGE = 'I am a Tplink Plug Agent'
DEFAULT_AGENTID = "TplinkAgent"
DEFAULT_HEARTBEAT_PERIOD = 5



class Plugagent(Agent):
    """
    Document agent constructor here.
    """

    # TODO -- Need Revise again
    def getstatus_proc(self, devices): # Function for MultiProcess

        # Devices is tuple index 0 is Devices ID , 1 is IPADDRESS

        _log.info(msg="Start Get Status from {}".format(devices[1]))

        try:
            plug = api.API(model='TPlinkPlug', api='API3',
                               agent_id='TPlinkPlugAgent', types='plug',
                               ip=devices[1], port=9999)

            _status = plug.getDeviceStatus()

            # TODO : Update Firebase with _status variable
            """
                    update value to Firebase

            """

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

    # -- Direct Control From Web Application
    @PubSub.subscribe('pubsub', "web/control/plug")
    def on_match_sendcommand(self, peer, sender, bus,  topic, headers, message):

        _log.info("Get Message : {}".format(message))
        msg = message
        # print(msg)
        deviceid = msg.get('deviceid')
        status = msg.get('status')

        print(deviceid)
        print(status)
        print("----------------------------------------------")
        ipaddress = self.members.get(deviceid)

        self.plug = api.API(model='TPlinkPlug', api='API3',
                            agent_id='TPlinkPlugAgent', types='plug',
                            ip=ipaddress, port=9999)

        # self.plug.getDeviceStatus()
        self.plug.setDeviceStatus({'status': status})
        # self.plug.getDeviceStatus()
        del self.plug

    @Core.schedule(periodic(60))
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
    utils.vip_main(Plugagent,
                   version=__version__)


if __name__ == '__main__':
    # Entry point for script
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        pass
