cmake_minimum_required(VERSION 3.8)
project(status_display)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(status_interfaces REQUIRED)
# 添加Qt5
find_package(Qt5 REQUIRED COMPONENTS Widgets)

add_executable(hello_qt src/hello_qt.cpp)
# 添加可执行文件
add_executable(sys_status_display src/sys_status_display.cpp)

# 其他库链接依赖
target_link_libraries(hello_qt Qt5::Widgets)
target_link_libraries(sys_status_display Qt5::Widgets)

# ros 库链接依赖
ament_target_dependencies(sys_status_display rclcpp status_interfaces)

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

# 拷贝
install(TARGETS hello_qt sys_status_display
  DESTINATION lib/${PROJECT_NAME}
)


ament_package()
