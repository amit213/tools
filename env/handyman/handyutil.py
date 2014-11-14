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
          event.event_payload_fn = self.getfn('error_reporting_callbackfn')
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
          tmpList = list(eventObj.event_payload.getPayloadPhrase())

          #exclude the head          
          if tmpList is not None:
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

      def getPayloadPhrase(self, outType=None,
                           keepheadKeyword=True):
          payloaditem = ""
          retval = ""
          if outType is None:
            outType = list
          for payloaditem in self.payload:            
            if isinstance(payloaditem, list):
              retval = list(payloaditem)

          if (keepheadKeyword == False):
            retval.pop(0)
          if (outType == str):
            return ' '.join(retval)

          return retval

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
                     paramDest='test',
                     paramKeywordMap={
                            'sleep'   : 'handysleep_callbackfn',
                            'd'       : 'dump_sample_data',
                                     }
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
                     paramKeywordMap={
                       'feeds'   : 'process_feeds',
                       'search'  : 'generate_search_result',
                       'chro'    : 'launch_browser_tab',
                       'mailme'  : 'test_mailme',
                       'shellvar': 'process_shell_var'
                                     }                                     
                     ))
        self.enqueue_fn(cToolParam(paramShort='-greet',
                     paramHelp='greetings on your way',
                     paramAction='append',
                     paramNargs ='+',                     
                     #paramType=self.getfn(fnName='hola')
                     ))
        self.enqueue_fn(cToolParam(paramShort='-list',
                     paramHelp='list items of your interest',
                     paramAction='append',
                     paramNargs ='+',                     
                     paramDest='list',
                     paramKeywordMap={
                       'bm'     :  'bm_callbackfn',
                       'conf'   :  'dump_handytool_config',
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
              if (phrase.count(None) == len(phrase)):
                # the arg was directly consumed by the callback fn
                # specified with the param. So no further events required.
                pass
              else:
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

class cEnvConfigVar(cToolBase):
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
     

     #self.print_conf_entries(self.conf)
     #self.hTool.envConfig.append_conf_entries(
     #                              listofEntries=['feeds', 'feedbookmarks'],
     #                              dataKeyVal = {'tc' : 'http://tc-crunch123'})
     #self.print_conf_entries(self.conf)
     #self.commit_conf_to_file(self.conf)
     #tmpstr = 'does this go'

     #self.conf.walk(self.conf_walkfn,
     #               call_on_sections=True, keyarg=tmpstr)     

     return
    def save_keyval_to_conf(self, 
                            eventObj=None,
                            key=None,
                            val=None,                            
                            parentSection=None,
                           ):
     
     if eventObj is not None and type(eventObj) is cEvent:       
       argList = eventObj.event_payload.getPayloadPhrase(
                                     keepheadKeyword=True)       
       if len(argList) == 3:
        #section, key, val - we allow 3 items at a time for now.
        parentSection, key, val = argList


     self.conf.walk(self.conf_walkfn,
                    call_on_sections=True, 
                    keyarg=key,
                    valarg=val,
                    parentSection=parentSection,
                    )
     return

    def get_value_from_conf(self, key=None, val=None,
                            parentSection=None):
     resultList = []
     self.conf.walk(self.conf_walkfn,
                    call_on_sections=True, 
                    keyarg=key, 
                    parentSection=parentSection,
                    resultList=resultList)
     if len(resultList) > 0:
        return resultList
     return None
     
    def conf_walkfn(self, section, key, 
                    keyarg=None, valarg=None,
                    parentSection=None, resultList=None):

     if keyarg and valarg:       
       if parentSection is not None and section.name == parentSection:
         #print ' saving new value... ', keyarg , valarg, section.name
         section[keyarg] = valarg         
         self.enqueue_fn(
          cEvent(evtPayload_fn=self.hTool.envConfig.commit_conf_to_file))


     if keyarg is not None and key == keyarg:
        if parentSection is not None and section.name != parentSection:
          return          
        if resultList is not None:
          resultList.append(section[key])
     return

    def commit_conf_to_file(self, confObjArg=None):
     if confObjArg is None or type(confObjArg) is not ConfigObj:
       confObjArg = self.hTool.envConfig.conf
     if confObjArg is not None and type(confObjArg) is ConfigObj: 
          confObjArg.write()
     return
    def append_conf_entries(self, 
                            listofEntries=None,
                            dataKeyVal=None):
     
     #self.conf["".join(self.conf.keys())][''.join(word)] = {}
     self.conf["".join(self.conf.keys())][''.join(listofEntries[0])] = {}
     self.conf["".join(self.conf.keys())][''.join(listofEntries[0])][''.join(listofEntries[1])] = {}
     self.conf["".join(self.conf.keys())][''.join(listofEntries[0])][''.join(listofEntries[1])] =  dataKeyVal
     #self.conf[self.conf.keys()][listofEntries[0]][listofEntries[1]]= 
     return

    def print_conf_entries(self, confObj=None):     
     if confObj is not ConfigObj:
        confObj = self.hTool.envConfig.conf

     if confObj is not None and type(confObj) is ConfigObj: 
       for itr in confObj.iterkeys():
         print '* ', itr, ' *'
       for level1 in confObj.sections:
        for level2 in confObj[level1]:
          print 'Section : ',level2
          print ' ',list(confObj[level1][level2])
          for data in confObj[level1][level2]:
            print '   ',confObj[level1][level2][data]
    def parse_conf(self, arg=None):

     return


class cToolWorker(cToolBase):
    """docstring for cToolWorker"""
    def __init__(self, arg=None):
        super(cToolWorker, self).__init__()
        self.arg = arg
        return
    def error_reporting_callbackfn(self, eventObj=None):
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

    def hola(self, hola='Florida'):
        if type(hola) is str:
          print "echoing :", hola        
        elif type(hola) is cEvent:
          print "echoing event :", hola.event_name        
        pass

    def spawn_this_cmd(self, eventObj=None):
        if type(eventObj.event_payload) is cToolPayload:
          cmdstr = eventObj.event_payload.getPayloadPhrase(phraseType=str)          
          #print subprocess.Popen(["ssh", "root@107.170.194.30", "-D 65000", "-C", "-p 465"],
          #print subprocess.Popen(["touch","/tmp/chimpfoobog.txt"],
          subprocess.Popen([cmdstr],
                           shell=False,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE
                          )
        return 

    def process_shell_var(self, eventObj=None):
        tmpstr =  eventObj.event_payload.getPayloadPhrase(outType=str,
                                     keepheadKeyword=True)
        tmplst = tmpstr.split()
        print tmplst[0]
        print ("".join(tmplst[1])).split('=')
        #if "=" in "".join(tmplst[1]) : 
        #  print "true"
        return    
    def test_mailme(self, eventObj=None):
        #cmdstr = 'echo subject | mail -s "`date`" trigger@recipe.ifttt.com  -f fgdswcfc@sharklasers.com'
        #cmdstr = 'touch /tmp/chimpfoobog.txt'
        #self.enqueue_fn(cEvent(evtName='spawn browser tab',
        #     evtPayload=cToolPayload(payloadArgPhrase=cmdstr),
        #     evtPayload_fn=self.spawn_this_cmd))

        """
        import smtplib
        from email.mime.text import MIMEText
        msg = MIMEText('hello Zion')
        msg['Subject'] = 'The contents of wall'
        msg['From'] = 'selfemailid'
        msg['To'] = 'trigger@recipe.ifttt.com'
        s = smtplib.SMTP('localhost')
        s.sendmail(me, [you], msg.as_string())
        s.quit()
        return """
    def spawn_browser_tab(self, eventObj=None):
        if type(eventObj.event_payload) is cToolPayload:
          url = eventObj.event_payload.getPayloadPhrase(phraseType=str)
          import webbrowser
          new = 2
          webbrowser.open(url,new=new)
        return 
    def launch_browser_tab(self, eventObj=None):              
        searchKey=""
        searchKey=self.getPhrase(eventObj=eventObj,
                                 filler='+')        
        url = 'http://www.google.com/search?q=' + searchKey
        #url = 'https://www.google.com/search?num=100&q=site:lifehacker.com&site:amazon.com&q=%s' % searchKey
        #url = 'https://www.google.com/search?num=100&q=site:lifehacker.com&site:amazon.com&q=' + searchKey
        #url = 'https://www.google.com/search?num=100&q=site:lifehacker.com&site:amazon.com&q=iphone6'        
        
        self.enqueue_fn(cEvent(evtName='spawn browser tab',
             evtPayload=cToolPayload(payloadArgPhrase=url),
             evtPayload_fn=self.spawn_browser_tab))
        return
    def process_feeds(self, eventObj=None):        
        import feedparser
        searchKey=u''
        #searchKey=self.getPhrase(eventObj=eventObj,
        #                         filler='+')
        feedArgs =  eventObj.event_payload.getPayloadPhrase(
                                     keepheadKeyword=False)

        #check if it's a bookmark saving task.
        if len(feedArgs) >= 2 and feedArgs[0] == 'bm':
          #this indicates key=val format.
          #feedArgs.pop(0)
          feedArgs[0] = 'feedbookmarks'
          feedbmList = (" ".join(feedArgs)).split(' ')
          self.enqueue_fn(
               cEvent(
                evtPayload=cToolPayload(payloadArgPhrase=feedbmList),
                evtPayload_fn=self.hTool.envConfig.save_keyval_to_conf))
          return

        if len(feedArgs) <= 0:
          feedsourcebm = 'gnews'
        elif len(feedArgs) > 1:
          feedsourcebm = feedArgs.pop(0)
          searchKey = '+'.join(feedArgs)
        else:
          feedsourcebm = feedArgs.pop(0)

        urlbm = self.hTool.envConfig.get_value_from_conf(feedsourcebm, 
                                     parentSection='feedbookmarks')
        
        if urlbm:

          url = ''.join(urlbm)
          url = url + searchKey

          feed = feedparser.parse(url)
          for post in feed.entries:
             print post.title

        return
    def generic_actionfn(self, eventObj=None):        
        argIsconsumed=False        
        if type(eventObj.event_payload) is cToolPayload:
          tmpparam = eventObj.event_payload.payload[0]
          if hasattr(tmpparam, 'paramKeywordMap'):
            if eventObj.event_name in tmpparam.paramKeywordMap.keys():
              tmpfn = self.getfn(tmpparam.paramKeywordMap[eventObj.event_name])
              #self.enqueue_fn(cEvent(evtPayload_fn=tmpfn))
              eventObj.event_payload_fn = tmpfn
              self.enqueue_fn(eventObj)
              argIsconsumed=True

        if not argIsconsumed:
          #print "**", eventObj.event_name, eventObj.event_type
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
        #napDuration = float(eventObj.event_payload.getPayloadPhrase(outType=str,
        #                             keepheadKeyword=True))
        napDuration=1
        sleep(napDuration)
        return
    def dump_handytool_config(self, eventObj=None):
        self.enqueue_fn(
          cEvent(evtPayload_fn=self.hTool.envConfig.print_conf_entries))
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






