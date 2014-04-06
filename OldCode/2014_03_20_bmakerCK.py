#!/usr/bin/env python
import rospy
import ik_solver
import baxter_interface
from std_msgs.msg import Float64, String
from sensor_msgs.msg import JointState
from geometry_msgs.msg import Point, Quaternion



 
# obj: move left arm to predetermined position, grip an object, move the end effector slightly in each direction and rotation, record effort on joints, guess weight and center of mass.
# movement is in meters 
seq = 0
invert = 1
rospy.init_node('move_left_hand')
EN = baxter_interface.RobotEnable()
EN.enable()
left = baxter_interface.Limb('left')
pose = left.endpoint_pose()
initialpose = pose
left.set_joint_position_speed(0.1)
x = initialpose["position"].x
y = initialpose["position"].y
z = initialpose["position"].z
x1 = initialpose["orientation"].x
y1 = initialpose["orientation"].y
z1 = initialpose["orientation"].z
w = initialpose["orientation"].w
orient = Quaternion(x1, y1, z1, w)
loc = Point(x,y,z)
nb = raw_input('input .feel file name\n')
F = open('./resources/%s.feel' %nb, 'w')
nc = raw_input('input path file name\n')
G = open('./resources/%s.txt' %nc, 'w')
nt = raw_input('how many seconds do you want to place an item in the gripper?\n')
rospy.sleep(int(nt))
gripper = baxter_interface.Gripper('left')
gripper.close(80)
rospy.sleep(int(nt)/10)

def callback(data):
     F.write(repr(data.effort))
    #F.write("\n"+repr(data.effort)+"\n")
def listener():
    rospy.Subscriber("/robot/joint_states", JointState, callback)
#NEED TO REMOVE RIGHT ARM VARIABLES FROM EFFORT OUTPUT
#move along x for 2 centimeters from initial position in the positive direction, then reverses and goes 2 centimeters from initial position in the negative direction, same behavior is repeated for all linear coordinates
hack = 0

print left.joint_angles()
while  (seq < 18):
        listener()
        if seq<3:
            x = initialpose["position"].x+0.05*invert
            if seq == 3:
               hack = 1
        if 3<=seq<6:
            y = initialpose["position"].y+0.05*invert
            if seq == 6:
               hack = 1
        if 6<=seq<9:
            z = initialpose["position"].z+0.05*invert
            if seq == 9:
               hack = 1
        if 9<=seq<12:
            x1 = initialpose["orientation"].x+0.05*invert
            if seq == 12:
               hack = 1
        if 12<=seq<15:
            y1 = initialpose["orientation"].y+0.05*invert
            if seq == 15:
               hack = 1
        if 15<=seq<18:
            z1 = initialpose["orientation"].z+0.05*invert
            if seq == 18:
               hack = 1
        orient = Quaternion(x1,y1,z1, w)
        loc = Point(x,y,z)
        limb_joints = ik_solver.ik_solve('left', loc, orient)
        if hack == 1:
           limb_joints = [-0.08, -1.0, -1.19, 1.94,  0.67, 1.03, -0.5]
        left.move_to_joint_positions(limb_joints)
        invert = -invert
        seq = seq +1
        G.write('solution number ' + repr(seq) + ' is:\n')
        G.write(repr(limb_joints))
        G.write('\n \n')

# use head wobbler and tuck arms as examples
#records /current command being executed/ along with timestamps, /a header/ and the effort seqiable from the topic. 

#write output of /robot/JointStates and look for the effort variable
#write out the effort seqiable as a seq of values for each joint