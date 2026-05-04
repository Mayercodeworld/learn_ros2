import rclpy
from rclpy.node import Node
import requests

class NovelPubNode(Node):
    def __init__(self, node_name: str):
        super().__init__(node_name)

        self.get_logger().info(f"{node_name}，启动！")

    def download(self, url: str):
        response = requests.get(url)
        response.encoding = 'utf-8'
        text = response.text
        self.get_logger().info(f"下载{url}，{len(text)}")
        
def main():
    rclpy.init()

    node = NovelPubNode('novel_pub')
    node.download('http://localhost:8000/novel1.txt')

    rclpy.spin(node)
    rclpy.shutdown()