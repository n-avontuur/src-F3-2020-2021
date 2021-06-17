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
from ariac_flexbe_states.get_gripper_status_state2 import GetGripperStatusState2
from ariac_flexbe_states.moveit_to_joints_dyn_ariac_state import MoveitToJointsDynAriacState
from ariac_flexbe_states.set_RobotParameters import set_Robot_Parameters
from ariac_flexbe_states.srdf_state_to_moveit_ariac_state import SrdfStateToMoveitAriac
from ariac_flexbe_states.vacuum_gripper_control_state2 import VacuumGripperControlState2
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
		# x:170 y:238, x:617 y:408
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['part_Type', 'drop_Pose'])
		_state_machine.userdata.part_Type = ''
		_state_machine.userdata.drop_Offset = 0
		_state_machine.userdata.drop_Rotation = 0
		_state_machine.userdata.falseVariable = False
		_state_machine.userdata.trueVariable = True
		_state_machine.userdata.drop_Pose = []
		_state_machine.userdata.offset = 0.1

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:77 y:59
			OperatableStateMachine.add('setRobotParameters',
										set_Robot_Parameters(),
										transitions={'continue': 'moveToPreDrop', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'part_Type': 'part_Type', 'UR10_move_group': 'UR10_move_group', 'UR10_action_topic_namespace': 'UR10_action_topic_namespace', 'UR10_action_topic': 'UR10_action_topic', 'UR10_tool_link': 'UR10_tool_link', 'UR10_robot_name': 'UR10_robot_name', 'gripper_service': 'gripper_service', 'gripper_status_topic': 'gripper_status_topic', 'gripper_status_attached': 'gripper_status_attached', 'gripper_status_enabled': 'gripper_status_enabled', 'armHomeDown': 'armHomeDown', 'armHomeUp': 'armHomeUp', 'armHomeAS': 'armHomeAS', 'pick_offset': 'part_offset', 'pick_rotation': 'part_rotation'})

			# x:1196 y:539
			OperatableStateMachine.add('computeDrop',
										ComputeGraspAriacState(joint_names=joint_names),
										transitions={'continue': 'moveToDrop', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'UR10_move_group', 'action_topic_namespace': 'UR10_action_topic_namespace', 'tool_link': 'UR10_tool_link', 'pose': 'drop_Pose', 'offset': 'drop_Offset', 'rotation': 'drop_Rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1186 y:296
			OperatableStateMachine.add('computeDrop_2',
										ComputeGraspAriacState(joint_names=joint_names),
										transitions={'continue': 'moveToDrop_2', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'UR10_move_group', 'action_topic_namespace': 'UR10_action_topic_namespace', 'tool_link': 'UR10_tool_link', 'pose': 'drop_Pose', 'offset': 'offset', 'rotation': 'drop_Rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:958 y:541
			OperatableStateMachine.add('moveToDrop',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'setGripperOff', 'planning_failed': 'wait_2', 'control_failed': 'wait_2'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'action_topic_namespace': 'UR10_action_topic_namespace', 'move_group': 'UR10_move_group', 'action_topic': 'UR10_action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1176 y:423
			OperatableStateMachine.add('moveToDrop_2',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'computeDrop', 'planning_failed': 'wait_2_2', 'control_failed': 'wait_2_2'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'action_topic_namespace': 'UR10_action_topic_namespace', 'move_group': 'UR10_move_group', 'action_topic': 'UR10_action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:101 y:483
			OperatableStateMachine.add('moveToDrop_3',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'moveToPreDrop_2', 'planning_failed': 'wait_2_3', 'control_failed': 'wait_2_3'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'action_topic_namespace': 'UR10_action_topic_namespace', 'move_group': 'UR10_move_group', 'action_topic': 'UR10_action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:446 y:124
			OperatableStateMachine.add('moveToPreDrop',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'computeDrop_2', 'planning_failed': 'wait', 'control_failed': 'wait', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'armHomeAS', 'move_group': 'UR10_move_group', 'action_topic_namespace': 'UR10_action_topic_namespace', 'action_topic': 'UR10_action_topic', 'robot_name': 'UR10_robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:118 y:333
			OperatableStateMachine.add('moveToPreDrop_2',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'finished', 'planning_failed': 'wait_4', 'control_failed': 'wait_4', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'armHomeUp', 'move_group': 'UR10_move_group', 'action_topic_namespace': 'UR10_action_topic_namespace', 'action_topic': 'UR10_action_topic', 'robot_name': 'UR10_robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:670 y:533
			OperatableStateMachine.add('setGripperOff',
										VacuumGripperControlState2(enable=False),
										transitions={'continue': 'wait_3', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off})

			# x:477 y:28
			OperatableStateMachine.add('wait',
										WaitState(wait_time=0.5),
										transitions={'done': 'moveToPreDrop'},
										autonomy={'done': Autonomy.Off})

			# x:1006 y:649
			OperatableStateMachine.add('wait_2',
										WaitState(wait_time=0.5),
										transitions={'done': 'moveToDrop'},
										autonomy={'done': Autonomy.Off})

			# x:1414 y:424
			OperatableStateMachine.add('wait_2_2',
										WaitState(wait_time=0.5),
										transitions={'done': 'moveToDrop_2'},
										autonomy={'done': Autonomy.Off})

			# x:122 y:579
			OperatableStateMachine.add('wait_2_3',
										WaitState(wait_time=0.5),
										transitions={'done': 'moveToDrop_3'},
										autonomy={'done': Autonomy.Off})

			# x:486 y:539
			OperatableStateMachine.add('wait_3',
										WaitState(wait_time=0.5),
										transitions={'done': 'checkGripperStatus'},
										autonomy={'done': Autonomy.Off})

			# x:301 y:293
			OperatableStateMachine.add('wait_4',
										WaitState(wait_time=0.5),
										transitions={'done': 'moveToPreDrop_2'},
										autonomy={'done': Autonomy.Off})

			# x:302 y:539
			OperatableStateMachine.add('checkGripperStatus',
										GetGripperStatusState2(),
										transitions={'continue': 'moveToDrop_3', 'fail': 'failed'},
										autonomy={'continue': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'enabled': 'enabled', 'attached': 'attached'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
