import bmakerCK
import rospy
import baxter_interface
from std_msgs.msg import Float64, String
from sensor_msgs.msg import JointState
from geometry_msgs.msg import Point, Quaternion

# simple use of bmakerCK to record a set of .feel files with the robot's hand standing somewhat still (no command is issued, only internal baxter controllers are operating)
samples = raw_input('input number of samples desired\n')
samples = int(samples)
a=0
T = [0]*samples
nb = raw_input('input .feel set root file names\n')
while a<samples:
	t=0
	rospy.init_node('move_left_hand')
	T[a] = bmakerCK.hand_shaker()
	gripper = baxter_interface.Gripper('left')
	gripper.close(80)
	T[a].F = open('./resources/%s-%s.feel' %(nb,a), 'w')
	T[a].listener()
	rospy.sleep(3.005)
        a=a+1
