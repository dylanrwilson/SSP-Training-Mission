# SSP-Training-Mission
Documentation & code for Team 1 CDHS

## main.py
The firmware to be uploaded to the Raspberry Pi Pico. Contains necessary configuration for I2C protocol and formatting structure for writing the binary data file. By adjusting the `frequency` and `ticksPerWrite` variables, you can modify the number of data samples taken per second and the number of samples stored in buffer before writing the data to the non-volatile flash memory. It is important to note that this is a balancing act; flash memory only contains ~100,000 write cycles in its working lifespan, which can quickly be reached using high sample rates. This can be balanced by increasing the number of samples per write, effectively reducing the number of writes necessary to log a given quantity of samples. The drawback of this is a higher risk of data loss, as in the event of a power system fault or any other catastrophic failure, the data stored in buffer will not be written to the binary data file. 

**DISCLAIMER:** the drivers are currently configured to down-sample the update frequency of the sensors to 100hz. Should you wish to exceed this frequency for your data collection frequency(which is ill-advised), you must reconfigure the drivers to allow for faster update speeds.

## driver.py
Contains the custom drivers for the MPU6050 and the BMP390 for use in the SSP Training Mission. Designed to be lightweight and efficient, including outputting raw data to minimize processing delays. Custom drivers allowed us to easily configure the sensors in the states that we needed them directly in the firmware. This keeps the file size super small, because it lacks infrastructure to change configuration from the main.py script, a functionality that is unnecessary in this application. 

## BinToCSV
Python program for interpreting raw binary data from the microcontroller, converting it to a CSV and performing necessary calculations to make the data in standard units
- The Pico reads sensor data at [TBD]hz and records that data to its internal flash memory. In order to minimize the data size, and thus maximize the number of samples, the data will be stored as raw binary in a .bin file.
- This means upon data retrieval, an additional python script will be necessary to convert the binary data to a CSV file that can be processed using a program such as excel. That script can be found here.
- This documentation will largely consist of explaining how data is being stored and by extension what kind of processing is necessary to make is usable for future reference.

---

### Things to Consider for Addition
- [ ] Delta encoding for temperature(?)
- [x] ~~Storing in buffer to write larger data chunks~~
- [ ] Modify oversample rate and output data rate to reduce noise in pressure readings, contingent upon frequency of sensor reading

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
