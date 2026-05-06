import rclpy
from rclpy.node import Node
from chapt4_interfaces.srv import FaceDetector
import face_recognition
import cv2 # 视觉
from ament_index_python.packages import get_package_share_directory # 获取功能包share目录绝对路径
import os
import time
from cv_bridge import CvBridge
from rcl_interfaces.srv import SetParameters
from rcl_interfaces.msg import Parameter, ParameterValue, ParameterType

class FaceDetectClientNode(Node):
    def __init__(self, node_name: str):
        super().__init__(node_name)
        self.bridge = CvBridge()
        self.default_image_path = os.path.join(get_package_share_directory('demo_python_service'), "resource/test1.png")
        self.get_logger().info("人脸检测客户端已经启动！")
        self.client = self.create_client(FaceDetector, 'face_detect')
        self.image = cv2.imread(self.default_image_path)


    def call_set_parameters(self, parameters):
        """
        调用服务，修改其他节点的参数值
        """
        # 1. 创建一个客户端，等待服务上线
        update_param_client = self.create_client(SetParameters, '/face_detect_node/set_parameters')
        while update_param_client.wait_for_service(timeout_sec=1.0) is False:
            self.get_logger().info("等待参数更新服务端上线")
        
        # 2. 创建 request
        request = SetParameters.Request()
        request.parameters = parameters

        # 3. 调用服务端更新参数
        future = update_param_client.call_async(request)
        rclpy.spin_until_future_complete(self, future)
        response = future.result()
        return response

    def update_detect_model(self, model = 'hog'):
        """
        根据传入的model，构造Paramters，然后调用 call_set_parameters更新服务端的参数
        """
        # 1. 创建参数对象
        param = Parameter()
        param.name = 'model'
        # 2. 创建 param_value
        param_value = ParameterValue()
        param_value.string_value = model
        param_value.type = ParameterType.PARAMETER_STRING
        param.value = param_value

        # 3. 请求更新参数
        response = self.call_set_parameters([param])
        for result in response.results:
            self.get_logger().info(f"设置参数结果：{result.successful} {result.reason}")


    def send_request(self):
        # 1. 判断服务端是否在线（阻塞）
        while self.client.wait_for_service(timeout_sec=1.0) is False:
            self.get_logger().info("等待服务端上线")
        
        # 2. 构造 Request
        request = FaceDetector.Request()
        # 将图像转换为 FaceDetector 及 sensor_msgs 的格式
        request.image = self.bridge.cv2_to_imgmsg(self.image)

        # 3. 发送请求并等待处理完成
        future = self.client.call_async(request) # 创建一个异步请求，现在的future 并没有包含响应结果，需要等待服务端处理完成才会把结果放到future中
        # while not future.done():
        #     time.sleep(1.0) # 休眠当前线程，等待服务处理完成，造成当前线程无法再接收来自服务端的返回，导致永远没有办法完成
        
        # 边去检测future 边去检测spin中的服务（不会直接造成阻塞）
        # rclpy.spin_until_future_complete(future) # 只有future完成获取后，该地方才会继续往下执行，其他地方并未阻塞
        
        # 使用回调函数解决
        def result_callback(result_future):
            response = result_future.result() # 获取响应        
            self.get_logger().info(f"接收到响应，共检测到 {response.number} 张人脸，耗时 {response.use_time} s")
            self.show_response(response)

        future.add_done_callback(result_callback)

    def show_response(self, response):
        for i in range(response.number):
            top = response.top[i]
            right = response.right[i]
            bottom = response.bottom[i]
            left = response.left[i]
            cv2.rectangle(self.image, (left, top), (right, bottom), (255, 0, 0), 4) # 绘制矩形框
        # cv2.imshow('Face Detect Result', self.image)
        # cv2.waitKey(0) # 也是阻塞，导致 spin 无法正常运行

def main():
    rclpy.init()
    node = FaceDetectClientNode('face_detect_client_node')
    node.update_detect_model('hog')
    node.send_request()
    node.update_detect_model('cnn')
    node.send_request()
    rclpy.spin(node)
    rclpy.shutdown()