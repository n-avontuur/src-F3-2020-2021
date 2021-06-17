#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from flexbe_core import EventState, Logger

class setPickParameters(EventState):
	'''
	State for know witch bin is empty

	># binPartType 		string[] 	array for all content in bins 
	#> bin 			string		name of empty bin
	#> bin_frame 		string		name frame of empty bin

	'''

	def __init__(self):
		super(setPickParameters,self).__init__(outcomes = ['continue', 'failed'])


	def execute(self, userdata):

		return 'continue'


	def on_enter(self, userdata):

		pass

	def on_exit(self, userdata):

		pass

	def on_start(self):
		pass


	def on_stop(self):
		pass
