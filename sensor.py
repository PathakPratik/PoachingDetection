import constants
import socket

class Sensor:

     def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        print(self.sock)


def main():
    host = socket.gethostbyname(socket.gethostname())
    sensor = Sensor(host, constants.SENSOR_PORT)
    sensor.sock.sendto(b"sensorpush", (host, constants.SENSOR_PORT))

if __name__ == '__main__':
    main()