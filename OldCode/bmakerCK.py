#!/usr/bin/env python
import rospy
import ik_solver
import baxter_interface
import rosbag
from std_msgs.msg import Float64, String
import sensor_msgs.msg
from geometry_msgs.msg import (    
Point,
Quaternion,
)

# obj: move right arm to predetermined position, grip an object, move the end effector slightly in each direction and rotation, record effort on joints, guess weight and center of mass.
# movement is in meters 
sequence = 0
b = 0
invert = 1
invertcount = 0
rospy.init_node('move_right_hand')
EN = baxter_interface.RobotEnable()
EN.enable()
right = baxter_interface.Limb('right')
pose = right.endpoint_pose()
initialpose = pose
b = True
right.set_joint_position_speed(1)
desiredpose = initialpose
x = desiredpose["position"].x + 0.04*invert
y = desiredpose["position"].y
z = desiredpose["position"].z
x1 = desiredpose["orientation"].x
y1 = desiredpose["orientation"].y
z1 = desiredpose["orientation"].z
w = initialpose["orientation"].w

orient = Quaternion(x1, y1, z1, w)
loc = Point(x,y,z)
F = open('hand.feel', 'w')
#move along x for 2 centimeters from initial position in the positive direction, then reverses and goes 2 centimeters from initial position in the negative direction, same behavior is repeated for all linear coordinates 
while  (sequence < 3):
    x = initialpose["position"].x+0.05*invert
    loc = Point(x,y,z)
    if invertcount > 1:
        desiredpose = initialpose
        x = desiredpose["position"].x
        y = desiredpose["position"].y
        z = desiredpose["position"].z
        loc = Point(x,y,z)
    invert = -invert
    sequence = sequence + 1    
    if invertcount == 0:
       names = {'Letter': 'X', 'Direction': 'Forward'}
       limb_joints1 = ik_solver.ik_solve('right', loc, orient)
       right.move_to_joint_positions(limb_joints1)
       F.write('moving along {Letter} in the {Direction} direction\n'.format(**names))
    if invertcount == 1:
       names = {'Letter': 'X', 'Direction': 'Backwards'}
       limb_joints1b = ik_solver.ik_solve('right', loc, orient)
       right.move_to_joint_positions(limb_joints1b)
       F.write('moving along {Letter} in the {Direction} direction\n'.format(**names)) 
    if invertcount == 2:
       names = {'Letter': 'X', 'Direction': 'Origin'}
       limb_joints1c = ik_solver.ik_solve('right', loc, orient)
       right.move_to_joint_positions(limb_joints1c)
       F.write('moving along {Letter} in the {Direction} direction\n'.format(**names))
    if invertcount > 2:
       invertcount = 0   
    F.write('\n')
    invertcount = invertcount + 1
while  (2 < sequence < 6):
    y = initialpose["position"].y+0.05*invert
    loc = Point(x,y,z)
    if invertcount > 1:
        desiredpose = initialpose
        x = desiredpose["position"].x
        y = desiredpose["position"].y
        z = desiredpose["position"].z
        loc = Point(x,y,z)
    invert = -invert
    sequence = sequence + 1       
    if invertcount == 0:
       names = {'Letter': 'Y', 'Direction': 'Forward'}
       limb_joints2 = ik_solver.ik_solve('right', loc, orient)
       right.move_to_joint_positions(limb_joints2)
       F.write('moving along {Letter} in the {Direction} direction\n'.format(**names))
    if invertcount == 1:
       names = {'Letter': 'Y', 'Direction': 'Backwards'}
       limb_joints2b = ik_solver.ik_solve('right', loc, orient)
       right.move_to_joint_positions(limb_joints2b)
       F.write('moving along {Letter} in the {Direction} direction\n'.format(**names)) 
    if invertcount == 2:
       names = {'Letter': 'Y', 'Direction': 'Origin'}
       limb_joints2c = ik_solver.ik_solve('right', loc, orient)
       right.move_to_joint_positions(limb_joints2c)
       F.write('moving along {Letter} in the {Direction} direction\n'.format(**names))
    if invertcount > 2:
             invertcount = 0
    
    F.write('the solution is: \n')
    invertcount = invertcount + 1
while  (5 < sequence < 9):
    z = initialpose["position"].z+0.05*invert
    loc = Point(x,y,z)
    if invertcount > 1:
        desiredpose = initialpose
        x = desiredpose["position"].x
        y = desiredpose["position"].y
        z = desiredpose["position"].z
        loc = Point(x,y,z)
    invert = -invert
    sequence = sequence + 1      
    if invertcount == 0:
       names = {'Letter': 'Z', 'Direction': 'Forward'}
       limb_joints3 = ik_solver.ik_solve('right', loc, orient)
       right.move_to_joint_positions(limb_joints3)
    if invertcount == 1:
       names = {'Letter': 'Z', 'Direction': 'Backwards'}
       limb_joints3b = ik_solver.ik_solve('right', loc, orient)
       right.move_to_joint_positions(limb_joints3b) 
    if invertcount == 2:
       names = {'Letter': 'Z', 'Direction': 'Origin'}
       limb_joints3c = ik_solver.ik_solve('right', loc, orient)
       right.move_to_joint_positions(limb_joints3c)
    if invertcount > 2:
             invertcount = 0
    F.write('moving along {Letter} in the {Direction} direction\n'.format(**names))
    F.write('the solution is: \n')
    invertcount = invertcount + 1
