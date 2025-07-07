# Notice：在测试之前请保证从本脚本开始，以此来保证基本的连接和内容检查完整，检查项：
# 1. 充电站已被CSMS系统接受
# 2. 充电站与CSMS系统保持稳定有效连接
# 3. 充电站连接器处于可用状态
# 4. 充电站处于空闲状态，无进行中交易
# 5. 充电站无故障状态
# 6. 充电站未激活任何充电计划
# 7. 充电站无有效预约
# 8. 配置变量AuthCtrlr.LocalPreAuthorize设为false
# 9. 充电站OCPP消息队列无待发送信息
# 10. 充电站未处于诊断数据传输状态
# 11. 充电站未进行固件下载
# 12. 充电站未处于固件升级状态
# 13. 充电站已准备就绪可接受/启动充电会话
# 14. 充电站未配置显示信息
# 15. 充电站未激活任何自定义监控程序

# Notice: Before testing, please ensure to start from this script to guarantee the completeness of basic connection and content checks. The checks include:
# General pre conditions:
# • Charging Station is Accepted by the CSMS
# • Charging Station has a stable active connection to the CSMS
# • Charging Station connectors are available
# • Charging Station is Idle, with no active transactions
# • Charging Station is clear of faults
# • Charging Station has no charging schedules active
# • Charging Station has no active reservations
# • The Configuration variable AuthCtrlr.LocalPreAuthorize is set to false.
# • Charging Station has no more OCPP messages to be send in queue
# • Charging Station is not busy with transfer of diagnostics
# • Charging Station is not busy with download of firmware
# • Charging Station is not upgrading firmware
# • Charging Station is ready to accept/start a charging session
# • Charging Station has no Display message configured
# • Charging Station has no active custom monitors
