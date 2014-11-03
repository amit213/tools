#!/usr/bin/env python
#
#util used by wrapper tool for automation and env config.
#
import argparse
#from handyman_main import handyMantool
import handyman_main
#from handyman_main import *

import subprocess
from subprocess import PIPE


class cEvent(object):
      def __init__(self, event_type=None,
                   event_name=None,
                   event_payload=None):
       self._event_type = event_type
       self._event_name = event_name
       self._event_payload = event_payload
       return
      @property
      def event_type(self):
          return self._event_type
      @event_type.setter
      def set_event_type(self, value):
          self._event_type = value
      @property
      def event_name(self):
          return self._event_name
      @event_name.setter
      def event_name(self, value):
          self._event_name = value
      @property
      def event_payload(self):
          return self._event_payload
      @event_payload.setter
      def event_payload(self, value):
          self._event_payload = value
      
      
class cHandyUtil(object):
    def __init__(self):
        return
    @classmethod
    def greetMe123(string):         
        #e1 = cEvent("task", "greet", string)
        hToolObj = None 
        hToolObj = handyman_main.handyMantool.getToolInstance() 
        hToolObj.enqueue_new_event(cEvent("task", "greet", string))
        return

    def utilParseParams(self, tmpObj=None):
        hToolObj = None 
        hToolObj = handyman_main.handyMantool.getToolInstance()     
        parser1 = hToolObj.toolParser
                
        for entries in hToolObj.getParamTable():        
            parser1.add_argument(entries[0], help=entries[1])
        #parser1.add_argument("foobog", nargs='?', type=int)
        fn = hToolObj.holaecho

        parser1.add_argument("-task", help="specify the task name", \
                            dest='task', action='append', nargs='+')
        parser1.add_argument("-pack", help="specify the task name", \
                            dest=None, action='append')

        parser1.add_argument("-bookmark", action=None)      

        parser1.add_argument("-greet", type=fn)
        args = parser1.parse_args() 
        hToolObj.toolArgs = args    
        return

    def utilVer():
        selfVer = "0.0.1u"      
        return selfVer


class cToolWorker(object):
    """docstring for cToolWorker"""
    def __init__(self, arg=None):
        super(cToolWorker, self).__init__()
        self.arg = arg
        return
    def samplebox_actionfn(self, eventObj=None):
        print 'SAMPLE_BOX ========>', eventObj.event_name
        return
    def generic_actionfn(self, eventObj=None):
        print "**", eventObj.event_name
        return
    def scanwifi_actionfn(self, eventObj=None):
        #print 'scanwifi ========>', eventObj.event_name
        print os.system("/System/Library/"
            "PrivateFrameworks/Apple80211.framework/Resources/airport --scan")
        return
    def opentunnel_actionfn(self, eventObj=None):
        print subprocess.Popen(["ssh", "root@107.170.194.30", "-D 65000", "-C", "-p 465"],
                         shell=False,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE
                        )        
        return


def myprint(args):
  print args
  return






