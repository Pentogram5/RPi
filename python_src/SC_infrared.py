import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

class ScInfrared:
    value = None # Последнее устреднённое значение
    rawValue = None # Последнее значение
    
    def __init__(self, id, pin, averageCount=10):
        self.id = id
        self.pin = pin
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
        return {'value': self.getNewValue(self)}