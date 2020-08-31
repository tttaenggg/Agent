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
import os

_log = logging.getLogger(__name__)
utils.setup_logging()
__version__ = "0.1"

DEFAULT_MESSAGE = 'I am a Projector Agent'
DEFAULT_AGENTID = "ProjectorAgent"
DEFAULT_HEARTBEAT_PERIOD = 5



class Projectoragent(Agent):
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

    # -- Direct Control From Web Application
    @PubSub.subscribe('pubsub', "web/control/projector")
    def on_match_sendcommand(self, peer, sender, bus,  topic, headers, message):

        _log.info("Get Message : {}".format(message))
        msg = message
        # print(msg)
        device_id = msg.get('device_id')
        if 'command' in msg.keys():
            command = json.loads(msg.get('command'))  # {status: ON}
        elif 'status' in msg.keys():
            command = {"status": msg.get('status')}
        else:
            command = {}

        print(device_id)
        print(command)
        print("----------------------------------------------")
        device_info = self.members.get(device_id)

        self.projector = api.API(model='Optoma', api='API3', agent_id='25PROPT101001', types='projector',
                                 ip=device_info['ip'], port=device_info['port'], command=device_info['command'])

        self.projector.setDeviceStatus(command)
        del self.projector



def main():
    """Main method called to start the agent."""
    utils.vip_main(Projectoragent,
                   version=__version__)


if __name__ == '__main__':
    # Entry point for script
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        pass
