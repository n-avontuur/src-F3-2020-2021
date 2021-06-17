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
from ariac_flexbe_states.detect_part_on_AGV_camera import DetectPartOnAGVCamera
from ariac_flexbe_states.get_object_pose import GetObjectPoseState
from ariac_flexbe_states.notify_assembly_ready_state import NotifyAssemblyReadyState
from ariac_flexbe_states.set_GantryParameters import set_GantryParameters
from ariac_flexbe_states.set_PickParameters import setPickParameters
from ariac_flexbe_states.start_assignment_state import StartAssignment
from ariac_logistics_flexbe_states.get_assembly_shipment_from_order_state import GetAssemblyShipmentFromOrderState
from ariac_logistics_flexbe_states.get_order_state import GetOrderState
from ariac_logistics_flexbe_states.get_part_from_products_state import GetPartFromProductsState
from ariac_support_flexbe_states.add_numeric_state import AddNumericState
from ariac_support_flexbe_states.equal_state import EqualState
from ariac_support_flexbe_states.replace_state import ReplaceState
from flexbe_states.wait_state import WaitState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon Jun 14 2021
@author: Niels Avontuur
'''
class setParameters_unit2SM(Behavior):
	'''
	Setting all parameters for moving the gantry and robot
	'''


	def __init__(self):
		super(setParameters_unit2SM, self).__init__()
		self.name = 'setParameters_unit2'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		joint_names = ['linear_arm_actuator_joint', 'shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']
		# x:96 y:483, x:383 y:490, x:993 y:744, x:383 y:190, x:683 y:290
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed', 'not_found', 'no_order', 'assemblyCompleet'], input_keys=['product_index'], output_keys=['gantry_AGV_Pose', 'gantry_move_group', 'gantry_action_topic_namespace', 'robot_name', 'home_Pose', 'table_Pose', 'gantry_action_topic', 'part_Type', 'section_Pose', 'drop_Pose', 'pick_Pose'])
		_state_machine.userdata.gantry_AGV_Pose = ''
		_state_machine.userdata.gantry_move_group = ''
		_state_machine.userdata.gantry_action_topic_namespace = ''
		_state_machine.userdata.gantry_action_topic = ''
		_state_machine.userdata.table_Pose = ''
		_state_machine.userdata.home_Pose = ''
		_state_machine.userdata.robot_name = ''
		_state_machine.userdata.part_Type = ''
		_state_machine.userdata.ref_frame = 'world'
		_state_machine.userdata.assembly_index = 0
		_state_machine.userdata.product_index = 0
		_state_machine.userdata.one = 1
		_state_machine.userdata.zero = 0
		_state_machine.userdata.section_Pose = ''
		_state_machine.userdata.drop_Pose = []
		_state_machine.userdata.pick_Pose = []

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:37 y:74
			OperatableStateMachine.add('startAssignment',
										StartAssignment(),
										transitions={'continue': 'wait'},
										autonomy={'continue': Autonomy.Off})

			# x:1274 y:74
			OperatableStateMachine.add('addAssambly',
										AddNumericState(),
										transitions={'done': 'replacePartIndex'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'assembly_index', 'value_b': 'one', 'result': 'assembly_index'})

			# x:626 y:174
			OperatableStateMachine.add('assemblyReady',
										NotifyAssemblyReadyState(),
										transitions={'continue': 'assemblyCompleet', 'fail': 'failed'},
										autonomy={'continue': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'as_id': 'station_id', 'shipment_type': 'shipment_type', 'success': 'success', 'inspection_result': 'inspection_result'})

			# x:974 y:174
			OperatableStateMachine.add('checkNumberOfAssembly',
										EqualState(),
										transitions={'true': 'assemblyReady', 'false': 'checkNumberOfPart'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'assembly_index', 'value_b': 'number_of_assembly_shipments'})

			# x:1274 y:174
			OperatableStateMachine.add('checkNumberOfPart',
										EqualState(),
										transitions={'true': 'addAssambly', 'false': 'getPartFromOrder'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'product_index', 'value_b': 'number_of_products'})

			# x:928 y:474
			OperatableStateMachine.add('findPartOnAGV1',
										DetectPartOnAGVCamera(time_out=0.5),
										transitions={'continue': 'setPickParameters', 'failed': 'failed', 'not_found': 'findPartOnAGV1_2'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'agv': 'first_agv', 'ref_frame': 'ref_frame', 'camera_topic': 'camera_topic1', 'camera_frame': 'camera_frame1', 'part': 'part_Type', 'part_Pose': 'pick_Pose', 'agv_Name': 'agv_Name'})

			# x:928 y:624
			OperatableStateMachine.add('findPartOnAGV1_2',
										DetectPartOnAGVCamera(time_out=0.5),
										transitions={'continue': 'getCasePose', 'failed': 'failed', 'not_found': 'not_found'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'agv': 'sec_agv', 'ref_frame': 'ref_frame', 'camera_topic': 'camera_topic2', 'camera_frame': 'camera_frame2', 'part': 'part_Type', 'part_Pose': 'pick_Pose', 'agv_Name': 'agv_Name'})

			# x:599 y:74
			OperatableStateMachine.add('getAssamblyOrder',
										GetAssemblyShipmentFromOrderState(),
										transitions={'continue': 'checkNumberOfAssembly', 'invalid_index': 'failed'},
										autonomy={'continue': Autonomy.Off, 'invalid_index': Autonomy.Off},
										remapping={'assembly_shipments': 'assembly_shipments', 'assembly_index': 'assembly_index', 'shipment_type': 'shipment_type', 'products': 'products', 'station_id': 'station_id', 'number_of_products': 'number_of_products'})

			# x:614 y:666
			OperatableStateMachine.add('getCasePose',
										GetObjectPoseState(),
										transitions={'continue': 'addAsPoseAndCasePose', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'ref_frame': 'ref_frame', 'frame': 'case_frame', 'pose': 'case_Pose'})

			# x:323 y:74
			OperatableStateMachine.add('getOrder',
										GetOrderState(),
										transitions={'order_found': 'getAssamblyOrder', 'no_order_found': 'no_order'},
										autonomy={'order_found': Autonomy.Off, 'no_order_found': Autonomy.Off},
										remapping={'order_id': 'order_id', 'kitting_shipments': 'kitting_shipments', 'number_of_kitting_shipments': 'number_of_kitting_shipments', 'assembly_shipments': 'assembly_shipments', 'number_of_assembly_shipments': 'number_of_assembly_shipments'})

			# x:1273 y:274
			OperatableStateMachine.add('getPartFromOrder',
										GetPartFromProductsState(),
										transitions={'continue': 'setSectionParameters', 'invalid_index': 'failed'},
										autonomy={'continue': Autonomy.Off, 'invalid_index': Autonomy.Off},
										remapping={'products': 'products', 'index': 'product_index', 'type': 'part_Type', 'pose': 'assambly_Pose'})

			# x:974 y:74
			OperatableStateMachine.add('replacePartIndex',
										ReplaceState(),
										transitions={'done': 'getAssamblyOrder'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'product_index', 'result': 'zero'})

			# x:100 y:628
			OperatableStateMachine.add('setPickParameters',
										setPickParameters(),
										transitions={'continue': 'finished', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'station_id': 'station_id', 'agv_Name': 'agv_Name', 'gantry_AGV_pose': 'gantry_AGV_pose'})

			# x:1283 y:367
			OperatableStateMachine.add('setSectionParameters',
										set_GantryParameters(),
										transitions={'continue': 'findPartOnAGV1', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'station_id': 'station_id', 'home_Pose': 'home_Pose', 'table_Pose': 'table_Pose', 'section_Pose': 'section_Pose', 'gantry_move_group': 'gantry_move_group', 'gantry_action_topic_namespace': 'gantry_action_topic_namespace', 'gantry_action_topic': 'gantry_action_topic', 'robot_name': 'robot_name', 'camera_frame1': 'camera_frame1', 'camera_topic1': 'camera_topic1', 'camera_frame2': 'camera_frame2', 'camera_topic2': 'camera_topic2', 'first_agv': 'first_agv', 'sec_agv': 'sec_agv', 'case_frame': 'case_frame'})

			# x:207 y:74
			OperatableStateMachine.add('wait',
										WaitState(wait_time=0.5),
										transitions={'done': 'getOrder'},
										autonomy={'done': Autonomy.Off})

			# x:372 y:665
			OperatableStateMachine.add('addAsPoseAndCasePose',
										AddOffsetToPoseState(),
										transitions={'continue': 'setPickParameters'},
										autonomy={'continue': Autonomy.Off},
										remapping={'input_pose': 'case_Pose', 'offset_pose': 'assambly_Pose', 'output_pose': 'drop_Pose'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
