#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from flexbe_core import EventState, Logger


class setBinPartType(EventState):
	'''
	this state sets the new pose for the part

	># bin string name of bin
	># part string name of part
	#> binPartType string[] list of the content of bins

	'''

	def __init__(self):
		super(setBinPartType,self).__init__(input_keys = ["bin","part","binPartType" ],outcomes = ['continue', 'failed'], output_keys = ['binPartType'])


	def execute(self, userdata):
		if userdata.bin == "bin1":
			userdata.binPartType[0]=self._part
		elif userdata.bin == "bin2":
			userdata.binPartType[1]=self._part
		elif userdata.bin == "bin3":
			userdata.binPartType[2]=self._part
		elif userdata.bin == "bin4":
			userdata.binPartType[3]=self._part
		elif userdata.bin == "bin5":
			userdata.binPartType[4]=self._part
		elif userdata.bin == "bin6":
			userdata.binPartType[5]=self._part
		return 'continue'

	def on_enter(self, userdata):
		self._part = userdata.part
		pass

	def on_exit(self, userdata):
		pass

	def on_start(self):
		pass


	def on_stop(self):
		pass
