from setuptools import find_packages, setup
from glob import glob

package_name = 'demo_python_service'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # 处理需要随包分发的图像、配置文件或其他静态资源的标准做法
        # 图片文件安装到包的resource子目录下，这些资源可能在服务或节点中被使用
        ('share/' + package_name + "/resource", ['resource/default.jpg', 'resource/test1.png']),
        ('share/' + package_name + "/launch", glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='root',
    maintainer_email='2942182304@qq.com',
    description='TODO: Package description',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    # 用于定义可执行的命令行脚本
    entry_points={
        'console_scripts': [
            'learn_face_detect=demo_python_service.learn_face_detect:main',
            'face_detect_node=demo_python_service.face_detect_node:main',
            'face_detect_client_node=demo_python_service.face_detect_client_node:main',
        ],
    },
)
