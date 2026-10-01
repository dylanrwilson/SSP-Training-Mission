# SSP-Training-Mission
Documentation & code for Team 1 CDHS

## BinToCSV
Python program for interpreting raw binary data from the microcontroller, converting it to a CSV and performing necessary calculations to make the data in standard units
- The Pico reads sensor data at [TBD]hz and records that data to its internal flash memory. In order to minimize the data size, and thus maximize the number of samples, the data will be stored as raw binary in a .bin file.
- This means upon data retrieval, an additional python script will be necessary to convert the binary data to a CSV file that can be processed using a program such as excel. That script can be found here.
- This documentation will largely consist of explaining how data is being stored and by extension what kind of processing is necessary to make is usable for future reference. 

### Things to Consider for Addition
- Delta encoding for temperature
- Storing in buffer to write larger data chunks
  + Pro: prevents premature wear on memory
  + Pro: higher throughput
  - Con: more data to be lost in event of power fault

### Temperature
- Data type: 16-bit signed integer
- Must be divided by 100 to achieve standard units
- Storing as 16-bit signed integer prevents conversion to a float data type, saving 2 bytes of data per sample

### Pressure
- Data type: 32-bit unsigned integer
- Must be divided by 256 to achieve standard units
- Storing as 32-bit unsigned integer prevents difficult, time-consuming floating-point division, increasing the speed of data handling

### Acceleration X, Y, Z
- Each to be stored as 16-bit signed integer
- Additional processing TBD depending on chosen library

### Gyroscope X, Y, Z
- Each to be stored as 16-bit signed integer
- Additional processing TBD depending on chosen library
