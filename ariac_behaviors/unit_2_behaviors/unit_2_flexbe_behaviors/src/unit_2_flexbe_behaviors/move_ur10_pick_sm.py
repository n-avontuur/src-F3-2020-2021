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
from ariac_flexbe_states.create_pose import CreatePoseState
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
		joint_names = ['gantry_arm_elbow_joint', 'gantry_arm_shoulder_lift_joint', 'gantry_arm_shoulder_pan_joint', 'gantry_arm_wrist_1_joint', 'gantry_arm_wrist_2_joint', 'gantry_arm_wrist_3_joint']
		gripper_service = '/ariac/gantry/arm/gripper/controle'
		# x:1583 y:390, x:130 y:463
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['part_Type', 'pick_Pose'])
		_state_machine.userdata.trueVariable = True
		_state_machine.userdata.falseVariable = False
		_state_machine.userdata.pick_Pose = []
		_state_machine.userdata.part_Type = ''

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:85 y:24
			OperatableStateMachine.add('setRobotParameters',
										set_Robot_Parameters(),
										transitions={'continue': 'moveToPrePick', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'part_Type': 'part_Type', 'UR10_move_group': 'UR10_move_group', 'UR10_action_topic_namespace': 'UR10_action_topic_namespace', 'UR10_action_topic': 'UR10_action_topic', 'UR10_tool_link': 'UR10_tool_link', 'UR10_robot_name': 'UR10_robot_name', 'gripper_service': 'gripper_service', 'gripper_status_topic': 'gripper_status_topic', 'gripper_status_attached': 'gripper_status_attached', 'gripper_status_enabled': 'gripper_status_enabled', 'armHomeDown': 'armHomeDown', 'armHomeUp': 'armHomeUp', 'pick_offset': 'pick_offset', 'pick_rotation': 'pick_rotation'})

			# x:1536 y:74
			OperatableStateMachine.add('checkGripperStatus',
										GetGripperStatusState(gripper_status_topic='/ariac/gantry/arm/gripper/state'),
										transitions={'continue': 'isPartAttached', 'fail': 'failed'},
										autonomy={'continue': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'enabled': 'gripper_Enabled', 'attached': 'gripper_Attached'})

			# x:479 y:24
			OperatableStateMachine.add('computePick',
										ComputeGraspAriacState(joint_names=joint_names),
										transitions={'continue': 'moveToPick', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'UR10_move_group', 'action_topic_namespace': 'UR10_action_topic_namespace', 'tool_link': 'UR10_tool_link', 'pose': 'pick_Pose', 'offset': 'pick_offset', 'rotation': 'pick_rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1339 y:224
			OperatableStateMachine.add('createDecreasePick',
										CreatePoseState(xyz=[0.0,0.0,-0.002], rpy=[0.0,0.0,0.0]),
										transitions={'continue': 'addDecreasePose', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'pose_Decrease'})

			# x:1524 y:174
			OperatableStateMachine.add('isPartAttached',
										EqualState(),
										transitions={'true': 'moveBackToPick', 'false': 'createDecreasePick'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'gripper_Attached', 'value_b': 'trueVariable'})

			# x:1534 y:274
			OperatableStateMachine.add('moveBackToPick',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'finished', 'planning_failed': 'wait_8', 'control_failed': 'wait_8', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'armHomeUp', 'move_group': 'UR10_move_group', 'action_topic_namespace': 'UR10_action_topic_namespace', 'action_topic': 'UR10_action_topic', 'robot_name': 'UR10_robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:671 y:24
			OperatableStateMachine.add('moveToPick',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'setGripperOn', 'planning_failed': 'wait_9', 'control_failed': 'wait_9'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'action_topic_namespace': 'UR10_action_topic_namespace', 'move_group': 'UR10_move_group', 'action_topic': 'UR10_action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:284 y:24
			OperatableStateMachine.add('moveToPrePick',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'computePick', 'planning_failed': 'wait', 'control_failed': 'wait', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'armHomeUp', 'move_group': 'UR10_move_group', 'action_topic_namespace': 'UR10_action_topic_namespace', 'action_topic': 'UR10_action_topic', 'robot_name': 'UR10_robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1174 y:24
			OperatableStateMachine.add('setGripperOn',
										VacuumGripperControlState(enable=True, service_name=gripper_service),
										transitions={'continue': 'wait_3', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off})

			# x:307 y:124
			OperatableStateMachine.add('wait',
										WaitState(wait_time=0.5),
										transitions={'done': 'moveToPrePick'},
										autonomy={'done': Autonomy.Off})

			# x:1407 y:24
			OperatableStateMachine.add('wait_3',
										WaitState(wait_time=0.5),
										transitions={'done': 'checkGripperStatus'},
										autonomy={'done': Autonomy.Off})

			# x:1707 y:274
			OperatableStateMachine.add('wait_8',
										WaitState(wait_time=0.5),
										transitions={'done': 'moveBackToPick'},
										autonomy={'done': Autonomy.Off})

			# x:657 y:124
			OperatableStateMachine.add('wait_9',
										WaitState(wait_time=0.5),
										transitions={'done': 'moveToPick'},
										autonomy={'done': Autonomy.Off})

			# x:1136 y:174
			OperatableStateMachine.add('addDecreasePose',
										AddOffsetToPoseState(),
										transitions={'continue': 'computePick'},
										autonomy={'continue': Autonomy.Off},
										remapping={'input_pose': 'pick_Pose', 'offset_pose': 'pose_Decrease', 'output_pose': 'pick_Pose'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
