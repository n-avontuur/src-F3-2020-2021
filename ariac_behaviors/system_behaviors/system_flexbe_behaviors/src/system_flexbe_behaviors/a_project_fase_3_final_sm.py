#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_states.end_assignment_state import EndAssignment
from ariac_flexbe_states.start_assignment_state import StartAssignment
from ariac_logistics_flexbe_states.get_order_state import GetOrderState
from ariac_support_flexbe_states.replace_state import ReplaceState
from flexbe_states.wait_state import WaitState
from unit_1_flexbe_behaviors.unit_1_finale_sm import unit_1_FINALESM
from unit_2_flexbe_behaviors.unit2_final_sm import unit2_FINALSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Fri Jun 18 2021
@author: Niels Avontuur
'''
class AProject_Fase_3_FinalSM(Behavior):
	'''
	This is the total program for fase 3 project
	'''


	def __init__(self):
		super(AProject_Fase_3_FinalSM, self).__init__()
		self.name = 'A.Project_Fase_3_Final'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(unit2_FINALSM, 'unit2_FINAL')
		self.add_behavior(unit_1_FINALESM, 'unit_1_FINALE')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:1246 y:714, x:640 y:319
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.kitting_index = 0
		_state_machine.userdata.zero = 0
		_state_machine.userdata.ProductIterator = 0
		_state_machine.userdata.product_index = 0

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:143 y:74
			OperatableStateMachine.add('startAssignment',
										StartAssignment(),
										transitions={'continue': 'getOrder'},
										autonomy={'continue': Autonomy.Off})

			# x:323 y:74
			OperatableStateMachine.add('getOrder',
										GetOrderState(),
										transitions={'order_found': 'resetAssemblyIndex', 'no_order_found': 'failed'},
										autonomy={'order_found': Autonomy.Off, 'no_order_found': Autonomy.Off},
										remapping={'order_id': 'order_id', 'kitting_shipments': 'kitting_shipments', 'number_of_kitting_shipments': 'number_of_kitting_shipments', 'assembly_shipments': 'assembly_shipments', 'number_of_assembly_shipments': 'number_of_assembly_shipments'})

			# x:527 y:75
			OperatableStateMachine.add('resetAssemblyIndex',
										ReplaceState(),
										transitions={'done': 'resetKittingIndex'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'zero', 'result': 'assembly_index'})

			# x:726 y:71
			OperatableStateMachine.add('resetKittingIndex',
										ReplaceState(),
										transitions={'done': 'unit_1_FINALE'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'zero', 'result': 'kitting_index'})

			# x:1171 y:490
			OperatableStateMachine.add('unit2_FINAL',
										self.use_behavior(unit2_FINALSM, 'unit2_FINAL'),
										transitions={'finished': 'endAssignment', 'failed': 'failed', 'part_assembly': 'wait'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'part_assembly': Autonomy.Inherit},
										remapping={'number_of_assembly_shipments': 'number_of_assembly_shipments', 'assembly_shipments': 'assembly_shipments', 'product_index': 'product_index'})

			# x:1186 y:314
			OperatableStateMachine.add('unit_1_FINALE',
										self.use_behavior(unit_1_FINALESM, 'unit_1_FINALE'),
										transitions={'finished': 'unit2_FINAL', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'number_of_kitting_shipments': 'number_of_kitting_shipments', 'kitting_shipments': 'kitting_shipments', 'kitting_index': 'kitting_index', 'ProductIterator': 'ProductIterator'})

			# x:984 y:381
			OperatableStateMachine.add('wait',
										WaitState(wait_time=0.5),
										transitions={'done': 'unit_1_FINALE'},
										autonomy={'done': Autonomy.Off})

			# x:1428 y:390
			OperatableStateMachine.add('wait_2',
										WaitState(wait_time=0.5),
										transitions={'done': 'unit2_FINAL'},
										autonomy={'done': Autonomy.Off})

			# x:1192 y:625
			OperatableStateMachine.add('endAssignment',
										EndAssignment(),
										transitions={'continue': 'finished'},
										autonomy={'continue': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
