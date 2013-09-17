#! /usr/bin/env python

import yaml
import rospy

from op_msgs.msg import *
from op_msgs.srv import *

class RoconServiceManager(object):

    rocon_services = []

    srv = {}
    pub = {}

    def __init__(self):    
        rospy.loginfo("Hola! in init")

        self.setup_srvs()
        self.setup_pubs()
        self.update()
        

    def setup_srvs(self):
        self.srv['add_a_service_from_file'] =rospy.Service('~add_a_service_from_file',AddServiceFromFile,self.process_add_service_from_file)
        self.srv['add_a_service'] =rospy.Service('~add_a_service',AddServiceFromFile,self.process_add_service)

    def setup_pubs(self):
        self.pub['list_service'] = rospy.Publisher('~list_service',ListRoconService,latch = True)


    def process_add_service(self,req):
        # TODO

        self.update()
        return AddServiceResponse(False)

    def process_add_service_from_file(self,req):

        resp = False

        try:
            service = self.load_service_from_file(req.filename)
            self.rocon_services.append(service)
            resp = True
        except:
            pass
            
        self.update()

        return AddServiceFromFileResponse(resp)
    
    def update(self):
        self.pub['list_service'].publish(self.rocon_services)

    def load_service_from_file(self,filename):
        with open(filename) as f:
            yaml_data = yaml.load(f)

        s = RoconService()
        s.name = yaml_data['name']
        s.desciption = yaml_data['desciption']

        return s

    def spin(self):
        rospy.loginfo("Hola! in spin")
        rospy.spin()
