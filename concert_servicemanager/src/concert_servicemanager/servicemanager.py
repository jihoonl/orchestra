#! /usr/bin/env python

import yaml
import rospy
import traceback

from utils import *
from roconservice_instance import *
from op_msgs.msg import *
from op_msgs.srv import *
from concert_msgs.msg import *

class ServiceManager(object):

    rocon_services = {}

    param = {}
    srv = {}
    pub = {}
    sub = {}

    def __init__(self):    
        self.log("Hola! in init")

        self.setup_srvs()
        self.setup_pubs()
        self.setup_subs()
        self.update()


    def setup_srvs(self):
        self.srv['add_a_service_from_file'] =rospy.Service('add_a_service_from_file',AddServiceFromFile,self.process_add_service_from_file)
        self.srv['add_a_service'] =rospy.Service('add_a_service',AddServiceFromFile,self.process_add_service)

        self.srv['enable_service'] = rospy.Service('enable_service',EnableService,self.process_enable_service)

    def setup_pubs(self):
        self.pub['list_service'] = rospy.Publisher('list_service',ListRoconService,latch = True)

    def setup_subs(self):
        self.sub['list_concert_clients'] = rospy.Subscriber('list_concert_clients',ConcertClients,self.process_list_concert_clients)


    def process_add_service(self,req):
        # TODO
        self.update()
        return AddServiceResponse(False)

    def process_add_service_from_file(self,req):
        resp = False

        try:
            service_name, service = self.load_service_from_file(req.filename)
            self.rocon_services[service_name] = service
            self.log("["+service_name+"] has been added")
            resp = True
        except Exception as e:
            self.log("Error in " + str(e) + " while parsing " +str(req.filename))
            tb = traceback.format_exc()
            self.log(str(tb))
            pass
            
        self.update()

        return AddServiceFromFileResponse(resp)

    def process_enable_service(self,req):
        act = "Enabling" if req.enable else "Disabling"
        self.log(str(act)+" Service - " + str(req.name))

        flag = True
        msg = "Success"

        try:
            if req.enable:
                self.rocon_services[req.name].enable()
            else:
                self.rocon_services[req.name].disable()
        except Exception as e:
            flag = False
            msg = str(e)
            
        self.update()
        return EnableServiceResponse(flag,msg)

    def process_list_concert_clients(self,msg):
        '''
            Receives a list of clients.
            Creates a list of tuples
            pass the list to check the current client lists fulfills services' requirements
            then update status of services

            TODO: Current just passes concert client lists directly to the service instance
                 this will be re-developed when dedicated_component idea is clear
        '''
#        tuples = create_tuple_dict(msg.clients)
        clients = {}
        for c in msg.clients:
            clients[c.name] = copy.deepcopy(c)

        for k, v in self.rocon_services.items():
            v.update_client_status(clients)

        self.update()

    def update(self):
        rs = [v.to_msg() for k,v in self.rocon_services.items()]
        self.pub['list_service'].publish(rs)

    def load_service_from_file(self,filename):
        with open(filename) as f:
            yaml_data = yaml.load(f)
            rsi = RoconServiceInstance(yaml_data)

        return rsi.get_name(), rsi

    def log(self,msg):
        rospy.loginfo("Service Manager \t: " + str(msg))

    def spin(self):
        self.log("Hola! in spin")
        rospy.spin()
