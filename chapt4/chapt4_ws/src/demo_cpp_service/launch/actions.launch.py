import launch
import launch_ros
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    action_declare_startup_rqt = launch.actions.DeclareLaunchArgument('startup_rqt', default_value="False")

    startup_rqt = launch.substitutions.LaunchConfiguration('startup_rqt', default="False")

    # 动作 1. 启动其他Launch
    multism_launch_path = [get_package_share_directory('turtlesim'), '/launch/', 'multisim.launch.py']
    action_include_launch = launch.actions.IncludeLaunchDescription(
        launch.launch_description_sources.PythonLaunchDescriptionSource(
            multism_launch_path
        )
    )

    # 动作 2. 打印数据
    action_log_info = launch.actions.LogInfo(msg=str(multism_launch_path))

    # 动作 3. 执行进程（执行一个命令行 ros2 topic list）
    # if startup_rqt
    #   run:rqt
    action_topic_list = launch.actions.ExecuteProcess(
        condition = launch.conditions.IfCondition(startup_rqt),
        cmd=['rqt']
    )

    # 动作 4. 组织动作成组，把多个动作放到一组
    action_group = launch.actions.GroupAction([
        # 动作 5. 定时器，定时启动时间
        launch.actions.TimerAction(period=2.0, actions=[action_include_launch]), # 在第2秒时启动
        launch.actions.TimerAction(period=4.0, actions=[action_topic_list]),
    ])

    return launch.LaunchDescription([
        # actions 动作
        action_declare_startup_rqt,
        action_log_info,
        action_group,
    ])