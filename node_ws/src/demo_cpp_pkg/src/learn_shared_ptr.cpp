/**
 * std::make_shared<>() 共享指针学习
 */

#include "iostream"
#include "memory"

int main()
{
    /**
     * std::make_shared<数据类型/类>(参数);
     * 返回值：对应类的共享指针，基于指向引用内存地址的指针数量
     */
    // p1指向了所在内存
    auto p1 = std::make_shared<std::string>("This is a str.");
    // p2指向了所在内存
    auto p2 = p1;

    std::cout << "p1的引用计数：" << p1.use_count() << "，指向内存地址：" << p1.get() << std::endl; // 2
    std::cout << "p2的引用计数：" << p2.use_count() << "，指向内存地址：" << p2.get() << std::endl; // 2
    
    p1.reset(); // p1释放引用，p1不再指向 "This is a str." 所在内存
    std::cout << "p1的引用计数：" << p1.use_count() << "，指向内存地址：" << p1.get() << std::endl; // 0
    std::cout << "p2的引用计数：" << p2.use_count() << "，指向内存地址：" << p2.get() << std::endl; // 1

    std::cout << "p2指向内存地址数据：" << p2->c_str() << std::endl; // p2指针调用成员方法
    
    return 0; 
}
