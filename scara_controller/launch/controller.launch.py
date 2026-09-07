import os
import re
import xacro
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch.conditions import UnlessCondition
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    is_sim = LaunchConfiguration('is_sim')

    is_sim_arg = DeclareLaunchArgument(
        'is_sim',
        default_value='True',
        description='Define se a execucao e em ambiente de simulacao'
    )

    # 1. Obtem o caminho do arquivo xacro
    xacro_file = os.path.join(
        get_package_share_directory("scara_description"),
        "urdf",
        "scara.urdf.xacro",
    )

    # 2. Processa o xacro nativamente em Python passando o is_sim
    doc = xacro.process_file(xacro_file, mappings={'is_sim': 'true'})
    robot_description_raw = doc.toxml()
    
    # 3. Limpeza Agressiva: Remove cabeçalho e marca d'água/comentários XML
    clean_xml = robot_description_raw.replace('<?xml version="1.0" ?>', '')
    clean_xml = re.sub(r'<!--.*?-->', '', clean_xml, flags=re.DOTALL)
    robot_description_clean = clean_xml

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{
            "robot_description": robot_description_clean,
            "use_sim_time": is_sim
        }],
    )

    controller_manager = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[
            {
                "robot_description": robot_description_clean,
                "use_sim_time": is_sim
            },
            os.path.join(
                get_package_share_directory("scara_controller"),
                "config",
                "scara_controllers.yaml",
            ),
        ],
        condition=UnlessCondition(is_sim),
    )

    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "joint_state_broadcaster",
            "--controller-manager",
            "/controller_manager",
        ],
        parameters=[{"use_sim_time": is_sim}],
    )

    arm_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["arm_controller", "--controller-manager", "/controller_manager"],
        parameters=[{"use_sim_time": is_sim}],
    )

    gripper_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["gripper_controller", "--controller-manager", "/controller_manager"],
        parameters=[{"use_sim_time": is_sim}],
    )

    return LaunchDescription(
        [
            is_sim_arg,
            robot_state_publisher_node,
            controller_manager,
            joint_state_broadcaster_spawner,
            arm_controller_spawner,
            gripper_controller_spawner,
        ]
    )