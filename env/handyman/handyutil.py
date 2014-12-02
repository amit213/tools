#!/usr/bin/env python
#
#util used by wrapper tool for automation and env config.
#
import argparse
import handyman_main
#from handyman_main import *
import os
import subprocess
import ConfigParser
from configobj import ConfigObj
import feedparser
import logging
import inspect
from inspect import currentframe, getframeinfo



class cToolException(Exception):
        pass
class cToolUnknownError(cToolException):
        pass

class cToolBase(object):
      """
      core base class to expose basic functions like
      enqueue and arg processing.
      Most new classes should have this as parent.
      """
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
            for token in tmpList:
              retval = token + filler + retval
        return retval

      def getArgPhrase(self, eventObj=None,
                       keepheadKeyword=None):
        retval = None        
        if eventObj and type(eventObj.event_payload) is cToolPayload:
           retval = eventObj.event_payload.getPayloadPhrase(
                                keepheadKeyword=keepheadKeyword)           
        return retval
      def getRedisInstance(self, dbNum=None):
        retval = None
        import redis
        # param as non-url redis.Redis(host='192.168.59.103',port=6500)
        redisurl = self.hTool.envConfig.get_value_from_conf(key='redisserverurl')
        dbgprint('connecting to redis server at (%s)'
                  % (redisurl))
        if redisurl:
          r = redis.from_url("".join(redisurl), db=dbNum)
          retval = r
        return retval

      def get_filtered_data(eventObj=None):
        retval = []
        retval = eventObj.hTool.toolWorker.redis_get_filtered_data(eventObj)
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
     """ class that wraps around all the tool 
         parameters exposed to the end user. 
         It can be dynamically manipulated to 
         support the plugin architecture.
     """
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
       
       #if type(payloadArgPhrase) is str:       
       payloadArgPhrase = list(payloadArgPhrase)

       self.packPayload(payloadArgPhrase)
       return      
      def packPayload(self, value):
          self._payloadList.append(value)
      @property
      def payload(self):
          return self._payloadList

      def getPayloadPhrase(self, outType=None,
                           keepheadKeyword=True,
                           argProcessing=False):
          payloaditem = ""
          retval = ""
          if outType is None:
            outType = list
          for payloaditem in self.payload:            
            if isinstance(payloaditem, list):
              retval = list(payloaditem)

          if (keepheadKeyword == False):
            retval.pop(0)
          
          if (outType == str) and argProcessing:
            return ' '.join(retval)
          if (outType == str):
            return ''.join(retval)
            


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
    """
    util interface class for basic util capabilities.
    """
    def __init__(self):
        self._logger = logging.getLogger()
        return
    @property
    def logger(self):
        return self._logger
    @logger.setter
    def logger(self, value):
        self._logger = value
    
    def init_tool_logger(self):
      #logging.basicConfig(filename='log_filename.txt')

      self.logger = logging.getLogger()
      self.logger.setLevel(logging.ERROR)
      logsh = logging.StreamHandler()
      logsh.setLevel(logging.DEBUG)
      #formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
      formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s')
      logsh.setFormatter(formatter)
      self.logger.addHandler(logsh)

      self.logger.debug('this is a debug msg')

      return
    def init_tool_params(self, eventObj=None, arg=None):
        self.init_tool_logger()
        self.enqueue_fn(cToolParam(paramShort='-test',
                     paramHelp='calling testfn',
                     paramAction='append',
                     paramNargs ='*',                     
                     #paramType=self.getfn(fnName='test_callbackfn')
                     paramDest='test',
                     paramKeywordMap={
                            'sleep'   : 'handysleep_callbackfn',
                            'd'       : 'dump_sample_data',
                            'plugin'  : 'invoke_plugin'
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
                       'shellvar': 'process_shell_var',
                       'conf'    : 'update_config_file',
                       'redis'   : 'redis_ops',
                       'i'       : 'dump_tool_info',
                       'words'   : 'generate_word_list',
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
        try:                                
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
                  dbgprint('argSwitch is (%s) phrase is (%s)' % (argSwitch, phrase))
                  pyld = cToolPayload(
                              payloadToolParamObj=self.getParamfromArgSwitch(argSwitch),
                              payloadArgPhrase=phrase)  

                  self.enqueue_fn(cEvent(evtType=argSwitch, 
                              evtName=headKeyword,
                              evtPayload=pyld,
                              evtPayload_fn=self.getfn(argSwitch=argSwitch, 
                                                       headKeyword=headKeyword)),
                              tags=None)
        except Exception, err:
           print "error : ",inspect.currentframe().f_back.f_code.co_name,": Line no.",inspect.currentframe().f_back.f_lineno, Exception, err
        finally:
           pass
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


     #print self.get_value_from_conf(key='feedbookmarks')
     #import tempfile
     #fp = tempfile.NamedTemporaryFile()
     #fp = tempfile.mktemp()
     #print fp.name
     #fp.write(u'Hello world!')
     #fp.seek(0)
     #print fp.read()
     #url = 'http://www.google.com/search?q=' + searchKey
     #url = 'https://en.wikipedia.org/wiki/Usa'
     #-----------------------
     return
     #-------------------------


     from threading import Thread
     #Threadarray = [0..20]

     for i in range(5):
      #Threadarray[i] = Thread(target=self.test_thread_proc)
      #Threadarray[i].start()
      t1 = Thread(target=self.test_thread_proc)
      t1.start()

     #t1.join()
     print "Exit--"
     return

    def test_thread_proc(self, arg=None):

     from time import sleep
     import time
     start_time = time.time()

     print 'Time Spent', (time.time() - start_time)
     return 

    def update_keyval_to_conf(self, 
                            eventObj=None,
                            key=None,
                            val=None,                            
                            parentSection=None,
                           ):
     createNewSection = False
     if eventObj is not None and type(eventObj) is cEvent:       
       argList = eventObj.event_payload.getPayloadPhrase(
                                     keepheadKeyword=True)

       if len(argList) == 1:
        parentSection = argList.pop(0)
        if not self.hTool.envConfig.does_section_exist(sectionName=parentSection):          
          createNewSection=True
       elif len(argList) == 2:
        parentSection, key = argList
       elif len(argList) == 3:
        #section, key, val - we allow 3 items at a time for now.
        parentSection, key, val = argList

     if createNewSection:
      tmpconfObj = self.hTool.envConfig.conf
      tmpList = tmpconfObj.keys()
      self.hTool.envConfig.conf[tmpList[0]][parentSection] = {}
      self.enqueue_fn(
          cEvent(evtPayload_fn=self.hTool.envConfig.commit_conf_to_file))
      return

     dbgprint('update item key=(%s) val=(%s) incoming-section=(%s)'
              % (key, val, parentSection))

     self.conf.walk(self.conf_walkfn,
                    call_on_sections=True, 
                    keyarg=key,
                    valarg=val,
                    parentSection=parentSection,
                    createNewSection=createNewSection,
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
                    parentSection=None, resultList=None,
                    sectionPresent=None,
                    createNewSection=None):

     if keyarg and valarg is None:
       if parentSection is not None and section.name == parentSection:         
         #this is a delete opration.
         if key == keyarg:           
           pass
                  
         self.enqueue_fn(
          cEvent(evtPayload_fn=self.hTool.envConfig.commit_conf_to_file))

     if keyarg and valarg:              
       if parentSection is not None and section.name == parentSection:
         dbgprint('saving new value key=(%s) val=(%s) section=(%s)'
                  % (keyarg, valarg, section.name))
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
    def does_section_exist(self, ConfigObj=None, sectionName=None):
     if sectionName:
       tmpbm = self.hTool.envConfig.get_value_from_conf(key=sectionName) 
       if tmpbm:
        return True
       else:
        return False
     return False
    def append_conf_entries(self, 
                            listofEntries=None,
                            dataKeyVal=None):
     
     return

    def print_conf_entries(self, confObj=None):
     """ Prints the config entries """
     try:
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
     except Exception, err:
       print Exception, err       

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
        url = 'http://www.google.com/search?q=' + searchKey        
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
          cmdstr = eventObj.event_payload.getPayloadPhrase(outType=str)          
          #print subprocess.Popen(["ssh", "root@107.170.194.30", "-D 65000", "-C", "-p 465"],
          #print subprocess.Popen(["touch","/tmp/chimpfoobog.txt"],
          subprocess.Popen([cmdstr],
                           shell=False,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE
                          )
        return 

    def process_shell_var(self, eventObj=None):

        tmpstr =  eventObj.event_payload.getPayloadPhrase(
                                     outType=str,
                                     keepheadKeyword=True)
        tmplst = tmpstr.split()
        print tmplst[0]

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
          url = eventObj.event_payload.getPayloadPhrase(outType=str)
          import webbrowser
          new = 2          
          webbrowser.open(url,new=new)
        return 

    def dump_tool_info(self, eventObj=None):
        """ this generates tool info / env info """
        try:
           userid = os.environ['USER']
           print 'user : ', userid, ' '
        except:
           pass
        return

    def launch_browser_tab(self, eventObj=None):              
        searchKey=""
        searchKey=self.getPhrase(eventObj=eventObj,
                                 filler='+')        
        url = 'http://www.google.com/search?q=' + searchKey
        
        self.enqueue_fn(cEvent(evtName='spawn browser tab',
             evtPayload=cToolPayload(payloadArgPhrase=url),
             evtPayload_fn=self.spawn_browser_tab))
        return
    def process_feeds(self, eventObj=None):
        """ read feeds / save feed source url bookmarks,
            other feeds related operations.
        """         
        import feedparser
        searchKey=u''
        feedArgs =  eventObj.event_payload.getPayloadPhrase(
                                     keepheadKeyword=False)

        if len(feedArgs) == 1 and feedArgs[0] == 'help':
          print ' feeds <source> <optional search keyword>'
          tmpbm = self.hTool.envConfig.get_value_from_conf(key='feedbookmarks')
          tmpbm = tmpbm.pop(0)
          for itr in tmpbm.keys():
            print ' - %-9s ' % itr , ' : ',tmpbm[itr]
          return
        #check if it's a bookmark saving task.
        if len(feedArgs) >= 2 and feedArgs[0] == 'bm':
          #this indicates "bm key val" format.
          feedArgs[0] = 'feedbookmarks'          
          feedbmList = (" ".join(feedArgs)).split(' ')    
          self.enqueue_fn(
              cEvent(
                evtPayload=cToolPayload(payloadArgPhrase=feedbmList),
                evtPayload_fn=self.hTool.envConfig.update_keyval_to_conf))
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
             self.save_to_temp_file(
               lineList=[post.link, post.title])

             #self.enqueue_fn(cEvent(evtName='spawn browser tab',
             #      evtPayload=cToolPayload(payloadArgPhrase=post.link),
             #      evtPayload_fn=self.spawn_browser_tab))     
        
        
        return
    def save_to_temp_file(self, lineList=None):
        """ template generator code. """
        fp = open("/tmp/testpad.html","a+")
        tmpList = []
        fp.write(u"\n\n")
        tmpList.append(u'<p>')
        tmpList.append(u'<a href="')
        tmpList.append(lineList[0])
        tmpList.append(u'">')
        tmpList.append(lineList[1])
        tmpList.append(u'</a>')
        tmpList.append(u'</p>')        
        fp.write(u" ".join(tmpList))
        tmpList = []

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
          dbgprint("unconsumed event: %s %s" % (eventObj.event_name, eventObj.event_type))
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
        self.enqueue_fn(cEvent(evtName="",evtPayload_fn=
                    self.getfn('dump_sample_data')))
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
            pass
        return
    def handysleep_callbackfn(self, eventObj=None):
        from time import sleep
        napDuration = 1
        arg = None
        if type(eventObj.event_payload) is cToolPayload:
          arg = eventObj.event_payload.getPayloadPhrase(
                                     outType = list,
                                     keepheadKeyword=True)        
        if arg and len(arg) > 1 and arg[0] == 'sleep':
          arg.pop(0)
        if arg and len(arg) >= 1: 
          napDuration = float("".join(arg))
        print 'sleeping for : ', napDuration
        sleep(napDuration)
        self.enqueue_fn(cEvent(
                evtPayload=cToolPayload(payloadArgPhrase=str(napDuration)),
                evtPayload_fn=self.handysleep_callbackfn))
        return
    def update_config_file(self, eventObj=None):
        if type(eventObj.event_payload) is cToolPayload:
           tmpPhrase = eventObj.event_payload.getPayloadPhrase(keepheadKeyword=True)
        if (len(tmpPhrase) >= 2) and tmpPhrase[0] == 'conf':
          tmpPhrase.pop(0)

        if tmpPhrase[0] == 'add':          
          tmpPhrase.pop(0)
          if len(tmpPhrase) == 1:
            #adding section.            
            tmpsection = tmpPhrase            
            self.enqueue_fn(
              cEvent(
                evtPayload=cToolPayload(payloadArgPhrase=tmpsection),
                evtPayload_fn=self.hTool.envConfig.update_keyval_to_conf)) 

          elif len(tmpPhrase) == 2:
            tmpkey, tmpval = tmpPhrase 
            #adding key val vars.            
            tmpList = []            
            tmpList.append('envvars')            
            tmpList = tmpList + tmpPhrase            
            self.enqueue_fn(
              cEvent(
                evtPayload=cToolPayload(payloadArgPhrase=tmpList),
                evtPayload_fn=self.hTool.envConfig.update_keyval_to_conf))
          return

        return

    def generate_word_list(self, eventObj=None):
        match = 'a'
        tmpList = self.getArgPhrase(eventObj=eventObj)
        if tmpList[0] != 'words':
          return        
        tmpList.pop(0)
        if len(tmpList) >= 1:
          match = tmpList[0]

        url = 'http://www.usconstitution.net/const.txt'
        import requests
        import html2text
        r = requests.get(url)        
        textStream =  str(html2text.html2text(r.text))
        textasList =  textStream.split()
        filter = lambda x: x[0]==match
        aSet =  ([x for x in textasList if x[0].lower()==match])
        uniq_aSet = list(set(aSet))
        import bisect
        sortList = []
        for item in uniq_aSet:                 
         bisect.insort(sortList, item)
        
        print sortList

        return    
    def redis_load_testdata(self, eventObj=None):
        tmpList = self.getArgPhrase(eventObj=eventObj)
        if tmpList[0] != 'testdata':
          return        
        tmpList.pop(0)

        url = 'http://www.usconstitution.net/const.txt'
        import requests
        #import HTMLParser
        import html2text
        #from HTMLParser import HTMLParser
        #from bs4 import BeautifulSoup
        #url = "http://search.yahoo.com/search?p=%s" 
        #query = "python"
        r = requests.get(url)        
        textStream =  str(html2text.html2text(r.text))
        testList = textStream.split()
        wordTable = {}
        for item in testList:
           wordTable[item] = 0
        for item in testList:
           wordTable[item] = wordTable[item] + 1

        r = self.getRedisInstance(dbNum=5)
        if r is not None:          
         for key in wordTable.keys():          
            r.set(key, wordTable[key])
        return

    def redis_get_filtered_data(self, eventObj=None):

        tmpList = self.getArgPhrase(eventObj=eventObj)

        retval = []
        if len(tmpList) < 1:
         return retval

        r = self.getRedisInstance(dbNum=5)
        if r is not None:             
          for key in r.keys():           
           if type(r.get(key)) is str:
            dbgprint('value - %s  type %s' % (r.get(key),type(r.get(key))))
            if (tmpList[0] == key[0]):
             retval.append(key)        
        return retval

    def redis_testdb(self, eventObj=None):
        tmpList = self.getArgPhrase(eventObj=eventObj)
        if tmpList[0] != 'testdb':
          return
        tmpList.pop(0)
        
        r = self.getRedisInstance(dbNum=5)
        if r is not None:     
          print ' ** Word : Count ** '     
          for key in r.keys():           
           if type(r.get(key)) is str:
            dbgprint('value - %s  type %s' % (r.get(key),type(r.get(key))))            
            if int(r.get(key)) > 80:
              print " ",key, " : ", r.get(key)
            
        return
    def redis_ops(self, eventObj=None):
        tmpList = self.getArgPhrase(eventObj=eventObj,
                                    keepheadKeyword=False)
        if tmpList[0] == 'testdb':
          self.enqueue_fn(
              cEvent(
                evtPayload=cToolPayload(payloadArgPhrase=tmpList),
                evtPayload_fn=self.redis_testdb))
          return

        if tmpList[0] == 'testdata':
          self.enqueue_fn(
              cEvent(
                evtPayload=cToolPayload(payloadArgPhrase=tmpList),
                evtPayload_fn=self.redis_load_testdata))
          return

        return    
    def dump_handytool_config(self, eventObj=None):
        """ Prints the config entries """
        self.enqueue_fn(
          cEvent(evtPayload_fn=self.hTool.envConfig.print_conf_entries))
        return
    def invoke_plugin(self, eventObj=None):
        """ entry hook for the plugin architecture """
        try:
            from toolplugin_main import cPluginLab
            tmp1 = cPluginLab()
            tmp1.entry_point(eventObj)
        except:
            dbgprint("could not invoke plugin.")
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

def dbgprint(arg=None,):

  hToolObj = handyman_main.handyMantool.getToolInstance() 
  hToolObj.toolUtil.logger.debug(arg)
  #hToolObj.toolUtil.logger.error(arg)
  return





