#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_states.srdf_state_to_moveit_ariac_state import SrdfStateToMoveitAriac
from ariac_support_flexbe_states.add_numeric_state import AddNumericState
from flexbe_states.wait_state import WaitState
from unit_2_flexbe_behaviors.home_ur10_sm import Home_UR10SM
from unit_2_flexbe_behaviors.move_ur10_drop_sm import Move_UR10_DropSM
from unit_2_flexbe_behaviors.move_ur10_pick_sm import Move_UR10_PickSM
from unit_2_flexbe_behaviors.setparameters_unit2_sm import setParameters_unit2SM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Wed Jun 16 2021
@author: Niels Avontuur
'''
class unit2_FINALSM(Behavior):
	'''
	Unit 2 main program
	'''


	def __init__(self):
		super(unit2_FINALSM, self).__init__()
		self.name = 'unit2_FINAL'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(Home_UR10SM, 'Home_UR10')
		self.add_behavior(Move_UR10_DropSM, 'Move_UR10_Drop')
		self.add_behavior(Move_UR10_PickSM, 'Move_UR10_Pick')
		self.add_behavior(setParameters_unit2SM, 'setParameters_unit2')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:

		# ! 161 10 
		# Made by Niels Avontuur



	def create(self):
		# x:833 y:40, x:636 y:305
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['number_of_assembly_shipments', 'assembly_shipments'])
		_state_machine.userdata.product_index = 0
		_state_machine.userdata.oneVariable = 1
		_state_machine.userdata.number_of_assembly_shipments = 0
		_state_machine.userdata.assembly_shipments = []

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:770 y:121
			OperatableStateMachine.add('setParameters_unit2',
										self.use_behavior(setParameters_unit2SM, 'setParameters_unit2'),
										transitions={'finished': 'Home_UR10', 'failed': 'failed', 'not_found': 'failed', 'assemblyCompleet': 'finished'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'not_found': Autonomy.Inherit, 'assemblyCompleet': Autonomy.Inherit},
										remapping={'product_index': 'product_index', 'assembly_shipments': 'assembly_shipments', 'number_of_assembly_shipments': 'number_of_assembly_shipments', 'gantry_AGV_Pose': 'AGV_Pose', 'gantry_move_group': 'move_group', 'gantry_action_topic_namespace': 'action_topic_namespace', 'robot_name': 'robot_name', 'home_Pose': 'home_Pose', 'table_Pose': 'table_Pose', 'gantry_action_topic': 'action_topic', 'part_Type': 'part_Type', 'section_Pose': 'section_Pose', 'drop_Pose': 'drop_Pose', 'pick_Pose': 'pick_Pose'})

			# x:420 y:471
			OperatableStateMachine.add('Move_UR10_Drop',
										self.use_behavior(Move_UR10_DropSM, 'Move_UR10_Drop'),
										transitions={'finished': 'addPart', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'part_Type': 'part_Type', 'drop_Pose': 'drop_Pose'})

			# x:920 y:471
			OperatableStateMachine.add('Move_UR10_Pick',
										self.use_behavior(Move_UR10_PickSM, 'Move_UR10_Pick'),
										transitions={'finished': 'moveToGantryAsHome_2', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'part_Type': 'part_Type', 'part_Pose': 'pick_Pose'})

			# x:174 y:474
			OperatableStateMachine.add('addPart',
										AddNumericState(),
										transitions={'done': 'moveToGantrySection_2'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'product_index', 'value_b': 'oneVariable', 'result': 'product_index'})

			# x:1134 y:424
			OperatableStateMachine.add('moveToGantryAsAGV',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'Move_UR10_Pick', 'planning_failed': 'wait_3', 'control_failed': 'wait_3', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'AGV_Pose', 'move_group': 'move_group', 'action_topic_namespace': 'action_topic_namespace', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1131 y:324
			OperatableStateMachine.add('moveToGantryAsHome',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'moveToGantryAsAGV', 'planning_failed': 'wait_2', 'control_failed': 'wait_2', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'section_Pose', 'move_group': 'move_group', 'action_topic_namespace': 'action_topic_namespace', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:676 y:474
			OperatableStateMachine.add('moveToGantryAsHome_2',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'Move_UR10_Drop', 'planning_failed': 'wait_2_2', 'control_failed': 'wait_2_2', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'table_Pose', 'move_group': 'move_group', 'action_topic_namespace': 'action_topic_namespace', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1134 y:224
			OperatableStateMachine.add('moveToGantrySection',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'moveToGantryAsHome', 'planning_failed': 'wait', 'control_failed': 'wait', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'section_Pose', 'move_group': 'move_group', 'action_topic_namespace': 'action_topic_namespace', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:178 y:374
			OperatableStateMachine.add('moveToGantrySection_2',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'setParameters_unit2', 'planning_failed': 'wait_4', 'control_failed': 'wait_4', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'section_Pose', 'move_group': 'move_group', 'action_topic_namespace': 'action_topic_namespace', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1357 y:224
			OperatableStateMachine.add('wait',
										WaitState(wait_time=0.5),
										transitions={'done': 'moveToGantrySection'},
										autonomy={'done': Autonomy.Off})

			# x:1357 y:324
			OperatableStateMachine.add('wait_2',
										WaitState(wait_time=0.5),
										transitions={'done': 'moveToGantryAsHome'},
										autonomy={'done': Autonomy.Off})

			# x:707 y:574
			OperatableStateMachine.add('wait_2_2',
										WaitState(wait_time=0.5),
										transitions={'done': 'moveToGantryAsHome_2'},
										autonomy={'done': Autonomy.Off})

			# x:1357 y:424
			OperatableStateMachine.add('wait_3',
										WaitState(wait_time=0.5),
										transitions={'done': 'moveToGantryAsAGV'},
										autonomy={'done': Autonomy.Off})

			# x:207 y:274
			OperatableStateMachine.add('wait_4',
										WaitState(wait_time=0.5),
										transitions={'done': 'moveToGantrySection_2'},
										autonomy={'done': Autonomy.Off})

			# x:1120 y:121
			OperatableStateMachine.add('Home_UR10',
										self.use_behavior(Home_UR10SM, 'Home_UR10'),
										transitions={'finished': 'moveToGantrySection', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
