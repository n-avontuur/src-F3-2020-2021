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
		super(set_Gantry_Parameters,self).__init__(input_keys = ['station_id'],outcomes = ['continue', 'failed'], output_keys = ['table_Pose','section_Pose','move_group','action_topic_namespace','action_topic','robot_name','camera_frame1','camera_topic1','camera_frame2','camera_topic2'])


	def execute(self, userdata):
		if userdata.station_id == 'as1' or userdata.station_id =='as3':
			userdata.section_Pose= "gantry_wp_as1_as3"
			if userdata.station_id == 'as1':
				userdata.table_Pose= "gantry_home_as1"
				userdata.camera_frame1 = 'logical_camera_station1_agv1_frame'
				userdata.camera_topic1 = '/ariac/logical_camera_station1_agv1'
				userdata.camera_frame2 = 'logical_camera_station1_agv2_frame'
				userdata.camera_topic2 = '/ariac/logical_camera_station1_agv2'
			elif userdata.station_id == 'as3':
				userdata.table_Pose= "gantry_home_as3"
				userdata.camera_frame1 = 'logical_camera_station3_agv3_frame'
				userdata.camera_topic1 = '/ariac/logical_camera_station3_agv3'
				userdata.camera_frame2 = 'logical_camera_station3_agv4_frame'
				userdata.camera_topic2 = '/ariac/logical_camera_station3_agv4'

		if userdata.station_id == 'as2' or  userdata.station_id =='as4':
			userdata.section_Pose= "gantry_wp_as2_as4"
			if userdata.station_id == 'as2':
				userdata.table_Pose= "gantry_home_as2"
				userdata.camera_frame1 = 'logical_camera_station2_agv1_frame'
				userdata.camera_topic1 = '/ariac/logical_camera_station2_agv1'
				userdata.camera_frame2 = 'logical_camera_station2_agv2_frame'
				userdata.camera_topic2 = '/ariac/logical_camera_station2_agv2'
			elif userdata.station_id == 'as4':
				userdata.table_Pose= "gantry_home_as4"
				userdata.camera_frame1 = 'logical_camera_station4_agv3_frame'
				userdata.camera_topic1 = '/ariac/logical_camera_station4_agv3'
				userdata.camera_frame2 = 'logical_camera_station4_agv4_frame'
				userdata.camera_topic2 = '/ariac/logical_camera_station4_agv4'
		return 'continue'


	def on_enter(self, userdata):
		userdata.move_group ='gantry_torso'
		userdata.action_topic_namespace = '/ariac/gantry'
		userdata.action_topic = '/move_group'
		userdata.robot_name= ''
		pass

	def on_exit(self, userdata):

		pass

	def on_start(self):
		pass


	def on_stop(self):
		pass
