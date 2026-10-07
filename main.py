from machine import Pin, I2C
from driver import BMP, MPU
import ustruct


def formatAndWrite(data, debug=False):
    with open("data.bin", "ab") as f:
        f.write(data)
    if debug == True:
        with open("data.bin", "rb") as f:
            print(f.read())
            
i2c = I2C(0, scl=Pin(9), sda=Pin(8))
bmp = BMP(i2c)
mpu = MPU(i2c)

readData = False
tickCounter = 0
ticksPerWrite = 300 #divide by frequency for number of seconds per write command
frequency = 30
dataBuffer = bytearray()

def timerFunc(timerObj):
    global readData
    readData = True
    
timer = machine.Timer(-1)
timer.init(mode=machine.Timer.PERIODIC, freq=frequency, callback=timerFunc)

while True:
    if readData:
        accelX, accelY, accelZ = mpu.acceleration()
        gyroX, gyroY, gyroZ = mpu.gyroscope()
        dataBuffer.extend(ustruct.pack('>iIhhhhhh', bmp.temperature(), bmp.pressure(), accelX, accelY, accelZ, gyroX, gyroY, gyroZ))
        tickCounter += 1
        readData = False
    if tickCounter == ticksPerWrite:
        tickCounter = 0
        formatAndWrite(dataBuffer, False)
        dataArray = bytearray()