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
from ariac_flexbe_states.moveit_to_joints_dyn_ariac_state import MoveitToJointsDynAriacState
from ariac_flexbe_states.set_RobotParameters import set_Robot_Parameters
from ariac_flexbe_states.srdf_state_to_moveit_ariac_state import SrdfStateToMoveitAriac
from ariac_flexbe_states.vacuum_gripper_control_state2 import VacuumGripperControlState2
from flexbe_states.wait_state import WaitState
from unit_2_flexbe_behaviors.checkgipper_sm import CheckGipperSM
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
		self.add_behavior(CheckGipperSM, 'CheckGipper')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:

		# ! 1654 8 
		# Made by Niels Avontuur

		# ! 42 30 
		# Made by Niels Avontuur



	def create(self):
		joint_names = ['gantry_arm_elbow_joint','gantry_arm_shoulder_lift_joint','gantry_arm_shoulder_pan_joint','gantry_arm_wrist_1_joint','gantry_arm_wrist_2_joint','gantry_arm_wrist_3_joint']
		# x:333 y:640, x:683 y:390
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['part_Type', 'part_Pose'])
		_state_machine.userdata.trueVariable = True
		_state_machine.userdata.falseVariable = False
		_state_machine.userdata.part_Pose = []
		_state_machine.userdata.part_Type = ''
		_state_machine.userdata.backout_offset = 0.2
		_state_machine.userdata.rotation = 0.0
		_state_machine.userdata.offset = 0.0
		_state_machine.userdata.preOffset = 0.2

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:85 y:174
			OperatableStateMachine.add('setRobotParameters',
										set_Robot_Parameters(),
										transitions={'continue': 'moveToPrePose', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'part_Type': 'part_Type', 'UR10_move_group': 'UR10_move_group', 'UR10_action_topic_namespace': 'UR10_action_topic_namespace', 'UR10_action_topic': 'UR10_action_topic', 'UR10_tool_link': 'UR10_tool_link', 'UR10_robot_name': 'UR10_robot_name', 'gripper_service': 'gripper_service', 'gripper_status_topic': 'gripper_status_topic', 'gripper_status_attached': 'gripper_status_attached', 'gripper_status_enabled': 'gripper_status_enabled', 'armHomeDown': 'armHomeDown', 'armHomeUp': 'armHomeUp', 'armHomeAS': 'armHomeAS', 'pick_offset': 'pick_offset', 'pick_rotation': 'pick_rotation', 'drop_offset': 'drop_offset'})

			# x:1186 y:374
			OperatableStateMachine.add('addDecreasePose',
										AddOffsetToPoseState(),
										transitions={'continue': 'computePrePick_2'},
										autonomy={'continue': Autonomy.Off},
										remapping={'input_pose': 'pick_Pose', 'offset_pose': 'pose_Decrease', 'output_pose': 'pick_Pose'})

			# x:836 y:124
			OperatableStateMachine.add('addPickOffsetPose',
										AddOffsetToPoseState(),
										transitions={'continue': 'computePrePick_2'},
										autonomy={'continue': Autonomy.Off},
										remapping={'input_pose': 'part_Pose', 'offset_pose': 'pick_offset_Pose', 'output_pose': 'pick_Pose'})

			# x:979 y:624
			OperatableStateMachine.add('compute Backout',
										ComputeGraspAriacState(joint_names=joint_names),
										transitions={'continue': 'moveToBackout', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'UR10_move_group', 'action_topic_namespace': 'UR10_action_topic_namespace', 'tool_link': 'UR10_tool_link', 'pose': 'part_Pose', 'offset': 'backout_offset', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1429 y:324
			OperatableStateMachine.add('computePick',
										ComputeGraspAriacState(joint_names=joint_names),
										transitions={'continue': 'moveToPick', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'UR10_move_group', 'action_topic_namespace': 'UR10_action_topic_namespace', 'tool_link': 'UR10_tool_link', 'pose': 'pick_Pose', 'offset': 'offset', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1179 y:124
			OperatableStateMachine.add('computePrePick_2',
										ComputeGraspAriacState(joint_names=joint_names),
										transitions={'continue': 'moveToPrePick_2', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'UR10_move_group', 'action_topic_namespace': 'UR10_action_topic_namespace', 'tool_link': 'UR10_tool_link', 'pose': 'part_Pose', 'offset': 'preOffset', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:637 y:124
			OperatableStateMachine.add('creatPickOffsetPose',
										CreateDropPoseState(),
										transitions={'continue': 'addPickOffsetPose', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'xyz': 'pick_offset', 'rpy': 'pick_rotation', 'pose': 'pick_offset_Pose'})

			# x:1189 y:474
			OperatableStateMachine.add('createDecreasePick',
										CreatePoseState(xyz=[0.0,0.0,-0.001], rpy=[0.0,0.0,0.0]),
										transitions={'continue': 'addDecreasePose', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'pose_Decrease'})

			# x:484 y:624
			OperatableStateMachine.add('moveBackToPick',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'finished', 'planning_failed': 'finished', 'control_failed': 'wait_8', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'armHomeUp', 'move_group': 'UR10_move_group', 'action_topic_namespace': 'UR10_action_topic_namespace', 'action_topic': 'UR10_action_topic', 'robot_name': 'UR10_robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:721 y:624
			OperatableStateMachine.add('moveToBackout',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'moveBackToPick', 'planning_failed': 'moveBackToPick', 'control_failed': 'wait_9_2'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'action_topic_namespace': 'UR10_action_topic_namespace', 'move_group': 'UR10_move_group', 'action_topic': 'UR10_action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1421 y:424
			OperatableStateMachine.add('moveToPick',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'setGripperOn', 'planning_failed': 'setGripperOn', 'control_failed': 'wait_9'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'action_topic_namespace': 'UR10_action_topic_namespace', 'move_group': 'UR10_move_group', 'action_topic': 'UR10_action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1421 y:217
			OperatableStateMachine.add('moveToPrePick_2',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'computePick', 'planning_failed': 'computePick', 'control_failed': 'wait_9_3'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'action_topic_namespace': 'UR10_action_topic_namespace', 'move_group': 'UR10_move_group', 'action_topic': 'UR10_action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:334 y:124
			OperatableStateMachine.add('moveToPrePose',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'creatPickOffsetPose', 'planning_failed': 'creatPickOffsetPose', 'control_failed': 'wait_3_2', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'armHomeDown', 'move_group': 'UR10_move_group', 'action_topic_namespace': 'UR10_action_topic_namespace', 'action_topic': 'UR10_action_topic', 'robot_name': 'UR10_robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1421 y:524
			OperatableStateMachine.add('setGripperOn',
										VacuumGripperControlState2(enable=True),
										transitions={'continue': 'wait_3', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off})

			# x:1457 y:624
			OperatableStateMachine.add('wait_3',
										WaitState(wait_time=0.5),
										transitions={'done': 'CheckGipper'},
										autonomy={'done': Autonomy.Off})

			# x:357 y:17
			OperatableStateMachine.add('wait_3_2',
										WaitState(wait_time=0.5),
										transitions={'done': 'moveToPrePose'},
										autonomy={'done': Autonomy.Off})

			# x:507 y:724
			OperatableStateMachine.add('wait_8',
										WaitState(wait_time=0.5),
										transitions={'done': 'moveBackToPick'},
										autonomy={'done': Autonomy.Off})

			# x:1657 y:424
			OperatableStateMachine.add('wait_9',
										WaitState(wait_time=0.5),
										transitions={'done': 'moveToPick'},
										autonomy={'done': Autonomy.Off})

			# x:757 y:724
			OperatableStateMachine.add('wait_9_2',
										WaitState(wait_time=0.5),
										transitions={'done': 'moveToBackout'},
										autonomy={'done': Autonomy.Off})

			# x:1657 y:224
			OperatableStateMachine.add('wait_9_3',
										WaitState(wait_time=0.5),
										transitions={'done': 'moveToPrePick_2'},
										autonomy={'done': Autonomy.Off})

			# x:1220 y:621
			OperatableStateMachine.add('CheckGipper',
										self.use_behavior(CheckGipperSM, 'CheckGipper'),
										transitions={'finished': 'compute Backout', 'failed': 'failed', 'decrees': 'createDecreasePick'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'decrees': Autonomy.Inherit},
										remapping={'attachedWanted': 'trueVariable'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
