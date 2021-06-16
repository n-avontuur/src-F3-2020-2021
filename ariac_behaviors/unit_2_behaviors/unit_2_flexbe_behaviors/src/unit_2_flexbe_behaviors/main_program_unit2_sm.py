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
from ariac_flexbe_states.start_assignment_state import StartAssignment
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
		self.add_behavior(Home_UR10SM, 'Home_UR10')
		self.add_behavior(Move_UR10_DropSM, 'Move_UR10_Drop')
		self.add_behavior(Move_UR10_PickSM, 'Move_UR10_Pick')
		self.add_behavior(setParameters_unit2SM, 'setParameters_unit2')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:

		# ! 1635 20 
		# Made by Niels Avontuur



	def create(self):
		# x:33 y:440, x:745 y:434, x:683 y:190, x:883 y:190
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed', 'no_Order', 'assambly_Compleet'])
		_state_machine.userdata.zero = 0
		_state_machine.userdata.part_Number = 0
		_state_machine.userdata.ref_frame = 'world'
		_state_machine.userdata.product_index = 0
		_state_machine.userdata.one = 1

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:30 y:40
			OperatableStateMachine.add('startAssignment',
										StartAssignment(),
										transitions={'continue': 'Home_UR10'},
										autonomy={'continue': Autonomy.Off})

			# x:470 y:571
			OperatableStateMachine.add('Move_UR10_Drop',
										self.use_behavior(Move_UR10_DropSM, 'Move_UR10_Drop'),
										transitions={'finished': 'addPart', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'part_Type': 'part_Type', 'drop_Pose': 'drop_Pose'})

			# x:1120 y:571
			OperatableStateMachine.add('Move_UR10_Pick',
										self.use_behavior(Move_UR10_PickSM, 'Move_UR10_Pick'),
										transitions={'finished': 'moveGantryHome_2', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'part_Type': 'part_Type', 'pick_Pose': 'pick_Pose'})

			# x:124 y:574
			OperatableStateMachine.add('addPart',
										AddNumericState(),
										transitions={'done': 'moveGantrySection_2'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'product_index', 'value_b': 'one', 'result': 'product_index'})

			# x:1334 y:574
			OperatableStateMachine.add('moveGantryAGV',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'Move_UR10_Pick', 'planning_failed': 'wait_4', 'control_failed': 'wait_4', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'gantry_AGV_Pose', 'move_group': 'gantry_move_group', 'action_topic_namespace': 'gantry_action_topic_namespace', 'action_topic': 'gantry_action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1334 y:274
			OperatableStateMachine.add('moveGantryHome',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'moveGantryAGV', 'planning_failed': 'wait_2', 'control_failed': 'wait_2', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'home_Pose', 'move_group': 'gantry_move_group', 'action_topic_namespace': 'gantry_action_topic_namespace', 'action_topic': 'gantry_action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:934 y:574
			OperatableStateMachine.add('moveGantryHome_2',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'moveGantryTable_2', 'planning_failed': 'wait_3', 'control_failed': 'wait_3', 'param_error': 'Move_UR10_Pick'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'home_Pose', 'move_group': 'gantry_move_group', 'action_topic_namespace': 'gantry_action_topic_namespace', 'action_topic': 'gantry_action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1334 y:74
			OperatableStateMachine.add('moveGantrySection',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'moveGantryHome', 'planning_failed': 'wait', 'control_failed': 'wait', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'section_Pose', 'move_group': 'gantry_move_group', 'action_topic_namespace': 'gantry_action_topic_namespace', 'action_topic': 'gantry_action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:133 y:424
			OperatableStateMachine.add('moveGantrySection_2',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'finished', 'planning_failed': 'wait_5', 'control_failed': 'wait_5', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'section_Pose', 'move_group': 'gantry_move_group', 'action_topic_namespace': 'gantry_action_topic_namespace', 'action_topic': 'gantry_action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:734 y:574
			OperatableStateMachine.add('moveGantryTable_2',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'Move_UR10_Drop', 'planning_failed': 'wait_3_2', 'control_failed': 'wait_3_2', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'table_Pose', 'move_group': 'gantry_move_group', 'action_topic_namespace': 'gantry_action_topic_namespace', 'action_topic': 'gantry_action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:720 y:71
			OperatableStateMachine.add('setParameters_unit2',
										self.use_behavior(setParameters_unit2SM, 'setParameters_unit2'),
										transitions={'finished': 'moveGantrySection', 'failed': 'failed', 'not_found': 'failed', 'no_order': 'no_Order', 'assemblyCompleet': 'assambly_Compleet'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'not_found': Autonomy.Inherit, 'no_order': Autonomy.Inherit, 'assemblyCompleet': Autonomy.Inherit},
										remapping={'product_index': 'product_index', 'gantry_AGV_Pose': 'gantry_AGV_Pose', 'gantry_move_group': 'gantry_move_group', 'gantry_action_topic_namespace': 'gantry_action_topic_namespace', 'robot_name': 'robot_name', 'home_Pose': 'home_Pose', 'table_Pose': 'table_Pose', 'gantry_action_topic': 'gantry_action_topic', 'part_Type': 'part_Type', 'section_Pose': 'section_Pose', 'drop_Pose': 'drop_Pose', 'pick_Pose': 'pick_Pose'})

			# x:1557 y:74
			OperatableStateMachine.add('wait',
										WaitState(wait_time=0.5),
										transitions={'done': 'moveGantrySection'},
										autonomy={'done': Autonomy.Off})

			# x:1557 y:274
			OperatableStateMachine.add('wait_2',
										WaitState(wait_time=0.5),
										transitions={'done': 'moveGantryHome'},
										autonomy={'done': Autonomy.Off})

			# x:957 y:674
			OperatableStateMachine.add('wait_3',
										WaitState(wait_time=0.5),
										transitions={'done': 'moveGantryHome_2'},
										autonomy={'done': Autonomy.Off})

			# x:757 y:674
			OperatableStateMachine.add('wait_3_2',
										WaitState(wait_time=0.5),
										transitions={'done': 'moveGantryTable_2'},
										autonomy={'done': Autonomy.Off})

			# x:1557 y:574
			OperatableStateMachine.add('wait_4',
										WaitState(wait_time=0.5),
										transitions={'done': 'moveGantryAGV'},
										autonomy={'done': Autonomy.Off})

			# x:157 y:224
			OperatableStateMachine.add('wait_5',
										WaitState(wait_time=0.5),
										transitions={'done': 'moveGantrySection_2'},
										autonomy={'done': Autonomy.Off})

			# x:370 y:64
			OperatableStateMachine.add('Home_UR10',
										self.use_behavior(Home_UR10SM, 'Home_UR10'),
										transitions={'finished': 'setParameters_unit2', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
