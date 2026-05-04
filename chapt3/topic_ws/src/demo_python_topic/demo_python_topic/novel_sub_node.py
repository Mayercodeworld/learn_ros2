import espeakng
import rclpy
from rclpy.node import Node
import requests
from example_interfaces.msg import String
from queue import Queue
import threading
import time

class NovelSubNode(Node):
    def __init__(self, node_name: str):
        super().__init__(node_name)
        self.get_logger().info(f"{node_name}，启动！")
        self.novels_quene_ = Queue()
        self.novel_subscriber_ = self.create_subscription(String, 'novel', self.novel_callback, 10)
        # 新建子线程处理朗读
        self.speech_thread_ = threading.Thread(target=self.speake_thread)
        self.speech_thread_.start()

    # 有消息时就会调用
    def novel_callback(self, msg):
        self.novels_quene_.put(msg.data)

    def speake_thread(self):
        speaker = espeakng.Speaker()
        speaker.voice = 'zh'

        while rclpy.ok(): # 检测当前 ROS 上下文是否 ok
            if self.novels_quene_.qsize() > 0:
                text = self.novels_quene_.get()
                self.get_logger().info(f"朗读：{text}")
                speaker.say(text)
                speaker.wait() # 等说完
            else:
                # 让当前的线程休眠 1 s
                time.sleep(1)
    
def main():
    rclpy.init()
    node = NovelSubNode('novel_sub')
    rclpy.spin(node)
    rclpy.shutdown()