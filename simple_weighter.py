import bmakerCK
import rospy
import baxter_interface
from std_msgs.msg import Float64, String
from sensor_msgs.msg import JointState
from geometry_msgs.msg import Point, Quaternion

t=0
rospy.init_node('weigh_left_hand')
T = bmakerCK.hand_shaker()
T.get_info()
T.listener()
