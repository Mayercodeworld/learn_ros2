#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/twist.hpp"
#include "turtlesim/msg/pose.hpp"
#include "chrono"
#include "chapt4_interfaces/srv/partol.hpp"
#include "rcl_interfaces/msg/set_parameters_result.hpp"

using Partol = chapt4_interfaces::srv::Partol;
using SetParametersResult = rcl_interfaces::msg::SetParametersResult;

using namespace std::chrono_literals;

class TurtleControlNode : public rclcpp::Node
{
private:
    OnSetParametersCallbackHandle::SharedPtr parameter_callback_handler_;
    rclcpp::Service<Partol>::SharedPtr partol_service_;
    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr publisher_; // 发布者的智能指针
    rclcpp::Subscription<turtlesim::msg::Pose>::SharedPtr subcriber_; // 订阅者的智能指针
    
    double target_x_{1.0}; // C++ 11 初始化语法
    double target_y_{1.0};
    double k_{1.0}; // 比例系数
    double max_speed_{3.0}; // 最大速度 

public:
    explicit TurtleControlNode(const std::string& node_name)
    :Node(node_name)
    {
        this->declare_parameter("k", 1.0);
        this->declare_parameter("max_speed", 1.0);
        this->get_parameter("k", k_);
        this->get_parameter("max_speed", max_speed_);
        this->set_parameter(rclcpp::Parameter("k", 2.0));
        // 参数更新时，调用回调函数
        parameter_callback_handler_ = this->add_on_set_parameters_callback(
            [&](const std::vector<rclcpp::Parameter> &parameters) 
            -> SetParametersResult {
                SetParametersResult result;
                result.successful = true;
                for (const auto &parameter : parameters) {
                    RCLCPP_INFO(this->get_logger(), "更新参数的值%s = %f", parameter.get_name().c_str(), parameter.as_double());
                    if (parameter.get_name() == "k") {
                      k_ = parameter.as_double();
                    }
                    if (parameter.get_name() == "max_speed") {
                      max_speed_ = parameter.as_double();
                    }
                }
                return result;
            }
        );

        partol_service_ = this->create_service<Partol>("partol", [&](
            const Partol::Request::SharedPtr request,
            Partol::Response::SharedPtr response) -> void {
                if(
                    (0 < request->target_x && request->target_x < 12.0f)&&
                    (0 < request->target_y && request->target_y < 12.0f)
                ) {
                    this->target_x_ = request->target_x;
                    this->target_y_ = request->target_y;
                    response->result = Partol::Response::SUCESS;
                } else {
                    response->result = Partol::Response::FAIL;
                }
        });

        // 发布者：发布海龟的动作信息
        publisher_ = this->create_publisher<geometry_msgs::msg::Twist>("/turtle1/cmd_vel", 10);
        // 订阅者：订阅当前海龟的位置信息
        // subcriber_ = this->create_subscription<turtlesim::msg::Pose>("/turtle1/pose", 10, std::bind(&TurtleControlNode::on_pose_received_, this, std::placeholders::_1));
        subcriber_ = this->create_subscription<turtlesim::msg::Pose>(
            "/turtle1/pose",
             10,
            [this](const turtlesim::msg::Pose::SharedPtr pose) -> void { this->on_pose_received_(pose); }
        );

    }

    void on_pose_received_(const turtlesim::msg::Pose::SharedPtr pose) { // 参数：收到数据的共享指针
        
        // 1. 获取当前位置
        auto current_x = pose->x;
        auto current_y = pose->y;
        RCLCPP_INFO(get_logger(), "当前：x=%f, y=%f", current_x, current_y);

        // 2. 计算当前海龟位置跟目标位置的距离差和角度差
        //两点距离公式
        auto distance = std::sqrt(
            (target_x_ - current_x)*(target_x_ - current_x) + 
            (target_y_ - current_y)*(target_y_ - current_y)
        );
        // 反正切：计算当前点与目标点的角度  arctan
        auto angle = std::atan2(target_y_ - current_y, target_x_ - current_x) - pose->theta; // pose->theta：当前海龟的朝向角度
        
        // 3. 控制策略
        auto msg = geometry_msgs::msg::Twist();
        if (distance > 0.1) {
            if(fabs(angle) > 0.2) {
                msg.angular.z = fabs(angle); // 角速度
            } else {
                msg.linear.x = k_ * distance; // 线速度
            }
        }

        // 4. 限制线速度最大值
        if(msg.linear.x > max_speed_) {
            msg.linear.x = max_speed_;
        }
        
        publisher_->publish(msg);
    }

};

int main(int argc, char* argv[]) 
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<TurtleControlNode>("turtle_control");
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
