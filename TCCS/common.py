# Notice：在测试之前请保证从本脚本开始，以此来保证基本的连接和内容检查完整，检查项：
# 1. 充电站已被CSMS系统接受 = check_accepted
# 2. 充电站与CSMS系统保持稳定有效连接 = check_2
# 3. 充电站连接器处于可用状态 = check_3
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

import asyncio
import logging
from datetime import datetime, timezone
from websockets.datastructures import Headers
from websockets.typing import Subprotocol

try:
    import websockets
except ModuleNotFoundError:
    print("This example relies on the 'websockets' package.")
    print("Please install it by running: ")
    print()
    print(" $ pip install websockets")
    import sys

    sys.exit(1)

from ocpp.routing import on
from ocpp.v201 import ChargePoint as cp
from ocpp.v201 import call_result
from ocpp.v201.enums import Action
from ocpp.v201 import enums as ocpp_enums
from ocpp.v201 import datatypes as ocpp_datatypes

logging.basicConfig(level=logging.INFO)


class ChargePoint(cp):
    check_accepted = False
    @on(Action.boot_notification)
    def on_boot_notification(self, charging_station, reason, **kwargs):
        logging.info("Boot Notification received from %s", self.id)
        logging.info("Charging Station: %s", charging_station)
        logging.info("Reason: %s", reason)
        self.check_accepted = True
        return call_result.BootNotification(
            current_time=datetime.now(timezone.utc).isoformat(),
            interval=60,
            status=ocpp_enums.RegistrationStatusEnumType.accepted,
        )

    @on(Action.heartbeat)
    def on_heartbeat(self):
        print("Got a Heartbeat!")
        return call_result.Heartbeat(
            current_time=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S") + "Z"
        )

    def cp_check(self):
        logging.info("Charge Point %s is ready for testing.", self.id)

async def on_connect(websocket):
    try:
        requested_protocols = websocket.request.headers["Sec-WebSocket-Protocol"]
    except KeyError:
        logging.error("Client hasn't requested any Subprotocol. Closing Connection")
        return await websocket.close()
    if websocket.subprotocol:
        logging.info("Protocols Matched: %s", websocket.subprotocol)
    else:
        logging.warning(
            "Protocols Mismatched | Expected Subprotocols: %s,"
            " but client supports %s | Closing connection",
            websocket.available_subprotocols,
            requested_protocols,
        )
        return await websocket.close()

    charge_point_id = websocket.request.path.strip("/")
    charge_point = ChargePoint(charge_point_id, websocket)

    await charge_point.start()

async def main():
    server = await websockets.serve(
        on_connect, "0.0.0.0", 9000, subprotocols=[Subprotocol("ocpp2.0.1")]
    )
    logging.info("Server Started listening to new connections...")
    await server.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())

