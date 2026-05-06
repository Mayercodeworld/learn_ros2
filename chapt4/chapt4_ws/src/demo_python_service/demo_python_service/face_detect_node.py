import rclpy
from rclpy.node import Node
from chapt4_interfaces.srv import FaceDetector
import face_recognition
import cv2 # 视觉
from ament_index_python.packages import get_package_share_directory # 获取功能包share目录绝对路径
import os
import time
from cv_bridge import CvBridge
from rcl_interfaces.msg import SetParametersResult

class FaceDetectNode(Node):
    def __init__(self, node_name: str):
        super().__init__(node_name)
        # 创建服务
        self.services_ = self.create_service(FaceDetector, 'face_detect', self.detect_face_callback)
        self.bridge = CvBridge()
        
        # 参数声明
        self.declare_parameter('number_of_times_to_upsample', 1)
        self.declare_parameter('model', 'hog')
        self.number_of_times_to_upsample = self.get_parameter('number_of_times_to_upsample').value
        self.model = self.get_parameter('model').value

        self.default_image_path = os.path.join(get_package_share_directory('demo_python_service'), "resource/default.jpg")
        self.get_logger().info("人脸检测服务已经启动！")

        # 当外部执行参数更新后，会调用 paramer_callback 回调函数
        self.add_on_set_parameters_callback(self.parameter_callback)    

        # 设置自身节点参数的方法
        self.set_parameters([rclpy.Parameter('model', rclpy.Parameter.Type.STRING, 'cnn')])

    def parameter_callback(self, parameters) -> SetParametersResult : 
        for parameter in parameters:
            self.get_logger().info(f"{parameter.name}->{parameter.value}")
            if parameter.name == 'number_of_times_to_upsample':
                self.number_of_times_to_upsample = parameter.value
            if parameter.name == 'model':
                self.model = parameter.value
        return SetParametersResult(successful=True)
        
    def detect_face_callback(self, request, response):
        if request.image.data:
            cv_image = self.bridge.imgmsg_to_cv2(request.image)
        else:
            cv_image= cv2.imread(self.default_image_path)
            self.get_logger().info(f"传入图像为空，使用默认图像！")
        # cv_image 已经是一个opencv格式的图像
        start_time = time.time()
        self.get_logger().info(f"加载图像完成，开始识别！")

        # 检测人脸
        face_localtions = face_recognition.face_locations(cv_image, self.number_of_times_to_upsample, self.model)
        response.use_time = time.time() - start_time
        response.number = len(face_localtions)

        # 绘制人脸框
        for top, right, bottom, left in face_localtions:
            response.top.append(top)
            response.right.append(right)
            response.bottom.append(bottom)
            response.left.append(left)

        return response # 必须返回 response

def main():
    rclpy.init()
    node = FaceDetectNode('face_detect_node')
    rclpy.spin(node)
    rclpy.shutdown()