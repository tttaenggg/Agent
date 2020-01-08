"""
Agent documentation goes here.
"""

__docformat__ = 'reStructuredText'

import logging
import sys
from pprint import pformat
from volttron.platform.agent import utils
from volttron.platform.vip.agent import Agent, Core, RPC, PubSub
from volttron.platform.vip.agent.subsystems.query import Query
import socket
import threading, time
import json

_log = logging.getLogger(__name__)
utils.setup_logging()
__version__ = "0.1"

DEFAULT_MESSAGE = 'I am a Discovery Agent'
DEFAULT_AGENTID = "discovery"
DEFAULT_HEARTBEAT_PERIOD = 5


class Discover(Agent):
    """
    Document agent constructor here.
    """

    def __init__(self, config_path, **kwargs):
        super().__init__(**kwargs)
        self.config = utils.load_config(config_path)
        self._agent_id = self.config.get('agentid', DEFAULT_AGENTID)
        self._message = self.config.get('message', DEFAULT_MESSAGE)
        self._heartbeat_period = self.config.get('heartbeat_period',
                                                 DEFAULT_HEARTBEAT_PERIOD)
        
        self._module_set = None
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


    @Core.receiver('onsetup')
    def onsetup(self, sender, **kwargs):
        # Demonstrate accessing a value from the config file
        _log.info(self.config.get('message', DEFAULT_MESSAGE))
        self._agent_id = self.config.get('agentid')
        # TODO : Create Socket on setup state
        self.port = 1025
        self.broadcast_msg = b'Are You AirM2M IOT Smart Device?'
        self._module = []
        
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        self._ipaddress = s.getsockname()[0]
        s.close()
        
        self.on_search()
        self._socket.close()
        
    def on_search(self):
        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 
                                        socket.IPPROTO_UDP)
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            self._socket.bind(("", self.port))

            sent = self._socket.sendto(self.broadcast_msg, ('<broadcast>', self.port))

        except Exception as e:
            _log.error(msg="Error : {}".format(e))
    
    def on_wait(self):
        try:
            self._soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM )
            self._soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            self._soc.bind((str(self._ipaddress), self.port))
            _log.info(msg="Server IP : {} is Bind on PORT {}".format(self._ipaddress, self.port))
            while True:
                (data, addr) = self._soc.recvfrom(1024)
                yield data
                
                self.module_set = set(self._module)
                self._module = []
                _log.info(msg="Module Founded : {}".format(self.module_set))
                module_len = len(self.module_set)
                
                # TODO : Publish Msg to Other Agent for handle here
                if self.module_set != self._module_set:
                    self._module_set = self.module_set
                    msg = json.dumps({'module':self.module_set})
                    self.vip.pubsub.publish('pubsub', topic="discoveryagent/send/command", 
                                            message=msg)
        
        except Exception as e:
            _log.error("Error : {}".format(e))
        

    @Core.receiver("onstart")
    def onstart(self, sender, **kwargs):
        #Example publish to pubsub
        #self.vip.pubsub.publish('pubsub', "some/random/topic", message="HI!")

        #Exmaple RPC call
        #self.vip.rpc.call("some_agent", "some_method", arg1, arg2)
        _log.info(msg="Agent Discovery Start and enable Threading for Listen on PORT {}".format(self.port))
        listener = threading.Thread(target=self.on_wait)
        listener.start()
        
        for data in self.on_wait():
            mac_addr = str(data).split('v2.')[-1].split()[0].replace('"','')
            ip_addr = str(data).split('v2.')[-1].split()[1].replace('"','')
            _log.info(msg="Found Airconet Module : IP = {} and MAC = {}".format(
                ip_addr, mac_addr
            ))
            # Write to Module Config File
            self._module.append(ip_addr)
            
        _log.info(msg="End of Receive Byte Data")
            
            
    @Core.receiver("onstop")
    def onstop(self, sender, **kwargs):
        """
        This method is called when the Agent is about to shutdown, but before it disconnects from
        the message bus.
        """
        try:
            self._soc.close()
            self._socket.close()

        except Exception as e:
            _log.error("Error : {}".format(e))
        
    @Core.periodic(60)
    def on_interval(self):
        # Broadcast Message from UDP Server
        _log.info(msg="Searching AirConet Module via UDP Broadcasting")
        self.on_search() # Call Function by Periodic
        self._socket.close()

def main():
    """Main method called to start the agent."""
    
    try:
        utils.vip_main(Discover, version=__version__)
    
    except Exception as e:
        _log.exception('Unhandle Exception')


if __name__ == '__main__':
    # Entry point for script
    sys.exit(main())
    
