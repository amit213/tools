#!/usr/bin/env python
#
#wrapper tool for automation and env config.
#
from handyutil import *
import argparse


class handyMantool(object):
      def __init__(self):   
       self.param_table = []
       return
      def init_tool_params(self):
       self.param_table = [
                            ['club', 'what does club param do'],
                            ['clean', 'what does clean param do'],
                            ['sample', 'what does sample param do'],
                          ]
       return
      def getParamTable(self):
       return self.param_table

      @classmethod
      def init(cls):       
       return cls


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
  global h1
  #selfVer = "0.0.1"
  #printVer()
  #create_ssh_bookmark()
  
  h1 = handyMantool()  
  h1.init_tool_params()  
  utilParseParams(h1) 
  return

h1 = None

if __name__ == "__main__":  main()


