#!/usr/bin/env python
#
#wrapper tool for automation and env config.
#
from handyutil import *
import argparse


class handyMantool(object):
      _toolObj = None
      def __init__(self):   
       self.param_table = []
       self._tag = None
       self._eventList = []       
       return
      def init_tool_params(self):
       self.param_table = [
                            ['club', 'what does club param do'],
                            ['clean', 'what does clean param do'],
                            ['sample', 'what does sample param do'],
                          ]       
       return
      def appendParamTable(self, value=None):
       self.param_table.append(value)
       return
      def getParamTable(self):
       return self.param_table
      @property
      def tag(self):
          return self._tag
      @tag.setter
      def tag_setter(self, value):
          self._tag = value          
      

      @classmethod
      def init(cls):       
       return cls
      @classmethod
      def getToolInstance(self): 
       return handyMantool._toolObj

      @classmethod
      def setToolInstance(self, toolObj):
       handyman_main.handyMantool._toolObj = toolObj
       return

      def holaecho(self, hola='Florida'):
       print "echoing :", hola
       pass

      def enqueue_new_event(self, eventObj=None):
       self._eventList.append(eventObj)
       return

      @property
      def eventList(self):
       return self._eventList

      def process_all_events(self):
       print "processing all events"
       for evt in self.eventList:
        print evt.event_name
        pass
       return 



class sshBookmark:
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



def printVer():
  print "handyman version :", selfVer
  utilVer()
  return

def create_ssh_bookmark():
  s1 = sshBookmark()
  s1.list_bookmark()
  return

def main():

  #selfVer = "0.0.1"
  #printVer()
  #create_ssh_bookmark()
  
  h1 = handyMantool()
  h1.setToolInstance(h1)
  h1.init_tool_params()  
  utilParseParams(h1) 
  h1.process_all_events()
  return



if __name__ == "__main__":  main()


