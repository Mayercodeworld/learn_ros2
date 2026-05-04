import rclpy
from rclpy.node import Node

def main():
    rclpy.init() # 初始化工作，分配资源
    # 创建一个节点
    node = Node("python_node")
    node.get_logger().info('你好 Python 节点--')
    node.get_logger().warn('你好 Python 节点')
    rclpy.spin(node) # 运行节点
    rclpy.shutdown()

if __name__=="__main__":
    main()