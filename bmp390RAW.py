from machine import I2C

class bmp:
    ID_LOC = 0x00
    DATA_LOC = 0x04
    COEFF_START_LOC = 0x31
    SDA = 8
    SCL = 9
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