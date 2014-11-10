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
import feedparser

class cTryRun(object):
      def __init__(self):
        pass

class cToolBase(object):
      def __init__(self, arg=None):          
       super(cToolBase, self).__init__()
       return
      @classmethod
      def base_echo(self, arg):
       print arg
       return
      def enqueue_fn(self, arg=None, tags=None):
       #import handyman_main
       hToolObj = handyman_main.handyMantool.getToolInstance() 
       if isinstance(arg, cEvent):
        hToolObj.enqueue_new_event(arg)
       elif isinstance(arg, cToolParam):
        hToolObj.paramList.append(arg)
       return
      def raise_error(self, event=None, errmsg=None):
       if type(event) is cEvent:
         if type(errmsg) is str:          
          event.event_payload = event.event_name + ' : ' + errmsg
          event.event_payload_fn = self.getfn('raise_error_callbackfn')
          self.enqueue_fn(event)
       return 
      def getfn(self, fnName=None, 
                argSwitch=None,
                headKeyword=None):
        fn = None        
        if fnName:      
         for memberobj in self.hTool.membObjList:
           for method in dir(getattr(self.hTool, memberobj)):
             if callable((getattr(getattr(self.hTool, memberobj),method))) and method == fnName:            
              fn = getattr(getattr(self.hTool, memberobj),method)
        # search fn signature from standard list of callbacks and actionfn(s)              
        if argSwitch is not None:
          if headKeyword is not None:
            if hasattr(self.hTool.toolWorker, headKeyword.lower() + '_actionfn'):
              fn = getattr(self.hTool.toolWorker, headKeyword.lower() + '_actionfn')
            #if hasattr(self.hTool.toolWorker, argSwitch.lower() + '_actionfn'):
            #  fn = getattr(self.hTool.toolWorker, argSwitch.lower() + '_actionfn')

        if fn is None:
          fn = getattr(self.hTool.toolWorker, 'generic' + '_actionfn')        
        return fn
      def getParamfromArgSwitch(self,argSwitch=None):
        tmpParamobj=None
        for param in self.hTool.paramList:
          if argSwitch == param.paramDest:
              tmpParamobj = param              
        return tmpParamobj
      def getPhrase(self, eventObj=None, 
                    returnType=None, 
                    filler=None):
        retval = ""
        if filler is None:
          filler = ""
        if eventObj is not None and type(eventObj) is cEvent:
          tmpList = list(eventObj.event_payload.getPhrase())

          #exclude the head
          tmpList.pop(0)

          # reverse it so that the final output comes out 
          # in proper order as fed in by the user.
          tmpList.reverse()          
          if tmpList is not None:
            #for token in eventObj.event_payload.getPhrase():
            for token in tmpList:
              retval = token + filler + retval
        return retval

      @property
      def hTool(self):
          self._hTool = handyman_main.handyMantool.getToolInstance() 
          return self._hTool
       
     
class cEvent(cToolBase):
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
                  paramType=None, paramKeywordMap=None,                
                 ):
      super(cToolParam, self).__init__()
      self.paramShort = paramShort
      self.paramHelp = paramHelp
      self.paramAction = paramAction
      self.paramDest = paramDest
      self.paramNargs = paramNargs
      self.paramType = paramType
      self.arg = arg
      self.paramKeywordMap = paramKeywordMap
      return
      @property
      def paramKeywordMap(self):
          return self._paramKeywordMap
      @paramKeywordMap.setter
      def paramKeywordMap(self, value):
          self._paramKeywordMap = value      
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

class cToolPayload(cToolBase):
      def __init__(self, payloadToolParamObj=None,
                   payloadArgPhrase=None):
       self._payloadList=[]
       self.packPayload(payloadToolParamObj)
       self.packPayload(payloadArgPhrase)
       return      
      def packPayload(self, value):
          self._payloadList.append(value)
      @property
      def payload(self):
          return self._payloadList
      def getPhrase(self):
          return self._payloadList[1]

