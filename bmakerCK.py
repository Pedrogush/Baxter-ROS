#!/usr/bin/env python
import rospy
#import ik_solver
import baxter_interface
from std_msgs.msg import Float64, String
from sensor_msgs.msg import JointState
from geometry_msgs.msg import Point, Quaternion

# bmaker method, purpose should be to generate one or a set of .feel files from the /robot/joint_states topic, recording the effort or other variables from each joint
#{'left_w0': 0.6495968976036508, 'left_w1': 1.0655294384279443, 'left_w2': -0.47238745495226575, 'left_e0': -0.9910781033735024, 'left_e1': 1.797212088205409, 'left_s0': -0.20026499418204616, 'left_s1': -0.9384675624715599} 
# 0.9809294775252653, 'left_w1': 1.194796205055456, 'left_w2': -0.8449171582167079, 'left_e0': -1.4621030022028167, 'left_e1': 2.0780019552204556, 'left_s0': 0.10242124929624877, 'left_s1': -0.7198712041812328

 
# obj: move left arm to predetermined position, grip an object, move the end effector slightly in each direction and rotation, record effort on joints, guess weight and center of mass.
# movement is in meters
class hand_shaker(object):
	def __init__(self):
		self.posmarkers = {1 : 'left_neutral', 2: 'left_+x', 3:'left_-x', 4:'left_neutral', 5:'left_+y', 6:'left_-y', 7:'left_neutral', 8:'left_-z', 9:'left_+z', 10: 'left_neutral', 11:'left_rotate_clock', 12:'left_rotate_aclock', 13:'left_neutral'}  
		self.positions = { 'left_neutral':  {'left_w0': 0.613592314453125, 'left_w1': 1.081839949420166, 'left_w2': -0.5522330830078125, 'left_e0': -1.151636075189209, 'left_e1': 1.7924565485961916, 'left_s0': -0.15109710743408203, 'left_s1': -0.9848156646972657}
, 'left_+x':{'left_w0': 0.65, 'left_w1': 1.07, 'left_w2': -0.47, 'left_e0': -0.99, 'left_e1': 1.80, 'left_s0': -0.20, 'left_s1': -0.94}
, 'left_-x':{'left_w0': 0.98, 'left_w1': 1.19, 'left_w2': -0.84, 'left_e0': -1.46, 'left_e1': 2.08, 'left_s0': 0.107, 'left_s1': -0.72}
, 'left_+y':{'left_w0': 0.70, 'left_w1': 1.11, 'left_w2': -0.59, 'left_e0': -1.04, 'left_e1': 1.77, 'left_s0': -0.27, 'left_s1': -0.89}
, 'left_-y':{'left_w0': 0.65, 'left_w1': 1.06, 'left_w2': -0.39, 'left_e0': -1.00, 'left_e1': 1.80, 'left_s0': -0.10, 'left_s1': -0.94}
, 'left_+z':{'left_w0': 0.64, 'left_w1': 1.20, 'left_w2': -0.54, 'left_e0': -1.10, 'left_e1': 1.71, 'left_s0': -0.22, 'left_s1': -0.95}
, 'left_-z':{'left_w0': 0.77, 'left_w1': 1.02, 'left_w2': -0.63, 'left_e0': -0.96, 'left_e1': 1.80, 'left_s0': -0.32, 'left_s1': -0.82}
,  'left_rotate_clock':{'left_w0': 0.613592314453125, 'left_w1': 1.081839949420166, 'left_w2': -0.5522330830078125, 'left_e0': -1.151636075189209, 'left_e1': 1.7924565485961916, 'left_s0': -0.15109710743408203, 'left_s1': -0.9848156646972657}
, 'left_rotate_aclock':{'left_w0': 0.613592314453125, 'left_w1': 1.081839949420166, 'left_w2': -0.5522330830078125, 'left_e0': -1.151636075189209, 'left_e1': 1.7924565485961916, 'left_s0': -0.15109710743408203, 'left_s1': -0.9848156646972657}
}
		self.gripper = baxter_interface.Gripper('left')
	        self.left = baxter_interface.Limb('left')
                self.loopvar = 0
		self.arg=1
		self.o=0

	def get_info(self):
		self.nb = raw_input('input .feel file name\n')
		self.F = open('./resources/%s.feel' %self.nb, 'w')
		self.nt = raw_input('how many seconds do you want to place an item in the gripper?\n')
		rospy.sleep(int(self.nt))
		self.gripper.close(80)
		rospy.sleep(int(self.nt)/10)
	        self.EN = baxter_interface.RobotEnable()
	        self.EN.enable()
	        self.left.set_joint_position_speed(1)

	def callback(self, data):
	     self.o=self.o+1
             if self.o<1000:
	     	self.F.write(repr(data.effort))
             if self.o>1000:
		self.F.close()

	def listener(self):
	    rospy.Subscriber("/robot/joint_states", JointState, self.callback, self.arg)

#NEED TO REMOVE RIGHT ARM VARIABLES FROM EFFORT OUTPUT
#move along x for 2 centimeters from initial position in the positive direction, then reverses and goes 2 centimeters from initialhttps://github.com/RethinkRobotics/sdk-docs/wiki

if __name__ == "__main__":
    main()
# use head wobbler and tuck arms as examples
#records /current command being executed/ along with timestamps, /a header/ and the effort seqiable from the topic. 

#write output of /robot/JointStates and look for the effort variable
#write out the effort seqiable as a seq of values for each joint
