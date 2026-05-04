import rclpy
from rclpy.node import Node
import requests
from example_interfaces.msg import String
from queue import Queue

class NovelPubNode(Node):
    def __init__(self, node_name: str):
        super().__init__(node_name)
        self.get_logger().info(f"{node_name}，启动！")
        self.novels_queue_ = Queue() # 创建队列
        """
        创建话题发布者
        self.create_publisher(消息类型, 话题名称, 队列大小)
        队列大小：（当发布速度 > 订阅速度时，最多缓存10条消息）
        """
        self.novel_publisher_ = self.create_publisher(String, 'novel', 10)
        # 创建定时器
        self.create_timer(5, self.timer_callback)
        
    def timer_callback(self):
        # 间隔 5 秒发布
        if self.novels_queue_.qsize() > 0:
            # 从队列中读取一个
            line = self.novels_queue_.get()
            msg = String()
            msg.data = line
            self.novel_publisher_.publish(msg)
            self.get_logger().info(f"发布了：{msg}")

    def download(self, url: str):
        response = requests.get(url)
        response.encoding = 'utf-8'
        text = response.text
        self.get_logger().info(f"下载{url}，{len(text)}")
        # 放入队列
        for line in text.splitlines():
            self.novels_queue_.put(line)

def main():
    rclpy.init()
    node = NovelPubNode('novel_pub')
    node.download('http://localhost:8000/novel1.txt')
    rclpy.spin(node)
    rclpy.shutdown()