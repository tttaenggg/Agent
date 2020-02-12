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

DEFAULT_MESSAGE = 'I am a Tplink Plug Agent'
DEFAULT_AGENTID = "TplinkAgent"
DEFAULT_HEARTBEAT_PERIOD = 5



class Plugagent(Agent):
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



    # -- Scene Agent Control
    # @PubSub.subscribe('pubsub', "scene/control/plug")
    # def on_match_scenecommand(self, peer, sender, bus,  topic, headers, message):
    #
    #     _log.debug(" >> Executed by Scene Agent")
    #     deviceid = message.get('deviceid')
    #     ipaddress = self.members.get(deviceid)
    #     status = message.get('status')
    #
    #     self.plug = api.API(model='TPlinkPlug', api='API3',
    #                        agent_id='TPlinkPlugAgent', types='plug',
    #                        ip=ipaddress, port=9999)
    #
    #     bef = self.plug.getDeviceStatus()
    #     self.plug.setDeviceStatus({'status': status})
    #     aft = self.plug.getDeviceStatus()
    #     if bef != aft :
    #         _log.debug("Scene Execute status : {} Successful".format(status))
    #
    #     self.plug = None



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
