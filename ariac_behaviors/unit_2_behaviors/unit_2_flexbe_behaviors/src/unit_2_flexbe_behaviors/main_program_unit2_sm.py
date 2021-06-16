#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_states.detect_part_on_AGV_camera import DetectPartOnAGVCamera
from ariac_flexbe_states.set_GantryParameters import set_GantryParameters
from ariac_flexbe_states.set_PickParameters import setPickParameters
from ariac_flexbe_states.srdf_state_to_moveit_ariac_state import SrdfStateToMoveitAriac
from ariac_flexbe_states.start_assignment_state import StartAssignment
from ariac_logistics_flexbe_states.get_assembly_shipment_from_order_state import GetAssemblyShipmentFromOrderState
from ariac_logistics_flexbe_states.get_order_state import GetOrderState
from ariac_logistics_flexbe_states.get_part_from_products_state import GetPartFromProductsState
from ariac_support_flexbe_states.add_numeric_state import AddNumericState
from ariac_support_flexbe_states.equal_state import EqualState
from ariac_support_flexbe_states.replace_state import ReplaceState
from flexbe_states.wait_state import WaitState
from unit_2_flexbe_behaviors.home_ur10_sm import Home_UR10SM
from unit_2_flexbe_behaviors.move_ur10_drop_sm import Move_UR10_DropSM
from unit_2_flexbe_behaviors.move_ur10_pick_sm import Move_UR10_PickSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon Jun 14 2021
@author: Niels Avontuur
'''
class Main_Program_unit2SM(Behavior):
	'''
	Main program for assembly
	'''


	def __init__(self):
		super(Main_Program_unit2SM, self).__init__()
		self.name = 'Main_Program_unit2'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(Home_UR10SM, 'Home_UR10')
		self.add_behavior(Move_UR10_DropSM, 'Move_UR10_Drop')
		self.add_behavior(Move_UR10_PickSM, 'Move_UR10_Pick')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:

		# ! 1635 20 
		# Made by Niels Avontuur



	def create(self):
		# x:173 y:205, x:745 y:434, x:288 y:205, x:468 y:178
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed', 'no_Order', 'assambly_Compleet'])
		_state_machine.userdata.zero = 0
		_state_machine.userdata.part_Number = 0
		_state_machine.userdata.ref_frame = 'world'
		_state_machine.userdata.product_index = 0
		_state_machine.userdata.one = 1
		_state_machine.userdata.assembly_index = 0

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:30 y:40
			OperatableStateMachine.add('startAssignment',
										StartAssignment(),
										transitions={'continue': 'wait_6'},
										autonomy={'continue': Autonomy.Off})

			# x:28 y:384
			OperatableStateMachine.add('Move_UR10_Drop',
										self.use_behavior(Move_UR10_DropSM, 'Move_UR10_Drop'),
										transitions={'finished': 'addPart', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'part_Type': 'part_Type', 'drop_Pose': 'drop_Pose'})

			# x:157 y:619
			OperatableStateMachine.add('Move_UR10_Pick',
										self.use_behavior(Move_UR10_PickSM, 'Move_UR10_Pick'),
										transitions={'finished': 'moveGantryHome_2', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'part_Type': 'part_Type', 'pick_Pose': 'pick_Pose'})

			# x:1241 y:39
			OperatableStateMachine.add('addAssambly',
										AddNumericState(),
										transitions={'done': 'zeroPartIndex'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'assembly_index', 'value_b': 'one', 'result': 'assembly_index'})

			# x:27 y:308
			OperatableStateMachine.add('addPart',
										AddNumericState(),
										transitions={'done': 'moveGantrySection_2'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'product_index', 'value_b': 'one', 'result': 'product_index'})

			# x:1067 y:120
			OperatableStateMachine.add('checkNumberOfAssembly',
										EqualState(),
										transitions={'true': 'assambly_Compleet', 'false': 'checkNumberOfPart'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'number_of_assembly_shipments', 'value_b': 'assembly_index'})

			# x:1348 y:125
			OperatableStateMachine.add('checkNumberOfPart',
										EqualState(),
										transitions={'true': 'addAssambly', 'false': 'getPartFromOrder'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'number_of_products', 'value_b': 'product_index'})

			# x:1365 y:360
			OperatableStateMachine.add('findPartOnAGV',
										DetectPartOnAGVCamera(time_out=0.5),
										transitions={'continue': 'setPickParameters', 'failed': 'failed', 'not_found': 'findPartOnAGV2'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'agv': 'first_agv', 'ref_frame': 'ref_frame', 'camera_topic': 'camera_topic1', 'camera_frame': 'camera_frame1', 'part': 'part_Type', 'part_Pose': 'pick_Pose', 'agv_Name': 'agv_Name'})

			# x:1366 y:434
			OperatableStateMachine.add('findPartOnAGV2',
										DetectPartOnAGVCamera(time_out=0.5),
										transitions={'continue': 'setPickParameters', 'failed': 'failed', 'not_found': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'agv': 'sec_agv', 'ref_frame': 'ref_frame', 'camera_topic': 'camera_topic2', 'camera_frame': 'camera_frame2', 'part': 'part_Type', 'part_Pose': 'pick_Pose', 'agv_Name': 'agv_Name'})

			# x:760 y:37
			OperatableStateMachine.add('getAssembly',
										GetAssemblyShipmentFromOrderState(),
										transitions={'continue': 'checkNumberOfAssembly', 'invalid_index': 'failed'},
										autonomy={'continue': Autonomy.Off, 'invalid_index': Autonomy.Off},
										remapping={'assembly_shipments': 'assembly_shipments', 'assembly_index': 'assembly_index', 'shipment_type': 'shipment_type', 'products': 'products', 'station_id': 'station_id', 'number_of_products': 'number_of_products'})

			# x:352 y:34
			OperatableStateMachine.add('getOrder',
										GetOrderState(),
										transitions={'order_found': 'Home_UR10', 'no_order_found': 'no_Order'},
										autonomy={'order_found': Autonomy.Off, 'no_order_found': Autonomy.Off},
										remapping={'order_id': 'order_id', 'kitting_shipments': 'kitting_shipments', 'number_of_kitting_shipments': 'number_of_kitting_shipments', 'assembly_shipments': 'assembly_shipments', 'number_of_assembly_shipments': 'number_of_assembly_shipments'})

			# x:1351 y:205
			OperatableStateMachine.add('getPartFromOrder',
										GetPartFromProductsState(),
										transitions={'continue': 'setGantryParameter', 'invalid_index': 'failed'},
										autonomy={'continue': Autonomy.Off, 'invalid_index': Autonomy.Off},
										remapping={'products': 'products', 'index': 'product_index', 'type': 'part_Type', 'pose': 'drop_Pose'})

			# x:956 y:660
			OperatableStateMachine.add('moveGantryAGV',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'Move_UR10_Pick', 'planning_failed': 'wait_4', 'control_failed': 'wait_4', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'gantry_AGV_Pose', 'move_group': 'gantry_move_group', 'action_topic_namespace': 'gantry_action_topic_namespace', 'action_topic': 'gantry_action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1199 y:643
			OperatableStateMachine.add('moveGantryHome',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'moveGantryAGV', 'planning_failed': 'wait_2', 'control_failed': 'wait_2', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'home_Pose', 'move_group': 'gantry_move_group', 'action_topic_namespace': 'gantry_action_topic_namespace', 'action_topic': 'gantry_action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:163 y:537
			OperatableStateMachine.add('moveGantryHome_2',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'moveGantryTable_2', 'planning_failed': 'wait_3', 'control_failed': 'wait_3', 'param_error': 'Move_UR10_Pick'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'home_Pose', 'move_group': 'gantry_move_group', 'action_topic_namespace': 'gantry_action_topic_namespace', 'action_topic': 'gantry_action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1195 y:565
			OperatableStateMachine.add('moveGantrySection',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'moveGantryHome', 'planning_failed': 'wait', 'control_failed': 'wait', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'section_Pose', 'move_group': 'gantry_move_group', 'action_topic_namespace': 'gantry_action_topic_namespace', 'action_topic': 'gantry_action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:28 y:229
			OperatableStateMachine.add('moveGantrySection_2',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'finished', 'planning_failed': 'wait_5', 'control_failed': 'wait_5', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'section_Pose', 'move_group': 'gantry_move_group', 'action_topic_namespace': 'gantry_action_topic_namespace', 'action_topic': 'gantry_action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:162 y:466
			OperatableStateMachine.add('moveGantryTable_2',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'Move_UR10_Drop', 'planning_failed': 'wait_3_2', 'control_failed': 'wait_3_2', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'table_Pose', 'move_group': 'gantry_move_group', 'action_topic_namespace': 'gantry_action_topic_namespace', 'action_topic': 'gantry_action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1378 y:283
			OperatableStateMachine.add('setGantryParameter',
										set_GantryParameters(),
										transitions={'continue': 'findPartOnAGV', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'station_id': 'station_id', 'home_Pose': 'home_Pose', 'table_Pose': 'table_Pose', 'section_Pose': 'section_Pose', 'gantry_move_group': 'gantry_move_group', 'gantry_action_topic_namespace': 'gantry_action_topic_namespace', 'gantry_action_topic': 'gantry_action_topic', 'robot_name': 'robot_name', 'camera_frame1': 'camera_frame1', 'camera_topic1': 'camera_topic1', 'camera_frame2': 'camera_frame2', 'camera_topic2': 'camera_topic2', 'first_agv': 'first_agv', 'sec_agv': 'sec_agv'})

			# x:1197 y:492
			OperatableStateMachine.add('setPickParameters',
										setPickParameters(),
										transitions={'continue': 'moveGantrySection', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'station_id': 'station_id', 'agv_Name': 'agv_Name', 'gantry_AGV_Pose': 'gantry_AGV_Pose'})

			# x:1379 y:564
			OperatableStateMachine.add('wait',
										WaitState(wait_time=0.5),
										transitions={'done': 'moveGantrySection'},
										autonomy={'done': Autonomy.Off})

			# x:1388 y:647
			OperatableStateMachine.add('wait_2',
										WaitState(wait_time=0.5),
										transitions={'done': 'moveGantryHome'},
										autonomy={'done': Autonomy.Off})

			# x:23 y:541
			OperatableStateMachine.add('wait_3',
										WaitState(wait_time=0.5),
										transitions={'done': 'moveGantryHome_2'},
										autonomy={'done': Autonomy.Off})

			# x:25 y:467
			OperatableStateMachine.add('wait_3_2',
										WaitState(wait_time=0.5),
										transitions={'done': 'moveGantryTable_2'},
										autonomy={'done': Autonomy.Off})

			# x:1006 y:741
			OperatableStateMachine.add('wait_4',
										WaitState(wait_time=0.5),
										transitions={'done': 'moveGantryAGV'},
										autonomy={'done': Autonomy.Off})

			# x:28 y:130
			OperatableStateMachine.add('wait_5',
										WaitState(wait_time=0.5),
										transitions={'done': 'moveGantrySection_2'},
										autonomy={'done': Autonomy.Off})

			# x:201 y:39
			OperatableStateMachine.add('wait_6',
										WaitState(wait_time=0.5),
										transitions={'done': 'getOrder'},
										autonomy={'done': Autonomy.Off})

			# x:1019 y:37
			OperatableStateMachine.add('zeroPartIndex',
										ReplaceState(),
										transitions={'done': 'getAssembly'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'product_index', 'result': 'zero'})

			# x:543 y:34
			OperatableStateMachine.add('Home_UR10',
										self.use_behavior(Home_UR10SM, 'Home_UR10'),
										transitions={'finished': 'getAssembly', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
