#!/usr/bin/env python
import rospy
import baxter_interface
#writing a simple file
invertcount=0
sequence=0
limb_joints = [0, 0, 0, 0, 0]
nam = {'limb_joints': limb_joints,'Letter' : '', 'Direction': ''}
while invertcount<3:
	if sequence == limb_joints[0]:
		if invertcount == 0:
			names = {'Letter': 'X', 'Direction': 'Forward'}
		if invertcount == 1:
			names = {'Letter': 'X', 'Direction': 'Backwards'}
		if invertcount == 2:
			names = {'Letter': 'X', 'Direction': 'Origin'}
	invertcount = invertcount + 1
        F = open('{Letter}{Direction}.txt'.format(**names), 'w')
        F.write('moving along {Letter} in the {Direction} direction\n'.format(**names))
        F.write('the solution is: \n')
        F.write(repr(repr('{limb_joints}{Letter}{Direction}'.format(**nam))))
        F.write('\n')
	F.close()
rospy.init_node('testing')
EN = baxter_interface.RobotEnable()
EN.enable()
left = baxter_interface.Gripper('left')
rospy.sleep(10)
left.open(80)
