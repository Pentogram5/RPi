import threading
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

# class TimeStamper:
#     def __init__(self):
#         self.old_t = time.time()

#     def timestamp(self):
#         dt = time.time() - self.old_t
#         self.old_t = time.time()
#         return dt
# ts = TimeStamper()

class ScInfrared:
    value = None # Последнее устреднённое значение
    rawValue = 0 # Последнее значение
    filteredValue = 0
    
    def __init__(self, id, pin, distance, averageCount=10):
        self.id = id
        self.pin = pin
        self.distance = distance
        self.averageCount = averageCount
        self.values = []  # Список для хранения последних значений
        # self.ts = TimeStamper()
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.start_update_thread()

    def getNewRawValue(self):
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

    def getSerialise(self):
        return {'id': str(self.id),
                'distance': self.distance,
                'value': self.rawValue,
                'filteredValue': self.filteredValue}
    
    def _update_thread(self):
        while True:
            # self.averageCount
            val = self.getNewRawValue()
            self.filteredValue = self._filter_value(val)
            # print(self.id,self.ts.timestamp())
            time.sleep(0)
    
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

IR_1 = ScInfrared('IR_GREEN', 22, 10)
IR_2 = ScInfrared('IR_RED', 18, 10)
IR_3 = ScInfrared('IR_BLACK', 27, 10)

if __name__=='__main__':
    IR_1.start_update_thread()
    IR_2.start_update_thread()
    IR_3.start_update_thread()
    
    while True:
        print(IR_1.filteredValue)
        # print(ts.timestamp())