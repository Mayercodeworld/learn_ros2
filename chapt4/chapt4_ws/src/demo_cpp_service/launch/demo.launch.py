import launch
import launch_ros
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    """
    产生launch描述
    """
    # 获取配置文件路径
    config_file = os.path.join(
        get_package_share_directory('demo_cpp_service'),
        'config',
        'node_params.yaml'
    )

    # 检查配置文件是否存在
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"未找到配置文件：{config_file}")

    # 1. 声明一个 launch 参数
    action_declare_arg_background_g = launch.actions.DeclareLaunchArgument('launch_arg_bg', default_value="150")
    
    action_node_turtlesim_node = launch_ros.actions.Node(
        package='turtlesim', # 功能包
        executable='turtlesim_node', # 可执行文件
        # 2. 把 launch 的参数手动传递给某个节点
        # 从 launch 中获取参数，需要通过转换为节点可用参数
        # parameters=[{'background_g': launch.substitutions.LaunchConfiguration('launch_arg_bg', default="150")}],
        
        parameters=[config_file],
        output='screen' # 输出格式
    )


    action_node_partol_client = launch_ros.actions.Node(
        package='demo_cpp_service', 
        executable='partol_client', 
        parameters=[config_file],
        output='log' 
    )

    action_node_turtle_control = launch_ros.actions.Node(
        package='demo_cpp_service', 
        executable='turtle_control', 
        parameters=[config_file],
        output='both'
    )

    return launch.LaunchDescription([
        # actions 动作
        action_declare_arg_background_g,
        action_node_turtlesim_node,
        action_node_partol_client,
        action_node_turtle_control
    ])