#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_states.start_assignment_state import StartAssignment
from ariac_logistics_flexbe_states.get_assembly_shipment_from_order_state import GetAssemblyShipmentFromOrderState
from ariac_logistics_flexbe_states.get_order_state import GetOrderState
from unit_2_flexbe_behaviors.move_gantry_unit2_sm import move_Gantry_unit2SM
from unit_2_flexbe_behaviors.move_ur10_unit2_sm import Move_UR10_unit2SM
from unit_2_flexbe_behaviors.setparameters_unit2_sm import setParameters_unit2SM
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
		self.add_behavior(Move_UR10_unit2SM, 'Move_UR10_unit2')
		self.add_behavior(move_Gantry_unit2SM, 'move_Gantry_unit2')
		self.add_behavior(setParameters_unit2SM, 'setParameters_unit2')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:1639 y:721, x:737 y:306, x:230 y:415
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed', 'no_Order'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:45 y:36
			OperatableStateMachine.add('startAsignment',
										StartAssignment(),
										transitions={'continue': 'getOrderInfo'},
										autonomy={'continue': Autonomy.Off})

			# x:1541 y:612
			OperatableStateMachine.add('Move_UR10_unit2',
										self.use_behavior(Move_UR10_unit2SM, 'Move_UR10_unit2'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:200 y:38
			OperatableStateMachine.add('getOrderInfo',
										GetOrderState(),
										transitions={'order_found': 'GetAssamblyOrderInfo', 'no_order_found': 'no_Order'},
										autonomy={'order_found': Autonomy.Off, 'no_order_found': Autonomy.Off},
										remapping={'order_id': 'order_id', 'kitting_shipments': 'kitting_shipments', 'number_of_kitting_shipments': 'number_of_kitting_shipments', 'assembly_shipments': 'assembly_shipments', 'number_of_assembly_shipments': 'number_of_assembly_shipments'})

			# x:1538 y:529
			OperatableStateMachine.add('move_Gantry_unit2',
										self.use_behavior(move_Gantry_unit2SM, 'move_Gantry_unit2'),
										transitions={'finished': 'Move_UR10_unit2', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:797 y:41
			OperatableStateMachine.add('setParameters_unit2',
										self.use_behavior(setParameters_unit2SM, 'setParameters_unit2'),
										transitions={'finished': 'move_Gantry_unit2', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:461 y:38
			OperatableStateMachine.add('GetAssamblyOrderInfo',
										GetAssemblyShipmentFromOrderState(),
										transitions={'continue': 'setParameters_unit2', 'invalid_index': 'failed'},
										autonomy={'continue': Autonomy.Off, 'invalid_index': Autonomy.Off},
										remapping={'assembly_shipments': 'assembly_shipments', 'assembly_index': 'number_of_assembly_shipments', 'shipment_type': 'part_Type', 'products': 'products', 'shipment_type': 'shipment_type', 'station_id': 'station_id', 'number_of_products': 'number_of_products'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
