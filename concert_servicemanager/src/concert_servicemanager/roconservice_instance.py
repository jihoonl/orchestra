#! /usr/bin/env python

import rospy
import roslaunch
from utils import *
from op_msgs.msg import *
from op_msgs.srv import *

class RoconServiceInstance(object):
    data = None
    launcher = None
    status = None

    def __init__(self,data):
        self.data = data 
        self.status = RoconService.DEACTIVATED

    def get_name(self):
        return self.data['name']

    def activate(self):
        if self.status == RoconService.ACTIVATED:
            self.log("It is already activated")
        else:
            self.launcher = roslaunch.ROSLaunch() 
            self.launcher.start()
            self.log("Activated")
            self.status = RoconService.ACTIVATED

    def deactivate(self):
        if self.status != RoconService.DEACTIVATED:
            self.launcher.stop()
            self.launcher = None
            self.log("Deactivated")
            self.status = RoconService.DEACTIVATED
        else:
            self.log("It has already deactivated")
    
    def to_msg(self):
        s = RoconService()
        s.name = self.data['name']
        s.description = self.data['description']
        s.author = self.data['author']
        s.type = self.data['type']
        s.status = self.status
        s.implementation = yaml_to_implementation(self.data['implementation'])

        return s

    def log(self,msg):
        rospy.loginfo(self.data['name'] + " : " + str(msg)) 
