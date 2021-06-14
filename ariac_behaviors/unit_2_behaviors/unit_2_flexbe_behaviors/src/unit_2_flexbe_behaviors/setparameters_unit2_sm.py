#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_states.dummy_state import DummyState
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
		# x:1011 y:55, x:130 y:415
		joint_names = ['linear_arm_actuator_joint', 'shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=[])
		_state_machine.userdata.assembly_shipments = ''
		_state_machine.userdata.assembly_index = ''
		
		
		_state_machine.userdata.offset = 0.0
		_state_machine.userdata.rotation = 180
		_state_machine.userdata.pick_Offset = []
		_state_machine.userdata.pick_Rotation = []
		_state_machine.userdata.trueVariable = True
		_state_machine.userdata.falseVariable = False
		_state_machine.userdata.robot_Name = ''
		_state_machine.userdata.preDrop_Config = ''
		_state_machine.userdata.prePick_Config = ''
		_state_machine.userdata.bin_Pose = []
		_state_machine.userdata.drop_Offset = []
		_state_machine.userdata.drop_Rotation = []
		_state_machine.userdata.pick_Pose = []
		_state_machine.userdata.home_Config = ''

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:30 y:40
			OperatableStateMachine.add('dummy',
										DummyState(),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
