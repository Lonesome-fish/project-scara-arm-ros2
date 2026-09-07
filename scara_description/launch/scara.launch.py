import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():
    # Caminho para o pacote scara_description
    scara_description_dir = get_package_share_directory('scara_description')

    # Argumento para pegar o caminho do arquivo xacro/urdf
    model_arg = DeclareLaunchArgument(
        name='model', 
        default_value=os.path.join(scara_description_dir, 'urdf', 'scara.urdf.xacro'),
        description='Absolute path to robot urdf file'
    )

    # Converte o Xacro para URDF puro usando o Command
    robot_description = ParameterValue(Command(['xacro ', LaunchConfiguration('model')]), value_type=str)

    # Nó do robot_state_publisher
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description}]
    )

    # Nó do joint_state_publisher_gui (para a janelinha de controle das juntas)
    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui'
    )

    # Nó do RViz2
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        # Puxa o arquivo de configuração salvo na etapa 9 da prática
        arguments=['-d', os.path.join(scara_description_dir, 'rviz', 'display.rviz')] 
    )

    # Retorna todos os nós e argumentos para serem executados
    return LaunchDescription([
        model_arg,
        joint_state_publisher_gui_node,
        robot_state_publisher_node,
        rviz_node
    ])