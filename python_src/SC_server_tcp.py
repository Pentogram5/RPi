import json
import socket
import threading
from SC_TCPRequests import StableConnectionServer
from SC_infrared import IR_R, IR_G, IR_B
from SC_fakemotor import RobotDirection
from SC_ultrasonic import ULTRASONIC
from SC_actions import perform_action_capture, perform_action_report, perform_action_throw_to_basket
from SC_head import look_forward, look_diagonal, look_down
from SC_utils import TimeStamper, ThreadRate

HOST = 'localhost'
PORT_SENSOR = 8081
PORT_COMMAND = 8082
PORT_ACTION = 8083  # Новый порт для действий
# UPDATE_RATE = 30  # Частота в Гц

rd = None

def init():
    global rd
    IR_G.start_update_thread()
    IR_R.start_update_thread()
    IR_B.start_update_thread()
    ULTRASONIC.start_update_thread()
    rd = RobotDirection()

def serialize_sensors():
    # print(IR_G)
    return {
        "IR_G": IR_G.serialize(),
        "IR_R": IR_R.serialize(),
        "IR_B": IR_B.serialize(),
        "ULTRASONIC": ULTRASONIC.serialize()
    }

class SensorServer(StableConnectionServer):
    def __init__(self, ip='127.0.0.1', port=8081):
        super().__init__(ip, port)
        self.sensors_data = serialize_sensors()

    def process_response(self, json_request):
        request_name = json_request.get("request_name")
        if request_name == "get_sensors":
            return self.get_sensors()
        else:
            return {"response_code": 400, "response_msg": "Unknown request"}

    def get_sensors(self):
        self.sensors_data = serialize_sensors()
        return {
            "response_code": 200,
            "response_msg": "Sensors data retrieved successfully",
            "sensors": self.sensors_data
        }


class SpeedControlServer(StableConnectionServer):
    def __init__(self, ip='127.0.0.1', port=8082):
        super().__init__(ip, port)

    def process_response(self, json_request):
        request_name = json_request.get("request_name")
        if request_name == "set_speed_cms":
            return self.set_speed_cms(json_request)
        else:
            return {"response_code": 400, "response_msg": "Unknown request"}

    def set_speed_cms(self, json_request):
        global rd
        lcms = json_request.get("lcms")
        rcms = json_request.get("rcms")
        rd.set_speed_cms_left (lcms)
        rd.set_speed_cms_right(rcms)
        
        if lcms is None or rcms is None:
            return {"response_code": 400, "response_msg": "lcms and rcms must be provided"}
        
        # Логика для установки скорости
        # print(f"Setting speed: left={lcms} cm/s, right={rcms} cm/s")
        
        return {"response_code": 200, "response_msg": "Speed set successfully"}

ts = TimeStamper()

class ActionServer(StableConnectionServer):
    def __init__(self, ip='127.0.0.1', port=8083):
        super().__init__(ip, port)

    def process_response(self, json_request):
        request_name = json_request.get("request_name")
        if request_name == "perform_action":
            return self.perform_action(json_request)
        else:
            return {"response_code": 400, "response_msg": "Unknown request"}

    def perform_action(self, json_request):
        # print(json_request)
        # print(ts.timestamp())
        action = json_request.get("atype")
        
        if action is None:
            return {"response_code": 400, "response_msg": "atype must be provided"}
        
        # Логика для выполнения действия
        # print(f"Performing action: {action}")
        if action == "perform_action_capture":
            result = perform_action_capture()
            # print(f"Capture action result: {result}")
        elif action == "perform_action_report":
            result = perform_action_report()
            # print(f"Report action result: {result}")
        elif action == "perform_action_throw_to_basket":
            result = perform_action_throw_to_basket()
            # print(f"Throw to basket action result: {result}")
        elif action == "perform_look_forward":
            angle = look_forward()
            # print(f"Look forward angle: {angle}")
        elif action == "perform_look_diagonal":
            angle = look_diagonal()
            # print(f"Look diagonal angle: {angle}")
        elif action == "perform_look_down":
            angle = look_down()
            # print(f"Look down angle: {angle}")
        
        return {"response_code": 200, "response_msg": f"Action {action} performed successfully", "result": f"Action {action} completed"}


if __name__ == "__main__":
    init()
    
    # Создаем и запускаем три сервера на разных портах
    sensor_server        = SensorServer(ip='127.0.0.1', port=8081)
    speed_control_server = SpeedControlServer(ip='127.0.0.1', port=8082)
    action_server        = ActionServer(ip='127.0.0.1', port=8083)

    sensor_server.start_process_responses()
    speed_control_server.start_process_responses()
    action_server.start_process_responses()

    try:
        while True:
            pass  # Все серверы работают в вечном цикле
    except KeyboardInterrupt:
        print("Stopping servers...")
        sensor_server.stop()
        speed_control_server.stop()
        action_server.stop()
