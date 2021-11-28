# import constants
import socket
import numpy as np
import random
import argparse
from PIL import Image
import constants



class Sensor:

    def imgarray(self):
        # im = Image.open('D:/DEsktop/Scalable Assignments/Project3/Images/poacher1.jpg')
        # rgb = np.array(im.convert('RGB'))
        # r = rgb[:, :, 0]
        # filelist = ['poacher1','lion','tiger','fox','poacher2','poacher3','bear','wolf','horse','giraffe','deer','scene1','scene2','scene3']
        filelist = ['water','Poacher1','Poacher2','cow','elephant']
        filename = filelist[random.randint(0,4)]
        print(filename)
        return filename

    def locate(self):
        return random.randint(40, 60)

    def accelerometer(self):
        x = random.randint(0, 20)
        y = random.randint(30, 50)
        z = random.randint(60, 80)
        acc = f'{"x axis : "}{x}{", y axis : "}{y}{", z axis : "}{z}'
        print("hi")
        print(acc)
        return acc

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        print(self.sock)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--sensorType', help='Type of Sensor', type=str)
    parser.add_argument('--area', help='Node Area', type=str)
    args = parser.parse_args()
    print(args.sensorType)

    host = socket.gethostbyname(socket.gethostname())
    sensor = Sensor(host, constants.SENSOR_PORT)

    if args.sensorType == 'Image':
        val = sensor.imgarray()
        valstr = val
        valcd = valstr.encode('utf-8')
        sensor.sock.sendto(valcd, (host, constants.SENSOR_PORT))

    if args.sensorType == 'Location':
        loc = sensor.locate()
        locstr = f'{"Location : "}{loc}'
        loccd = locstr.encode('utf-8')
        print(locstr)
        sensor.sock.sendto(loccd, (host, constants.SENSOR_PORT))

    if args.sensorType == 'Accelerometer':
        acc = sensor.accelerometer()
        accstr = f'{"Accelerometer : "}{acc}'
        acccd = accstr.encode('utf-8')
        print(accstr)
        sensor.sock.sendto(acccd, (host, constants.SENSOR_PORT))

    if args.sensorType == 'Barometer':
        acc = sensor.accelerometer()
        accstr = f'{"Barometer : "}{acc}'
        acccd = accstr.encode('utf-8')
        print(accstr)
        sensor.sock.sendto(acccd, (host, constants.SENSOR_PORT))

if __name__ == '__main__':
    main()
