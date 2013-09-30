#! /usr/bin/env python

import rospy

from node import Node 
from concert_orchestra import implementation


class Implementation(implementation.Implementation):

    nodes    = []
    _topics  = []
    _actions = []
    _edges   = []
    _dot_graph = ""

    def __init__(self,yaml,name):
        self._name = name
        self.nodes = []
        for param in yaml['nodes']:
            self.nodes.append(Node(param))

        self._topics  = yaml['topics'] if yaml['topics'] else []
        self._actions = yaml['actions'] if yaml['actions'] else []
        self._edges   = yaml['edges'] if yaml['edges'] else []
        
