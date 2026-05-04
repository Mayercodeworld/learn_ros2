from setuptools import find_packages, setup

"""
ROS 2 Python 功能包的构建说明书
告诉 colcon 编译工具，代码结构是怎样的、有哪些依赖，
以及如何把 Python 脚本变成可以运行的指令
"""

package_name = 'demo_python_pkg'

setup(
    name=package_name,
    version='0.0.0', # 版本号
    # 自动扫描当前目录下包含 __init__.py 的文件夹(python 包中的模块)
    packages=find_packages(exclude=['test']), # 自动查找包
    data_files=[
        # 系统的索引目录里注册这个包。如果没有这一行，ros2 run 指令将找不到包 
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        # 将 package.xml 文件拷贝到安装目录，以便 ROS 2 系统在运行时读取包的元数据
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='root', # 维护者名字
    maintainer_email='root@todo.todo',
    description='TODO: Package description', # 描述信息
    license='Apache-2.0', # 软件许可证
    extras_require={
        'test': [
            'pytest',
        ],
    },
    # 可执行程序入口
    entry_points={
        'console_scripts': [
            # python_node: 在终端里运行的命令名称
            # demo_python_pkg.python_demo_pkg:main: 向代码的物理路径
            # 编译完成后可以直接：ros2 run demo_python_pkg python_node
            'python_node = demo_python_pkg.python_node:main'            
        ],
    },
)
