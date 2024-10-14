import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

class ScInfrared:
    value = None # Последнее устреднённое значение
    rawValue = None # Последнее значение
    
    def __init__(self, id, pin, distance, averageCount=10):
        self.id = id
        self.pin = pin
        self.distance = distance
        self.averageCount = averageCount
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def getNewRawValue(self):
        self.rawValue = GPIO.input(self.pin)
        return self.rawValue
    
    def getRawValue(self):
        return self.rawValue
    
    def getNewValue(self):
        S = 0
        for _ in range(self.averageCount):
            S += self.getNewRawValue() 
        self.value = round(S / self.averageCount)
        return self.value
    
    def getValue(self):
        return self.value

    def getSerialise(self):
        return {'id': str(self.id),
                'distance': self.distance,
                'value': self.getNewValue(self)}

RI_1 = ScInfrared(1, 22, 10)
RI_2 = ScInfrared(2, 18, 10)
RI_3 = ScInfrared(3, 27, 10)