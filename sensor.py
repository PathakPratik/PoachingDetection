import constants
import socket
import random
import time

class SensorClass:

    def getData(self):
        while True:
            # Sending image from image sensor to identify if its a poacher or not
            print("SENDING DATA FROM SENSOR")
            host = socket.gethostbyname(socket.gethostname())
            sensor = SensorClass(host, constants.SENSOR_PORT)

            filelist = ['Scene1','Poacher1','Animal3','Animal1 ','Animal2','Scene2','Scene3','Scene4','Scene5','Animal4','Animal6','Scene6','Scene7','Scene8','Scene9','Scene10','Scene11','Scene12','Animal7','Animal8','Animal9']
            filename = filelist[random.randint(0,20)]
            image = f'{"Recieved Image is of : "}{filename}'
            encdata = image.encode("utf-8")
            print("Sending Image data from sensor")
            sensor.sock.sendto(encdata, (host, constants.SENSOR_PORT))

            # Sending location coordinates from
            lat = round(random.uniform(53.1, 60.9), 5)
            long = round(random.uniform(6.0, 6.9), 5)
            # loc = {'latitude': lat, 'longitude': long}
            loc = f'{"Recieved Location - latitude : "}{lat}{" longitude : "}{long}'
            encdata = loc.encode("utf-8")
            print("Sending Location data from sensor")
            sensor.sock.sendto(encdata, (host, constants.SENSOR_PORT))

            xaxis_acc = round(random.uniform(53.1, 60.9), 5)
            yaxis_acc = round(random.uniform(20.1, 60.9), 5)
            zaxis_acc = round(random.uniform(70.1, 900.9), 5)
            acc = f'{"Recieved Accelerometer X axis: "}{xaxis_acc}{"Y axis:"}{yaxis_acc}{"Z axis:"}{zaxis_acc}'
            encdata = image.encode("utf-8")
            print("Sending Accelerometer data from sensor")
            sensor.sock.sendto(encdata, (host, constants.SENSOR_PORT))

            batteryval = f'{"Battery:"}{random.randint(10, 100)}'
            encdata = batteryval.encode("utf-8")
            print("Sending Battery data from sensor")
            sensor.sock.sendto(encdata, (host, constants.SENSOR_PORT))

            xaxis_gyr = round(random.uniform(53.1, 60.9), 5)
            yaxis_gyr = round(random.uniform(20.1, 60.9), 5)
            zaxis_gyr = round(random.uniform(70.1, 90.9), 5)
            gyr = f'{"Recieved Gyroscope - X axis:"}{xaxis_gyr}{"Y axis:"}{yaxis_gyr}{"Z axis:"}{zaxis_gyr}'
            encdata = gyr.encode("utf-8")
            print("Sending Gyroscope data from sensor")
            sensor.sock.sendto(encdata, (host, constants.SENSOR_PORT))

            xaxis_mag = round(random.uniform(50, 60.9), 5)
            yaxis_mag = round(random.uniform(50.1, 60.9), 5)
            zaxis_mag = round(random.uniform(0, 20.9), 5)
            mag = f'{"Recieved Magnetometer - X axis:"}{xaxis_mag}{"Y axis:"}{yaxis_mag}{"Z axis:"}{zaxis_mag}'
            encdata = mag.encode("utf-8")
            print("Sending Magnetometer data from sensor")
            sensor.sock.sendto(encdata, (host, constants.SENSOR_PORT))

            barom = round(random.uniform(14.1, 20.9), 5)
            battery = f'{"Recieved Barometer :"}{barom}'
            encdata = battery.encode("utf-8")
            print("Sending Barometer data from sensor")
            sensor.sock.sendto(encdata, (host, constants.SENSOR_PORT))
            time.sleep(30)

    def _init_(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

def main():
    print("main")

if __name__ == '_main_':
    main()