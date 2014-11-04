#!/usr/bin/env python
#
#util used by wrapper tool for automation and env config.
#
import argparse
#from handyman_main import handyMantool
import handyman_main
#from handyman_main import *
import os
import subprocess
import ConfigParser
from configobj import ConfigObj


class cEvent(object):
      def __init__(self, event_type=None,
                   event_name=None,
                   event_payload=None,
                   event_payload_fn = None):
       self._event_type = event_type
       self._event_name = event_name
       self._event_payload = event_payload
       self._event_payload_fn = event_payload_fn
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
      @property
      def event_payload_fn(self):
          return self._event_payload_fn
      @event_payload_fn.setter
      def event_payload_fn(self, value):
          self._event_payload_fn = value

class cToolParam(object):
     """docstring for cToolParam"""
     def __init__(self, arg=None, paramShort=None,
                  paramHelp=None, paramAction=None,
                  paramDest=None, paramNargs=None,
                  paramType=None                  
                 ):
      super(cToolParam, self).__init__()
      self.paramShort = paramShort
      self.paramHelp = paramHelp
      self.paramAction = paramAction
      self.paramDest = paramDest
      self.paramNargs = paramNargs
      self.paramType = paramType
      self.arg = arg
      return
      @property
      def paramType(self):
          return self._paramType
      @paramType.setter
      def paramType(self, value):
          self._paramType = value
      
      
      @property
      def paramShort(self):
          return self._paramShort
      @paramShort.setter
      def paramShort(self, value):
          self._paramShort = value
      @property
      def paramHelp(self):
          return self._paramHelp
      @paramHelp.setter
      def paramHelp(self, value):
          self._paramHelp = value
      @property
      def paramAction(self):
          return self._paramAction
      @paramAction.setter
      def paramAction(self, value):
          self._paramAction = value
      @property
      def paramDest(self):
          return self._paramDest
      @paramDest.setter
      def paramDest(self, value):
          self._paramDest = value
      @property
      def paramNargs(self):
          return self._paramNargs
      @paramNargs.setter
      def paramNargs(self, value):
          self._paramNargs = value

      
class sshBookmark(object):
      #
      # store, launch and run ssh sessions.
      #
      def __init__(self):
       self.name="empty"
       return

      def __init__(self, name="null", 
                   connectToPort="22",
                   username="user"):
       self.name=name
       self.connectToPort=connectToPort
       self.username=username
       self.connectToIP=""
       return


      def list_bookmark(self):
       print self.name
       return
      
class cHandyUtil(object):
    def __init__(self):
        return
    @classmethod
    def greetMe123(string):
        hToolObj = handyman_main.handyMantool.getToolInstance() 
        hToolObj.enqueue_new_event(cEvent("task", "greet", string))
        return

    def utilParseParams(self, tmpObj=None):
        hToolObj = None 
        hToolObj = handyman_main.handyMantool.getToolInstance()     
        parser1 = hToolObj.toolParser
                
        for entries in hToolObj.paramList:
          parser1.add_argument(entries.paramShort, 
                               help=entries.paramHelp,
                               dest=entries.paramDest,
                               action=entries.paramAction,
                               nargs=entries.paramNargs,
                               type=entries.paramType)

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

class cEnvConfigVar(object):
    def __init__(self, file=None):
     self._conf = ConfigObj(file)
     pass
    def dump_sample_data():
     print "dumping sample data"
     return



class cToolWorker(object):
    """docstring for cToolWorker"""
    def __init__(self, arg=None):
        super(cToolWorker, self).__init__()
        self.arg = arg
        return
    def samplebox_actionfn(self, eventObj=None):
        pass
        return
    def generic_actionfn(self, eventObj=None):
        print "**", eventObj.event_name
        return
    def scanwifi_actionfn(self, eventObj=None):
        print os.system("/System/Library/"
            "PrivateFrameworks/Apple80211.framework/Resources/airport --scan")
        return
    def spawnssh_callbackfn(self, eventObj=None):
        print isinstance(eventObj.event_payload, sshBookmark)
        return
    def test_callbackfn(self, arg=None):
        print ">>>>>>>>>>>", arg
        return
    def opentunnel_actionfn(self, eventObj=None):

        #print subprocess.Popen(["ssh", "root@107.170.194.30", "-D 65000", "-C", "-p 465"],
        #                 shell=False,
        #                 stdout=subprocess.PIPE,
        #                 stderr=subprocess.PIPE
        #                )
        b1 = sshBookmark()
        hToolObj = handyman_main.handyMantool.getToolInstance() 
        hToolObj.enqueue_new_event(cEvent("subtask","spawnssh", 
                                   b1, self.spawnssh_callbackfn),                                   
                                  )
        return


def myprint(args):
  print args
  return






