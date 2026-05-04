#include "iostream" // 系统默认库

int main(int argc, char** argv) // argc：命令行启动时传入的参数数量 argv：所有传参二维数组
{
    std::cout<<"参数数量="<<argc<<std::endl;
    std::cout<<"程序名称="<<argv[0]<<std::endl;
    if (argv[1]) 
    {
        std::cout<<"第一个参数="<<argv[1]<<std::endl;

        std::string arg1 = argv[1];
        if (arg1 == "--help")
        {
            std::cout <<"这里是程序帮助，但是这个程序什么用都没有" << std::endl;
        }
    }
    

    return 0;
}