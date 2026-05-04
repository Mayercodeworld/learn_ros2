
import rclpy
from rclpy.node import Node
"""
PersonNode：人类节点
继承 Node 类，其属性和方法均被继承
"""
class PersonNode(Node):
    def __init__(self, node_name: str, name: str, age: int):
        """
        初始化阶段：使用super().__init__()
        运行阶段：使用self.method()
        """
        super().__init__(node_name)
        # 类属性
        self.name = name
        self.age = age

    def eat(self, food_name: str):
        """
        方法：吃东西
        :food_name 食物名称
        """
        # print(f"{self.name}，{self.age}岁，爱吃{food_name}")
        
        # 调用Node 类中的get_logger方法，并打印日志
        self.get_logger().info(f"{self.name}，{self.age}岁，爱吃{food_name}")
    

def main():
    rclpy.init()
    node = PersonNode('zhangsan', '法外狂徒张三', 10)
    # node1 = PersonNode('法外狂徒王五', 15)
    node.eat('鱼香肉丝')
    # node1.eat('排骨')
    rclpy.spin(node)
    rclpy.shutdown()
