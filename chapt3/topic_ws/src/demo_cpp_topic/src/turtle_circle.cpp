#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/twist.hpp"
#include "chrono"

using namespace std::chrono_literals;

class TurtleCircleNode : public rclcpp::Node
{
private:
    rclcpp::TimerBase::SharedPtr timer_; // 定时器
    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr publisher_; // 发布者的智能指针


public:
    explicit TurtleCircleNode(const std::string& node_name)
    :Node(node_name)
    {
        publisher_ = this->create_publisher<geometry_msgs::msg::Twist>("/turtle1/cmd_vel", 10);
        /**
         * 成员函数与普通函数不同，它需要一个隐式的 this 指针
         * &TurtleCircleNode::timer_callback：指向成员函数的指针
         * this：当前对象的指针
         * std::bind 将两者绑定，创建一个可调用对象
         */
        // timer_ = this->create_wall_timer(1000ms, std::bind(&TurtleCircleNode::timer_callback, this));

        // 或者可以使用 lambda 表达式解决

        // 传入的都是包含函数调用机制的类对象
        timer_ = this->create_wall_timer(1000ms, [this]()->void {this->timer_callback();});
    }

    void timer_callback() {
        auto msg = geometry_msgs::msg::Twist();
        msg.linear.x = 1.0;
        msg.angular.z = 0.5;
        publisher_ -> publish(msg);
    }
};

int main(int argc, char* argv[]) 
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<TurtleCircleNode>("turtle_circle");
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
