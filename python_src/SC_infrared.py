import threading
import time
import RPi.GPIO as GPIO
import json
GPIO.setmode(GPIO.BCM)

# class TimeStamper:
#     def __init__(self):
#         self.old_t = time.time()

#     def timestamp(self):
#         dt = time.time() - self.old_t
#         self.old_t = time.time()
#         return dt
# ts = TimeStamper()

from SC_utils import ThreadRate

class ScInfrared:
    rawValue = 0 # Последнее значение
    filteredValue = 0
    timestamp = 0
    
    def __init__(self, id='IR_GREEN', pin=22, distance=10, averageCount=10,
                 rawValue=None, filteredValue=None, timestamp=None,
                 update_rate=30):
        self.id = id
        self.pin = pin
        self.distance = distance
        self.averageCount = averageCount
        self.values = []  # Список для хранения последних значений
        if rawValue:
            self.rawValue = rawValue
        if filteredValue:
            self.filteredValue = filteredValue
        if timestamp:
            self.timestamp = timestamp
        # self.ts = TimeStamper()
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.tr = ThreadRate(update_rate)

    def getNewRawValue(self):
        # if self.id=="IR_GREEN":
        #     print(GPIO.input(self.pin))
        self.rawValue = GPIO.input(self.pin)
        # self.rawValue = (self.rawValue+1) % 100
        return self.rawValue
    
    def getRawValue(self):
        return self.rawValue
    
    # def getNewValue(self):
    #     S = 0
    #     for _ in range(self.averageCount):
    #         S += self.getNewRawValue() 
    #     self.value = round(S / self.averageCount)
    #     return self.value
    
    def getValue(self):
        return self.value

    def serialize(self):
        return {'id': str(self.id),
                'distance': self.distance,
                'rawValue': self.rawValue,
                'filteredValue': self.filteredValue,
                'timestamp': time.time_ns()}
    
    @staticmethod    
    def deserialize(json_data):
        # data = json.loads(json_str)
        data = json_data
        return ScInfrared(
            id=data['id'],
            distance=data['distance'],
            rawValue=data['rawValue'],
            filteredValue=data['filteredValue'],
            timestamp=data['timestamp']
        )
    
    def _update_thread(self):
        while True:
            # self.averageCount
            val = self.getNewRawValue()
            self.filteredValue = self._filter_value(val)
            # print(self.id,self.ts.timestamp())
            self.tr.sleep()
    
    def _filter_value(self, new_value):
        # Добавляем новое значение в список
        self.values.append(new_value)

        # Удаляем старые значения, если их больше чем averageCount
        if len(self.values) > self.averageCount:
            self.values.pop(0)

        # Вычисляем среднее значение
        return sum(self.values) / len(self.values)
        
    def start_update_thread(self):
        self.update_thread = threading.Thread(target=self._update_thread)
        self.update_thread.start()
    
    def __repr__(self):
        return f'ScInfrared({self.id},distance={self.distance},rawValue={self.rawValue},filteredValue={self.filteredValue},timestamp={self.timestamp})'

    def __str__(self):
        return self.__repr__()

IR_G = ScInfrared('IR_GREEN', 22, 10)
IR_R = ScInfrared('IR_RED', 18, 10)
IR_B = ScInfrared('IR_BLACK', 27, 10)

if __name__=='__main__':
    IR_G.start_update_thread()
    IR_R.start_update_thread()
    IR_B.start_update_thread()
    
    while True:
        print(IR_G.filteredValue)
        # print(ts.timestamp())