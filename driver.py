from machine import I2C

class BMP:
    ID_LOC = 0x00
    DATA_LOC = 0x04
    ADDRESS = 0x77
    
    def __init__(self, i2cObj):
        self.i2c = i2cObj
        
        if self.i2c.readfrom_mem(self.ADDRESS, self.ID_LOC, 1)[0] != 0x60:
            raise RuntimeError("BMP390 not found")
        
        self.i2c.writeto_mem(self.ADDRESS, 0x1C, b'\x00')#Set oversample rate to 1
        
        self.i2c.writeto_mem(self.ADDRESS, 0x1B, b'\x33')#Power mode normal
        
    def pressure(self):
        data = self.i2c.readfrom_mem(self.ADDRESS, self.DATA_LOC, 6)
        rawTemp = (data[2] << 16) | (data[1] << 8) | data[0]
        return rawTemp
    def temperature(self):
        data = self.i2c.readfrom_mem(self.ADDRESS, self.DATA_LOC, 6)
        rawPres = (data[5] << 16) | (data[4] << 8) | data[3]
        return rawPres
    
class MPU:
    ACCEL_OUT_BEGIN = 0x3B #6-bytes, 2 for each X, Y, Z
    GYRO_OUT_BEGIN = 0x43 #6-byte, 2 for each X, Y, Z
    ADDRESS = 0x68
    ID_LOC = 0x75
    
    def __init__(self, i2cObj):
        self.i2c = i2cObj
        
        if self.i2c.readfrom_mem(self.ADDRESS, self.ID_LOC, 1)[0] != 0x68:
            raise RuntimeError("MPU6050 not found")
        
        self.i2c.writeto_mem(self.ADDRESS, 0x19, b'\x4F') #sets gyroscope output to 8khz/(1 + 79) = 100hz, accelerometer downsamples to match 100hz frequency
        self.i2c.writeto_mem(self.ADDRESS, 0x6B, b'\x08') #takes out of sleep mode, disables temperature sensor, and selects internal crystal oscillator
        self.i2c.writeto_mem(self.ADDRESS, 0x1C, b'\x18') #selects highest full-scale range for accelerometer(+-16g)
        self.i2c.writeto_mem(self.ADDRESS, 0x1B, b'\x18') #selects highest full-scale range for gyroscope(+-2000 degrees/sec)
        
    def acceleration(self):
        data = self.i2c.readfrom_mem(self.ADDRESS, self.ACCEL_OUT_BEGIN, 6)
        accelX = (data[0] << 8) | data[1]
        accelY = (data[2] << 8) | data[3]
        accelZ = (data[4] << 8) | data[5]
        return accelX, accelY, accelZ
        
    def gyroscope(self):
        data = self.i2c.readfrom_mem(self.ADDRESS, self.GYRO_OUT_BEGIN, 6)
        gyroX = (data[0] << 8) | data[1]
        gyroY = (data[2] << 8) | data[3]
        gyroZ = (data[4] << 8) | data[5]
        return gyroX, gyroY, gyroZ
        