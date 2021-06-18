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
from ariac_flexbe_states.detect_part_camera_ariac_state import DetectPartCameraAriacState
from ariac_flexbe_states.get_gripper_status_state import GetGripperStatusState
from ariac_flexbe_states.lookup_from_table import LookupFromTableState
from ariac_flexbe_states.moveit_to_joints_dyn_ariac_state import MoveitToJointsDynAriacState
from ariac_flexbe_states.srdf_state_to_moveit_ariac_state import SrdfStateToMoveitAriac
from ariac_flexbe_states.vacuum_gripper_control_state import VacuumGripperControlState
from ariac_logistics_flexbe_states.get_material_locations import GetMaterialLocationsState
from ariac_support_flexbe_states.equal_state import EqualState
from ariac_support_flexbe_states.get_item_from_list_state import GetItemFromListState
from ariac_support_flexbe_states.text_to_float_state import TextToFloatState as ariac_support_flexbe_states__TextToFloatState
from flexbe_states.wait_state import WaitState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sun Apr 25 2021
@author: docent
'''
class pick_part_from_binSM(Behavior):
	'''
	pick's a specific part form a it's bin
	'''


	def __init__(self):
		super(pick_part_from_binSM, self).__init__()
		self.name = 'pick_part_from_bin'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		gripper_status_topic = '/ariac/kitting/arm/gripper/state'
		gripper_service = '/ariac/kitting/arm/gripper/control'
		# x:179 y:267, x:457 y:293
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['part', 'action_topic_namespace', 'home', 'move_group'])
		_state_machine.userdata.part_pose = []
		_state_machine.userdata.joint_values = []
		_state_machine.userdata.joint_names = []
		_state_machine.userdata.offset = 0.1
		_state_machine.userdata.move_group = ''
		_state_machine.userdata.action_topic_namespace = ''
		_state_machine.userdata.home = ''
		_state_machine.userdata.action_topic = '/move_group'
		_state_machine.userdata.robot_name = ''
		_state_machine.userdata.robot_config = ''
		_state_machine.userdata.camera_ref_frame = 'linear_arm_actuator'
		_state_machine.userdata.camera_topic = ''
		_state_machine.userdata.camera_frame = ''
		_state_machine.userdata.tool_link = 'ee_link'
		_state_machine.userdata.agv_pose = []
		_state_machine.userdata.part_rotation = 0
		_state_machine.userdata.part_drop_offset = 0.1
		_state_machine.userdata.bin = ''
		_state_machine.userdata.locations = []
		_state_machine.userdata.zero = 0
		_state_machine.userdata.gripper_status_attached = False
		_state_machine.userdata.gripper_status_enabled = False
		_state_machine.userdata.OneValue = 1
		_state_machine.userdata.drop_gripper = 0.001
		_state_machine.userdata.true = True
		_state_machine.userdata.part_height = ''
		_state_machine.userdata.part = []
		_state_machine.userdata.has_part = True
		_state_machine.userdata.offset_pose = []
		_state_machine.userdata.location_type = 'bin'

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:225 y:135
			OperatableStateMachine.add('MoveR1Home',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'GetPartLocation', 'planning_failed': 'WaitState1', 'control_failed': 'WaitState1', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'home', 'move_group': 'move_group', 'action_topic_namespace': 'action_topic_namespace', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:919 y:453
			OperatableStateMachine.add('ComputePick',
										ComputeGraspAriacState(joint_names=['linear_arm_actuator_joint', 'shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']),
										transitions={'continue': 'MoveR1ToPick1', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'move_group', 'action_topic_namespace': 'action_topic_namespace', 'tool_link': 'tool_link', 'pose': 'pose', 'offset': 'part_height', 'rotation': 'part_rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:558 y:136
			OperatableStateMachine.add('GetBinFromLocation',
										GetItemFromListState(),
										transitions={'done': 'LookupCameraTopic', 'invalid_index': 'failed'},
										autonomy={'done': Autonomy.Off, 'invalid_index': Autonomy.Off},
										remapping={'list': 'locations', 'index': 'zero', 'item': 'bin'})

			# x:377 y:138
			OperatableStateMachine.add('GetPartLocation',
										GetMaterialLocationsState(),
										transitions={'continue': 'GetBinFromLocation'},
										autonomy={'continue': Autonomy.Off},
										remapping={'part': 'part', 'location_type': 'location_type', 'material_locations': 'locations'})

			# x:1103 y:383
			OperatableStateMachine.add('HeightParts',
										LookupFromTableState(parameter_name='/ariac_tables_unit1', table_name='part_param', index_title='part', column_title='part_height'),
										transitions={'found': 'TextToFloat', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'part', 'column_value': 'part_height'})

			# x:928 y:142
			OperatableStateMachine.add('LookupCameraFrame',
										LookupFromTableState(parameter_name='/ariac_tables_unit1', table_name='unit1_table', index_title='bin', column_title='camera_frame'),
										transitions={'found': 'LookupPreGrasp', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'bin', 'column_value': 'camera_frame'})

			# x:771 y:139
			OperatableStateMachine.add('LookupCameraTopic',
										LookupFromTableState(parameter_name='/ariac_tables_unit1', table_name='unit1_table', index_title='bin', column_title='camera_topic'),
										transitions={'found': 'LookupCameraFrame', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'bin', 'column_value': 'camera_topic'})

			# x:1094 y:148
			OperatableStateMachine.add('LookupPreGrasp',
										LookupFromTableState(parameter_name='/ariac_tables_unit1', table_name='unit1_table', index_title='bin', column_title='robot_config'),
										transitions={'found': 'detect camera part', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'bin', 'column_value': 'robot_config'})

			# x:1103 y:297
			OperatableStateMachine.add('MoveR1Pregrasp1',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'HeightParts', 'planning_failed': 'WaitState2', 'control_failed': 'WaitState2', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'robot_config', 'move_group': 'move_group', 'action_topic_namespace': 'action_topic_namespace', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:669 y:447
			OperatableStateMachine.add('MoveR1ToPick1',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'ActivateGripper', 'planning_failed': 'ActivateGripper', 'control_failed': 'ActivateGripper'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'action_topic_namespace': 'action_topic_namespace', 'move_group': 'move_group', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:17 y:368
			OperatableStateMachine.add('MoveR1ToPregrasp2',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'finished', 'planning_failed': 'WaitState4', 'control_failed': 'WaitState4', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'robot_config', 'move_group': 'move_group', 'action_topic_namespace': 'action_topic_namespace', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1093 y:453
			OperatableStateMachine.add('TextToFloat',
										ariac_support_flexbe_states__TextToFloatState(),
										transitions={'done': 'ComputePick'},
										autonomy={'done': Autonomy.Off},
										remapping={'text_value': 'part_height', 'float_value': 'part_height'})

			# x:177 y:439
			OperatableStateMachine.add('WachtEven',
										WaitState(wait_time=3),
										transitions={'done': 'has part'},
										autonomy={'done': Autonomy.Off})

			# x:245 y:13
			OperatableStateMachine.add('WaitState1',
										WaitState(wait_time=5),
										transitions={'done': 'MoveR1Home'},
										autonomy={'done': Autonomy.Off})

			# x:1319 y:298
			OperatableStateMachine.add('WaitState2',
										WaitState(wait_time=5),
										transitions={'done': 'MoveR1Pregrasp1'},
										autonomy={'done': Autonomy.Off})

			# x:694 y:379
			OperatableStateMachine.add('WaitState3',
										WaitState(wait_time=1),
										transitions={'done': 'MoveR1ToPick1'},
										autonomy={'done': Autonomy.Off})

			# x:11 y:265
			OperatableStateMachine.add('WaitState4',
										WaitState(wait_time=5),
										transitions={'done': 'MoveR1ToPregrasp2'},
										autonomy={'done': Autonomy.Off})

			# x:540 y:553
			OperatableStateMachine.add('create offset',
										AddOffsetToPoseState(),
										transitions={'continue': 'ComputePick'},
										autonomy={'continue': Autonomy.Off},
										remapping={'input_pose': 'pose', 'offset_pose': 'offset_pose', 'output_pose': 'pose'})

			# x:377 y:551
			OperatableStateMachine.add('create offset pose',
										CreatePoseState(xyz=[0,0,-0.005], rpy=[0,0,0]),
										transitions={'continue': 'create offset', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'offset_pose'})

			# x:1084 y:228
			OperatableStateMachine.add('detect camera part',
										DetectPartCameraAriacState(time_out=5.0),
										transitions={'continue': 'MoveR1Pregrasp1', 'failed': 'failed', 'not_found': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ref_frame': 'camera_ref_frame', 'camera_topic': 'camera_topic', 'camera_frame': 'camera_frame', 'part': 'part', 'pose': 'pose'})

			# x:286 y:444
			OperatableStateMachine.add('get gripper state',
										GetGripperStatusState(topic_name='/ariac/kitting/arm/gripper/state'),
										transitions={'continue': 'WachtEven', 'fail': 'failed'},
										autonomy={'continue': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'enabled': 'gripper_status_enabled', 'attached': 'gripper_status_attached'})

			# x:6 y:451
			OperatableStateMachine.add('has part',
										EqualState(),
										transitions={'true': 'MoveR1ToPregrasp2', 'false': 'create offset pose'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'gripper_status_attached', 'value_b': 'has_part'})

			# x:479 y:448
			OperatableStateMachine.add('ActivateGripper',
										VacuumGripperControlState(enable=True, service_name=gripper_service),
										transitions={'continue': 'get gripper state', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
