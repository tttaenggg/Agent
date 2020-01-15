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
from .extension import protocol


_log = logging.getLogger(__name__)
utils.setup_logging()
__version__ = "0.1"

DEFAULT_MESSAGE = 'I am a UDP Agent'
DEFAULT_AGENTID = "udpserver"
DEFAULT_HEARTBEAT_PERIOD = 5


#------
import crcmod


# -----
class Udpagent(Agent):
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
        self._module_set = None
        self.command_conf = {
                                "power": "ON",
                                "mode" : "COLD",
                                "fan": "FAN1",
                                "setpoint": 25
                                }
        
        self.port = 22533
        self.protocol = protocol.Protocol()
        self.adaptor = None
        
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
    
    def sendconf(self, ipaddress, conf):
        
        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 
                                        socket.IPPROTO_UDP)
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            self._socket.bind(("", self.port))
            payload = bytes.fromhex(conf)
            # print(payload)
            sent = self._socket.sendto(payload, (ipaddress, self.port))

        except Exception as e:
            _log.error(msg="Error : {}".format(e))
        
    
    # @Core.receiver('onsetup')
    # def onsetup():
    #     # TODO : Configuration Parameter of UDP Server Here
        
    #     pass        
            
    @Core.receiver("onstart")
    def onstart(self, sender, **kwargs):
        """
        This is method is called once the Agent has successfully connected to the platform.
        This is a good place to setup subscriptions if they are not dynamic or
        do any other startup activities that require a connection to the message bus.
        Called after any configurations methods that are called at startup.

        Usually not needed if using the configuration store.
        """
        #Example publish to pubsub
        #self.vip.pubsub.publish('pubsub', "some/random/topic", message="HI!")

        #Exmaple RPC call
        #self.vip.rpc.call("some_agent", "some_method", arg1, arg2)
        
        # TODO :  Start Server Listener Here
        pass
    
    @Core.receiver("onstop")
    def onstop(self, sender, **kwargs):
        """
        This method is called when the Agent is about to shutdown, but before it disconnects from
        the message bus.
        """
        pass

    @PubSub.subscribe('pubsub', "ui/command/conf")
    def on_match_sendcommand(self, peer, sender, bus,  topic, headers, message):
        
        self._logfn(
            "Peer: {0}, Sender: {1}:, Bus: {2}, Topic: {3}, Headers: {4}, "
            "Message: \n{5}".format(peer, sender, bus, topic, headers, pformat(message)))
        
        self.command_conf.update(json.loads(message))
        _log.debug(msg="Receive Message : {}".format(self.command_conf))
        if None in self.command_conf.values():
            if self.command_conf['power'] is None:
                pass
            
            elif self.command_conf['power'] == "ON":
                # TODO : Send Only ON command
                self.command_conf.update({'msg': "on_fix"})

            elif self.command_conf['power'] == "OFF":
                self.command_conf.update({'msg': "off_fix"})
                
        else:
            self.command_conf.update({'msg': 'variable_tx'})
        
        _log.debug(msg="Complete Command : {}".format(self.command_conf))  

        command = self.protocol.encode(self.command_conf)
        
        print("Log Command Encoded : {}".format(self.adaptor))
        
        # conf = adaptor.command
        # TODO : Send Command via UDP Server
        for ipaddress in self._module_set:
            print("IP Module : {}".format(ipaddress))
            self.sendconf(ipaddress, conf=command)
    
    @PubSub.subscribe('pubsub', "discovery/send/command")
    def on_match_discover(self, peer, sender, bus,  topic, headers, message):
        
        self._logfn(
            "Peer: {0}, Sender: {1}:, Bus: {2}, Topic: {3}, Headers: {4}, "
            "Message: \n{5}".format(peer, sender, bus, topic, headers, pformat(message)))
        
        # Update module set start here
        msg = json.loads(message)
        self._module_set = msg.get('module', None) # If run in test please config IP-Address
        _log.info(msg="Found Module : {}".format(self._module_set))
        

    @Core.periodic(60)
    def on_interval(self):
        # Broadcast Message from UDP Server
        _log.info(msg="Send Command to module to get status")

        if self._module_set is None:
            # TODO : publish to discovery agent to get IPADDRESS
            _log.info(msg="Module Set IP address Not Found")

        else:

            command = self.protocol.encode({'msg': 'status'})
            try:
                for ipaddress in self._module_set:
                    _log.info(msg="Send Status Request to {} with Commmand : {}".format(ipaddress, command))
                    self.sendconf(ipaddress=ipaddress, conf=command)

            except Exception as e:
                _log.error(msg="Error : {}".format(e))
        


def main():
    """Main method called to start the agent."""
    utils.vip_main(Udpagent, 
                   version=__version__)


if __name__ == '__main__':
    # Entry point for script
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        pass
