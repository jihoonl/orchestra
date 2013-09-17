#!/usr/bin/env python
#
# License: BSD
#   https://raw.github.com/robotics-in-concert/rocon_concert/hydro-devel/concert_orchestra/LICENSE
#
##############################################################################
# Imports
##############################################################################

import rospy
import re
import concert_msgs.msg as concert_msgs
import pydot

# local imports
from node import Node

##############################################################################
# Classes
##############################################################################


def yaml_to_implementation(yaml_data):
    '''
      If a solution implementation is being loaded, this stores the data.
    '''
    nodes     = []
    _topics   = []
    _actions  = []
    _edges    = []

        # This will need some modification if we go to multiple solutions on file.
    for node in yaml_data['nodes']:
        nodes.append(Node(node))
    _topics = yaml_data['topics']
    _actions = yaml_data['actions'] 
    _edges = yaml_data['edges'] 

    '''
      Might be easier just serving up the whole implementation file and saving that
      in a string here.
    '''
    implementation = concert_msgs.Implementation()
    for node in nodes:
        implementation.link_graph.nodes.append(concert_msgs.LinkNode(node.id, node.tuple, node.min, node.max, node.force_name_matching))
    for topic in _topics:
        implementation.link_graph.topics.append(concert_msgs.LinkConnection(topic['id'], topic['type']))
    for action in _actions:
        implementation.link_graph.actions.append(concert_msgs.LinkConnection(action['id'], action['type']))
    for edge in _edges:
        implementation.link_graph.edges.append(concert_msgs.LinkEdge(edge['start'], edge['finish'], edge['remap_from'], edge['remap_to']))

    return implementation
