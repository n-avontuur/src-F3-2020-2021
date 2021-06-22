#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_states.check_Gripper import checkGripper
from ariac_flexbe_states.get_gripper_status_state2 import GetGripperStatusState2
from ariac_support_flexbe_states.equal_state import EqualState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Tue Jun 22 2021
@author: Niels Avontuur
'''
class CheckGipperSM(Behavior):
	'''
	Checking if gripper has part
	'''


	def __init__(self):
		super(CheckGipperSM, self).__init__()
		self.name = 'CheckGipper'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:558 y:287, x:216 y:215, x:911 y:132
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed', 'decrees'], input_keys=['attachedWanted'])
		_state_machine.userdata.attempts = 0
		_state_machine.userdata.attachedWanted = False

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:143 y:54
			OperatableStateMachine.add('checkGripperState',
										GetGripperStatusState2(),
										transitions={'continue': 'isPartAttached', 'fail': 'failed'},
										autonomy={'continue': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'enabled': 'enabled', 'attached': 'attached'})

			# x:400 y:103
			OperatableStateMachine.add('isPartAttached',
										EqualState(),
										transitions={'true': 'finished', 'false': 'checkGripper'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'attached', 'value_b': 'attachedWanted'})

			# x:656 y:47
			OperatableStateMachine.add('checkGripper',
										checkGripper(),
										transitions={'continue': 'checkGripperState', 'failed': 'decrees'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'attempts': 'attempts'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
