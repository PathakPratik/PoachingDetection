import constants
import socket
import random
import time
import threading

class SensorClass:

    def getData(self):
        while True:
            # Sending image from image sensor to identify if its a poacher or not
            filelist = ['water','Poacher1','Poacher2','cow','elephant']
            filename = filelist[random.randint(0,4)]
            image = {'Image': filename}

            # Sending location coordinates latitude and longitude
            lat = round(random.uniform(53.1, 60.9), 5)
            long = round(random.uniform(6.0, 6.9), 5)
            loc = {'latitude': lat, 'longitude': long}
            location = {'location': loc}
            print(location[location])

            # sending accelerometer values
            xaxis_acc = round(random.uniform(53.1, 60.9), 5)
            yaxis_acc = round(random.uniform(20.1, 60.9), 5)
            zaxis_acc = round(random.uniform(70.1, 900.9), 5)
            acc = {'X axis': xaxis_acc, 'Y axis': yaxis_acc, 'Z axis': zaxis_acc}
            accelerometer = {'accelerometer': acc}

            # sending battery value to check position of the drone
            batteryval = random.randint(10, 100)
            bat = {'Battery': batteryval}

            # sending gyrometer values to check angular position
            xaxis_gyr = round(random.uniform(53.1, 60.9), 5)
            yaxis_gyr = round(random.uniform(20.1, 60.9), 5)
            zaxis_gyr = round(random.uniform(70.1, 900.9), 5)
            gyr = {'X axis': xaxis_gyr, 'Y axis': yaxis_gyr,'Z axis': zaxis_gyr}
            gyro = {'Gyroscope': gyr}

            # sending barometer values to check height based on air pressure reading
            barom = round(random.uniform(14.1, 20.9), 3)
            bar = {'Barometer' : barom}

            host = socket.gethostbyname(socket.gethostname())
            sensor = SensorClass(host, constants.SENSOR_PORT)
            data = image.encode('utf-8')
            sensor.sock.sendto(data, (host, constants.SENSOR_PORT))
            time.sleep(30)

    def __init__(self, host, port):
        # getDataThread = threading.Thread(target=self.getData)
        # getDataThread.setDaemon(True)
        # getDataThread.start()
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        print(self.sock)

def main():
    print("main")

if __name__ == '__main__':
    main()