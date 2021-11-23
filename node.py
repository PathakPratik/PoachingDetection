import socket
import struct
import threading
import constants

MCAST_GRP = constants.MCAST_GRP
MCAST_PORT = constants.MCAST_PORT
IS_ALL_GROUPS = True
MULTICAST_TTL = constants.MULTICAST_TTL

class Node:
    
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        print(self.sock)

    def handleClient(self):
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if IS_ALL_GROUPS:
            # on this port, receives ALL multicast groups
            self.sock.bind(('', MCAST_PORT))
        else:
            # on this port, listen ONLY to MCAST_GRP
            self.sock.bind((MCAST_GRP, MCAST_PORT))
        
        print((MCAST_GRP, MCAST_PORT))
        print((self.host, constants.SENSOR_PORT))
        # This port will listen to unicast sensor communication
        self.sock.bind((self.host, constants.SENSOR_PORT))

        mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        while True:
            data, addr = self.sock.recvfrom(10240)
            print(data)
            # print(addr)
            # if addr not in addr_list:
            #     addr_list.append(addr)
            #     print("IP address list: ", addr_list)
            #     print(data)
        
    #Function to check if there is a drop in connection of any node
    def checkNodes(self):
        pass
        
    def start(self):
        listenerThread = threading.Thread(target=self.handleClient)
        listenerThread.setDaemon(True)
        listenerThread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")    
        print("[STARTING] server is starting...")
        # checkNodesThread = threading.Thread(target=self.checkNodes)
        # checkNodesThread.start()

    def sendMsgToAll(strMsg):
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)
        sock.sendto(b"strMsg", (MCAST_GRP, MCAST_PORT))
        
    def sendMsgToNode(strMsg, ip_addr):
        unicastSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        unicastSock.sendto(strMsg, ip_addr)

def main():
    hostname = socket.gethostname()
    host = socket.gethostbyname(hostname)
    print(hostname,host)
    node = Node(host, MCAST_PORT)
    node.start()
    # to test mcast handler is working
    node.sock.sendto(b"robot", (MCAST_GRP, MCAST_PORT))
    # to test unicast sensor handler is working
    node.sock.sendto(b"sensortest", (host, constants.SENSOR_PORT))
    while True:
        pass
    
if __name__ == '__main__':
    main()
    