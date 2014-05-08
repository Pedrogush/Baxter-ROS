#!/usr/bin/env python
import rospy
#import ik_solver
import baxter_interface
from std_msgs.msg import Float64, String
from sensor_msgs.msg import JointState
from geometry_msgs.msg import Point, Quaternion

import argparse
import math
import random

import rospy

from std_msgs.msg import (
    UInt16,
)
# bmaker method, purpose should be to generate one or a set of .feel files from the /robot/joint_states topic, recording the effort or other variables from each joint
#{'left_w0': 0.6495968976036508, 'left_w1': 1.0655294384279443, 'left_w2': -0.47238745495226575, 'left_e0': -0.9910781033735024, 'left_e1': 1.797212088205409, 'left_s0': -0.20026499418204616, 'left_s1': -0.9384675624715599} 
# 0.9809294775252653, 'left_w1': 1.194796205055456, 'left_w2': -0.8449171582167079, 'left_e0': -1.4621030022028167, 'left_e1': 2.0780019552204556, 'left_s0': 0.10242124929624877, 'left_s1': -0.7198712041812328

#!/usr/bin/env python

# Copyright (c) 2013, Rethink Robotics
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. Neither the name of the Rethink Robotics nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.



class Wobbler(object):

    def __init__(self, h):
        """
        'Wobbles' both arms by commanding joint velocities sinusoidally.
        """
        self._pub_rate = rospy.Publisher('robot/joint_state_publish_rate',
                                         UInt16)
        self._left_arm = baxter_interface.limb.Limb("left")
        self._right_arm = baxter_interface.limb.Limb("right")
        self._left_joint_names = self._left_arm.joint_names()
        self._right_joint_names = self._right_arm.joint_names()
        print("Getting robot state... ")
        self._rs = baxter_interface.RobotEnable()
        self._init_state = self._rs.state().enabled
        print("Enabling robot... ")
        self._rs.enable()

        # set joint state publishing to 100Hz
        self._pub_rate.publish(100)

    def _reset_control_modes(self):
        rate = rospy.Rate(100)
        for _ in xrange(100):
            if rospy.is_shutdown():
                return False
            self._left_arm.exit_control_mode()
            self._right_arm.exit_control_mode()
            self._pub_rate.publish(100)
            rate.sleep()
        return True

    def set_neutral(self):
        """
        Sets both arms back into a neutral pose.
        """
        print("Moving to neutral pose...")
        self._left_arm.move_to_neutral()
        self._right_arm.move_to_neutral()

    def clean_shutdown(self):
        print("\nExiting example...")
        #return to normal
        self._reset_control_modes()
        self.set_neutral()
        if not self._init_state:
            print("Disabling robot...")
            self._rs.disable()
        return True

    def wobble(self, h):
        self.set_neutral()
        """
        Performs the wobbling of both arms.
        """
        rate = rospy.Rate(100)
        start = rospy.Time.now()

        def make_v_func():
            """
            returns a randomly parameterized cosine function to control a
            specific joint.
            """
            period_factor = 1
            amplitude_factor = 0.2

            def v_func(elapsed):
                w = period_factor * elapsed.to_sec()
                return amplitude_factor * math.cos(w * 2 * math.pi)
            return v_func

        v_funcs = [make_v_func() for _ in self._right_joint_names]

        def make_cmd(joint_names, elapsed):
            return dict([(joint, v_funcs[i](elapsed))
                         for i, joint in enumerate(joint_names)])

        print("Wobbling. Press Ctrl-C to stop...")
        while not rospy.is_shutdown():
            self._pub_rate.publish(100)
            elapsed = rospy.Time.now() - start
            cmd = make_cmd(self._left_joint_names, elapsed)
            self._left_arm.set_joint_velocities(cmd)
            cmd = make_cmd(self._right_joint_names, elapsed)
            self._right_arm.set_joint_velocities(cmd)
	    h.listener()
            rate.sleep()


def mainwobbler():
    """RSDK Joint Velocity Example: Wobbler

    Commands joint velocities of randomly parameterized cosine waves
    to each joint. Demonstrates Joint Velocity Control Mode.
    """
    arg_fmt = argparse.RawDescriptionHelpFormatter
    parser = argparse.ArgumentParser(formatter_class=arg_fmt,
                                     description=main.__doc__)
    parser.parse_args(rospy.myargv()[1:])

    print("Initializing node... ")
    rospy.init_node("rsdk_joint_velocity_wobbler")
    h = hand_shaker()
    h.get_info()
    wobbler = Wobbler(h)
    rospy.on_shutdown(wobbler.clean_shutdown)
    wobbler.wobble(h)
    print("Done.")

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
		self.arg=0
		self.o=0
		self.strt = rospy.Time.now()
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
#56 readings cost roughly 7kb
	def callback(self, data):
	     readinterval = rospy.Time.now() - self.strt
             if self.o<3000 and readinterval.to_sec() >0.01:
	     	self.F.write(repr(data.effort))
		print readinterval.to_sec()
		self.strt = rospy.Time.now()
		self.o=self.o+1
             if self.o>3000:
		self.F.close()
	     if self.o == 3000:
		self.o += 1
		print 'file written'
	def listener(self): 
	    rospy.Subscriber("/robot/joint_states", JointState, self.callback)
	
def main():
	mainwobbler()
	

	
#NEED TO REMOVE RIGHT ARM VARIABLES FROM EFFORT OUTPUT
#move along x for 2 centimeters from initial position in the positive direction, then reverses and goes 2 centimeters from initialhttps://github.com/RethinkRobotics/sdk-docs/wiki
# The equation that most likely describes the weights is T = T0 + Te + Tw, with Tw = KX, K=(T-T0)/X +-Te/X
if __name__ == "__main__":
    main()
# use head wobbler and tuck arms as examples
#records /current command being executed/ along with timestamps, /a header/ and the effort seqiable from the topic. 

#write output of /robot/JointStates and look for the effort variable
#write out the effort seqiable as a seq of values for each joint
