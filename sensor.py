import constants
import socket
import random
import time
import json
import threading

class SensorClass:

    def getData(self):
        while True:
            # Sending image from image sensor to identify if its a poacher or not
            print("SENDING DATA FROM SENSOR")
            host = socket.gethostbyname(socket.gethostname())
            sensor = SensorClass(host, constants.SENSOR_PORT)

            filelist = ['water','Poacher1','Poacher2','cow','elephant']
            filename = filelist[random.randint(0,4)]
            image = f'{"Image is of : "}{filename}'
            encdata = image.encode("utf-8")
            sensor.sock.sendto(encdata, (host, constants.SENSOR_PORT))

            # Sending location coordinates from
            lat = round(random.uniform(53.1, 60.9), 5)
            long = round(random.uniform(6.0, 6.9), 5)
            # loc = {'latitude': lat, 'longitude': long}
            loc = f'{"Location - latitude : "}{lat}{" longitude : "}{long}'
            encdata = loc.encode("utf-8")
            sensor.sock.sendto(encdata, (host, constants.SENSOR_PORT))

            xaxis_acc = round(random.uniform(53.1, 60.9), 5)
            yaxis_acc = round(random.uniform(20.1, 60.9), 5)
            zaxis_acc = round(random.uniform(70.1, 900.9), 5)
            acc = f'{"X axis: "}{xaxis_acc}{"Y axis:"}{yaxis_acc}{"Z axis:"}{zaxis_acc}'
            encdata = image.encode("utf-8")
            sensor.sock.sendto(encdata, (host, constants.SENSOR_PORT))

            batteryval = f'{"Battery:"}{random.randint(10, 100)}'
            encdata = batteryval.encode("utf-8")
            sensor.sock.sendto(encdata, (host, constants.SENSOR_PORT))

            xaxis_gyr = round(random.uniform(53.1, 60.9), 5)
            yaxis_gyr = round(random.uniform(20.1, 60.9), 5)
            zaxis_gyr = round(random.uniform(70.1, 900.9), 5)
            gyr = f'{" Gyroscope - X axis:"}{xaxis_gyr}{"Y axis:"}{yaxis_gyr}{"Z axis:"}{zaxis_gyr}'
            encdata = gyr.encode("utf-8")
            sensor.sock.sendto(encdata, (host, constants.SENSOR_PORT))

            barom = round(random.uniform(14.1, 20.9), 5)
            battery = f'{"Battery :"}{barom}'
            encdata = battery.encode("utf-8")
            sensor.sock.sendto(encdata, (host, constants.SENSOR_PORT))

            print("Data sent")
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
    hostname = socket.gethostname()
    host = socket.gethostbyname(hostname)
    # sensor = SensorClass(host, constants.SENSOR_PORT)
    # sensor.getData()

if __name__ == '__main__':
    main()