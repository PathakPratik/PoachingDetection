import socket
import struct
import threading
import constants
import time

MCAST_GRP = constants.MCAST_GRP
MCAST_DISC_PORT = constants.MCAST_DISC_PORT
IS_ALL_GROUPS = True
MULTICAST_TTL = constants.MULTICAST_TTL

class Node:
    nodeTimestampList = {}
    nodeName = ""
    
    def __init__(self, host, port, hostname):
        self.host = host
        self.hostname = hostname
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.unicastsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        
    def setNodeName(self,name):
        self.nodeName = name

    def handleDiscovery(self):
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if IS_ALL_GROUPS:
            # on this port, receives ALL multicast groups
            self.sock.bind(('', MCAST_DISC_PORT))
        else:
            # on this port, listen ONLY to MCAST_GRP
            self.sock.bind((MCAST_GRP, MCAST_DISC_PORT))

        mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        while True:
            data, addr = self.sock.recvfrom(10240)
            print(time.time(), "::Received message in handleDiscovery: ", data, " from IP: ", addr)
            self.nodeTimestampList[addr] = time.time()
            print("handleDiscovery IP Address List: ",self.nodeTimestampList)

    def listenToSensor(self):
        # Remove this after we decide how to adress each node
        self.unicastsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # This port will listen to unicast sensor communication
        self.unicastsock.bind((self.hostname, constants.SENSOR_PORT))

        while True:
            data, _ = self.unicastsock.recvfrom(10240)
            print(data)

    #Function to check if there is a drop in connection of any node
    def checkNodes(self):
        while(True):
            currTime = time.time()
            for addr in list(self.nodeTimestampList):
                print("checkNodes:: Checking if node ", addr, " is present...")
                if currTime - self.nodeTimestampList[addr] > 180:
                    #Remove the address and timestamp from the list
                    print("Removing node ", addr, " from list, as difference between timestamps is: ", currTime - self.nodeTimestampList[addr])
                    self.nodeTimestampList.pop(addr)
                    print("removed")
                    
            time.sleep(5)
        
    def start(self):
        self.setNodeName("root")
        listenerThread = threading.Thread(target=self.handleDiscovery)
        listenerThread.setDaemon(True)
        listenerThread.start()
        SensorThread = threading.Thread(target=self.listenToSensor)
        SensorThread.setDaemon(True)
        #SensorThread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")    
        print("[STARTING] server is starting...")
        checkNodesThread = threading.Thread(target=self.checkNodes)
        checkNodesThread.start()
        broadcastNodeThread = threading.Thread(target=self.broadcastNode)
        broadcastNodeThread.start()
        
    def broadcastNode(self):
        while(True):
            self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)
            self.sock.sendto(self.nodeName.encode('utf-8'), (MCAST_GRP, MCAST_DISC_PORT))
            print(self.nodeName, " has broadcasted...")
            time.sleep(10)

    def sendMsgToAll(strMsg):
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)
        sock.sendto(b"strMsg", (MCAST_GRP, MCAST_DISC_PORT))
        
    def sendMsgToNode(strMsg, ip_addr):
        unicastSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        unicastSock.sendto(strMsg, ip_addr)

def main():
    hostname = socket.gethostname()
    host = socket.gethostbyname(hostname)
    node = Node(host, MCAST_DISC_PORT, hostname)
    node.start()
    # to test mcast handler is working
    node.sock.sendto(b"robot", (MCAST_GRP, MCAST_DISC_PORT))
    # to test unicast sensor handler is working
    #node.unicastsock.sendto(b"sensortest", (hostname, constants.SENSOR_PORT))
    while True:
        pass
    
if __name__ == '__main__':
    main()
    