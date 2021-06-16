#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_example_behaviors.notify_shipment_ready_sm import notify_shipment_readySM
from ariac_flexbe_states.start_assignment_state import StartAssignment
from ariac_logistics_flexbe_states.get_order_state import GetOrderState
from ariac_logistics_flexbe_states.get_part_from_products_state import GetPartFromProductsState
from ariac_logistics_flexbe_states.get_products_from_shipment_state import GetProductsFromShipmentState
from ariac_support_flexbe_states.add_numeric_state import AddNumericState
from ariac_support_flexbe_states.equal_state import EqualState
from ariac_support_flexbe_states.replace_state import ReplaceState
from flexbe_states.wait_state import WaitState
from unit_1_flexbe_behaviors.pick_part_from_bin_sm import pick_part_from_binSM
from unit_1_flexbe_behaviors.place_part_on_agv_sm import place_part_on_agvSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Tue Jun 01 2021
@author: Jesse
'''
class TransportBinToAgvSM(Behavior):
	'''
	onderdelen overplaatsen van bin naar agv
	'''


	def __init__(self):
		super(TransportBinToAgvSM, self).__init__()
		self.name = 'TransportBinToAgv'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(notify_shipment_readySM, 'notify_shipment_ready')
		self.add_behavior(pick_part_from_binSM, 'pick_part_from_bin')
		self.add_behavior(place_part_on_agvSM, 'place_part_on_agv')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:949 y:757, x:827 y:92
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.order_id = ''
		_state_machine.userdata.number_of_shipments = ''
		_state_machine.userdata.shipments = []
		_state_machine.userdata.agv_id = ''
		_state_machine.userdata.shipment_index = 1
		_state_machine.userdata.shipment_type = ''
		_state_machine.userdata.ShipmentIterator = 0
		_state_machine.userdata.OneValue = 1
		_state_machine.userdata.ProductIterator = 0
		_state_machine.userdata.ProductType = ''
		_state_machine.userdata.ProductPose = []
		_state_machine.userdata.products = []
		_state_machine.userdata.number_of_products = ''
		_state_machine.userdata.part_pose = ''
		_state_machine.userdata.agv2 = 'agv2'
		_state_machine.userdata.action_topic_namespace_R2 = '/ariac/arm2'
		_state_machine.userdata.action_topic_namespace_unused = ''
		_state_machine.userdata.action_topic_namespace_R1 = '/ariac/arm1'
		_state_machine.userdata.action_topic_namespace = ''
		_state_machine.userdata.homeR2 = 'homeR2'
		_state_machine.userdata.homeR1 = 'homeR1'
		_state_machine.userdata.home = ''
		_state_machine.userdata.gripper_service_r1 = '/ariac/arm1/gripper/control'
		_state_machine.userdata.gripper_service_r2 = '/ariac/arm2/gripper/control'
		_state_machine.userdata.gripper_service = ''
		_state_machine.userdata.gripper_status_topic_r1 = '/ariac/arm1/gripper/state'
		_state_machine.userdata.gripper_status_topic_r2 = '/ariac/arm2/gripper/state'
		_state_machine.userdata.gripper_status_topic = ''
		_state_machine.userdata.traypredrop = ''
		_state_machine.userdata.tray = ''
		_state_machine.userdata.traypredrop_r1 = 'tray1PreDrop'
		_state_machine.userdata.traypredrop_r2 = 'tray2PreDrop'
		_state_machine.userdata.tray_r1 = 'kit_tray_1'
		_state_machine.userdata.tray_r2 = 'kit_tray_2'
		_state_machine.userdata.zero = 0

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:70 y:57
			OperatableStateMachine.add('StartAssignment',
										StartAssignment(),
										transitions={'continue': 'GetOrder'},
										autonomy={'continue': Autonomy.Off})

			# x:1083 y:661
			OperatableStateMachine.add('CompareShepmentsIterator',
										EqualState(),
										transitions={'true': 'wait', 'false': 'GetProducts'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'ShipmentIterator', 'value_b': 'number_of_shipments'})

			# x:202 y:53
			OperatableStateMachine.add('GetOrder',
										GetOrderState(),
										transitions={'continue': 'reset shipment iterator'},
										autonomy={'continue': Autonomy.Off},
										remapping={'order_id': 'order_id', 'shipments': 'shipments', 'number_of_shipments': 'number_of_shipments'})

			# x:1088 y:72
			OperatableStateMachine.add('GetPart',
										GetPartFromProductsState(),
										transitions={'continue': 'pick_part_from_bin', 'invalid_index': 'failed'},
										autonomy={'continue': Autonomy.Off, 'invalid_index': Autonomy.Off},
										remapping={'products': 'products', 'index': 'ProductIterator', 'type': 'ProductType', 'pose': 'ProductPose'})

			# x:552 y:55
			OperatableStateMachine.add('GetProducts',
										GetProductsFromShipmentState(),
										transitions={'continue': 'robot selection', 'invalid_index': 'failed'},
										autonomy={'continue': Autonomy.Off, 'invalid_index': Autonomy.Off},
										remapping={'shipments': 'shipments', 'index': 'ShipmentIterator', 'shipment_type': 'shipment_type', 'agv_id': 'agv_id', 'products': 'products', 'number_of_products': 'number_of_products'})

			# x:1094 y:344
			OperatableStateMachine.add('IncrementProductIterator',
										AddNumericState(),
										transitions={'done': 'CompareProductIterator'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'ProductIterator', 'value_b': 'OneValue', 'result': 'ProductIterator'})

			# x:1094 y:571
			OperatableStateMachine.add('IncrementShipmentsIterator',
										AddNumericState(),
										transitions={'done': 'CompareShepmentsIterator'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'ShipmentIterator', 'value_b': 'OneValue', 'result': 'ShipmentIterator'})

			# x:482 y:252
			OperatableStateMachine.add('define predrop 1',
										ReplaceState(),
										transitions={'done': 'set robot 1'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'traypredrop_r1', 'result': 'traypredrop'})

			# x:695 y:256
			OperatableStateMachine.add('define predrop 2',
										ReplaceState(),
										transitions={'done': 'set robot 2'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'traypredrop_r2', 'result': 'traypredrop'})

			# x:485 y:526
			OperatableStateMachine.add('gripper service set',
										ReplaceState(),
										transitions={'done': 'gripper topic'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'gripper_service_r1', 'result': 'gripper_service'})

			# x:701 y:542
			OperatableStateMachine.add('gripper service set_2',
										ReplaceState(),
										transitions={'done': 'gripper topic_2'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'gripper_service_r2', 'result': 'gripper_service'})

			# x:481 y:604
			OperatableStateMachine.add('gripper topic',
										ReplaceState(),
										transitions={'done': 'tray frame 1'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'gripper_status_topic_r1', 'result': 'gripper_status_topic'})

			# x:703 y:609
			OperatableStateMachine.add('gripper topic_2',
										ReplaceState(),
										transitions={'done': 'gripper topic_4'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'gripper_status_topic_r2', 'result': 'gripper_status_topic'})

			# x:708 y:672
			OperatableStateMachine.add('gripper topic_4',
										ReplaceState(),
										transitions={'done': 'GetPart'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'tray_r2', 'result': 'tray'})

			# x:1067 y:461
			OperatableStateMachine.add('notify_shipment_ready',
										self.use_behavior(notify_shipment_readySM, 'notify_shipment_ready'),
										transitions={'finished': 'IncrementShipmentsIterator', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:1082 y:164
			OperatableStateMachine.add('pick_part_from_bin',
										self.use_behavior(pick_part_from_binSM, 'pick_part_from_bin'),
										transitions={'finished': 'place_part_on_agv', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'part': 'ProductType', 'gripper_status_topic': 'gripper_status_topic', 'gripper_service': 'gripper_service', 'action_topic_namespace': 'action_topic_namespace', 'home': 'home'})

			# x:1088 y:250
			OperatableStateMachine.add('place_part_on_agv',
										self.use_behavior(place_part_on_agvSM, 'place_part_on_agv'),
										transitions={'finished': 'IncrementProductIterator', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'ProductType': 'ProductType', 'ProductIterator': 'ProductIterator', 'action_topic_namespace': 'action_topic_namespace', 'traypredrop': 'traypredrop', 'gripper_status_topic': 'gripper_status_topic', 'gripper_service': 'gripper_service', 'tray': 'tray'})

			# x:1314 y:460
			OperatableStateMachine.add('reset product iterator_2',
										ReplaceState(),
										transitions={'done': 'notify_shipment_ready'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'zero', 'result': 'ProductIterator'})

			# x:374 y:48
			OperatableStateMachine.add('reset shipment iterator',
										ReplaceState(),
										transitions={'done': 'GetProducts'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'zero', 'result': 'ShipmentIterator'})

			# x:555 y:135
			OperatableStateMachine.add('robot selection',
										EqualState(),
										transitions={'true': 'define predrop 2', 'false': 'define predrop 1'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'agv_id', 'value_b': 'agv2'})

			# x:483 y:322
			OperatableStateMachine.add('set robot 1',
										ReplaceState(),
										transitions={'done': 'set robot home 2'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'action_topic_namespace_R1', 'result': 'action_topic_namespace'})

			# x:694 y:322
			OperatableStateMachine.add('set robot 2',
										ReplaceState(),
										transitions={'done': 'set robot home 1'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'action_topic_namespace_R2', 'result': 'action_topic_namespace'})

			# x:699 y:387
			OperatableStateMachine.add('set robot home 1',
										ReplaceState(),
										transitions={'done': 'gripper service set_2'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'homeR2', 'result': 'home'})

			# x:484 y:389
			OperatableStateMachine.add('set robot home 2',
										ReplaceState(),
										transitions={'done': 'gripper service set'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'homeR1', 'result': 'home'})

			# x:481 y:666
			OperatableStateMachine.add('tray frame 1',
										ReplaceState(),
										transitions={'done': 'GetPart'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'tray_r1', 'result': 'tray'})

			# x:232 y:153
			OperatableStateMachine.add('wait',
										WaitState(wait_time=5),
										transitions={'done': 'GetOrder'},
										autonomy={'done': Autonomy.Off})

			# x:1337 y:337
			OperatableStateMachine.add('CompareProductIterator',
										EqualState(),
										transitions={'true': 'reset product iterator_2', 'false': 'GetPart'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'ProductIterator', 'value_b': 'number_of_products'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
