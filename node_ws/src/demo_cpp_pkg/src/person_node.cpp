// 双引号：现在项目目录查找，再在系统目录查找
#include "rclcpp/rclcpp.hpp"

// 尖括号：直接在系统目录查找
// #include <iostream>

/**
 * C++ 继承外部包中的类
 */
class PersonNode : public rclcpp::Node
{
    
private:
    // 私有属性
    std::string name_;
    int age_;

public:
    // 构造函数
    /* &var 引用传递，避免拷贝 */
    PersonNode(const std::string &node_name, const std::string &name, const int &age)
        : Node(node_name) /* 调用父类的构造函数，等同于Python中的super().__init__*/
    {
        this->name_ = name;
        this->age_ = age;
    };
    // 方法
    void eat(const std::string &food_name)
    {
        // 宏定义的 RCLCPP_INFO
        RCLCPP_INFO(this->get_logger(), "我是%s, %d岁，爱吃%s", this->name_.c_str(), this->age_, food_name.c_str());
    };
};

int main(int argc, char** argv) // argc：命令行启动时传入的参数数量 argv：所有传参二维数组
{
    rclcpp::init(argc, argv); // 初始化

    // 智能指针 shared_ptr：基于引用计数
    auto node = std::make_shared<PersonNode>("person_node", "里斯", 18); // 创建节点
    RCLCPP_INFO(node->get_logger(), "你好 person_node");
    node->eat("鱼香肉丝");
    rclcpp::spin(node);
    rclcpp::shutdown();

    return 0;
}