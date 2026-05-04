#include <QApplication>
#include <QLabel>
#include <QString>
#include <rclcpp/rclcpp.hpp>
#include <status_interfaces/msg/system_status.hpp>

using SystemStatus = status_interfaces::msg::SystemStatus;

class SysStatusDishplay : public rclcpp::Node
{
private:
    rclcpp::Subscription<SystemStatus>::SharedPtr subscriber_;
    QLabel *label_;

public:
    SysStatusDishplay(const std::string &node_name)
        : Node(node_name)
    {
        subscriber_ = this->create_subscription<SystemStatus>("sys_status", 10,
           [&](const SystemStatus::SharedPtr msg) -> void
           { label_->setText(get_qstr_from_msg(msg)); 
        });

        label_ = new QLabel();
        label_->setFont(QFont("WenQuanYi Micro Hei", 18));
        label_->setText(get_qstr_from_msg(std::make_shared<SystemStatus>()));
        label_->show();
    };

    QString get_qstr_from_msg(const SystemStatus::SharedPtr msg)
    {
        std::stringstream show_str;
        show_str << "===========系统状态可视化显示工具===========\n"
                 << "数 据 时 间：\t" << msg->stamp.sec << "\ts\n"
                 << "主 机 名 称：\t" << msg->host_name << "\t\n"
                 << " CPU 使用率：\t" << msg->cpu_percent << "\t%\n"
                 << " 内存使用率：\t" << msg->memory_percent << "\t%\n"
                 << " 内存总大小：\t" << msg->memory_total << "\tMB\n"
                 << "剩余有效内存：\t" << msg->memory_available << "\tMB\n"
                 << " 网络发送量：\t" << msg->net_sent << "\tMB\n"
                 << " 网络接收量：\t" << msg->net_recv << "\tMB\n"
                 << "==========================================\n";

        return QString::fromStdString(show_str.str());
    }
};

int main(int argc, char *argv[])
{

    rclcpp::init(argc, argv);
    QApplication app(argc, argv);
    auto node = std::make_shared<SysStatusDishplay>("sys_status_display");
    // 单独开一个子线程处理监听 rclcpp.spin()
    // 定义时初始化
    std::thread spin_thread([&]()->void{
        rclcpp::spin(node); // 子线程阻塞代码
        
    });
    spin_thread.detach();
    rclcpp::shutdown();
    app.exec(); // 主线程阻塞代码

    return 0;
}