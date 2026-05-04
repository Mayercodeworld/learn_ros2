/**
 * Lambda函数学习
 */

#include "iostream"
#include "algorithm"

int main()
{
    auto add = [](int a, int b) -> int {return a + b;};
    int sum = add(200, 50);

    // 捕获 sum
    auto print_sum = [sum]() -> void {std::cout << sum << std::endl;};

    print_sum();
    return 0;
}