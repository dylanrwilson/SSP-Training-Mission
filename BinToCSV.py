import struct
import csv

#Calibration Coefficients
T1 = 7069184.0
T2 = 1.8200838e-05
T3 = -2.4868996e-14
P1 = 0.0069065096 - (2**14 / 2**20)
P2 = 1.0756776e-05 - (2**14 / 2**29)
P3 = 1.3969838e-09
P4 = 7.275958e-12
P5 = 154680.0
P6 = 369.84376
P7 = 0.01171875
P8 = -0.000183105468
P9 = 1.4271252e-11
P10 = 2.1316282e-14
P11 = -2.981556e-19

def decode(file):
    with open(file, "rb") as f:
        totalbin = bytearray(f.read())
        decodedList = list(struct.unpack(f'>{"iIhhhhhh" * (len(totalbin)//20)}', totalbin))
    return decodedList
    
def normalizeTemp(temp):
    pd1 = temp - T1
    pd2 = pd1 * T2
    temperature = pd2 + (pd1 * pd1) * T3
    return round(temperature, 4)

def normalizePres(pres, temp):
    pd1 = P6 * temp
    pd2 = P7 * (temp ** 2)
    pd3 = P8 * (temp ** 3)
    po1 = P5 + pd1 + pd2 + pd3
    pd1 = P2 * temp
    pd2 = P3 * (temp ** 2)
    pd3 = P4 * (temp ** 3)
    po2 = pres * (P1 + pd1 + pd2 + pd3)
    pd1 = pres ** 2
    pd2 = P9 + P10 * temp
    pd3 = pd1 * pd2
    pd4 = pd3 + (pres ** 3) * P11    
    pressure = (po1 + po2 + pd4)  # Output in Pa
    return pressure

def binToCSV(binList):
    with open("data.csv", 'w', newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Temperature", "Pressure", "Acceleration X", "Acceleration Y", "Acceleration Z", "Gyroscope X", "Gyroscope Y", "Gyroscope Z"])
        binListOfMeasures = []
        for i in range(len(binList)//8):
            binListOfMeasures.append(binList[i*8:(i*8+8)])
        for i in binListOfMeasures[:]:
            i[0] = normalizeTemp(i[0])
            i[1] = normalizePres(i[1], i[0])
        writer.writerows(binListOfMeasures)

filename = input("Filename: ")
binToCSV(decode(filename))