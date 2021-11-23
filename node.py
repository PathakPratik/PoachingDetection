import socket
import struct
import threading

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007
IS_ALL_GROUPS = True
MULTICAST_TTL = 2

class Node:
    
    def __init__():
        self.host = host
        self.port = port
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    def handleClient():
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if IS_ALL_GROUPS:
            # on this port, receives ALL multicast groups
            sock.bind(('', MCAST_PORT))
        else:
            # on this port, listen ONLY to MCAST_GRP
            sock.bind((MCAST_GRP, MCAST_PORT))
        mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        while True:
            data, addr = sock.recvfrom(10240)
            print(data)
            print(addr)
            if addr not in addr_list:
                addr_list.append(addr)
                print("IP address list: ", addr_list)
                print(data)
        
    #Function to check if there is a drop in connection of any node
    def checkNodes():
        pass
        
    def start():
        listenerThread = threading.Thread(target=handleClient)
        listenerThread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")    
        print("[STARTING] server is starting...")
        checkNodesThread = threading.Thread(target=checkNodes)
        checkNodesThread.start()

    def sendMsgToAll(strMsg):
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)
        sock.sendto(b"strMsg", (MCAST_GRP, MCAST_PORT))
        
    def sendMsgToNode(strMsg, ip_addr):
        unicastSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        unicastSock.sendto(strMsg, ip_addr)

def main():
    hostname = socket.gethostname()
    host = socket.gethostbyname(hostname)
    node = Node(host, MCAST_PORT)
    
if __name__ == '__main__':
    main()
    