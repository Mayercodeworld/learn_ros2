import rclpy
from demo_python_pkg.person_node import PersonNode

"""
WriterNode：作家节点
继承 PersonNode 节点
"""
class WriterNode(PersonNode):
    def __init__(self, node_name: str, name: str, age: int, book: str):
        # 调用父类的__init__方法
        super().__init__(node_name, name, age)
        self.book = book
    
    def write(self):
        self.get_logger().info(f"{self.name}，{self.age}正在创作{self.book}")

def main():
    rclpy.init()
    node = WriterNode('zhangsan', '张三', 10, '论快速成功')
    node.eat('鱼香肉丝')
    node.write()
    rclpy.spin(node)
    rclpy.shutdown()
