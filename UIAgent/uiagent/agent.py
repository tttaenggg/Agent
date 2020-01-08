"""
Agent documentation goes here.
"""

__docformat__ = 'reStructuredText'

import logging
import sys
from volttron.platform.agent import utils
from volttron.platform.vip.agent import Agent, Core, RPC, PubSub
from tkinter import *
import tkinter


_log = logging.getLogger(__name__)
utils.setup_logging()
__version__ = "0.1"


DEFAULT_MESSAGE = 'I am a UI Agent'
DEFAULT_AGENTID = "uiagent"
DEFAULT_HEARTBEAT_PERIOD = 5


class Uiagent(Agent):
    """
    Document agent constructor here.
    """

    def __init__(self, config_path,
                 **kwargs):
        super().__init__(**kwargs)
        self.config = utils.load_config(config_path)
        
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
        top = tkinter.Tk()
        # Code to add widgets will go here...

        top.geometry("480x320")
        
        def ecoCallBack():
            # TODO : Send Command Here
            pass

        def drCallBack():
            # TODO : Send Command Here
            pass

        def doSendCommand():
            print(switch_variable.get())

        eco_btn = Button(top, text = "ECO MODE", command = ecoCallBack, height = 5, width = 15)
        eco_btn.grid(row=2, column=0)
        eco_btn.place(x = 10,y = 30)

        dr_btn = Button(top, text = "DR MODE", command = drCallBack, height = 5, width = 15)
        dr_btn.grid(row=2, column=0)
        dr_btn.place(x = 10,y = 150)

        ok_btn = Button(top, text = "OK", command = doSendCommand, height = 5, width = 30)
        ok_btn.grid(row=2, column=0)
        ok_btn.place(x = 180,y = 150)

        switch_frame = tkinter.Frame(top)
        switch_frame.pack()

        switch_variable = IntVar()
        switch_variable.set(1)
        # selection = var.get()

        switch_variable = tkinter.StringVar(value="medium")

        aut_button = tkinter.Radiobutton(switch_frame, text="Auto", variable=switch_variable,
                                    indicatoron=False, value="auto", width=8)
        low_button = tkinter.Radiobutton(switch_frame, text="Low", variable=switch_variable,
                                    indicatoron=False, value="low", width=8)
        med_button = tkinter.Radiobutton(switch_frame, text="Medium", variable=switch_variable,
                                    indicatoron=False, value="medium", width=8)
        high_button = tkinter.Radiobutton(switch_frame, text="High", variable=switch_variable,
                                    indicatoron=False, value="high", width=8)

        aut_button.pack(side="left")
        low_button.pack(side="left")
        med_button.pack(side="left")
        high_button.pack(side="left")

        switch_frame.place(x=180, y=30)



        if switch_variable.get() == 'auto':
            print('auto')
        elif switch_variable.get() =='low':
            print('low')
        elif switch_variable.get() =='medium':
            print('medium')
        elif switch_variable.get() == 'high':
            print('high')
        else:
            print('Can not get val')

        top.mainloop()
        
        

    @Core.receiver("onstop")
    def onstop(self, sender, **kwargs):
        """
        This method is called when the Agent is about to shutdown, but before it disconnects from
        the message bus.
        """
        pass

    @RPC.export
    def rpc_method(self, arg1, arg2, kwarg1=None, kwarg2=None):
        """
        RPC method

        May be called from another agent via self.core.rpc.call """
        return self.setting1 + arg1 - arg2

def main():
    """Main method called to start the agent."""
    utils.vip_main(Uiagent, 
                   version=__version__)


if __name__ == '__main__':
    # Entry point for script
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        pass
