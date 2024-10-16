import socket
import json
import threading
import time
from SC_infrared import IR_R, IR_G, IR_B
from SC_fakemotor import RobotDirection
from SC_ultrasonic import ULTRASONIC
from SC_actions import perform_action_capture, perform_action_report, perform_action_throw_to_basket
from SC_head import look_forward, look_diagonal, look_down
from SC_utils import *

HOST = 'localhost'
PORT_SENSOR = 8081
PORT_COMMAND = 8082
PORT_ACTION = 8083  # Новый порт для действий
UPDATE_RATE = 30  # Частота в Гц

rd = None

def init():
    global rd
    IR_G.start_update_thread()
    IR_R.start_update_thread()
    IR_B.start_update_thread()
    ULTRASONIC.start_update_thread()
    rd = RobotDirection()

def serialize_sensors():
    return {
        "IR_G": IR_G.serialize(),
        "IR_R": IR_R.serialize(),
        "IR_B": IR_B.serialize(),
        "ULTRASONIC": ULTRASONIC.serialize()
    }

def handle_sensor_client(conn):
    rate_limiter = ThreadRate(UPDATE_RATE)
    while True:
        try:
            data = json.dumps(serialize_sensors())
            conn.sendall(data.encode('utf-8'))
            rate_limiter.sleep()  # Сохраняем фиксированную частоту обновления
        except (ConnectionResetError, BrokenPipeError):
            print("Sensor client disconnected.")
            break
    conn.close()

def parse_json_from_buffer(buffer):
    json_objects = []
    last_valid_json = None  # Keep track of the last valid JSON object
    start_index = 0  # Initialize the starting index for searching

    while True:
        try:
            # Find the next opening brace
            start_index = buffer.index('{', start_index)
            open_braces = 1  # Counter for nested braces
            
            # Find the corresponding closing brace
            end_index = start_index + 1
            while open_braces > 0 and end_index < len(buffer):
                if buffer[end_index] == '{':
                    open_braces += 1
                elif buffer[end_index] == '}':
                    open_braces -= 1
                end_index += 1
            
            # If we found a complete object, extract it
            if open_braces == 0:
                json_str = buffer[start_index:end_index]  # Extract complete JSON string
                json_objects.append(json.loads(json_str))  # Parse and append to the list
                last_valid_json = json.loads(json_str)  # Update last valid JSON
                
                # Move the starting index past this object for further searching
                start_index = end_index
            else:
                break  # Exit if we didn't find a complete object
            
        except (ValueError, json.JSONDecodeError):
            # If we can't find another opening brace or if there's an error in decoding, break out of the loop
            break

    return last_valid_json  # Return parsed objects, remaining buffer, and last valid JSON

def handle_command_client(conn):
    buffer = ""
    
    while True:
        try:
            data = conn.recv(1024).decode('utf-8')
            if not data:
                print("No data received. Client may have disconnected.")
                break
            
            buffer += data
            
            # Пытаемся распарсить полные JSON-объекты из буфера
            while True:
                try:
                    command = parse_json_from_buffer(buffer)
                    buffer = ""  # Очищаем буфер после успешного парсинга
                    execute_command(command)
                    break  # Выходим из внутреннего цикла для продолжения получения данных
                except:
                    break  # Ждем больше данных

        except (ConnectionResetError, json.JSONDecodeError) as e:
            print(f"Command client disconnected or error in data: {e}")
            break
    
    conn.close()

def handle_action_client(conn):
    buffer = ""
    
    while True:
        try:
            data = conn.recv(1024).decode('utf-8')
            if not data:
                print("No data received. Client may have disconnected.")
                break
            
            buffer += data
            
            # Пытаемся распарсить полные JSON-объекты из буфера
            while True:
                try:
                    action_command = parse_json_from_buffer(buffer)
                    buffer = ""  # Очищаем буфер после успешного парсинга
                    execute_action(action_command)
                    break  # Выходим из внутреннего цикла для продолжения получения данных
                except:
                    break  # Ждем больше данных

        except (ConnectionResetError, json.JSONDecodeError) as e:
            print(f"Action client disconnected or error in data: {e}")
            break
    
    conn.close()

def execute_command(command):
    if "set_speed" in command:
        left_speed = command["set_speed"].get("left", 0)
        right_speed = command["set_speed"].get("right", 0)
        rd.set_speed_cms_left(left_speed)
        rd.set_speed_cms_right(right_speed)
        # print(f"Setting speed - Left: {left_speed}, Right: {right_speed}")

def execute_action(action_command):
    action = action_command.get("action")
    if action == "perform_action_capture":
        result = perform_action_capture()
        print(f"Capture action result: {result}")
    elif action == "perform_action_report":
        result = perform_action_report()
        print(f"Report action result: {result}")
    elif action == "perform_action_throw_to_basket":
        result = perform_action_throw_to_basket()
        print(f"Throw to basket action result: {result}")
    elif action == "perform_look_forward":
        angle = look_forward()
        # print(f"Look forward angle: {angle}")
    elif action == "perform_look_diagonal":
        angle = look_diagonal()
        print(f"Look diagonal angle: {angle}")
    elif action == "perform_look_down":
        angle = look_down()
        print(f"Look down angle: {angle}")

def start_sensor_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT_SENSOR))
        s.listen()
        print(f"Sensor server listening on {HOST}:{PORT_SENSOR}")
        
        while True:
            conn, addr = s.accept()
            print(f"Accepted connection from sensor client: {addr}")
            threading.Thread(target=handle_sensor_client, args=(conn,)).start()

def start_command_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT_COMMAND))
        s.listen()
        print(f"Command server listening on {HOST}:{PORT_COMMAND}")
        
        while True:
            conn, addr = s.accept()
            print(f"Accepted connection from command client: {addr}")
            threading.Thread(target=handle_command_client, args=(conn,)).start()

def start_action_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT_ACTION))
        s.listen()
        print(f"Action server listening on {HOST}:{PORT_ACTION}")
        
        while True:
            conn, addr = s.accept()
            print(f"Accepted connection from action client: {addr}")
            threading.Thread(target=handle_action_client, args=(conn,)).start()

if __name__ == '__main__':
    init()
    threading.Thread(target=start_sensor_server).start()
    threading.Thread(target=start_command_server).start()
    threading.Thread(target=start_action_server).start()
