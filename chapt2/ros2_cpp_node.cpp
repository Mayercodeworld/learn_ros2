#include "rclcpp/rclcpp.hpp" 

int main(int argc, char** argv) // argc：命令行启动时传入的参数数量 argv：所有传参二维数组
{
    rclcpp::init(argc, argv); // 初始化
    auto node = std::make_shared<rclcpp::Node>("cpp_node"); // 创建节点
    RCLCPP_INFO(node->get_logger(), "你好C++ 节点");
    
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}