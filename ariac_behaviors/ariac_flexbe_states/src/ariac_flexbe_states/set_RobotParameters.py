#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from flexbe_core import EventState, Logger

class set_Robot_Parameters(EventState):
	'''
	State for know witch bin is empty

	># binPartType 		string[] 	array for all content in bins 
	#> bin 			string		name of empty bin
	#> bin_frame 		string		name frame of empty bin

	'''

	def __init__(self):
		super(set_Robot_Parameters,self).__init__(input_keys=['part_Type'],outcomes = ['continue', 'failed'], output_keys = ['UR10_move_group','UR10_action_topic_namespace','UR10_action_topic','UR10_tool_link','UR10_robot_name','gripper_service','gripper_status_topic','gripper_status_attached','gripper_status_enabled','armHomeDown','armHomeUp','pick_offset','pick_rotation'])


	def execute(self, userdata):
		if userdata.part_Type == 'assembly_pomp_green' or userdata.part_Type == 'assembly_pomp_red' or userdata.part_Type == 'assembly_pomp_blue':
			userdata.pick_offset = 0.075
			userdata.pick_rotation = 0.0
		elif userdata.part_Type == 'assembly_sensor_green' or userdata.part_Type == 'assembly_sensor_red' or userdata.part_Type == 'assembly_sensor_blue':
			userdata.pick_offset = 0.060
			userdata.pick_rotation = 0.0
		elif userdata.part_Type == 'assembly_regulator_green' or userdata.part_Type == 'assembly_regulator_red' or userdata.part_Type == 'assembly_regulator_blue':
			userdata.pick_offset = 0.060
			userdata.pick_rotation = 0.0
		elif userdata.part_Type == 'assembly_battery_green' or userdata.part_Type == 'assembly_battery_red' or userdata.part_Type == 'assembly_battery_blue':
			userdata.pick_offset = 0.050
			userdata.pick_rotation = 0.0
		else :
			Logger.logwarn('set RobotParameters :part_Type is not defined for offset')
			return 'failed'
		return 'continue'


	def on_enter(self, userdata):
		userdata.UR10_move_group = 'gantry_arm'
		userdata.UR10_action_topic_namespace = '/ariac/gantry'
		userdata.UR10_action_topic = '/move_group'
		userdata.UR10_robot_name = ''
		userdata.UR10_tool_link = 'gantry_arm_ee_link'
		userdata.armHomeDown = 'gantry_arm_homeDOWN'
		userdata.armHomeUp = 'gantry_arm_homeUP'
		pass

	def on_exit(self, userdata):

		pass

	def on_start(self):
		pass


	def on_stop(self):
		pass
