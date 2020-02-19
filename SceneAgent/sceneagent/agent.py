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
import time
from multiprocessing import Process
import asyncio

_log = logging.getLogger(__name__)
utils.setup_logging()
__version__ = "0.1"

DEFAULT_MESSAGE = 'I am a Scene Agent'
DEFAULT_AGENTID = "SceneAgent"
DEFAULT_HEARTBEAT_PERIOD = 5



class Sceneagent(Agent):

    def __init__(self, config_path,
                 **kwargs):
        super().__init__(**kwargs)

        self.config = utils.load_config(config_path)
        self._agent_id = self.config.get('agentid', DEFAULT_AGENTID)
        self._message = self.config.get('message', DEFAULT_MESSAGE)
        self._heartbeat_period = self.config.get('heartbeat_period',
                                                 DEFAULT_HEARTBEAT_PERIOD)
        self._scenelist_path = self.config.get('scenelistpath')
        self.sceneconf = json.load(open(self._scenelist_path))

        _log.info(">>> : Found {} Scene Control List".format(len(self.sceneconf.get('scenelist'))))

        self.scenelist = self.sceneconf.get('scenelist')
        self.sceneid = [scene.get('sceneid') for scene in self.scenelist]
        _log.info(">>> : Scene ID : {}".format(self.sceneid))



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


    async def sendCommand(self, data):

        pub_topic = data.get('topic')
        pub_body = data.get('body')
        pid = data.get('id')

        _log.debug(msg="MultiProcess : {}".format(pid))
        _log.debug("TOPIC PUB : {}".format(pub_topic))
        _log.debug("BODY : {}".format(pub_body))
        _log.debug("----------------------------------------------")

        self.vip.pubsub.publish('pubsub', pub_topic,
                                message=pub_body
                                )

        _log.info("Published")


    @PubSub.subscribe('pubsub', "web/control/scene")
    def on_match_sendcommand(self, peer, sender, bus,  topic, headers, message):
        _topic = self.sceneconf.get('topic')
        sceneid = message.get('sceneid')

        procs = []

        if sceneid in self.sceneid:
            _log.debug(" >>> :Scene ID matched")
            for i in self.scenelist:

                if sceneid == i.get('sceneid'):
                    # - do stuff control Device
                    scenecontrol = i.get('scenecontrol')
                    # _log.debug("GET SCENE CONTROL : {}".format(scenecontrol))
                    break
            i = 0
            for device in scenecontrol:

                pub_topic = _topic + (device.get('device_type')).lower()
                pub_body = device.get('device_control')

                data = {"topic": pub_topic, "body": pub_body,"id": i}
                # self.sendCommand(data=data)

                # asyncio.run(self.sendCommand(device))

                loop = asyncio.get_event_loop()
                loop.run_until_complete(self.sendCommand(data))
                # i += 1
                # proc = Process(target=self.sendCommand, args=(data,))
                # procs.append(proc)
                # proc.start()


            # TODO : remove if no need waitting
            # for proc in procs:
            #     pid = proc.pid
            #     proc.join()
            #     _log.info(msg="Process ID : {} Completed".format(pid))



def main():
    """Main method called to start the agent."""
    utils.vip_main(Sceneagent,
                   version=__version__)


if __name__ == '__main__':
    # Entry point for script
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        pass
