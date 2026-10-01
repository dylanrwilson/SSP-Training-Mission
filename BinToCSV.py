import struct
import csv

def decode(file):
    with open(file, "rb") as f:
        totalbin = bytearray(f.read())
        decodedList = list(struct.unpack(f'>{"hLhhhhhh" * (len(totalbin)//18)}', totalbin))
    return decodedList
    
def binToCSV(binList):
    with open("data.csv", 'w', newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Temperature RAW", "Pressure RAW", "Acceleration X", "Acceleration Y", "Acceleration Z", "Gyroscope X", "Gyroscope Y", "Gyroscope Z"])
        binListOfMeasures = []
        for i in range(len(binList)//8):
            binListOfMeasures.append(binList[i*8:(i*8+8)])
        for i in binListOfMeasures[:]:
            i[0] /= 100
            i[1] /= 256
        writer.writerows(binListOfMeasures)

filename = input("Filename: ")
binToCSV(decode(filename))
