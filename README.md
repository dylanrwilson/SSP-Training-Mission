# SSP-Training-Mission
Documentation & code for Team 1 CDHS

## BinToCSV
Python program for interpreting raw binary data from the microcontroller, converting it to a CSV and performing necessary calculations to make the data in standard units
- The Pico reads sensor data at [TBD]hz and records that data to its internal flash memory. In order to minimize the data size, and thus maximize the number of samples, the data will be stored as raw binary in a .bin file.
- This means upon data retrieval, an additional python script will be necessary to convert the binary data to a CSV file that can be processed using a program such as excel. That script can be found here.
- This documentation will largely consist of explaining how data is being stored and by extension what kind of processing is necessary to make is usable for future reference. 

### Things to Consider for Addition
- Delta encoding for temperature(?)
- ~~Storing in buffer to write larger data chunks~~
- Modify oversample rate and output data rate to reduce noise in pressure readings, contingent upon frequency of sensor reading

### Temperature
- Data type: 32-bit signed integer
- Due to 24-bit resolution of the BMP390, a 32-bit integer is the only option for data storage without data loss
- To avoid slow and taxing calculations, the raw sensor data will be recorded in binary, and then they will be processed according to the datasheet by BinToCSV upon retrieval

### Pressure
- Data type: 32-bit unsigned integer
- Due to 24-bit resolution of the BMP390, a 32-bit integer is the only option for data storage without data loss
- To avoid slow and taxing calculations, the raw sensor data will be recorded in binary, and then they will be processed according to the datasheet by BinToCSV upon retrieval

### Acceleration X, Y, Z
- Each to be stored as 16-bit signed integer
- Additional processing TBD depending on chosen library

### Gyroscope X, Y, Z
- Each to be stored as 16-bit signed integer
- Additional processing TBD depending on chosen library
