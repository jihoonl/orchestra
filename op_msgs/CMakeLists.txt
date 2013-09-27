cmake_minimum_required(VERSION 2.8.3)
project(op_msgs)

find_package(catkin REQUIRED COMPONENTS message_generation message_runtime std_msgs concert_msgs)

# find_package(Boost REQUIRED COMPONENTS system)

## Generate messages in the 'msg' folder
add_message_files(
  FILES
  RoconService.msg
  ListRoconService.msg
  DedicatedApp.msg
)

add_service_files(
  FILES
  AddService.srv
  AddServiceFromFile.srv
  EnableService.srv
)

generate_messages(
  DEPENDENCIES
  std_msgs  # Or other packages containing msgs
  concert_msgs
)

###################################
## catkin specific configuration ##
###################################
catkin_package(
)

###########
## Build ##
###########

## Specify additional locations of header files
## Your package locations should be listed before other locations
# include_directories(include)
include_directories(
  ${catkin_INCLUDE_DIRS}
)

