#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_states.add_offset_to_pose_state import AddOffsetToPoseState
from ariac_flexbe_states.compute_grasp_ariac_state import ComputeGraspAriacState
from ariac_flexbe_states.get_object_pose import GetObjectPoseState
from ariac_flexbe_states.moveit_to_joints_dyn_ariac_state import MoveitToJointsDynAriacState
from ariac_flexbe_states.srdf_state_to_moveit_ariac_state import SrdfStateToMoveitAriac
from ariac_flexbe_states.vacuum_gripper_control_state import VacuumGripperControlState
from flexbe_states.wait_state import WaitState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Tue Jun 01 2021
@author: Jesse
'''
class place_part_on_agvSM(Behavior):
	'''
	Part van bin naar AGV verplaatsen
	'''


	def __init__(self):
		super(place_part_on_agvSM, self).__init__()
		self.name = 'place_part_on_agv'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		gripper_service = '/ariac/kitting/arm/gripper/control'
		gripper_status_topic = '/ariac/kitting/arm/gripper/state'
		# x:1364 y:325, x:795 y:769
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['ProductType', 'ProductIterator', 'action_topic_namespace', 'traypredrop', 'tray', 'move_group', 'ProductPose'])
		_state_machine.userdata.part_pose = []
		_state_machine.userdata.joint_values = []
		_state_machine.userdata.joint_names = []
		_state_machine.userdata.offset = 0.1
		_state_machine.userdata.move_group = 'manipulator'
		_state_machine.userdata.action_topic_namespace = ''
		_state_machine.userdata.action_topic = '/move_group'
		_state_machine.userdata.robot_name = ''
		_state_machine.userdata.robot_config = ''
		_state_machine.userdata.camera_ref_frame = 'linear_arm_actuator'
		_state_machine.userdata.camera_topic = ''
		_state_machine.userdata.camera_frame = ''
		_state_machine.userdata.tool_link = 'ee_link'
		_state_machine.userdata.agv_pose = []
		_state_machine.userdata.part_drop_offset = 0.15
		_state_machine.userdata.tray = 'kit_tray_1'
		_state_machine.userdata.bin = ''
		_state_machine.userdata.locations = []
		_state_machine.userdata.zero = 0
		_state_machine.userdata.gripper_status_attached = False
		_state_machine.userdata.gripper_status_enabled = False
		_state_machine.userdata.pose_on_agv = []
		_state_machine.userdata.part = []
		_state_machine.userdata.end_pose = []
		_state_machine.userdata.part_pose = ''
		_state_machine.userdata.part_pose2 = []
		_state_machine.userdata.ProductType = ''
		_state_machine.userdata.offset_pose = 0.3
		_state_machine.userdata.ProductIterator = 0
		_state_machine.userdata.part_count_0 = 0
		_state_machine.userdata.part_count_1 = 1
		_state_machine.userdata.part_count_2 = 2
		_state_machine.userdata.pose_offset = []
		_state_machine.userdata.traypredrop = ''
		_state_machine.userdata.part_rotation = 0
		_state_machine.userdata.ProductPose = []

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:167 y:139
			OperatableStateMachine.add('MoveR1PreDrop',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'GetAgvPose', 'planning_failed': 'WaitState5', 'control_failed': 'WaitState5', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'traypredrop', 'move_group': 'move_group', 'action_topic_namespace': 'action_topic_namespace', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1016 y:138
			OperatableStateMachine.add('DeactivateGripper',
										VacuumGripperControlState(enable=False, service_name=gripper_service),
										transitions={'continue': 'MoveR1PreDrop2', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off})

			# x:341 y:141
			OperatableStateMachine.add('GetAgvPose',
										GetObjectPoseState(),
										transitions={'continue': 'offsetagvpose', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'ref_frame': 'camera_ref_frame', 'frame': 'tray', 'pose': 'agv_pose'})

			# x:1298 y:135
			OperatableStateMachine.add('MoveR1PreDrop2',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'finished', 'planning_failed': 'WaitState7', 'control_failed': 'WaitState7', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'traypredrop', 'move_group': 'move_group', 'action_topic_namespace': 'action_topic_namespace', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:809 y:134
			OperatableStateMachine.add('MoveR1ToDrop',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'DeactivateGripper', 'planning_failed': 'WaitState6', 'control_failed': 'WaitState6'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'action_topic_namespace': 'action_topic_namespace', 'move_group': 'move_group', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:192 y:33
			OperatableStateMachine.add('WaitState5',
										WaitState(wait_time=5),
										transitions={'done': 'MoveR1PreDrop'},
										autonomy={'done': Autonomy.Off})

			# x:848 y:29
			OperatableStateMachine.add('WaitState6',
										WaitState(wait_time=5),
										transitions={'done': 'MoveR1ToDrop'},
										autonomy={'done': Autonomy.Off})

			# x:1309 y:50
			OperatableStateMachine.add('WaitState7',
										WaitState(wait_time=5),
										transitions={'done': 'MoveR1PreDrop2'},
										autonomy={'done': Autonomy.Off})

			# x:471 y:130
			OperatableStateMachine.add('offsetagvpose',
										AddOffsetToPoseState(),
										transitions={'continue': 'ComuteDrop'},
										autonomy={'continue': Autonomy.Off},
										remapping={'input_pose': 'agv_pose', 'offset_pose': 'ProductPose', 'output_pose': 'agv_pose'})

			# x:605 y:133
			OperatableStateMachine.add('ComuteDrop',
										ComputeGraspAriacState(joint_names=['linear_arm_actuator_joint', 'shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']),
										transitions={'continue': 'MoveR1ToDrop', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'move_group', 'action_topic_namespace': 'action_topic_namespace', 'tool_link': 'tool_link', 'pose': 'agv_pose', 'offset': 'part_drop_offset', 'rotation': 'part_rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
