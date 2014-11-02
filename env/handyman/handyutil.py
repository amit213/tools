#!/usr/bin/env python
#
#util used by wrapper tool for automation and env config.
#
import argparse

#from handyman_main import handyMantool
import handyman_main

#from handyman_main import pSelf
#import handyman_main as mm
#from handyman_main import h1

def myprint(args):
  print args
  return

def utilVer():
	selfVer = "0.0.1u"
	print "util version :", selfVer
	return


def utilParseParams(tmpObj=None):
	
	parser1 = argparse.ArgumentParser()

	parser1.add_argument('greet', nargs='?', help='issue a greeting')
	parser1.add_argument('opentunnels', nargs='?', help='open tunnels based on envconfig')
	parser1.add_argument('listopentunnels', help='open tunnels based on envconfig', nargs='?')
	
	for entries in tmpObj.getParamTable():		
		parser1.add_argument(entries[0], help=entries[1], nargs='?')

	parser1.parse_args()                    
	return