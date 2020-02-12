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


_log = logging.getLogger(__name__)
utils.setup_logging()
__version__ = "0.1"

DEFAULT_MESSAGE = 'I am a Daikin Agent'
DEFAULT_AGENTID = "DaikinAgent"
DEFAULT_HEARTBEAT_PERIOD = 5



class Daikinagent(Agent):
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
        # _log.info("Found in Config File: {}".format(self.config.get('members')))
        #
        # for k,v in self.members.items():
        # ip = self.members.get('air004')
        # self.daikin = api.API(model='daikin', type='AC', api='API', agent_id='ACAgent', url=ip,
        #                       port=502, parity='E', baudrate=9600, startregis=2006, startregisr=2012)
        #
        # self.daikin.getDeviceStatus()
        # self.daikin.setDeviceStatus({"status": "ON"})
        # self.daikin.getDeviceStatus()
        pass



    @PubSub.subscribe('pubsub','web/control/aircon')
    def on_match_sendcommand(self, peer, sender, bus,  topic, headers, message):

        _log.info("Get Message : {}".format(message))

        msg = message
        deviceid = msg.get('deviceid')
        msg.pop('deviceid')
        status = msg

        print(deviceid)
        print(status)
        print("----------------------------------------------")
        ipaddress = self.members.get(deviceid)
        print(ipaddress)

        self.daikin = api.API(model='daikin', type='AC', api='API', agent_id='ACAgent', url=ipaddress,
                              port=502, parity='E', baudrate=9600, startregis=2006, startregisr=2012)

        self.daikin.getDeviceStatus()
        self.daikin.setDeviceStatus(status)
        self.daikin.getDeviceStatus()
        del self.daikin


def main():
    """Main method called to start the agent."""
    utils.vip_main(Daikinagent,
                   version=__version__)


if __name__ == '__main__':
    # Entry point for script
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        pass