while (8 < sequence < 12):
    x1 = initialpose["orientation"].x+0.1*invert
    orient = Quaternion(x1, y1, z1, w)
    if invertcount > 1:
        desiredpose = initialpose
        x1 = desiredpose["orientation"].x
        y1 = desiredpose["orientation"].y
        z1 = desiredpose["orientation"].z
        orient = Quaternion(x1,y1,z1, w)
    invert = -invert
    sequence = sequence + 1   
    if invertcount == 0:
       names = {'Letter': 'A1', 'Direction': 'F'}
       limb_joints4 = ik_solver.ik_solve('right', loc, orient)
       right.move_to_joint_positions(limb_joints4)
    if invertcount == 1:
       names = {'Letter': 'A1', 'Direction': 'B'}
       limb_joints4b = ik_solver.ik_solve('right', loc, orient)
       right.move_to_joint_positions(limb_joints4b) 
    if invertcount == 2:
       names = {'Letter': 'A1', 'Direction': 'O'}
       limb_joints4c = ik_solver.ik_solve('right', loc, orient)
       right.move_to_joint_positions(limb_joints4c)  
    if invertcount > 2:
             invertcount = 0
    F.write('moving along {Letter} in the {Direction} direction\n'.format(**names))
    F.write('the solution is: \n')
    F.write('\n')
    invertcount = invertcount + 1
while  (11 < sequence < 15):
    y1 = initialpose["orientation"].y+0.1*invert
    orient = Quaternion(x1, y1, z1, w)
    if invertcount > 1:
        desiredpose = initialpose
        x1 = desiredpose["orientation"].x
        y1 = desiredpose["orientation"].y
        z1 = desiredpose["orientation"].z
        orient = Quaternion(x1,y1,z1, w)
    invert = -invert
    sequence = sequence + 1
    if invertcount == 0:
       names = {'Letter': 'A2', 'Direction': 'F'}
       limb_joints5 = ik_solver.ik_solve('right', loc, orient)
       right.move_to_joint_positions(limb_joints5)
    if invertcount == 1:
       names = {'Letter': 'A2', 'Direction': 'B'}
       limb_joints5b = ik_solver.ik_solve('right', loc, orient)
       right.move_to_joint_positions(limb_joints5b) 
    if invertcount == 2:
       names = {'Letter': 'A2', 'Direction': 'O'}
       limb_joints5c = ik_solver.ik_solve('right', loc, orient)
       right.move_to_joint_positions(limb_joints5c) 
    if invertcount > 2:
             invertcount = 0
    F.write('moving along {Letter} in the {Direction} direction\n'.format(**names))
    F.write('the solution is: \n')
    F.write('\n')
    invertcount = invertcount + 1
while  (14 < sequence < 18):
    z1 = initialpose["orientation"].z+0.1*invert
    orient = Quaternion(x1, y1, z1, w)
    if invertcount > 1:
        desiredpose = initialpose
        x1 = desiredpose["orientation"].x
        y1 = desiredpose["orientation"].y
        z1 = desiredpose["orientation"].z
        orient = Quaternion(x1,y1,z1, w)
    invert = -invert
    sequence = sequence + 1    
    if invertcount == 0:
       names = {'Letter': 'A3', 'Direction': 'F'}
       limb_joints6 = ik_solver.ik_solve('right', loc, orient)
       right.move_to_joint_positions(limb_joints6)
    if invertcount == 1:
       names = {'Letter': 'A3', 'Direction': 'B'}
       limb_joints6b = ik_solver.ik_solve('right', loc, orient)
       right.move_to_joint_positions(limb_joints6b) 
    if invertcount == 2:
       names = {'Letter': 'A3', 'Direction': 'O'}
       limb_joints6c = ik_solver.ik_solve('right', loc, orient)
       right.move_to_joint_positions(limb_joints6c)
    if invertcount > 2:
            invertcount = 0 
    F.write('moving along {Letter} in the {Direction} direction\n'.format(**names))
    F.write('the solution is: \n')
    F.write('\n')
    invertcount = invertcount + 1
F.close()

#records /current command being executed/ along with timestamps, /a header/ and the effort variable from the topic. 

#/write current limb_joints in a text file name $Letter$$Direction$.txt/
#write output of /robot/JointStates and look for the effort variable
#write out the effort variable as a sequence of values for each joint
