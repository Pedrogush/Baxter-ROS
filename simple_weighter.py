import bmakerCK
import rospy
import baxter_interface
from std_msgs.msg import Float64, String
from sensor_msgs.msg import JointState
from geometry_msgs.msg import Point, Quaternion

t=0
rospy.init_node('move_left_hand')
T = bmakerCK.hand_shaker()
T.get_info()
while t<14:
	T.listener()
        rospy.sleep(0.01)
        t = t+1
