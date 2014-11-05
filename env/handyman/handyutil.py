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



class cToolBase(object):
      def __init__(self, arg=None):          
       super(cToolBase, self).__init__()
       return
      def enqueue_fn(self, arg=None):
       hToolObj = handyman_main.handyMantool.getToolInstance() 
       if isinstance(arg, cEvent):
        hToolObj.enqueue_new_event(arg)
       elif isinstance(arg, cToolParam):
        hToolObj.paramList.append(arg)
       return
      @property
      def hTool(self):
          self._hTool = handyman_main.handyMantool.getToolInstance() 
          return self._hTool
       
     
class cEvent(object):
      def __init__(self, evtType=None,
                   evtName=None,
                   evtPayload=None,
                   evtPayload_fn = None):
       self._event_type = evtType
       self._event_name = evtName
       self._event_payload = evtPayload
       self._event_payload_fn = evtPayload_fn
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
      
class cHandyUtil(cToolBase):
    def __init__(self):
        return
    @classmethod
    def greetMe123(self, string):        
        self.enqueue_fn(cEvent("task", "greet", string))
        return
    def init_tool_params(self, arg=None):
        self.enqueue_fn(cToolParam(paramShort='-gabu',
                     paramHelp='guucha puucha',
                     paramAction='append',
                     paramNargs ='?',
                     #paramType=self.get_callback_fn('test_callbackfn')
                     ))
        pass
        return

    def utilParseParams(self, tmpObj=None):
        parser1 = self.hTool.toolParser

        for entries in self.hTool.paramList:
          parser1.add_argument(entries.paramShort, 
                               help=entries.paramHelp,
                               dest=entries.paramDest,
                               action=entries.paramAction,
                               nargs=entries.paramNargs,
                               type=entries.paramType)




        args = parser1.parse_args() 
        self.hTool.toolArgs = args    
        return

    def utilVer():
        selfVer = "0.0.1u"      
        return selfVer

class cEnvConfigVar(object):
    def __init__(self, file=None):
     self._conf = ConfigObj(file,
                            list_values=True,
                            indent_type='    ')
     pass
    @property
    def conf(self):
        return self._conf
    @conf.setter
    def conf(self, value):
        self._conf = value
    def dump_sample_data(self, arg=None):
     """ 
     self.conf['mbuser'] = {}
     self.conf['mbuser']['sshbookmarks'] = {}
     self.conf['mbuser']['sshbookmarks']['bm001'] = {
                                  "bookmarkname" : "ssh5050via465",
                                  "sshtoIP" : "127.0.0.1",
                                  "bindtoLocalPort" : "5050",
                                  "sshtoPort" : "465",
                                  "sshoptions" : "-C -N"

                                  }
     """
     #self.conf.write()
     #self.conf
     #self.conf.append()
     #print self.conf.sections
     #print self.conf.scalars
     #print self.conf.section('mbuser')
     #print list(self.conf['mbuser']['sshbookmarks'])
     #('bookmarkname')

     #for itr in self.conf.itervalues():
     # print itr
     for level1 in self.conf.sections:
      for level2 in self.conf[level1]:
        print list(self.conf[level1][level2])
        
          
     return
    def parse_conf(self, arg=None):

     return


class cToolWorker(cToolBase):
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
        self.enqueue_fn(cEvent(evtName="homeland",evtPayload_fn=
                    #self.generic_actionfn))
                    self.hTool.envConfig.dump_sample_data))
                    #cEnvConfigVar().dump_sample_data))
        return
    def opentunnel_actionfn(self, eventObj=None):

        #print subprocess.Popen(["ssh", "root@107.170.194.30", "-D 65000", "-C", "-p 465"],
        #                 shell=False,
        #                 stdout=subprocess.PIPE,
        #                 stderr=subprocess.PIPE
        #                )
        b1 = sshBookmark()        
        self.enqueue_fn(cEvent("subtask","spawnssh", 
                                   b1, self.spawnssh_callbackfn),                                   
                                  )
        return


def myprint(args):
  print args
  return






