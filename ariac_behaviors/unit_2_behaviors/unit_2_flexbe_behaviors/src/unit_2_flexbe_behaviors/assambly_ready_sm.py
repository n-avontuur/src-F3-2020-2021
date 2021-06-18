#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_states.notify_assembly_ready_state import NotifyAssemblyReadyState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu Jun 17 2021
@author: Niels Avontuur
'''
class assambly_readySM(Behavior):
	'''
	Behavoir for ready assambly
	'''


	def __init__(self):
		super(assambly_readySM, self).__init__()
		self.name = 'assambly_ready'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:

		# ! 67 29 
		# Made by Niels Avontuur



	def create(self):
		# x:742 y:122, x:524 y:413
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['station_id', 'shipment_type', 'assembly_index'], output_keys=['success', 'inspection_result', 'assembly_index'])
		_state_machine.userdata.station_id = ''
		_state_machine.userdata.shipment_type = ''
		_state_machine.userdata.success = 0
		_state_machine.userdata.inspection_result = 0
		_state_machine.userdata.assembly_index = 0
		_state_machine.userdata.zero = 0

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:169 y:127
			OperatableStateMachine.add('notifyAssamblyReady',
										NotifyAssemblyReadyState(),
										transitions={'continue': 'finished', 'fail': 'failed'},
										autonomy={'continue': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'as_id': 'station_id', 'shipment_type': 'shipment_type', 'success': 'success', 'inspection_result': 'inspection_result'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
