import os

# Define paths
pkg_name = "g1_moveit_config"
base_path = os.path.join("src", pkg_name)
config_path = os.path.join(base_path, "config")
launch_path = os.path.join(base_path, "launch")

# Create Directories
os.makedirs(config_path, exist_ok=True)
os.makedirs(launch_path, exist_ok=True)

# 1. Create package.xml
package_xml = f"""<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
<package format="3">
  <name>{pkg_name}</name>
  <version>0.1.0</version>
  <description>MoveIt config for G1</description>
  <maintainer email="user@todo.todo">User</maintainer>
  <license>TODO</license>

  <buildtool_depend>ament_cmake</buildtool_depend>

  <exec_depend>moveit_ros_move_group</exec_depend>
  <exec_depend>moveit_kinematics</exec_depend>
  <exec_depend>moveit_planners</exec_depend>
  <exec_depend>moveit_simple_controller_manager</exec_depend>
  <exec_depend>joint_state_publisher</exec_depend>
  <exec_depend>joint_state_publisher_gui</exec_depend>
  <exec_depend>tf2_ros</exec_depend>
  <exec_depend>xacro</exec_depend>
  <exec_depend>g1_description</exec_depend>

  <export>
    <build_type>ament_cmake</build_type>
  </export>
</package>
"""

# 2. Create CMakeLists.txt
cmake_lists = f"""cmake_minimum_required(VERSION 3.8)
project({pkg_name})
find_package(ament_cmake REQUIRED)

install(DIRECTORY config launch DESTINATION share/${{PROJECT_NAME}})
ament_package()
"""

# 3. Create G1.SRDF (The Brain - Defines Arms)
srdf_content = """<?xml version="1.0" encoding="UTF-8"?>
<robot name="g1_29dof_with_hand_rev_1_0">
    <group name="left_arm">
        <chain base_link="torso_link" tip_link="left_hand_palm_link"/>
    </group>
    <group name="right_arm">
        <chain base_link="torso_link" tip_link="right_hand_palm_link"/>
    </group>

    <group_state name="home" group="left_arm">
        <joint name="left_shoulder_pitch_joint" value="0"/>
        <joint name="left_shoulder_roll_joint" value="0"/>
        <joint name="left_shoulder_yaw_joint" value="0"/>
        <joint name="left_elbow_joint" value="0"/>
        <joint name="left_wrist_roll_joint" value="0"/>
        <joint name="left_wrist_pitch_joint" value="0"/>
        <joint name="left_wrist_yaw_joint" value="0"/>
    </group_state>
    <group_state name="home" group="right_arm">
        <joint name="right_shoulder_pitch_joint" value="0"/>
        <joint name="right_shoulder_roll_joint" value="0"/>
        <joint name="right_shoulder_yaw_joint" value="0"/>
        <joint name="right_elbow_joint" value="0"/>
        <joint name="right_wrist_roll_joint" value="0"/>
        <joint name="right_wrist_pitch_joint" value="0"/>
        <joint name="right_wrist_yaw_joint" value="0"/>
    </group_state>

    <virtual_joint name="virtual_joint" type="floating" parent_frame="world" child_link="base_link"/>

    <disable_collisions link1="torso_link" link2="left_shoulder_pitch_link" reason="Adjacent"/>
    <disable_collisions link1="torso_link" link2="right_shoulder_pitch_link" reason="Adjacent"/>
    <disable_collisions link1="torso_link" link2="head_link" reason="Adjacent"/>
    <disable_collisions link1="pelvis" link2="torso_link" reason="Adjacent"/>
</robot>
"""

# 4. Create kinematics.yaml
kinematics_yaml = """
left_arm:
  kinematics_solver: kdl_kinematics_plugin/KDLKinematicsPlugin
  kinematics_solver_search_resolution: 0.005
  kinematics_solver_timeout: 0.005

right_arm:
  kinematics_solver: kdl_kinematics_plugin/KDLKinematicsPlugin
  kinematics_solver_search_resolution: 0.005
  kinematics_solver_timeout: 0.005
"""

# 5. Create minimal launch file
launch_file = """import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from moveit_configs_utils import MoveItConfigsBuilder

def generate_launch_description():
    moveit_config = (
        MoveItConfigsBuilder("g1", package_name="g1_moveit_config")
        .robot_description(file_path="config/g1.urdf.xacro")
        .robot_description_semantic(file_path="config/g1.srdf")
        .trajectory_execution(file_path="config/moveit_controllers.yaml")
        .to_moveit_configs()
    )

    run_move_group_node = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        output="screen",
        parameters=[moveit_config.to_dict()],
    )

    rviz_config_file = os.path.join(
        get_package_share_directory("g1_moveit_config"), "config", "moveit.rviz"
    )

    run_rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", rviz_config_file],
        parameters=[
            moveit_config.robot_description,
            moveit_config.robot_description_semantic,
            moveit_config.planning_pipelines,
            moveit_config.robot_description_kinematics,
        ],
    )

    return LaunchDescription([run_move_group_node, run_rviz_node])
"""

# 6. Create dummy controllers yaml
controllers_yaml = """
controller_names: []
"""

# Write files
with open(os.path.join(base_path, "package.xml"), "w") as f: f.write(package_xml)
with open(os.path.join(base_path, "CMakeLists.txt"), "w") as f: f.write(cmake_lists)
with open(os.path.join(config_path, "g1.srdf"), "w") as f: f.write(srdf_content)
with open(os.path.join(config_path, "kinematics.yaml"), "w") as f: f.write(kinematics_yaml)
with open(os.path.join(config_path, "moveit_controllers.yaml"), "w") as f: f.write(controllers_yaml)
with open(os.path.join(launch_path, "demo.launch.py"), "w") as f: f.write(launch_file)

print("Manual MoveIt Config package generated at src/g1_moveit_config")
