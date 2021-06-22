#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from flexbe_core import EventState, Logger

class set_GantryParameters(EventState):
	'''
	State for know witch bin is empty

	># binPartType 		string[] 	array for all content in bins 
	#> bin 			string		name of empty bin
	#> bin_frame 		string		name frame of empty bin

	'''

	def __init__(self):
		super(set_GantryParameters,self).__init__(input_keys = ['station_id'],outcomes = ['continue', 'failed'], output_keys = ['home_Pose','table_Pose','section_Pose','gantry_move_group','gantry_action_topic_namespace','gantry_action_topic','robot_name','camera_frame1','camera_topic1','camera_frame2','camera_topic2','first_agv','sec_agv','case_frame'])


	def execute(self, userdata):
		if userdata.station_id == 'as1' or userdata.station_id =='as3':
			userdata.section_Pose= "gantry_wp_as1_as3"
			if userdata.station_id == 'as1':
				userdata.case_frame = 'briefcase_1'
				userdata.table_Pose= "AS1"
				userdata.home_Pose='AS1_Home'
				userdata.camera_frame1 = 'logical_camera_station1_agv1_frame'
				userdata.camera_topic1 = '/ariac/logical_camera_station1_agv1'
				userdata.camera_frame2 = 'logical_camera_station1_agv2_frame'
				userdata.camera_topic2 = '/ariac/logical_camera_station1_agv2'
				userdata.first_agv = 'agv1'
				userdata.sec_agv = 'agv2'
			elif userdata.station_id == 'as3':
				userdata.case_frame = 'briefcase_3'
				userdata.table_Pose= "AS3"
				userdata.home_Pose='AS3_Home'
				userdata.camera_frame1 = 'logical_camera_station3_agv3_frame'
				userdata.camera_topic1 = '/ariac/logical_camera_station3_agv3'
				userdata.camera_frame2 = 'logical_camera_station3_agv4_frame'
				userdata.camera_topic2 = '/ariac/logical_camera_station3_agv4'
				userdata.first_agv = 'agv3'
				userdata.sec_agv = 'agv4'

		if userdata.station_id == 'as2' or  userdata.station_id =='as4':
			userdata.section_Pose= "gantry_wp_as2_as4"
			if userdata.station_id == 'as2':
				userdata.case_frame = 'briefcase_2'
				userdata.table_Pose= "AS2"
				userdata.home_Pose='AS2_Home'
				userdata.camera_frame1 = 'logical_camera_station2_agv1_frame'
				userdata.camera_topic1 = '/ariac/logical_camera_station2_agv1'
				userdata.camera_frame2 = 'logical_camera_station2_agv2_frame'
				userdata.camera_topic2 = '/ariac/logical_camera_station2_agv2'
				userdata.first_agv = 'agv1'
				userdata.sec_agv = 'agv2'
			elif userdata.station_id == 'as4':
				userdata.case_frame = 'briefcase_4'
				userdata.table_Pose= "AS4"
				userdata.home_Pose='AS4_Home'
				userdata.camera_frame1 = 'logical_camera_station4_agv3_frame'
				userdata.camera_topic1 = '/ariac/logical_camera_station4_agv3'
				userdata.camera_frame2 = 'logical_camera_station4_agv4_frame'
				userdata.camera_topic2 = '/ariac/logical_camera_station4_agv4'
				userdata.first_agv = 'agv3'
				userdata.sec_agv = 'agv4'
		return 'continue'


	def on_enter(self, userdata):
		userdata.gantry_move_group ='gantry_torso'
		userdata.gantry_action_topic_namespace = '/ariac/gantry'
		userdata.gantry_action_topic = '/move_group'
		userdata.robot_name= ''
		pass

	def on_exit(self, userdata):

		pass

	def on_start(self):
		pass


	def on_stop(self):
		pass
