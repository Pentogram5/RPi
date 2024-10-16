import json
import time
from SC_TCPRequests import StableConnectionServer

class MyServer(StableConnectionServer):
    def process_response(self, json_request):
        # Пример обработки запроса
        print(f"Received request: {json_request}")
        response = {
            "response_code": 200,
            "response_msg": f"Hello, {json_request['request_name']}!"
        }
        return response

if __name__ == "__main__":
    server = MyServer(ip='127.0.0.1', port=5000)
    server.start_process_responses()
    
    try:
        while True:
            time.sleep(1)  # Сервер работает в вечном цикле
    except KeyboardInterrupt:
        print("Stopping server...")
        server.stop()
