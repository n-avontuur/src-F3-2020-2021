#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from flexbe_core import EventState, Logger, logger


class setNewPosePart(EventState):
	'''
	this state sets the new pose for the part

	'''

	def __init__(self):
		super(setNewPosePart,self).__init__(input_keys = ['part_Content','numberOfModels','bin','bin_Content'],outcomes = ['continue', 'failed','bin_Full'], output_keys = ['drop_Offset','pick_Offset','drop_Rotation','pick_Rotation','numberOfModels','bin_Content'])

	def on_enter(self, userdata):
		offset=userdata.part_Content[0]
		self._offset=offset[0]
		liststr = ' '.join([str(elem) for elem in offset])
		rospy.loginfo('list of offset: ' + liststr)

		try:
			offset_z=userdata.part_Content[1]		
			self._offset_z=offset_z[0]
		except:
			Logger.logwarn('offsetZ not correct')

		try:	
			numberParts=userdata.numberOfModels
			self._numberParts=numberParts
		except:
			Logger.logwarn('numberparts not correct')

		try:
			maxNumberParts=userdata.part_Content[3]
			self._maxNumberParts=maxNumberParts
			self._maxNumberPartsX=maxNumberParts[0]
			self._maxNumberPartsY=maxNumberParts[1]
		except:
			Logger.logwarn('maxnumberparts not correct')
		pass


	def execute(self, userdata):
		max_X=self._maxNumberPartsX
		max_Y=self._maxNumberPartsY
		max_parts=max_Y*max_X
		numberOfParts=self._numberParts
		offset=[]
		if (self._numberParts == max_parts):
			self._numberParts = 0
			return 'bin_Full'
		matrix= [[0 for _ in range(max_Y)] for _ in range(max_X)]
		for i in range(max_X):
			for j in range(max_Y):
				matrix[i][j] = i*max_Y+j
		liststr = ' '.join([str(elem) for elem in matrix])
		Logger.loginfo('matrix :'+liststr)
		for i in range(max_X):
			for j in range(max_Y):
				if ((numberOfParts) == matrix[i][j]):
					offset=self._offset[i][j]
					liststr = ' '.join([str(elem) for elem in offset])
					Logger.loginfo('offset :'+liststr)
					self._offset_x=offset[0]
					self._offset_y=offset[1]
				Logger.loginfo('inhoud matrix:'+str(matrix[i][j]))


		userdata.drop_Offset=[self._offset_x,self._offset_y,self._offset_z+0.02]
		userdata.pick_Offset=[0.0,0.0,self._offset_z]
		userdata.drop_Rotation=[0.0,0.0,0.0]
		userdata.pick_Rotation=[0.0,0.0,0.0]
		try:
			liststr = ' '.join([str(elem) for elem in userdata.pick_Offset])
			Logger.loginfo('pick offset: '+liststr)
			liststr = ' '.join([str(elem) for elem in userdata.drop_Offset])
			Logger.loginfo('drop offset: '+liststr)
		except:
			Logger.loginfo('reading pick and drop offset went wrong')
		return 'continue'

	def on_exit(self, userdata):
		userdata.numberOfModels = self._numberParts
		pass

	def on_start(self):
		pass


	def on_stop(self):
		pass
