import launch
import launch_ros

def generate_launch_description():
    """
    产生launch描述
    """
    action_node_turtlesim_node = launch_ros.actions.Node(
        package='turtlesim', # 功能包
        executable='turtlesim_node', # 可执行文件
        output='screen' # 输出格式
    )

    action_node_partol_client = launch_ros.actions.Node(
        package='demo_cpp_service', 
        executable='partol_client', 
        output='log' 
    )

    action_node_turtle_control = launch_ros.actions.Node(
        package='demo_cpp_service', 
        executable='turtle_control', 
        output='both'
    )

    return launch.LaunchDescription([
        # actions 动作
        action_node_turtlesim_node,
        action_node_partol_client,
        action_node_turtle_control
    ])