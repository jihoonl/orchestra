cmake_minimum_required(VERSION 2.8.3)
project(orchestration_platform)
find_package(catkin REQUIRED COMPONENTS concert_rolemanager rospy op_msgs)

catkin_python_setup()

catkin_package(
  CATKIN_DEPENDS op_msgs
)

install(PROGRAMS
  scripts/concert_orchestra.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(DIRECTORY launch
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
