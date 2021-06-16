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
from ariac_flexbe_states.create_dropPose import CreateDropPoseState
from ariac_flexbe_states.create_pose import CreatePoseState
from ariac_flexbe_states.get_gripper_status_state2 import GetGripperStatusState2
from ariac_flexbe_states.moveit_to_joints_dyn_ariac_state import MoveitToJointsDynAriacState
from ariac_flexbe_states.set_RobotParameters import set_Robot_Parameters
from ariac_flexbe_states.srdf_state_to_moveit_ariac_state import SrdfStateToMoveitAriac
from ariac_flexbe_states.vacuum_gripper_control_state2 import VacuumGripperControlState2
from ariac_support_flexbe_states.equal_state import EqualState
from flexbe_states.wait_state import WaitState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Tue Jun 15 2021
@author: Niels Avontuur
'''
class Move_UR10_PickSM(Behavior):
	'''
	For picking up products
	'''


	def __init__(self):
		super(Move_UR10_PickSM, self).__init__()
		self.name = 'Move_UR10_Pick'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:

		# ! 1654 8 
		# Made by Niels Avontuur



	def create(self):
		joint_names = ['gantry_arm_elbow_joint','gantry_arm_shoulder_lift_joint','gantry_arm_shoulder_pan_joint','gantry_arm_wrist_1_joint','gantry_arm_wrist_2_joint','gantry_arm_wrist_3_joint']
		# x:366 y:674, x:419 y:463
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['part_Type', 'part_Pose'])
		_state_machine.userdata.trueVariable = True
		_state_machine.userdata.falseVariable = False
		_state_machine.userdata.part_Pose = []
		_state_machine.userdata.part_Type = ''
		_state_machine.userdata.drop_offset = 0.3
		_state_machine.userdata.rotation = 0.0
		_state_machine.userdata.offset = 0.0

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:85 y:24
			OperatableStateMachine.add('setRobotParameters',
										set_Robot_Parameters(),
										transitions={'continue': 'moveToPrePick', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'part_Type': 'part_Type', 'UR10_move_group': 'UR10_move_group', 'UR10_action_topic_namespace': 'UR10_action_topic_namespace', 'UR10_action_topic': 'UR10_action_topic', 'UR10_tool_link': 'UR10_tool_link', 'UR10_robot_name': 'UR10_robot_name', 'gripper_service': 'gripper_service', 'gripper_status_topic': 'gripper_status_topic', 'gripper_status_attached': 'gripper_status_attached', 'gripper_status_enabled': 'gripper_status_enabled', 'armHomeDown': 'armHomeDown', 'armHomeUp': 'armHomeUp', 'armHomeAS': 'armHomeAS', 'pick_offset': 'pick_offset', 'pick_rotation': 'pick_rotation'})

			# x:638 y:28
			OperatableStateMachine.add('addPickOffsetPose',
										AddOffsetToPoseState(),
										transitions={'continue': 'computePick'},
										autonomy={'continue': Autonomy.Off},
										remapping={'input_pose': 'part_Pose', 'offset_pose': 'pick_offset_Pose', 'output_pose': 'part_Pose'})

			# x:1421 y:237
			OperatableStateMachine.add('checkGripperStatus',
										GetGripperStatusState2(),
										transitions={'continue': 'isPartAttached', 'fail': 'failed'},
										autonomy={'continue': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'enabled': 'gripper_Enabled', 'attached': 'gripper_Attached'})

			# x:1425 y:430
			OperatableStateMachine.add('compute Backout',
										ComputeGraspAriacState(joint_names=joint_names),
										transitions={'continue': 'moveToBackout', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'UR10_move_group', 'action_topic_namespace': 'UR10_action_topic_namespace', 'tool_link': 'UR10_tool_link', 'pose': 'part_Pose', 'offset': 'drop_offset', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:842 y:20
			OperatableStateMachine.add('computePick',
										ComputeGraspAriacState(joint_names=joint_names),
										transitions={'continue': 'moveToPick', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'UR10_move_group', 'action_topic_namespace': 'UR10_action_topic_namespace', 'tool_link': 'UR10_tool_link', 'pose': 'part_Pose', 'offset': 'offset', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:474 y:29
			OperatableStateMachine.add('creatPickOffsetPose',
										CreateDropPoseState(),
										transitions={'continue': 'addPickOffsetPose', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'xyz': 'pick_offset', 'rpy': 'pick_rotation', 'pose': 'pick_offset_Pose'})

			# x:1144 y:338
			OperatableStateMachine.add('createDecreasePick',
										CreatePoseState(xyz=[0.0,0.0,-0.001], rpy=[0.0,0.0,0.0]),
										transitions={'continue': 'addDecreasePose', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'pose_Decrease'})

			# x:1408 y:338
			OperatableStateMachine.add('isPartAttached',
										EqualState(),
										transitions={'true': 'compute Backout', 'false': 'createDecreasePick'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'gripper_Attached', 'value_b': 'trueVariable'})

			# x:1354 y:655
			OperatableStateMachine.add('moveBackToPick',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'finished', 'planning_failed': 'wait_8', 'control_failed': 'wait_8', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'armHomeUp', 'move_group': 'UR10_move_group', 'action_topic_namespace': 'UR10_action_topic_namespace', 'action_topic': 'UR10_action_topic', 'robot_name': 'UR10_robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1418 y:540
			OperatableStateMachine.add('moveToBackout',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'moveBackToPick', 'planning_failed': 'wait_9_2', 'control_failed': 'wait_9_2'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'action_topic_namespace': 'UR10_action_topic_namespace', 'move_group': 'UR10_move_group', 'action_topic': 'UR10_action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1071 y:19
			OperatableStateMachine.add('moveToPick',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'setGripperOn', 'planning_failed': 'wait_9', 'control_failed': 'wait_9'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'action_topic_namespace': 'UR10_action_topic_namespace', 'move_group': 'UR10_move_group', 'action_topic': 'UR10_action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:284 y:24
			OperatableStateMachine.add('moveToPrePick',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'creatPickOffsetPose', 'planning_failed': 'wait', 'control_failed': 'wait', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'armHomeDown', 'move_group': 'UR10_move_group', 'action_topic_namespace': 'UR10_action_topic_namespace', 'action_topic': 'UR10_action_topic', 'robot_name': 'UR10_robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1387 y:45
			OperatableStateMachine.add('setGripperOn',
										VacuumGripperControlState2(enable=True),
										transitions={'continue': 'wait_3', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off})

			# x:307 y:124
			OperatableStateMachine.add('wait',
										WaitState(wait_time=0.5),
										transitions={'done': 'moveToPrePick'},
										autonomy={'done': Autonomy.Off})

			# x:1446 y:165
			OperatableStateMachine.add('wait_3',
										WaitState(wait_time=0.5),
										transitions={'done': 'checkGripperStatus'},
										autonomy={'done': Autonomy.Off})

			# x:1605 y:663
			OperatableStateMachine.add('wait_8',
										WaitState(wait_time=0.5),
										transitions={'done': 'moveBackToPick'},
										autonomy={'done': Autonomy.Off})

			# x:1138 y:150
			OperatableStateMachine.add('wait_9',
										WaitState(wait_time=0.5),
										transitions={'done': 'moveToPick'},
										autonomy={'done': Autonomy.Off})

			# x:1633 y:555
			OperatableStateMachine.add('wait_9_2',
										WaitState(wait_time=0.5),
										transitions={'done': 'moveToBackout'},
										autonomy={'done': Autonomy.Off})

			# x:910 y:276
			OperatableStateMachine.add('addDecreasePose',
										AddOffsetToPoseState(),
										transitions={'continue': 'computePick'},
										autonomy={'continue': Autonomy.Off},
										remapping={'input_pose': 'part_Pose', 'offset_pose': 'pose_Decrease', 'output_pose': 'part_Pose'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
