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
		super(setPickParameters,self).__init__(input_keys = ['station_id','agv_Name'],outcomes = ['continue', 'failed'], output_keys = ['gantry_AGV_pose'])


	def execute(self, userdata):
		if userdata.station_id == 'as1':
			if userdata.agv_Name == 'agv1':
				userdata.gantry_AGV_pose = 'AS1_AGV1'
			elif userdata.agv_Name == 'agv2':
				userdata.gantry_AGV_pose = 'AS1_AGV2'
			else :
				Logger.logwarn('No agv_name')
				return 'failed'
		if userdata.station_id == 'as2':
			if userdata.agv_Name == 'agv1':
				userdata.gantry_AGV_pose = 'AS2_AGV1'
			elif userdata.agv_Name == 'agv2':
				userdata.gantry_AGV_pose = 'AS2_AGV2'
			else :
				Logger.logwarn('No agv_name')
				return 'failed'
		
		if userdata.station_id == 'as3':
			if userdata.agv_Name == 'agv3':
				userdata.gantry_AGV_pose = 'AS3_AGV3'
			elif userdata.agv_Name == 'agv4':
				userdata.gantry_AGV_pose = 'AS3_AGV4'
			else :
				Logger.logwarn('No agv_name')
				return 'failed'
		if userdata.station_id == 'as4':
			if userdata.agv_Name == 'agv3':
				userdata.gantry_AGV_pose = 'AS4_AGV3'
			elif userdata.agv_Name == 'agv4':
				userdata.gantry_AGV_pose = 'AS4_AGV4'
			else :
				Logger.logwarn('No agv_name')
				return 'failed'
		else :
			Logger.logwarn('No station ID')
			return 'failed'				
		return 'continue'


	def on_enter(self, userdata):

		pass

	def on_exit(self, userdata):

		pass

	def on_start(self):
		pass


	def on_stop(self):
		pass
