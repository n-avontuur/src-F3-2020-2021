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
from ariac_flexbe_states.get_object_pose import GetObjectPoseState
from ariac_flexbe_states.lookup_from_table import LookupFromTableState
from ariac_flexbe_states.moveit_to_joints_dyn_ariac_state import MoveitToJointsDynAriacState
from ariac_flexbe_states.srdf_state_to_moveit_ariac_state import SrdfStateToMoveitAriac
from ariac_flexbe_states.vacuum_gripper_control_state import VacuumGripperControlState
from ariac_support_flexbe_states.add_numeric_state import AddNumericState
from ariac_support_flexbe_states.equal_state import EqualState
from ariac_support_flexbe_states.replace_state import ReplaceState
from flexbe_states.wait_state import WaitState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon May 31 2021
@author: kemla buke
'''
class place_part_on_binSM(Behavior):
	'''
	plaatst de parts in de bin
	'''


	def __init__(self):
		super(place_part_on_binSM, self).__init__()
		self.name = 'place_part_on_bin'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:1706 y:620, x:1032 y:553
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['part', 'action_topic_namespace', 'gripper_service', 'gripper_status_topic', 'gear_position', 'gasket_position', 'piston_position'], output_keys=['gear_position', 'gasket_position', 'piston_position'])
		_state_machine.userdata.index = 0
		_state_machine.userdata.part_drop_offset = 0.1
		_state_machine.userdata.move_group = 'manipulator'
		_state_machine.userdata.action_topic_namespace = '/ariac/arm2'
		_state_machine.userdata.action_topic = '/move_group'
		_state_machine.userdata.part = 'piston_rod_part'
		_state_machine.userdata.camera_ref_frame = 'arm2_linear_arm_actuator'
		_state_machine.userdata.camera_topic = ''
		_state_machine.userdata.camera_frame = ''
		_state_machine.userdata.robot_name = ''
		_state_machine.userdata.robot_config = ''
		_state_machine.userdata.tool_link = 'ee_link'
		_state_machine.userdata.locations = []
		_state_machine.userdata.bin1 = 'bin1'
		_state_machine.userdata.part_height = 0
		_state_machine.userdata.gripper_service = '/ariac/arm2/gripper/control'
		_state_machine.userdata.gripper_status_topic = '/ariac/arm2/gripper/state'
		_state_machine.userdata.gripper_status_attached = False
		_state_machine.userdata.gripper_status_enabled = False
		_state_machine.userdata.gasket_part = 'gasket_part'
		_state_machine.userdata.piston_part = 'piston_rod_part'
		_state_machine.userdata.gear_part = 'gear_part'
		_state_machine.userdata.bin2 = 'bin2'
		_state_machine.userdata.bin6 = 'bin6'
		_state_machine.userdata.pose = []
		_state_machine.userdata.offset = 0.1
		_state_machine.userdata.rotation = 0
		_state_machine.userdata.bin1_frame = 'bin1_frame'
		_state_machine.userdata.bin2_frame = 'bin2_frame'
		_state_machine.userdata.bin6_frame = 'bin6_frame'
		_state_machine.userdata.gear_position = 0
		_state_machine.userdata.gasket_position = 0
		_state_machine.userdata.piston_position = 0
		_state_machine.userdata.position_add_1 = 1
		_state_machine.userdata.position = 0
		_state_machine.userdata.pose_offset = []
		_state_machine.userdata.position_1 = 1
		_state_machine.userdata.position_2 = 2
		_state_machine.userdata.position_3 = 3

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:90 y:47
			OperatableStateMachine.add('equals gasket',
										EqualState(),
										transitions={'true': 'lookup predrop gasket list', 'false': 'equals gear'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'part', 'value_b': 'gasket_part'})

			# x:427 y:142
			OperatableStateMachine.add('add gear position',
										AddNumericState(),
										transitions={'done': 'replace position value_2'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'position_add_1', 'value_b': 'gear_position', 'result': 'gear_position'})

			# x:425 y:254
			OperatableStateMachine.add('add piston position',
										AddNumericState(),
										transitions={'done': 'replace position value_3'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'position_add_1', 'value_b': 'piston_position', 'result': 'piston_position'})

			# x:1646 y:210
			OperatableStateMachine.add('compute drop',
										ComputeGraspAriacState(joint_names=['linear_arm_actuator_joint', 'shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']),
										transitions={'continue': 'move unit 2 to drop', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'move_group', 'action_topic_namespace': 'action_topic_namespace', 'tool_link': 'tool_link', 'pose': 'pose', 'offset': 'offset', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1446 y:63
			OperatableStateMachine.add('create offset pose',
										CreatePoseState(xyz=[-0.2,0,0], rpy=[0,0,0]),
										transitions={'continue': 'offset computed pose', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'pose_offset'})

			# x:1440 y:130
			OperatableStateMachine.add('create offset pose_2',
										CreatePoseState(xyz=[0,0,0], rpy=[0,0,0]),
										transitions={'continue': 'offset computed pose', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'pose_offset'})

			# x:1440 y:204
			OperatableStateMachine.add('create offset pose_3',
										CreatePoseState(xyz=[0,-0.2,0], rpy=[0,0,0]),
										transitions={'continue': 'offset computed pose', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'pose_offset'})

			# x:1629 y:371
			OperatableStateMachine.add('deactivate gripper',
										VacuumGripperControlState(enable=False),
										transitions={'continue': 'wait4', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'service_name': 'gripper_service'})

			# x:90 y:143
			OperatableStateMachine.add('equals gear',
										EqualState(),
										transitions={'true': 'lookup predrop gear list', 'false': 'equals piston'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'part', 'value_b': 'gear_part'})

			# x:84 y:255
			OperatableStateMachine.add('equals piston',
										EqualState(),
										transitions={'true': 'lookup predrop piston', 'false': 'failed'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'part', 'value_b': 'piston_part'})

			# x:775 y:140
			OperatableStateMachine.add('get bin 2 pose',
										GetObjectPoseState(),
										transitions={'continue': 'move unit 2 to predrop', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'ref_frame': 'camera_ref_frame', 'frame': 'bin1_frame', 'pose': 'pose'})

			# x:781 y:248
			OperatableStateMachine.add('get bin 3 pose',
										GetObjectPoseState(),
										transitions={'continue': 'move unit 2 to predrop', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'ref_frame': 'camera_ref_frame', 'frame': 'bin6_frame', 'pose': 'pose'})

			# x:777 y:42
			OperatableStateMachine.add('get bin pose',
										GetObjectPoseState(),
										transitions={'continue': 'move unit 2 to predrop', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'ref_frame': 'camera_ref_frame', 'frame': 'bin2_frame', 'pose': 'pose'})

			# x:257 y:49
			OperatableStateMachine.add('lookup predrop gasket list',
										LookupFromTableState(parameter_name='/ariac_tables_unit2', table_name='unit2_table', index_title='bin', column_title='robot_config'),
										transitions={'found': 'add gasket position', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'bin2', 'column_value': 'robot_config'})

			# x:270 y:146
			OperatableStateMachine.add('lookup predrop gear list',
										LookupFromTableState(parameter_name='/ariac_tables_unit2', table_name='unit2_table', index_title='bin', column_title='robot_config'),
										transitions={'found': 'add gear position', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'bin1', 'column_value': 'robot_config'})

			# x:275 y:257
			OperatableStateMachine.add('lookup predrop piston',
										LookupFromTableState(parameter_name='/ariac_tables_unit2', table_name='unit2_table', index_title='bin', column_title='robot_config'),
										transitions={'found': 'add piston position', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'bin6', 'column_value': 'robot_config'})

			# x:1653 y:521
			OperatableStateMachine.add('move back to predrop',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'finished', 'planning_failed': 'wait3', 'control_failed': 'wait3', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'robot_config', 'move_group': 'move_group', 'action_topic_namespace': 'action_topic_namespace', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1625 y:310
			OperatableStateMachine.add('move unit 2 to drop',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'deactivate gripper', 'planning_failed': 'wait2', 'control_failed': 'wait2'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'action_topic_namespace': 'action_topic_namespace', 'move_group': 'move_group', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1064 y:64
			OperatableStateMachine.add('move unit 2 to predrop',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'position check', 'planning_failed': 'wait', 'control_failed': 'wait', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'robot_config', 'move_group': 'move_group', 'action_topic_namespace': 'action_topic_namespace', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1648 y:94
			OperatableStateMachine.add('offset computed pose',
										AddOffsetToPoseState(),
										transitions={'continue': 'compute drop'},
										autonomy={'continue': Autonomy.Off},
										remapping={'input_pose': 'pose', 'offset_pose': 'pose_offset', 'output_pose': 'pose'})

			# x:1227 y:63
			OperatableStateMachine.add('position check',
										EqualState(),
										transitions={'true': 'create offset pose', 'false': 'position check_2'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'position', 'value_b': 'position_1'})

			# x:1221 y:127
			OperatableStateMachine.add('position check_2',
										EqualState(),
										transitions={'true': 'create offset pose_2', 'false': 'position check_3'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'position', 'value_b': 'position_2'})

			# x:1221 y:199
			OperatableStateMachine.add('position check_3',
										EqualState(),
										transitions={'true': 'create offset pose_3', 'false': 'failed'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'position', 'value_b': 'position_3'})

			# x:591 y:46
			OperatableStateMachine.add('replace position value',
										ReplaceState(),
										transitions={'done': 'get bin pose'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'gasket_position', 'result': 'position'})

			# x:586 y:141
			OperatableStateMachine.add('replace position value_2',
										ReplaceState(),
										transitions={'done': 'get bin 2 pose'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'gear_position', 'result': 'position'})

			# x:581 y:253
			OperatableStateMachine.add('replace position value_3',
										ReplaceState(),
										transitions={'done': 'get bin 3 pose'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'piston_position', 'result': 'position'})

			# x:1088 y:142
			OperatableStateMachine.add('wait',
										WaitState(wait_time=5),
										transitions={'done': 'move unit 2 to predrop'},
										autonomy={'done': Autonomy.Off})

			# x:1513 y:313
			OperatableStateMachine.add('wait2',
										WaitState(wait_time=5),
										transitions={'done': 'move unit 2 to drop'},
										autonomy={'done': Autonomy.Off})

			# x:1516 y:485
			OperatableStateMachine.add('wait3',
										WaitState(wait_time=5),
										transitions={'done': 'move back to predrop'},
										autonomy={'done': Autonomy.Off})

			# x:1670 y:448
			OperatableStateMachine.add('wait4',
										WaitState(wait_time=2),
										transitions={'done': 'move back to predrop'},
										autonomy={'done': Autonomy.Off})

			# x:424 y:48
			OperatableStateMachine.add('add gasket position',
										AddNumericState(),
										transitions={'done': 'replace position value'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'position_add_1', 'value_b': 'gasket_position', 'result': 'gasket_position'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
