from SC_infrared import IR_R, IR_G, IR_B
# from xr_motor import RobotDirection
from SC_fakemotor import RobotDirection
from SC_ultrasonic import ULTRASONIC
from SC_actions import perform_action_capture, perform_action_report, perform_action_throw_to_basket
from aiohttp import web
import json

rd = None

def init():
    global rd
    IR_G.start_update_thread()
    IR_R.start_update_thread()
    IR_B.start_update_thread()
    ULTRASONIC.start_update_thread()
    rd = RobotDirection()


# Запросы сенсоров
async def handle_get_ir_sensor(request):
    sensor_id = request.match_info['sensor_id']
    if sensor_id=="G":
        return web.json_response(IR_G.serialize())
    if sensor_id=="R":
        return web.json_response(IR_R.serialize())
    if sensor_id=="B":
        return web.json_response(IR_B.serialize())
    # return web.json_response({"ok?": True, "sensor_id": sensor_id})

async def handle_get_ultrasonic_sensor(request):
    return web.json_response(ULTRASONIC.serialize())


# Запросы моторов
async def handle_set_speed(request):
    direction = request.match_info['direction']
    cms_str = request.query.get('cms')
    
    if cms_str is not None:
        try:
            cms = float(cms_str)
            # return web.json_response({"ok?": True, "direction": direction, "speed_cms": cms_value})
            resulted_speed = None
            if   direction=="left" :
                resulted_speed = rd.set_speed_cms_left(cms)
            elif direction=="right":
                resulted_speed = rd.set_speed_cms_left(cms)
            
            if direction:
                return web.json_response({"resulted_speed":resulted_speed})
            else:
                return web.json_response({"direction is invalid"}, status=400)
        except ValueError:
            return web.json_response({"error": "Invalid cms value"}, status=400)
    else:
        return web.json_response({"error": "cms parameter is required"}, status=400)


# Запросы клешни (действий)
async def handle_action_capture(request):
    result = perform_action_capture()
    if result:
        return web.json_response({"result":"action perform succeeded"})
    else:
        return web.json_response({"error": "cms parameter is required"}, status=400)

async def handle_action_report(request):
    result = perform_action_report()
    if result:
        return web.json_response({"result":"action perform succeeded"})
    else:
        return web.json_response({"error": "cms parameter is required"}, status=400)

async def handle_action_throw_to_basket(request):
    result = perform_action_throw_to_basket()
    if result:
        return web.json_response({"result":"action perform succeeded"})
    else:
        return web.json_response({"error": "cms parameter is required"}, status=400)


app = web.Application()

# Определяем маршруты
app.router.add_get('/get_IR_{sensor_id}', handle_get_ir_sensor)  # Для get_IR_G, get_IR_R, get_IR_B
app.router.add_get('/get_ultrasonic_sensor', handle_get_ultrasonic_sensor)
app.router.add_get('/set_speed_cms_{direction}', handle_set_speed)  # Для set_speed_cms_left и set_speed_cms_right
app.router.add_get('/perform_action_capture', handle_action_capture)  # действие захвата
app.router.add_get('/perform_action_report' , handle_action_report )  # действие отчёта о положении предмета на базу
app.router.add_get('/perform_action_throw_to_basket', handle_action_throw_to_basket)  # действие бросания 

if __name__ == '__main__':
    init()
    web.run_app(app, port=8080)
