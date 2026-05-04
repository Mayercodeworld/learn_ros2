/**
 * 函数包装器学习
 */

#include "iostream"
#include "functional" // 函数包装器头文件

// 自由函数
void save_with_free_fun(const std::string& file_name)
{
    std::cout << "自由函数:" << file_name << std::endl;
}


// 成员函数
class FileSave
{
private:
    /* data */
public:
    FileSave(/* args */)=default;
    ~FileSave()=default;

    void save_with_member_fun(const std::string& file_name)
    {
        std::cout << "成员函数:" << file_name << std::endl;
    };
};

int main()
{
    FileSave file_save;

    // Lambda 函数
    auto save_with_lambda_fun = [](const std::string& file_name) -> void {
        std::cout << "Lambda函数:" << file_name << std::endl;
    };

    // // 1. 自由函数
    // save_with_free_fun("file.txt");
    // // 2. 成员函数
    // file_save.save_with_member_fun("file.txt");
    // // 3. Lambda函数
    // save_with_lambda_fun("file.txt");

    std::function<void(const std::string&)> save1 = save_with_free_fun;
    std::function<void(const std::string&)> save2 = save_with_lambda_fun;
    // 成员函数，放入包装器
    std::function<void(const std::string&)> save3 = std::bind(&FileSave::save_with_member_fun, &file_save, std::placeholders::_1);

    // 统一调用方法
    save1("file.txt");
    save2("file.txt");
    save3("file.txt");

    return 0;
}


