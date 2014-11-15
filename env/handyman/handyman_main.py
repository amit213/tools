#!/usr/bin/env python
#
#wrapper tool for automation and env config.
#
from handyutil import *
import argparse
import handyutil
from time import sleep

class cTryRun2(object):
      def __init__(self):
        pass

class handyMantool(object):
      _toolObj = None
      def __init__(self):
       self._toolBase = cToolBase()       
       self.paramList = []
       self._tag = None
       self._eventList = []       
       self._toolParser = argparse.ArgumentParser(description='The handyman is here.')
       self._toolArgs = None
       self._toolUtil = cHandyUtil()
       self._toolWorker = cToolWorker()
       self._envConfig = cEnvConfigVar(r'/tmp/gaboo.conf')
       self._membObjList = []
       self.compileMemberObjList()
       #self.q = cTryRun()
       return
      def init_tool(self, arg=None):
       #self.toolUtil.init_tool_params()
       #from handyutil import cToolBase
       #cToolBase.base_echo("mangle box 123")
       #print callable()

       #self.enqueue_new_event(cEvent("preshut", 
       #           "shutdown",
       #           evtPayload_fn=self.toolWorker.hola),
       #           tags='at end')

       self.enqueue_new_event(cEvent("housekeeping", 
                  "setupparamtable",
                  evtPayload_fn=self.toolUtil.init_tool_params))
       self.enqueue_new_event(cEvent("housekeeping", 
                  "initparamandparseargs",
                  evtPayload_fn=self.toolUtil.utilParseParams))
       self.enqueue_new_event(cEvent("housekeeping", 
                  "geneventsfromargs",
                  evtPayload_fn=self.gen_events_from_parsed_args))
       return
      @property
      def paramList(self):
          return self._paramList
      @paramList.setter
      def paramList(self, value):  #TODO confirm this action
          #self._paramList.append(value)
          self._paramList = value

      def getParamList(self): return self._paramList
      @property
      def envConfig(self):
          return self._envConfig
      @envConfig.setter
      def envConfig(self, value):
          self._envConfig = value
      
      @property
      def toolParser(self):
          return self._toolParser
      @property
      def toolArgs(self):
          return self._toolArgs
      @toolArgs.setter
      def toolArgs(self, value):
          self._toolArgs = value
      
      @property
      def eventList(self):
          return self._eventList
      @eventList.setter
      def eventList(self, value):
          self._eventList = value
      
      @property
      def tag(self):
          return self._tag
      @tag.setter
      def tag_setter(self, value):
          self._tag = value          
      @property
      def toolWorker(self):
          return self._toolWorker
      @property
      def toolUtil(self):
          return self._toolUtil
      @toolUtil.setter
      def toolUtil(self, value):
          self._toolUtil = value           
      @classmethod
      def init(cls):       
       return cls
      @classmethod
      def getToolInstance(self): 
       return handyMantool._toolObj

      @classmethod
      def setToolInstance(self, toolObj):
       handyman_main.handyMantool._toolObj = toolObj
       #self._toolBase.hTool = toolObj       
       return
      @property
      def membObjList(self):
          return self._membObjList
      @membObjList.setter
      def membObjList(self, value):
          self._membObjList.append(value)
          
      def compileMemberObjList(self, arg=None):
       for attr, value in self.__dict__.iteritems():
          self.membObjList = attr       
       return



      def gen_event_for_argSwitch(self, argSwitch=None, 
                                        switchValueList=None):
       """ argSwitch is -list, -task etc. top level switch. """
       """ switchValueList is the values supplied for given switch """         
       if switchValueList is not None :                  
         for itr in sum(switchValueList, []):
          if itr is not None:            
            if hasattr(self.toolWorker, itr.lower() + '_actionfn'):
              fn = getattr(self.toolWorker, itr.lower() + '_actionfn')
            elif hasattr(self.toolWorker, argSwitch.lower() + '_actionfn'):
              fn = getattr(self.toolWorker, argSwitch.lower() + '_actionfn')
            else:
              fn = getattr(self.toolWorker, 'generic' + '_actionfn')

            #attaching original param Entry as payload. For invoking call chain.
            eventPayload = None
            for param in self.paramList:
                if argSwitch == param.paramDest:
                 eventPayload = param
            
            self.enqueue_new_event(cEvent(evtType=argSwitch, 
                                          evtName=itr.lower(),
                                          evtPayload=eventPayload, 
                                          evtPayload_fn=fn),                                                     
                                   tags=None)

       return
      def gen_events_from_parsed_args(self, eventObj=None):
       for argSwitch in self.getmembListForObj(self.toolArgs):
          if getattr(self.toolArgs, argSwitch) is not None:
            switchValueList = getattr(self.toolArgs, argSwitch)
            if switchValueList is not None:             
             self.toolUtil.gen_event_for_argPhrase(argSwitch=argSwitch,
                                     switchValueList=switchValueList)

            #self.gen_event_for_argSwitch(
            #         argSwitch=argSwitch,  # -list, -task etc.
            #         switchValueList=switchValueList)  # -list <one two three>


       """
       if self.toolArgs.task is not None :
         for itr in sum(self.toolArgs.task, []):
            if hasattr(self.toolWorker, itr.lower() + '_actionfn'):
              fn = getattr(self.toolWorker, itr.lower() + '_actionfn')
            else:
              fn = getattr(self.toolWorker, 'generic' + '_actionfn')
            self.enqueue_new_event(cEvent('task', itr.lower(), None, fn),
                                   tags=None)
       """
       return

      #def tool_parse_params(self):
      # self.toolUtil.utilParseParams()       
      # self.gen_events_from_parsed_args()
      # return
      def enqueue_new_event(self, eventObj=None,
                            tags=None):
       if tags == 'insertBeforeLast':
         self.eventList.insert(len(self.eventList)-1, eventObj) 
       else:
         self.eventList.append(eventObj)       
       return

      @property
      def eventList(self):
       return self._eventList

      def printToolSummary(self):
       print self._toolArgs
       return

      def process_all_events(self):        
       for evt in self.eventList:
        func = evt.event_payload_fn
        eventObj = evt
        func(eventObj)
        #evt.event_payload_fn(evt)
        pass
       return 
      def get_callback_fn(self, name=None):
       return getattr(self.toolWorker,name)       

      def getmembListForObj(self, obj=None):
        lst1 = []
        for attr, value in obj.__dict__.iteritems():
          lst1.append(attr)
        return lst1



def printVer():
  print "handyman version :", selfVer
  utilVer()
  return

def create_ssh_bookmark():
  s1 = sshBookmark()
  s1.list_bookmark()
  return

def main():  
    
  h1 = handyMantool()
  
  h1.setToolInstance(h1)  

  h1.init_tool()

  h1.process_all_events()

  return


if __name__ == "__main__":  main()


