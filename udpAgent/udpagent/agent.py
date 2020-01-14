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
# from extension.Protocol import encode
# from extension.Protocol import decode


_log = logging.getLogger(__name__)
utils.setup_logging()
__version__ = "0.1"

DEFAULT_MESSAGE = 'I am a UDP Agent'
DEFAULT_AGENTID = "udpserver"
DEFAULT_HEARTBEAT_PERIOD = 5


#------
import crcmod


class Protocol:
    
    def __init__(self, *args, **kwargs):
        print("------------------------- > Adaptor Protocol Execute")
        self.tx = None
        self.rx = None
        self.msg = None
        self.command = None
        self.power = {'55': 'ON', 'AA': 'OFF'}
        
        self.mode = {'11': 'COLD', '22': 'HOT', '33': 
                    'AUTO', '44': 'FAN', '55': 'DRY'}
        
        self.fan = {'01': 'FAN1','02': 'FAN2','03': 'FAN3', '00' : 'FANA'}
        
        self.setpoint = {'00A0':'16', '00AA':'17', '00B4':'18', '00BE':'19' ,
                        '00C8':'20', '00D2':'21', '00DC':'22', '00E6': '23', 
                        '00F0': '24', '00FA': '25', '0104': '26', '010E':'27' }
        
    def crccal(self, hexstr): # Calculation CRC-16 from Command 
        crc16 = crcmod.mkCrcFun(0x18005,0xFFFF, True, 0x0000) # Initial State of CRC
        tmp = hex(crc16(bytes.fromhex(hexstr)))
        print("CRC = {}".format(tmp))
        tmp = tmp.split('x')[-1]
        
        while len(tmp) < 4 :
            tmp = "0"+tmp
        
        return hexstr+"{}{}".format(tmp[2:4], tmp[0:2])
    
    def encode(self, conf):  #Build Command for sending
        print("-------------------->  Method Encode Execute")
        print(conf) 
        self.msg = conf['msg']
        if self.msg == 'on_fix':
            self.command = '01069C4000556671'
        
        elif self.msg == 'off_fix':
            self.command = '01069C4000AA2631'
        
        elif self.msg == 'status':
            self.command = '01039C4000086B88'
        
        elif self.msg == 'variable_tx':
            print("------->  ENCODE FUNCTION EXECUTE <------------------")
            # if kwargs['power'] in self.power.values():
            power = dict((v,k) for k,v in self.power.items())[conf['power']]
            print(power)
            mode = dict((v,k) for k,v in self.mode.items())[conf['mode']]
            print(mode)
            setpoint = dict((v,k) for k,v in self.setpoint.items())[str(conf['setpoint'])]
            print(setpoint)
            fan = dict((v,k) for k,v in self.fan.items())[conf['fan']]
            print(fan)
            # print("ARGS : {}".format(kwargs['fan']))
            print({'power': power, 'mode': mode, 'fan': fan, 'setpoint':setpoint})
            # print({'power': power })
            
            self.tx_template = '01109C4000081000{power}000000{mode}00{fan}00000000{setpoint}0B01'.format(power=power, mode=mode, fan=fan, setpoint=setpoint)

            self.command = (self.crccal(self.tx_template)).upper()
            return self.command
        else:
            print("Not Found MSG Key")
            return None

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
    
    def sendconf(self, ipaddress):
        
        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 
                                        socket.IPPROTO_UDP)
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            self._socket.bind(("", self.port))
            payload = bytes.fromhex(self.adaptor)
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
        
        self.protocol = Protocol()
        self.adaptor = self.protocol.encode(self.command_conf)
        
        print("Log Command Encoded : {}".format(self.adaptor))
        
        # conf = adaptor.command
        # TODO : Send Command via UDP Server
        for ipaddress in self._module_set:
            print("IP Module : {}".format(ipaddress))
            self.sendconf(ipaddress)
    
    @PubSub.subscribe('pubsub', "discovery/send/command")
    def on_match_discover(self, peer, sender, bus,  topic, headers, message):
        
        self._logfn(
            "Peer: {0}, Sender: {1}:, Bus: {2}, Topic: {3}, Headers: {4}, "
            "Message: \n{5}".format(peer, sender, bus, topic, headers, pformat(message)))
        
        # Update module set start here
        msg = json.loads(message)
        self._module_set = msg.get('module', None) # If run in test please config IP-Address
        _log.info(msg="Found Module : {}".format(self._module_set))
        

    
    # @Core.periodic(60)
    # def on_interval(self):
    #     # Broadcast Message from UDP Server
    #     _log.info(msg="Send Command to module to get status")
        
    #     try:
    #         self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 
    #                                     socket.IPPROTO_UDP)
    #         self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    #         self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    #         self._socket.bind(("", self.port))

    #         sent = self._socket.sendto(self.broadcast_msg, ('<broadcast>', self.port))

    #     except Exception as e:
    #         _log.error(msg="Error : {}".format(e))
        


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
