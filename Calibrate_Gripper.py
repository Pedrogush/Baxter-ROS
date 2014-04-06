import rospy
import baxter_interface

rospy.init_node('testing')
EN = baxter_interface.RobotEnable()
EN.enable()
left = baxter_interface.Gripper('left')
left.calibrate()
