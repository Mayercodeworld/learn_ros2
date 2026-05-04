cmake_minimum_required(VERSION 3.8)
project(demo_cpp_pkg)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED) # 直接查找到对应的头文件和库文件

add_executable(cpp_node src/cpp_node.cpp)

# message(STATUS ${rclcpp_INCLUDE_DIRS}) # 头文件：rclcpp依赖的头文件
# message(STATUS ${rclcpp_LIBRARIES}) # 库文件

# target_include_directories(cpp_node PUBLIC ${rclcpp_INCLUDE_DIRS}) # 头文件包含
# target_link_libraries(cpp_node ${rclcpp_LIBRARIES}) # 库文件链接

ament_target_dependencies(cpp_node rclcpp)

# 手动拷贝
install(TARGETS cpp_node
  DESTINATION lib/${PROJECT_NAME}
)

# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

# ament相关指令结束
ament_package()