class sshBookmark(cToolBase):
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

    def init_tool_params(self, eventObj=None, arg=None):

        self.enqueue_fn(cToolParam(paramShort='-test',
                     paramHelp='calling testfn',
                     paramAction='append',
                     paramNargs ='*',                     
                     #paramType=self.getfn(fnName='test_callbackfn')
                     ))
        self.enqueue_fn(cToolParam(paramShort='-dump',
                     paramHelp='dump sample config file',
                     paramAction='append',
                     paramNargs ='?'
                     ))
        self.enqueue_fn(cToolParam(paramShort='-task',
                     paramHelp='task to execute',
                     paramAction='append',
                     paramNargs ='+',                     
                     paramDest='task',
                     paramKeywordMap={'gnews'  : 'get_news_headlines',
                                      'search' : 'generate_search_result'
                                     }                                     
                     ))
        self.enqueue_fn(cToolParam(paramShort='-greet',
                     paramHelp='greetings on your way',
                     paramAction='append',
                     paramNargs ='+',                     
                     paramType=self.hTool.holaecho
                     ))
        self.enqueue_fn(cToolParam(paramShort='-list',
                     paramHelp='list items of your interest',
                     paramAction='append',
                     paramNargs ='+',                     
                     paramDest='list',
                     paramKeywordMap={'bm' : 'bm_callbackfn'
                                     }                     
                     #paramType=self.getfn(fnName='list_actionfn')                     
                     ))                             
        pass
        return


    def utilParseParams(self, tmpObj=None):        

        for entries in self.hTool.paramList:
          self.hTool.toolParser.add_argument(entries.paramShort, 
                               help=entries.paramHelp,
                               dest=entries.paramDest,
                               action=entries.paramAction,
                               nargs=entries.paramNargs,
                               type=entries.paramType)

        self.hTool.toolArgs = self.hTool.toolParser.parse_args()         
        return

    def utilVer():
        selfVer = "0.0.1u"      
        return selfVer

    def gen_event_for_argPhrase(self, argSwitch=None, 
                                switchValueList=None):        
        if switchValueList is not None:
          listOflists = list(switchValueList)
          while listOflists:
            phrase = listOflists.pop(0)
            headKeyword = phrase[0]
            pyld = cToolPayload(
                        payloadToolParamObj=self.getParamfromArgSwitch(argSwitch),
                        payloadArgPhrase=phrase)  

            self.enqueue_fn(cEvent(evtType=argSwitch, 
                        evtName=headKeyword,
                        evtPayload=pyld,
                        evtPayload_fn=self.getfn(argSwitch=argSwitch, 
                                                 headKeyword=headKeyword)),
                        tags=None)
        return

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
    def raise_error_callbackfn(self, eventObj=None):
        if type(eventObj) is cEvent and eventObj is not None:
           print eventObj.event_payload
        return    
    def samplebox_actionfn(self, eventObj=None):
        pass
        return

    def generate_search_result(self, eventObj=None):        
        import feedparser
        searchKey = u'local'
        searchKey = self.getPhrase(eventObj=eventObj, filler='+')
        #url = 'http://www.google.com/search?q=' + searchKey
        url = 'http://www.google.com/search?q=akshar'
        import requests
        #from bs4 import BeautifulSoup
        url = "http://search.yahoo.com/search?p=%s"
        query = "python"
        r = requests.get(url % query) 

        
        


    def get_news_headlines(self, eventObj=None):        
        import feedparser
        searchKey=u'local'
        #url = 'http://news.google.com/news?pz=1&cf=all&ned=us&hl=en&q=openstack&output=rss'
        searchKey=self.getPhrase(eventObj=eventObj,
                                 filler='+')
        #url = 'http://news.google.com/news?pz=1&cf=all&ned=us&hl=en&output=rss'
        #url = 'http://news.google.com/news?pz=1&cf=all&ned=us&hl=en&topic=snc&output=rss'
        #url = 'http://www.bhaskar.com/rss-feed/2313/'

        #url = 'http://news.google.com/news?pz=1&cf=all&ned=us&hl=en&q=' + searchKey + '&output=rss'
        url = 'http://feeds.bbci.co.uk/news/rss.xml'

        # just some GNews feed - I'll use a specific search later
        feed = feedparser.parse(url)
        for post in feed.entries:
           print post.title
        return
    def generic_actionfn(self, eventObj=None):        
        argIsconsumed=False        
        if type(eventObj.event_payload) is cToolPayload:
          tmpparam = eventObj.event_payload.payload[0]
          if eventObj.event_name in tmpparam.paramKeywordMap.keys():
            tmpfn = self.getfn(tmpparam.paramKeywordMap[eventObj.event_name])
            #self.enqueue_fn(cEvent(evtPayload_fn=tmpfn))
            eventObj.event_payload_fn = tmpfn
            self.enqueue_fn(eventObj)
            argIsconsumed=True

        if not argIsconsumed:
          print "**", eventObj.event_name, eventObj.event_type
          eventObj.raise_error(event=eventObj, 
                 errmsg='invalid ' + eventObj.event_type + ' option')

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
                    #self.hTool.envConfig.dump_sample_data))
                    self.getfn('dump_sample_data')))
                    #cEnvConfigVar().dump_sample_data))
        print self.getfn('dump_sample_data').im_class
        return
    def list_actionfn(self, eventObj=None):
        #print "calling list_actionfn ", type(eventObj), eventObj #eventObj.event_name

        #if type(eventObj) is cEvent:
        #  eventObj.event_payload = eventObj.event_name + " is an invalid list option."
        #  eventObj.event_payload_fn = self.getfn('raise_error_callbackfn')
        #  self.enqueue_fn(eventObj)
        #eventObj.event_name
        #eventObj.event_payload_fn=self.hTool.holaecho
        #self.enqueue_fn(eventObj)

        if type(eventObj) is cEvent:
         self.raise_error(event=eventObj, errmsg='invalid list option')
        elif type(eventObj) is str:
         # test code
         # 
         self.raise_error(errmsg=eventObj) 
        return        
    def bm_callbackfn(self, eventObj=None):
        print "printing the big list of bookmarks", eventObj.event_name, eventObj.event_payload.getPhrase()
        if type(eventObj) is cEvent:        
          if type(eventObj.event_payload) is cToolPayload:
            #print 'proper payload --> ', eventObj.event_payload.getPhrase()
            pass
        return
    def handysleep_callbackfn(self, eventObj=None):
        from time import sleep
        sleep(2)
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






