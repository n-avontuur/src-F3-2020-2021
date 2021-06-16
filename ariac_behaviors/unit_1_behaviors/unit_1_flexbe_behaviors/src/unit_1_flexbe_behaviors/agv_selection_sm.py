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
from ariac_support_flexbe_states.equal_state import EqualState
from ariac_support_flexbe_states.replace_state import ReplaceState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon Jun 14 2021
@author: kemal buke
'''
class agvselectionSM(Behavior):
	'''
	takes the agv id given by the order and defines the tray predrop for the rest of the program
	'''


	def __init__(self):
		super(agvselectionSM, self).__init__()
		self.name = 'agv selection'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:1110 y:139, x:210 y:483
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['agv_id'], output_keys=['traypredrop', 'tray'])
		_state_machine.userdata.agv1 = 'agv1'
		_state_machine.userdata.agv2 = 'agv2'
		_state_machine.userdata.agv3 = 'agv3'
		_state_machine.userdata.agv4 = 'agv4'
		_state_machine.userdata.agv_id = 'agv2'
		_state_machine.userdata.agv2_drop = 'kitting_agv_2'
		_state_machine.userdata.agv3_drop = 'kitting_agv_2'
		_state_machine.userdata.agv4_drop = 'kitting_agv_2'
		_state_machine.userdata.agv1_drop = 'kitting_agv_1'
		_state_machine.userdata.traypredrop = ''
		_state_machine.userdata.agv2_tray = 'kit_tray_2'
		_state_machine.userdata.agv3_tray = 'kit_tray_3'
		_state_machine.userdata.agv4_tray = 'kit_tray_4'
		_state_machine.userdata.agv1_tray = 'kit_tray_1'
		_state_machine.userdata.tray = ''

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:161 y:32
			OperatableStateMachine.add('equals agv1',
										EqualState(),
										transitions={'true': 'over write tray predrop', 'false': 'equals agv1_2'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'agv1', 'value_b': 'agv_id'})

			# x:161 y:124
			OperatableStateMachine.add('equals agv1_2',
										EqualState(),
										transitions={'true': 'over write tray predrop_2', 'false': 'equals agv1_3'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'agv2', 'value_b': 'agv_id'})

			# x:161 y:216
			OperatableStateMachine.add('equals agv1_3',
										EqualState(),
										transitions={'true': 'over write tray predrop_3', 'false': 'equals agv1_4'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'agv3', 'value_b': 'agv_id'})

			# x:161 y:308
			OperatableStateMachine.add('equals agv1_4',
										EqualState(),
										transitions={'true': 'over write tray predrop_4', 'false': 'message'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'agv4', 'value_b': 'agv_id'})

			# x:159 y:370
			OperatableStateMachine.add('message',
										MessageState(),
										transitions={'continue': 'failed'},
										autonomy={'continue': Autonomy.Off},
										remapping={'message': 'agv_id'})

			# x:727 y:42
			OperatableStateMachine.add('over write tray frame',
										ReplaceState(),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'agv1_tray', 'result': 'tray'})

			# x:726 y:108
			OperatableStateMachine.add('over write tray frame_2',
										ReplaceState(),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'agv2_tray', 'result': 'tray'})

			# x:723 y:180
			OperatableStateMachine.add('over write tray frame_3',
										ReplaceState(),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'agv3_tray', 'result': 'tray'})

			# x:723 y:265
			OperatableStateMachine.add('over write tray frame_4',
										ReplaceState(),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'agv4_tray', 'result': 'tray'})

			# x:409 y:35
			OperatableStateMachine.add('over write tray predrop',
										ReplaceState(),
										transitions={'done': 'over write tray frame'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'agv1_drop', 'result': 'traypredrop'})

			# x:409 y:112
			OperatableStateMachine.add('over write tray predrop_2',
										ReplaceState(),
										transitions={'done': 'over write tray frame_2'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'agv2_drop', 'result': 'traypredrop'})

			# x:409 y:189
			OperatableStateMachine.add('over write tray predrop_3',
										ReplaceState(),
										transitions={'done': 'over write tray frame_3'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'agv3_drop', 'result': 'traypredrop'})

			# x:409 y:266
			OperatableStateMachine.add('over write tray predrop_4',
										ReplaceState(),
										transitions={'done': 'over write tray frame_4'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'agv4_drop', 'result': 'traypredrop'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
