#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_states.detect_part_camera_ariac_state import DetectPartCameraAriacState
from ariac_flexbe_states.set_GantryParameters import set_Gantry_Parameters
from ariac_flexbe_states.srdf_state_to_moveit_ariac_state import SrdfStateToMoveitAriac
from ariac_flexbe_states.start_assignment_state import StartAssignment
from ariac_logistics_flexbe_states.get_assembly_shipment_from_order_state import GetAssemblyShipmentFromOrderState
from ariac_logistics_flexbe_states.get_order_state import GetOrderState
from ariac_logistics_flexbe_states.get_part_from_products_state import GetPartFromProductsState
from flexbe_states.wait_state import WaitState
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

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:1639 y:721, x:745 y:434, x:230 y:415
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed', 'no_Order'])
		_state_machine.userdata.zero = 0
		_state_machine.userdata.part_Number = 0
		_state_machine.userdata.ref_frame = 'world'

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:30 y:40
			OperatableStateMachine.add('startAssignment',
										StartAssignment(),
										transitions={'continue': 'getOrderInfo'},
										autonomy={'continue': Autonomy.Off})

			# x:1483 y:369
			OperatableStateMachine.add('detectPart',
										DetectPartCameraAriacState(time_out=0.5),
										transitions={'continue': 'finished', 'failed': 'failed', 'not_found': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ref_frame': 'ref_frame', 'camera_topic': 'camera_topic', 'camera_frame': 'camera_frame', 'part': 'part_Type', 'pose': 'part_Pose'})

			# x:207 y:37
			OperatableStateMachine.add('getOrderInfo',
										GetOrderState(),
										transitions={'order_found': 'GetAssamblyOrderInfo', 'no_order_found': 'no_Order'},
										autonomy={'order_found': Autonomy.Off, 'no_order_found': Autonomy.Off},
										remapping={'order_id': 'order_id', 'kitting_shipments': 'kitting_shipments', 'number_of_kitting_shipments': 'number_of_kitting_shipments', 'assembly_shipments': 'assembly_shipments', 'number_of_assembly_shipments': 'number_of_assembly_shipments'})

			# x:672 y:38
			OperatableStateMachine.add('getPartFromOrder',
										GetPartFromProductsState(),
										transitions={'continue': 'setGantry', 'invalid_index': 'failed'},
										autonomy={'continue': Autonomy.Off, 'invalid_index': Autonomy.Off},
										remapping={'products': 'products', 'index': 'part_Number', 'type': 'part_Type', 'pose': 'drop_Pose'})

			# x:1106 y:41
			OperatableStateMachine.add('moveGantrySection',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'moveGantrySection_2', 'planning_failed': 'wait', 'control_failed': 'wait', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'section_Pose', 'move_group': 'move_group', 'action_topic_namespace': 'action_topic_namespace', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1322 y:47
			OperatableStateMachine.add('moveGantrySection_2',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'detectPart', 'planning_failed': 'wait_2', 'control_failed': 'wait_2', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'table_Pose', 'move_group': 'move_group', 'action_topic_namespace': 'action_topic_namespace', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:892 y:42
			OperatableStateMachine.add('setGantry',
										set_Gantry_Parameters(),
										transitions={'continue': 'moveGantrySection', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'station_id': 'station_id', 'table_Pose': 'table_Pose', 'section_Pose': 'section_Pose', 'move_group': 'move_group', 'action_topic_namespace': 'action_topic_namespace', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'camera_frame': 'camera_frame', 'camera_topic': 'camera_topic'})

			# x:1110 y:166
			OperatableStateMachine.add('wait',
										WaitState(wait_time=0.5),
										transitions={'done': 'moveGantrySection'},
										autonomy={'done': Autonomy.Off})

			# x:1325 y:159
			OperatableStateMachine.add('wait_2',
										WaitState(wait_time=0.5),
										transitions={'done': 'moveGantrySection_2'},
										autonomy={'done': Autonomy.Off})

			# x:431 y:36
			OperatableStateMachine.add('GetAssamblyOrderInfo',
										GetAssemblyShipmentFromOrderState(),
										transitions={'continue': 'getPartFromOrder', 'invalid_index': 'failed'},
										autonomy={'continue': Autonomy.Off, 'invalid_index': Autonomy.Off},
										remapping={'assembly_shipments': 'assembly_shipments', 'assembly_index': 'zero', 'shipment_type': 'part_Type', 'products': 'products', 'station_id': 'station_id', 'number_of_products': 'number_of_products'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
