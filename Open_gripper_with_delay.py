import rospy
import baxter_interface

rospy.init_node('open')
EN = baxter_interface.RobotEnable()
EN.enable()
left = baxter_interface.Gripper('left')
rospy.sleep(10)
left.open(80)
