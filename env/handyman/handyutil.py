#!/usr/bin/env python
#
#util used by wrapper tool for automation and env config.
#
import argparse
#from handyman_main import handyMantool
#from handyman_main import cEvent
import handyman_main
#from handyman_main import *




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
      
      

def myprint(args):
  print args
  return

def utilVer():
	selfVer = "0.0.1u"
	print "util version :", selfVer
	return


def greetMe(string):	
	
	#e1 = cEvent("task", "greet", string)
	hToolObj = None	
	hToolObj = handyman_main.handyMantool.getToolInstance()	
	#print hToolObj.getParamTable()
	#hToolObj.appendParamTable([string, string])
	#print hToolObj.getParamTable()
	hToolObj.enqueue_new_event(cEvent("task", "greet", string))
	return

def utilParseParams(tmpObj=None):
	
	parser1 = argparse.ArgumentParser(description='The handyman is here.')

	
	#parser1.add_argument('greet', nargs='?', help='issue a greeting')
	#parser1.add_argument('opentunnels', nargs='?', help='open tunnels based on envconfig')
	#parser1.add_argument('listopentunnels', help='open tunnels based on envconfig', nargs='?')
	
	#for entries in tmpObj.getParamTable():		
	#	parser1.add_argument(entries[0], help=entries[1], nargs='?')
	#parser1.add_argument("foobog", nargs='?', type=int)
	parser1.add_argument("-t", "-task", help="specify the task name", \
						required=False)
	parser1.add_argument("-bookmark")
	parser1.add_argument("-greet", type=greetMe)
	args = parser1.parse_args()
	
	#print (args.task)	
	return


def utilApiCall():
	z1 = handyman_main.handyMantool().getToolInstance()
	z2 = handyman_main.handyMantool()._toolObj	
	z2.holaecho('sing Bond')
	z1.holaecho('sing Zoo')
	return






