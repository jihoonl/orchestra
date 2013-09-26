#! /usr/bin/env python

import yaml
import rospy
import traceback

from roconservice_instance import *
from op_msgs.msg import *
from op_msgs.srv import *

class ServiceManager(object):

    rocon_services = {}

    param = {}
    srv = {}
    pub = {}

    def __init__(self):    
        rospy.loginfo("Hola! in init")

        self.setup_srvs()
        self.setup_pubs()
        self.update()


    def setup_srvs(self):
        self.srv['add_a_service_from_file'] =rospy.Service('add_a_service_from_file',AddServiceFromFile,self.process_add_service_from_file)
        self.srv['add_a_service'] =rospy.Service('add_a_service',AddServiceFromFile,self.process_add_service)

        self.srv['activate_a_service'] = rospy.Service('activate_a_service',ActivateService,self.process_activate_service)

    def setup_pubs(self):
        self.pub['list_service'] = rospy.Publisher('list_service',ListRoconService,latch = True)


    def process_add_service(self,req):
        # TODO
        self.update()
        return AddServiceResponse(False)

    def process_add_service_from_file(self,req):
        resp = False

        try:
            service_name, service = self.load_service_from_file(req.filename)
            self.rocon_services[service_name] = service
            rospy.loginfo("Service["+service_name+"] has been added")
            resp = True
        except Exception as e:
            rospy.loginfo("Error in " + str(e) + " while parsing " +str(req.filename))
            tb = traceback.format_exc()
            rospy.loginfo(str(tb))
            pass
            
        self.update()

        return AddServiceFromFileResponse(resp)

    def process_activate_service(self,req):
        
        act = "Activating" if req.activate else "Deactivating"
        rospy.loginfo(str(act)+" Service - " + str(req.name))

        flag = True
        msg = "Success"

        try:
            if req.activate:
                self.rocon_services[req.name].activate()
            else:
                self.rocon_services[req.name].deactivate()
        except Exception as e:
            flag = False
            msg = str(e)
            
        self.update()
        return ActivateServiceResponse(flag,msg)

    def update(self):
        rs = [v.to_msg() for k,v in self.rocon_services.items()]
        self.pub['list_service'].publish(rs)

    def load_service_from_file(self,filename):
        with open(filename) as f:
            yaml_data = yaml.load(f)
            rsi = RoconServiceInstance(yaml_data)

        return rsi.get_name(), rsi

    def spin(self):
        rospy.loginfo("Hola! in spin")
        rospy.spin()
