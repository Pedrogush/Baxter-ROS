import bmakerCK
import rospy
import baxter_interface
from std_msgs.msg import Float64, String
from sensor_msgs.msg import JointState
from geometry_msgs.msg import Point, Quaternion

# simple use of bmakerCK to record a set of .feel files with the robot's hand standing somewhat still (no command is issued, only internal baxter controllers are operating) 
a=0
T = [0]*30
while a<30:
	t=0
	rospy.init_node('move_left_hand')
	T[a] = bmakerCK.hand_shaker()
	T[a].F = open('./resources/%s.feel' %a, 'w')
	T[a].listener()
	while t<50:
		rospy.sleep(0.01)
		t = t+1
        T[a].arg=0
        a=a+1
