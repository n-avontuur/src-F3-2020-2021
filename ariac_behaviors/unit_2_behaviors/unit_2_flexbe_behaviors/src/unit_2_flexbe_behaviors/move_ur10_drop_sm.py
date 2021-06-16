#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_states.compute_grasp_ariac_state import ComputeGraspAriacState
from ariac_flexbe_states.get_gripper_status_state import GetGripperStatusState
from ariac_flexbe_states.moveit_to_joints_dyn_ariac_state import MoveitToJointsDynAriacState
from ariac_flexbe_states.set_RobotParameters import set_Robot_Parameters
from ariac_flexbe_states.srdf_state_to_moveit_ariac_state import SrdfStateToMoveitAriac
from ariac_flexbe_states.vacuum_gripper_control_state import VacuumGripperControlState
from ariac_support_flexbe_states.equal_state import EqualState
from flexbe_states.wait_state import WaitState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Tue Jun 15 2021
@author: Niels Avontuur
'''
class Move_UR10_DropSM(Behavior):
	'''
	Program for dropping the part on the correct location
	'''


	def __init__(self):
		super(Move_UR10_DropSM, self).__init__()
		self.name = 'Move_UR10_Drop'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		joint_names = ['gantry_arm_elbow_joint', 'gantry_arm_shoulder_lift_joint', 'gantry_arm_shoulder_pan_joint', 'gantry_arm_wrist_1_joint', 'gantry_arm_wrist_2_joint', 'gantry_arm_wrist_3_joint']
		service_name = '/ariac/gantry/arm/gripper/controle'
		gripper_status_topic = '/ariac/gantry/arm/gripper/state'
		# x:1107 y:701, x:617 y:408
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['part_Type', 'drop_Pose'])
		_state_machine.userdata.part_Type = ''
		_state_machine.userdata.drop_Pose = []
		_state_machine.userdata.drop_Offset = 0
		_state_machine.userdata.drop_Rotation = 0
		_state_machine.userdata.falseVariable = False
		_state_machine.userdata.trueVariable = True

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:135 y:174
			OperatableStateMachine.add('setRobotParameters',
										set_Robot_Parameters(),
										transitions={'continue': 'moveToPreDrop', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'part_Type': 'part_Type', 'UR10_move_group': 'UR10_move_group', 'UR10_action_topic_namespace': 'UR10_action_topic_namespace', 'UR10_action_topic': 'UR10_action_topic', 'UR10_tool_link': 'UR10_tool_link', 'UR10_robot_name': 'UR10_robot_name', 'gripper_service': 'gripper_service', 'gripper_status_topic': 'gripper_status_topic', 'gripper_status_attached': 'gripper_status_attached', 'gripper_status_enabled': 'gripper_status_enabled', 'armHomeDown': 'armHomeDown', 'armHomeUp': 'armHomeUp', 'pick_offset': 'part_offset', 'pick_rotation': 'part_rotation'})

			# x:579 y:174
			OperatableStateMachine.add('computeDrop',
										ComputeGraspAriacState(joint_names=joint_names),
										transitions={'continue': 'moveToDrop', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'UR10_move_group', 'action_topic_namespace': 'UR10_action_topic_namespace', 'tool_link': 'UR10_tool_link', 'pose': 'drop_Pose', 'offset': 'drop_Offset', 'rotation': 'drop_Rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:771 y:174
			OperatableStateMachine.add('moveToDrop',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'setGripperOff', 'planning_failed': 'wait_2', 'control_failed': 'wait_2'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'action_topic_namespace': 'UR10_action_topic_namespace', 'move_group': 'UR10_move_group', 'action_topic': 'UR10_action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:334 y:174
			OperatableStateMachine.add('moveToPreDrop',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'computeDrop', 'planning_failed': 'wait', 'control_failed': 'wait', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'armHomeUp', 'move_group': 'UR10_move_group', 'action_topic_namespace': 'UR10_action_topic_namespace', 'action_topic': 'UR10_action_topic', 'robot_name': 'UR10_robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1136 y:516
			OperatableStateMachine.add('moveToPreDrop_2',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'finished', 'planning_failed': 'wait_4', 'control_failed': 'wait_4', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'armHomeUp', 'move_group': 'UR10_move_group', 'action_topic_namespace': 'UR10_action_topic_namespace', 'action_topic': 'UR10_action_topic', 'robot_name': 'UR10_robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1221 y:370
			OperatableStateMachine.add('partDettached',
										EqualState(),
										transitions={'true': 'moveToPreDrop_2', 'false': 'setGripperOff'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'falseVariable', 'value_b': 'gripper_attached'})

			# x:1024 y:174
			OperatableStateMachine.add('setGripperOff',
										VacuumGripperControlState(enable=False, service_name=service_name),
										transitions={'continue': 'wait_3', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off})

			# x:357 y:17
			OperatableStateMachine.add('wait',
										WaitState(wait_time=0.5),
										transitions={'done': 'moveToPreDrop'},
										autonomy={'done': Autonomy.Off})

			# x:805 y:40
			OperatableStateMachine.add('wait_2',
										WaitState(wait_time=0.5),
										transitions={'done': 'moveToDrop'},
										autonomy={'done': Autonomy.Off})

			# x:1256 y:176
			OperatableStateMachine.add('wait_3',
										WaitState(wait_time=0.5),
										transitions={'done': 'checkGripperStatus'},
										autonomy={'done': Autonomy.Off})

			# x:1401 y:522
			OperatableStateMachine.add('wait_4',
										WaitState(wait_time=0.5),
										transitions={'done': 'moveToPreDrop_2'},
										autonomy={'done': Autonomy.Off})

			# x:1246 y:290
			OperatableStateMachine.add('checkGripperStatus',
										GetGripperStatusState(gripper_status_topic=gripper_status_topic),
										transitions={'continue': 'partDettached', 'fail': 'failed'},
										autonomy={'continue': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'enabled': 'gripper_enabled', 'attached': 'gripper_attached'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
