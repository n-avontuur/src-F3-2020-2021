#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_states.message_state import MessageState
from ariac_flexbe_states.start_assignment_state import StartAssignment
from ariac_logistics_flexbe_states.get_kitting_shipment_from_order_state import GetKittingShipmentFromOrderState
from ariac_logistics_flexbe_states.get_order_state import GetOrderState
from ariac_logistics_flexbe_states.get_part_from_products_state import GetPartFromProductsState
from ariac_support_flexbe_states.add_numeric_state import AddNumericState
from ariac_support_flexbe_states.equal_state import EqualState
from ariac_support_flexbe_states.replace_state import ReplaceState
from flexbe_states.wait_state import WaitState
from unit_1_flexbe_behaviors.agv_selection_sm import agvselectionSM
from unit_1_flexbe_behaviors.notify_shipment_ready_sm import notify_shipment_readySM
from unit_1_flexbe_behaviors.pick_part_from_bin_sm import pick_part_from_binSM
from unit_1_flexbe_behaviors.place_part_on_agv_sm import place_part_on_agvSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sun Jun 13 2021
@author: kemal buke
'''
class unit_1_testSM(Behavior):
	'''
	test bench unit 1 fase 3
	'''


	def __init__(self):
		super(unit_1_testSM, self).__init__()
		self.name = 'unit_1_test'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(agvselectionSM, 'agv selection')
		self.add_behavior(notify_shipment_readySM, 'notify_shipment_ready')
		self.add_behavior(pick_part_from_binSM, 'pick_part_from_bin')
		self.add_behavior(place_part_on_agvSM, 'place_part_on_agv')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		gripper_status_topic = '/ariac/kitting/arm/gripper/state'
		gripper_service = '/ariac/kitting/arm/gripper/control'
		# x:1167 y:751, x:691 y:318
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.order_id = ''
		_state_machine.userdata.shipments = []
		_state_machine.userdata.number_of_shipments = 0
		_state_machine.userdata.zero = 0
		_state_machine.userdata.ShipmentIterator = 0
		_state_machine.userdata.shipment_type = []
		_state_machine.userdata.agv_id = ''
		_state_machine.userdata.products = []
		_state_machine.userdata.number_of_products = 0
		_state_machine.userdata.OneValue = 1
		_state_machine.userdata.ProductIterator = 0
		_state_machine.userdata.ProductType = ''
		_state_machine.userdata.ProductPose = []
		_state_machine.userdata.action_topic_namespace = '/ariac/kitting'
		_state_machine.userdata.home = 'kitting_home'
		_state_machine.userdata.traypredrop = ''
		_state_machine.userdata.tray = ''
		_state_machine.userdata.kitting_shipments = []
		_state_machine.userdata.kitting_index = 0
		_state_machine.userdata.move_group = 'kitting_arm'
		_state_machine.userdata.action_topic = '/move_group'
		_state_machine.userdata.station_id = ''
		_state_machine.userdata.assembly_station_name = ''
		_state_machine.userdata.ProductPose = []

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:70 y:57
			OperatableStateMachine.add('StartAssignment',
										StartAssignment(),
										transitions={'continue': 'GetOrder'},
										autonomy={'continue': Autonomy.Off})

			# x:1337 y:337
			OperatableStateMachine.add('CompareProductIterator',
										EqualState(),
										transitions={'true': 'reset product iterator_2', 'false': 'GetPart'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'ProductIterator', 'value_b': 'number_of_products'})

			# x:202 y:53
			OperatableStateMachine.add('GetOrder',
										GetOrderState(),
										transitions={'order_found': 'reset kitting shipment iterator', 'no_order_found': 'wait_2'},
										autonomy={'order_found': Autonomy.Off, 'no_order_found': Autonomy.Off},
										remapping={'order_id': 'order_id', 'kitting_shipments': 'kitting_shipments', 'number_of_kitting_shipments': 'number_of_kitting_shipments', 'assembly_shipments': 'assembly_shipments', 'number_of_assembly_shipments': 'number_of_assembly_shipments'})

			# x:1088 y:72
			OperatableStateMachine.add('GetPart',
										GetPartFromProductsState(),
										transitions={'continue': 'message', 'invalid_index': 'failed'},
										autonomy={'continue': Autonomy.Off, 'invalid_index': Autonomy.Off},
										remapping={'products': 'products', 'index': 'ProductIterator', 'type': 'ProductType', 'pose': 'ProductPose'})

			# x:1088 y:557
			OperatableStateMachine.add('Increment kitting index',
										AddNumericState(),
										transitions={'done': 'Compare kitting index'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'kitting_index', 'value_b': 'OneValue', 'result': 'kitting_index'})

			# x:1094 y:344
			OperatableStateMachine.add('IncrementProductIterator',
										AddNumericState(),
										transitions={'done': 'CompareProductIterator'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'ProductIterator', 'value_b': 'OneValue', 'result': 'ProductIterator'})

			# x:824 y:62
			OperatableStateMachine.add('agv selection',
										self.use_behavior(agvselectionSM, 'agv selection'),
										transitions={'finished': 'GetPart', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'agv_id': 'agv_id', 'traypredrop': 'traypredrop', 'tray': 'tray'})

			# x:573 y:55
			OperatableStateMachine.add('get kittingshipment',
										GetKittingShipmentFromOrderState(),
										transitions={'continue': 'agv selection', 'invalid_index': 'failed'},
										autonomy={'continue': Autonomy.Off, 'invalid_index': Autonomy.Off},
										remapping={'kitting_shipments': 'kitting_shipments', 'kitting_index': 'kitting_index', 'shipment_type': 'shipment_type', 'products': 'products', 'agv_id': 'agv_id', 'station_id': 'station_id', 'number_of_products': 'number_of_products'})

			# x:1317 y:99
			OperatableStateMachine.add('message',
										MessageState(),
										transitions={'continue': 'pick_part_from_bin'},
										autonomy={'continue': Autonomy.Off},
										remapping={'message': 'ProductPose'})

			# x:1077 y:428
			OperatableStateMachine.add('notify_shipment_ready',
										self.use_behavior(notify_shipment_readySM, 'notify_shipment_ready'),
										transitions={'finished': 'Increment kitting index', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'agv_id': 'agv_id', 'station_id': 'station_id', 'shipment_type': 'shipment_type', 'assembly_station_name': 'assembly_station_name'})

			# x:1082 y:164
			OperatableStateMachine.add('pick_part_from_bin',
										self.use_behavior(pick_part_from_binSM, 'pick_part_from_bin'),
										transitions={'finished': 'place_part_on_agv', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'part': 'ProductType', 'action_topic_namespace': 'action_topic_namespace', 'home': 'home', 'move_group': 'move_group'})

			# x:1088 y:250
			OperatableStateMachine.add('place_part_on_agv',
										self.use_behavior(place_part_on_agvSM, 'place_part_on_agv'),
										transitions={'finished': 'IncrementProductIterator', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'ProductType': 'ProductType', 'ProductIterator': 'ProductIterator', 'action_topic_namespace': 'action_topic_namespace', 'traypredrop': 'traypredrop', 'tray': 'tray', 'move_group': 'move_group', 'ProductPose': 'ProductPose'})

			# x:390 y:54
			OperatableStateMachine.add('reset kitting shipment iterator',
										ReplaceState(),
										transitions={'done': 'get kittingshipment'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'zero', 'result': 'kitting_index'})

			# x:1341 y:428
			OperatableStateMachine.add('reset product iterator_2',
										ReplaceState(),
										transitions={'done': 'notify_shipment_ready'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'zero', 'result': 'ProductIterator'})

			# x:225 y:152
			OperatableStateMachine.add('wait_2',
										WaitState(wait_time=5),
										transitions={'done': 'GetOrder'},
										autonomy={'done': Autonomy.Off})

			# x:1083 y:661
			OperatableStateMachine.add('Compare kitting index',
										EqualState(),
										transitions={'true': 'finished', 'false': 'get kittingshipment'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'number_of_kitting_shipments', 'value_b': 'kitting_index'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
