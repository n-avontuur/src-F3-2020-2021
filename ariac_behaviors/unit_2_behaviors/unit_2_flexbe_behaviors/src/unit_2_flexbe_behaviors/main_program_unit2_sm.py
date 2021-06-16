#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_states.add_offset_to_pose_state import AddOffsetToPoseState
from ariac_flexbe_states.compute_grasp_ariac_state import ComputeGraspAriacState
from ariac_flexbe_states.create_dropPose import CreateDropPoseState
from ariac_flexbe_states.create_pose import CreatePoseState
from ariac_flexbe_states.detect_part_on_AGV_camera import DetectPartOnAGVCamera
from ariac_flexbe_states.get_gripper_status_state2 import GetGripperStatusState2
from ariac_flexbe_states.moveit_to_joints_dyn_ariac_state import MoveitToJointsDynAriacState
from ariac_flexbe_states.set_GantryParameters import set_GantryParameters
from ariac_flexbe_states.set_PickParameters import setPickParameters
from ariac_flexbe_states.set_RobotParameters import set_Robot_Parameters
from ariac_flexbe_states.srdf_state_to_moveit_ariac_state import SrdfStateToMoveitAriac
from ariac_flexbe_states.start_assignment_state import StartAssignment
from ariac_flexbe_states.vacuum_gripper_control_state2 import VacuumGripperControlState2
from ariac_logistics_flexbe_states.get_assembly_shipment_from_order_state import GetAssemblyShipmentFromOrderState
from ariac_logistics_flexbe_states.get_order_state import GetOrderState
from ariac_logistics_flexbe_states.get_part_from_products_state import GetPartFromProductsState
from ariac_support_flexbe_states.equal_state import EqualState
from flexbe_states.wait_state import WaitState
from unit_2_flexbe_behaviors.home_ur10_sm import Home_UR10SM
from unit_2_flexbe_behaviors.move_ur10_drop_sm import Move_UR10_DropSM
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

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:

		# ! 1635 20 
		# Made by Niels Avontuur



	def create(self):
		joint_names = ['gantry_arm_elbow_joint','gantry_arm_shoulder_lift_joint', 'gantry_arm_shoulder_pan_joint', 'gantry_arm_wrist_1_joint', 'gantry_arm_wrist_2_joint', 'gantry_arm_wrist_3_joint']
		# x:225 y:389, x:745 y:434, x:438 y:171
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed', 'no_Order'])
		_state_machine.userdata.zero = 0
		_state_machine.userdata.part_Number = 0
		_state_machine.userdata.ref_frame = 'world'
		_state_machine.userdata.trueVariable = True
		_state_machine.userdata.falseVariable = False
		_state_machine.userdata.rotation = 0.0
		_state_machine.userdata.offset = 0.0
		_state_machine.userdata.backout_offset = 0.1

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:30 y:40
			OperatableStateMachine.add('startAssignment',
										StartAssignment(),
										transitions={'continue': 'Home_UR10'},
										autonomy={'continue': Autonomy.Off})

			# x:32 y:122
			OperatableStateMachine.add('Home_UR10',
										self.use_behavior(Home_UR10SM, 'Home_UR10'),
										transitions={'finished': 'getOrderInfo', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:159 y:504
			OperatableStateMachine.add('Move_UR10_Drop',
										self.use_behavior(Move_UR10_DropSM, 'Move_UR10_Drop'),
										transitions={'finished': 'moveGantrySection_2', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'drop_Pose': 'drop_Pose', 'part_Type': 'part_Type'})

			# x:1319 y:205
			OperatableStateMachine.add('WitchAGVIsProductOn1',
										DetectPartOnAGVCamera(time_out=0.5),
										transitions={'continue': 'setPickParameters', 'failed': 'failed', 'not_found': 'WitchAGVIsProductOn1_2'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'agv': 'first_agv', 'ref_frame': 'ref_frame', 'camera_topic': 'camera_topic1', 'camera_frame': 'camera_frame1', 'part': 'part_Type', 'part_Pose': 'part_Pose', 'agv_Name': 'agv_Name'})

			# x:1584 y:210
			OperatableStateMachine.add('WitchAGVIsProductOn1_2',
										DetectPartOnAGVCamera(time_out=0.5),
										transitions={'continue': 'setPickParameters', 'failed': 'failed', 'not_found': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'agv': 'sec_agv', 'ref_frame': 'ref_frame', 'camera_topic': 'camera_topic2', 'camera_frame': 'camera_frame2', 'part': 'part_Type', 'part_Pose': 'part_Pose', 'agv_Name': 'agv_Name'})

			# x:1461 y:703
			OperatableStateMachine.add('addOffsetToPose',
										AddOffsetToPoseState(),
										transitions={'continue': 'computePick'},
										autonomy={'continue': Autonomy.Off},
										remapping={'input_pose': 'part_Pose', 'offset_pose': 'pickoffset_pose', 'output_pose': 'part_Pose'})

			# x:998 y:673
			OperatableStateMachine.add('addPose',
										AddOffsetToPoseState(),
										transitions={'continue': 'computePick'},
										autonomy={'continue': Autonomy.Off},
										remapping={'input_pose': 'part_Pose', 'offset_pose': 'decrees_pose', 'output_pose': 'part_Pose'})

			# x:1434 y:775
			OperatableStateMachine.add('computePick',
										ComputeGraspAriacState(joint_names=joint_names),
										transitions={'continue': 'moveToPick', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'UR10_move_group', 'action_topic_namespace': 'UR10_action_topic_namespace', 'tool_link': 'UR10_tool_link', 'pose': 'part_Pose', 'offset': 'offset', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:184 y:841
			OperatableStateMachine.add('computePick_2',
										ComputeGraspAriacState(joint_names=joint_names),
										transitions={'continue': 'moveToBackout', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'UR10_move_group', 'action_topic_namespace': 'UR10_action_topic_namespace', 'tool_link': 'UR10_tool_link', 'pose': 'part_Pose', 'offset': 'backout_offset', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:530 y:680
			OperatableStateMachine.add('createDecrees',
										CreatePoseState(xyz=[0.0,0.0,-0.01], rpy=[0.0,0.0,0.0]),
										transitions={'continue': 'addPose', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'decrees_pose'})

			# x:1465 y:634
			OperatableStateMachine.add('createOffsetPose',
										CreateDropPoseState(),
										transitions={'continue': 'addOffsetToPose', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'xyz': 'pick_offset', 'rpy': 'pick_rotation', 'pose': 'pickoffset_pose'})

			# x:673 y:766
			OperatableStateMachine.add('getGripperStatus',
										GetGripperStatusState2(),
										transitions={'continue': 'isPartAttached', 'fail': 'failed'},
										autonomy={'continue': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'enabled': 'gripper_enabled', 'attached': 'gripper_attached'})

			# x:174 y:34
			OperatableStateMachine.add('getOrderInfo',
										GetOrderState(),
										transitions={'order_found': 'GetAssamblyOrderInfo', 'no_order_found': 'no_Order'},
										autonomy={'order_found': Autonomy.Off, 'no_order_found': Autonomy.Off},
										remapping={'order_id': 'order_id', 'kitting_shipments': 'kitting_shipments', 'number_of_kitting_shipments': 'number_of_kitting_shipments', 'assembly_shipments': 'assembly_shipments', 'number_of_assembly_shipments': 'number_of_assembly_shipments'})

			# x:672 y:61
			OperatableStateMachine.add('getPartFromOrder',
										GetPartFromProductsState(),
										transitions={'continue': 'set_GantryParameters', 'invalid_index': 'failed'},
										autonomy={'continue': Autonomy.Off, 'invalid_index': Autonomy.Off},
										remapping={'products': 'products', 'index': 'part_Number', 'type': 'part_Type', 'pose': 'drop_Pose'})

			# x:462 y:764
			OperatableStateMachine.add('isPartAttached',
										EqualState(),
										transitions={'true': 'computePick_2', 'false': 'createDecrees'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'gripper_attached', 'value_b': 'trueVariable'})

			# x:1463 y:380
			OperatableStateMachine.add('moveGantryAGV',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'setRobotParameters', 'planning_failed': 'wait_4', 'control_failed': 'wait_4', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'gantry_AGV_Pose', 'move_group': 'gantry_move_group', 'action_topic_namespace': 'gantry_action_topic_namespace', 'action_topic': 'gantry_action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1327 y:123
			OperatableStateMachine.add('moveGantryHome',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'WitchAGVIsProductOn1', 'planning_failed': 'wait_2', 'control_failed': 'wait_2', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'home_Pose', 'move_group': 'gantry_move_group', 'action_topic_namespace': 'gantry_action_topic_namespace', 'action_topic': 'gantry_action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:184 y:674
			OperatableStateMachine.add('moveGantryHome_2',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'moveGantryTable_2', 'planning_failed': 'wait_3', 'control_failed': 'wait_3', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'home_Pose', 'move_group': 'gantry_move_group', 'action_topic_namespace': 'gantry_action_topic_namespace', 'action_topic': 'gantry_action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1106 y:116
			OperatableStateMachine.add('moveGantrySection',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'moveGantryHome', 'planning_failed': 'wait', 'control_failed': 'wait', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'section_Pose', 'move_group': 'gantry_move_group', 'action_topic_namespace': 'gantry_action_topic_namespace', 'action_topic': 'gantry_action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:186 y:435
			OperatableStateMachine.add('moveGantrySection_2',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'finished', 'planning_failed': 'wait_5', 'control_failed': 'wait_5', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'section_Pose', 'move_group': 'gantry_move_group', 'action_topic_namespace': 'gantry_action_topic_namespace', 'action_topic': 'gantry_action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:187 y:583
			OperatableStateMachine.add('moveGantryTable_2',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'Move_UR10_Drop', 'planning_failed': 'wait_3_2', 'control_failed': 'wait_3_2', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'table_Pose', 'move_group': 'gantry_move_group', 'action_topic_namespace': 'gantry_action_topic_namespace', 'action_topic': 'gantry_action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:183 y:748
			OperatableStateMachine.add('moveToBackout',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'moveGantryHome_2', 'planning_failed': 'wait_7_2', 'control_failed': 'wait_7_2'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'action_topic_namespace': 'UR10_action_topic_namespace', 'move_group': 'UR10_move_group', 'action_topic': 'UR10_action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1189 y:775
			OperatableStateMachine.add('moveToPick',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'setGripperON', 'planning_failed': 'wait_7', 'control_failed': 'wait_7'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'action_topic_namespace': 'UR10_action_topic_namespace', 'move_group': 'UR10_move_group', 'action_topic': 'UR10_action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1465 y:559
			OperatableStateMachine.add('moveToPrePick',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'createOffsetPose', 'planning_failed': 'wait_6', 'control_failed': 'wait_6', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'armHomeDown', 'move_group': 'UR10_move_group', 'action_topic_namespace': 'UR10_action_topic_namespace', 'action_topic': 'UR10_action_topic', 'robot_name': 'UR10_robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1000 y:774
			OperatableStateMachine.add('setGripperON',
										VacuumGripperControlState2(enable=True),
										transitions={'continue': 'wait_8', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off})

			# x:1469 y:296
			OperatableStateMachine.add('setPickParameters',
										setPickParameters(),
										transitions={'continue': 'moveGantryAGV', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'station_id': 'station_id', 'agv_Name': 'agv_Name', 'gantry_AGV_pose': 'gantry_AGV_Pose'})

			# x:1466 y:466
			OperatableStateMachine.add('setRobotParameters',
										set_Robot_Parameters(),
										transitions={'continue': 'moveToPrePick', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'part_Type': 'part_Type', 'UR10_move_group': 'UR10_move_group', 'UR10_action_topic_namespace': 'UR10_action_topic_namespace', 'UR10_action_topic': 'UR10_action_topic', 'UR10_tool_link': 'UR10_tool_link', 'UR10_robot_name': 'UR10_robot_name', 'gripper_service': 'gripper_service', 'gripper_status_topic': 'gripper_status_topic', 'gripper_status_attached': 'gripper_status_attached', 'gripper_status_enabled': 'gripper_status_enabled', 'armHomeDown': 'armHomeDown', 'armHomeUp': 'armHomeUp', 'pick_offset': 'pick_offset', 'pick_rotation': 'pick_rotation'})

			# x:880 y:61
			OperatableStateMachine.add('set_GantryParameters',
										set_GantryParameters(),
										transitions={'continue': 'moveGantrySection', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'station_id': 'station_id', 'home_Pose': 'home_Pose', 'table_Pose': 'table_Pose', 'section_Pose': 'section_Pose', 'gantry_move_group': 'gantry_move_group', 'gantry_action_topic_namespace': 'gantry_action_topic_namespace', 'gantry_action_topic': 'gantry_action_topic', 'robot_name': 'robot_name', 'camera_frame1': 'camera_frame1', 'camera_topic1': 'camera_topic1', 'camera_frame2': 'camera_frame2', 'camera_topic2': 'camera_topic2', 'first_agv': 'first_agv', 'sec_agv': 'sec_agv'})

			# x:1134 y:23
			OperatableStateMachine.add('wait',
										WaitState(wait_time=0.5),
										transitions={'done': 'moveGantrySection'},
										autonomy={'done': Autonomy.Off})

			# x:1345 y:22
			OperatableStateMachine.add('wait_2',
										WaitState(wait_time=0.5),
										transitions={'done': 'moveGantryHome'},
										autonomy={'done': Autonomy.Off})

			# x:28 y:660
			OperatableStateMachine.add('wait_3',
										WaitState(wait_time=0.5),
										transitions={'done': 'moveGantryHome_2'},
										autonomy={'done': Autonomy.Off})

			# x:28 y:587
			OperatableStateMachine.add('wait_3_2',
										WaitState(wait_time=0.5),
										transitions={'done': 'moveGantryTable_2'},
										autonomy={'done': Autonomy.Off})

			# x:1656 y:392
			OperatableStateMachine.add('wait_4',
										WaitState(wait_time=0.5),
										transitions={'done': 'moveGantryAGV'},
										autonomy={'done': Autonomy.Off})

			# x:24 y:435
			OperatableStateMachine.add('wait_5',
										WaitState(wait_time=0.5),
										transitions={'done': 'moveGantrySection_2'},
										autonomy={'done': Autonomy.Off})

			# x:1672 y:570
			OperatableStateMachine.add('wait_6',
										WaitState(wait_time=0.5),
										transitions={'done': 'moveToPrePick'},
										autonomy={'done': Autonomy.Off})

			# x:1220 y:850
			OperatableStateMachine.add('wait_7',
										WaitState(wait_time=0.5),
										transitions={'done': 'moveToPick'},
										autonomy={'done': Autonomy.Off})

			# x:42 y:749
			OperatableStateMachine.add('wait_7_2',
										WaitState(wait_time=0.5),
										transitions={'done': 'moveToBackout'},
										autonomy={'done': Autonomy.Off})

			# x:868 y:767
			OperatableStateMachine.add('wait_8',
										WaitState(wait_time=0.5),
										transitions={'done': 'getGripperStatus'},
										autonomy={'done': Autonomy.Off})

			# x:431 y:53
			OperatableStateMachine.add('GetAssamblyOrderInfo',
										GetAssemblyShipmentFromOrderState(),
										transitions={'continue': 'getPartFromOrder', 'invalid_index': 'failed'},
										autonomy={'continue': Autonomy.Off, 'invalid_index': Autonomy.Off},
										remapping={'assembly_shipments': 'assembly_shipments', 'assembly_index': 'zero', 'shipment_type': 'part_Type', 'products': 'products', 'station_id': 'station_id', 'number_of_products': 'number_of_products'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
