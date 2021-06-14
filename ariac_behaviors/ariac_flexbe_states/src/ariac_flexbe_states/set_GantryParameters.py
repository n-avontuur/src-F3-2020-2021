#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from flexbe_core import EventState, Logger

class set_Gantry_Parameters(EventState):
	'''
	State for know witch bin is empty

	># binPartType 		string[] 	array for all content in bins 
	#> bin 			string		name of empty bin
	#> bin_frame 		string		name frame of empty bin

	'''

	def __init__(self):
		super(set_Gantry_Parameters,self).__init__(input_keys = ['table_Name'],outcomes = ['continue', 'failed'], output_keys = ['table_Pose','section_Pose'])


	def execute(self, userdata):
		if userdata.table_Name == 'as1':
			userdata.section_Pose= "gantry_wp_as1_as3"
			userdata.table_Pose= "gantry_home_as1"
			
		elif userdata.table_Name == 'as2':
			userdata.section_Pose= "gantry_wp_as2_as4"
			userdata.table_Pose= "gantry_home_as2"

		elif userdata.table_Name == 'as3':
			userdata.section_Pose= "gantry_wp_as1_as3"
			userdata.table_Pose= "gantry_home_as3"

		elif userdata.table_Name == 'as4':
			userdata.section_Pose= "gantry_wp_as2_as4"
			userdata.table_Pose= "gantry_home_as4"
			
		return 'continue'


	def on_enter(self, userdata):
		pass

	def on_exit(self, userdata):

		pass

	def on_start(self):
		pass


	def on_stop(self):
		pass
