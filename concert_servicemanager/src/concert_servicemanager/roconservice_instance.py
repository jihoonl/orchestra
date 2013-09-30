#! /usr/bin/env python

import rospy
import roslaunch
import copy

from utils import *
from op_msgs.msg import *
from op_msgs.srv import *
from implementation import *
from concert_orchestra import compatibility_tree

class RoconServiceInstance(object):
    data = None
    launcher = None
    status = None

    # keep track the previous status. When service disabled by insufficient clients and become sufficient by accepting new clients, 
    # previous_status can be used to reenable the service automatically
    previous_status = None 

    def __init__(self,data):
        self.data = data
        self.status = RoconService.DISABLED

    def get_name(self):
        return self.data['name']

    def enable(self):
        if self.status == RoconService.ENABLED:
            self.log("It is already enabled")
            raise Exception("Service is already enabled")
        elif self.status == RoconService.DISABLED:
            self.start()
        elif self.status == RoconService.INSUFFICIENT_CLIENTS:
            raise Exception("System does not have enough clients to enable the service")
        else:
            # TODO Should we specify the reasons of errors?
            raise Exception("Service is in unknown error status...")

    def disable(self):
        if self.status == RoconService.ENABLED:
            self.stop()
        elif self.status == RoconService.DISABLED:
            raise Exception("Service is already disabled")
        elif self.status == RoconService.INSUFFICIENT_CLIENTS:
            raise Exception("System does not have enough clients to enable the service")
        else:
            raise Exception("Unkonw Error!")

    def start(self):
        # Check whether all of dedicated apps are present
        # If everyone is present, starts launcher and nodes with implementation
        # if not, raise exception
        self.launcher = roslaunch.ROSLaunch() 
        self.launcher.start()
        self.log("Enabled")
        self.previous_status = self.status
        self.status = RoconService.ENABLED

    def stop(self):
        self.launcher.stop()
        self.launcher = None
        self.log("Disabled")
        self.previous_status = self.status
        self.status = RoconService.DISABLED

    def to_msg(self):
        '''
            parses yaml data and creates RoconService msg
        '''
        s = RoconService()
        s.name = self.data['name']
        s.description = self.data['description']
        s.author = self.data['author']
        s.dedicated_apps = yaml_to_dedicated_apps(self.data['dedicated_apps']) 
        s.status = self.status
        
        s.implementation = yaml_to_implementation_msg(self.data['implementation'])

        return s

    def update_client_status(self,clients):
        '''
            compares app tuples and dedicated app lists.
            updates whether the service can be enabled
            then disable the service if it is insufficient client status 

            TODO: All of nodes in implementation is used as dedicated components at the moment.
                  Will replace this in later milestone 
        '''
        self.log("in update_client_status")
        impl = Implementation(self.data['implementation'],self.data['name'])
        nodes = impl.nodes
        tree = compatibility_tree.create_compatibility_tree(nodes,clients)
    
        self.log(str(tree))


        
    def log(self,msg):
        rospy.loginfo(self.data['name'] + " : " + str(msg)) 
