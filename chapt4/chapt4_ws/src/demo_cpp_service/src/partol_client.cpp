#include "rclcpp/rclcpp.hpp"
#include "chapt4_interfaces/srv/partol.hpp"
#include <chrono>
#include <ctime>
#include "rcl_interfaces/msg/parameter.hpp"
#include "rcl_interfaces/msg/parameter_value.hpp"
#include "rcl_interfaces/msg/parameter_type.hpp"
#include "rcl_interfaces/srv/set_parameters.hpp"

using SetP = rcl_interfaces::srv::SetParameters;
using Partol = chapt4_interfaces::srv::Partol;
using namespace std::chrono_literals; // 使用 10s 100ms 代表时间

class PartolClient : public rclcpp::Node
{
private:
    rclcpp::TimerBase::SharedPtr timer_;
    rclcpp::Client<Partol>::SharedPtr partol_client_;

public:
    PartolClient(const std::string &node_name) 
    : Node(node_name) 
    {
        srand(time(NULL)); // 初始化随机数种子
        partol_client_ = this->create_client<Partol>("partol");
        timer_ = this->create_wall_timer(10s, [&]() -> void {
            // 1. 检测服务端是否上线
            while (!this->partol_client_->wait_for_service(1s))
            {
                if(!rclcpp::ok()) {
                    RCLCPP_ERROR(this->get_logger() ,"等待服务上线过程中，rclcpp挂了");
                    return ;
                }
                RCLCPP_INFO(this->get_logger(), "等待服务上线中...");
                
            }
            // 2. 构造请求对象
            auto request = std::make_shared<Partol::Request>();
            request->target_x = rand() % 15;
            request->target_y = rand() % 15;
            RCLCPP_INFO(this->get_logger(), "准备好目标点%f, %f", request->target_x, request->target_y);

            // 3. 发送请求，异步调用
            this->partol_client_->async_send_request(request, 
                [&](rclcpp::Client<Partol>::SharedFuture result_future) -> void {
                    auto response =result_future.get();
                    if(response->result==Partol::Response::SUCESS){
                        RCLCPP_INFO(this->get_logger(), "请求训练目标点成功");
                    }
                    if(response->result==Partol::Response::FAIL){
                        RCLCPP_INFO(this->get_logger(), "请求训练目标点失败");
                    }
            });
        });
    }

    /**
     * 创建客户端发送请求，返回结果
     */
    SetP::Response::SharedPtr call_set_parameters(const rcl_interfaces::msg::Parameter &param)
    {
        auto param_client = this->create_client<SetP>("/turtle_control/set_parameters");
    
        // 1. 检测服务端是否上线
        while (!param_client->wait_for_service(1s))
        {
            if(!rclcpp::ok()) {
                RCLCPP_ERROR(this->get_logger() ,"等待参数修改服务上线过程中，rclcpp挂了");
                return nullptr;
            }
            RCLCPP_INFO(this->get_logger(), "等待参数修改服务上线中...");
            
        }
        // 2. 构造请求对象
        auto request = std::make_shared<SetP::Request>();
        request->parameters.push_back(param);

        // 3. 发送请求，异步调用

        auto future = param_client->async_send_request(request); 
        rclcpp::spin_until_future_complete(this->get_node_base_interface(), future); // 等待获取完整 future
        auto response = future.get();
        return response;

        // param_client->async_send_request(request, 
        //     [&](rclcpp::Client<Partol>::SharedFuture result_future) -> void {
        //         auto response =result_future.get();
        //         if(response->result==Partol::Response::SUCESS){
        //             RCLCPP_INFO(this->get_logger(), "请求训练目标点成功");
        //         }
        //         if(response->result==Partol::Response::FAIL){
        //             RCLCPP_INFO(this->get_logger(), "请求训练目标点失败");
        //         }
        // });
    }

    /**
     * 更新参数K
     */
    void update_server_param_k(double k)
    {
        // 1. 创建参数对象
        auto param = rcl_interfaces::msg::Parameter();
        param.name = "k";
        // 2. 创建参数值
        auto param_value = rcl_interfaces::msg::ParameterValue();
        param_value.type = rcl_interfaces::msg::ParameterType::PARAMETER_DOUBLE;
        param_value.double_value = k;
        param.value = param_value;
        // 3. 请求更新参数并处理
        auto response = this->call_set_parameters(param);
        if(response == NULL)
        {
            RCLCPP_INFO(this->get_logger(), "参数更新失败");
            return;
        }

        for(auto result:response->results)
        {
            if(result.successful == false)
            {
                RCLCPP_INFO(this->get_logger(), "参数更新失败，原因：%s", result.reason.c_str());
            } else {
                RCLCPP_INFO(this->get_logger(), "参数更新的值为 k=%f", k);
            }
        }
    }
};

int main(int argc, char* argv[]) 
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<PartolClient>("turtle_client");
    // TODO 消息发送阻塞
    node->update_server_param_k(4.0);
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
