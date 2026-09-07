import os
import re
import xacro
from ament_index_python.packages import get_package_share_directory, get_package_prefix

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, SetEnvironmentVariable
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node

def generate_launch_description():
    scara_description_dir = get_package_share_directory('scara_description')
    scara_description_share = os.path.join(get_package_prefix('scara_description'), 'share')
    gazebo_ros_dir = get_package_share_directory('gazebo_ros')

    # 1. Caminho fixo para o arquivo xacro
    xacro_file = os.path.join(scara_description_dir, 'urdf', 'scara.urdf.xacro')

    # 2. Processa o arquivo Xacro nativamente via Python
    doc = xacro.process_file(xacro_file)
    robot_description_raw = doc.toxml()
    
    # 3. Limpeza Agressiva: Remove cabeçalho e marca d'água/comentários XML
    clean_xml = robot_description_raw.replace('<?xml version="1.0" ?>', '')
    clean_xml = re.sub(r'<!--.*?-->', '', clean_xml, flags=re.DOTALL)
    robot_description_clean = clean_xml

    model_arg = DeclareLaunchArgument(
        name='model', 
        default_value=xacro_file,
        description='Absolute path to robot urdf file'
    )

    env_var = SetEnvironmentVariable('GAZEBO_MODEL_PATH', scara_description_share)

    # 4. Injeta a string limpa diretamente no nó
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': robot_description_clean,
            'use_sim_time': True
        }]
    )

    start_gazebo_server = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gazebo_ros_dir, 'launch', 'gzserver.launch.py')
        )
    )

    start_gazebo_client = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gazebo_ros_dir, 'launch', 'gzclient.launch.py')
        )
    )

    spawn_robot = Node(
        package='gazebo_ros', 
        executable='spawn_entity.py',
        arguments=[
            '-entity', 'scara',
            '-topic', 'robot_description',
        ],
        parameters=[{'use_sim_time': True}],
        output='screen'
    )

    return LaunchDescription([
        env_var,
        model_arg,
        start_gazebo_server,
        start_gazebo_client,
        robot_state_publisher_node,
        spawn_robot
    ])