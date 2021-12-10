import socket
import struct
import threading
import constants
import time
import sys
import json
from sensor import SensorClass

MCAST_DISC_PORT = constants.MCAST_DISC_PORT
MCAST_ROUTING_PORT = constants.MCAST_ROUTING_PORT
IS_ALL_GROUPS = True
MULTICAST_TTL = constants.MULTICAST_TTL

class Node:
    nodeTimestampList = {}
    nodeName = ""
    routingDB = {}
    discoverDB = {}
    
    def __init__(self, host, port, hostname, networkname):
        self.host = host
        self.hostname = hostname
        self.port = port
        self.mcast_grp = constants.MCAST_GRP[int(networkname.replace('network', '')) - 1]
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.unicastsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.routingsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.gatewaysock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        
    def setNodeName(self, name):
        self.nodeName = name
        
    def handleRootFailure(self):
        minNode = 1000000
        #Iterate through the entire list of nodes and find out the lowest number
        for addr in list(self.discoverDB):
            nodeNumber = addr[4:]
            print("THIS IS NODE NUMBER::", int(nodeNumber))
            if int(nodeNumber) < minNode:
                minNode = int(nodeNumber)
                
        newRoot = "node" + str(minNode)
        #If this is the nim node, set noneName to root
        if self.nodeName == newRoot:
            self.setNodeName("root")
            print("node", minNode, " is new root")
        
    def handleRouting(self):
        self.routingsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if IS_ALL_GROUPS:
            # on this port, receives ALL multicast groups
            self.routingsock.bind(('', MCAST_ROUTING_PORT))
        else:
            # on this port, listen ONLY to MCAST_GRP
            self.routingsock.bind((self.mcast_grp, MCAST_ROUTING_PORT))

        mreq = struct.pack("4sl", socket.inet_aton(self.mcast_grp), socket.INADDR_ANY)
        self.routingsock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        while True:
            data, addr = self.routingsock.recvfrom(10240)
            broadcastDBJson = data.decode("utf-8")
            print("BROADCAST DB RECEIVED:::: ", broadcastDBJson)
            db = json.loads(broadcastDBJson)
            for key in db:    #Take every key in the incoming db
                print("AFTER PARSING:: ", db[key]);
                currentValue = self.routingDB[key]
                newValue = db[key]
                newValue[1] = newValue[1]+1   #Increment hop
                
                if key == self.nodeName:
                    continue                 # This is out own key, do nothing
                if key in self.routingDB:    # If key is present in routingDB
                    
                    if currentValue[1] > newValue[1]:     # If current hop count is greater than received hop count, replace with new
                        self.routingDB[key] = newValue 
                        print("routingDB after entry::", self.routingDB)
                    else:                        # key is not present in DB, so make a new entry
                        self.routingDB[key] = newValue
            
    def broadcastDatabase(self):
        while(True):
            #Create the routing database
            for node in self.discoverDB:
                values = self.discoverDB[node]
                self.routingDB[node] = values
                print("Routing DB new entry::: ", self.routingDB)
            print("Routing DB: ", self.routingDB)
            self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)
            dict_json = json.dumps(self.routingDB)
            print("!!!!!!!!!!!!!", dict_json)
            self.sock.sendto(dict_json.encode('utf-8'), (self.mcast_grp, MCAST_ROUTING_PORT))
            print(self.nodeName, " has broadcasted its database...")
            time.sleep(30)


    def handleDiscovery(self):
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if IS_ALL_GROUPS:
            # on this port, receives ALL multicast groups
            self.sock.bind(('', MCAST_DISC_PORT))
        else:
            # on this port, listen ONLY to self.mcast_grp
            self.sock.bind((self.mcast_grp, MCAST_DISC_PORT))

        mreq = struct.pack("4sl", socket.inet_aton(self.mcast_grp), socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        while True:
            data, addr = self.sock.recvfrom(10240)
            nodeName = data.decode("utf-8")
            print(time.time(), "::Received message in handleDiscovery: ", nodeName, " from IP: ", addr)
            self.nodeTimestampList[nodeName] = time.time()
            print("handleDiscovery IP Address List: ",self.nodeTimestampList)
            if addr not in list(self.nodeTimestampList):
                self.discoverDB[nodeName] = list()
                values = [addr, 1]
                self.discoverDB[nodeName].extend(values)
                
            print("Node ", self.nodeName, "connected to: ", self.discoverDB[nodeName])
            detail = self.discoverDB[nodeName]
            print(detail[0])
            print(detail[1])

    def generateSensorData(self):
        hostname = socket.gethostname()
        host = socket.gethostbyname(hostname)
        sensorobj = SensorClass(host, constants.SENSOR_PORT)
        while True:
            sensorobj.getData()

    def listenToSensor(self):
        self.unicastsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
        # This port will listen to unicast sensor communication
        self.unicastsock.bind((self.hostname, constants.SENSOR_PORT))

        while True:
            data, _ = self.unicastsock.recvfrom(10240)
            if self.nodeName == "root":
                self.detectPoacher(data)

    def detectPoacher(self, data):
        print("SENSOR DATA RECIEVED")
        sensorJson = data.decode("utf-8")
        if (sensorJson[:14] == "Recieved Image"):
            if( sensorJson.find('Poacher') != -1 ):
                print("################### SOS #######################")
                print("----------   POACHER HAS APPEARED  -----------")
                print("################### SOS #######################")
        else:
            print(sensorJson)

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
                    self.discoverDB.pop(addr)
                    self.routingDB.pop(addr)
                    if addr == 'root':
                        self.handleRootFailure()
                    
            time.sleep(60)

    def gatewayListen(self):
        self.gatewaysock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.gatewaysock.bind((self.hostname, constants.INTERNETWORK_PORT))

        while True:
            data, _ = self.gatewaysock.recvfrom(10240)
            # if self.nodeName == "root":
            print("################ INTERNETWORK DATA ###########")
            print(data)    
            print("################ INTERNETWORK DATA ###########")

    def start(self, nodeName):
        self.setNodeName(str(sys.argv[1]))
        
        gatewayThread = threading.Thread(target=self.gatewayListen)
        gatewayThread.setDaemon(True)
        gatewayThread.start()

        discoveryThread = threading.Thread(target=self.handleDiscovery)
        discoveryThread.setDaemon(True)
        discoveryThread.start()
        
        SensorThread = threading.Thread(target=self.listenToSensor)
        SensorThread.setDaemon(True)
        SensorThread.start()
            
        print("[STARTING] server is starting...")
        
        checkNodesThread = threading.Thread(target=self.checkNodes)
        checkNodesThread.setDaemon(True)
        checkNodesThread.start()
        
        broadcastNodeThread = threading.Thread(target=self.broadcastNode)
        broadcastNodeThread.setDaemon(True)
        broadcastNodeThread.start()
        
        time.sleep(15)
        
        routingThread = threading.Thread(target=self.handleRouting)
        routingThread.setDaemon(True)
        routingThread.start()
        
        broadcastDatabaseThread = threading.Thread(target=self.broadcastDatabase)
        broadcastDatabaseThread.setDaemon(True)
        broadcastDatabaseThread.start()

        getDataThread = threading.Thread(target=self.generateSensorData)
        getDataThread.setDaemon(True)
        getDataThread.start()

    def broadcastNode(self):
        while(True):
            self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)
            self.sock.sendto(self.nodeName.encode('utf-8'), (self.mcast_grp, MCAST_DISC_PORT))
            print(self.nodeName, " has broadcasted...")
            time.sleep(30)

    def unicastNode(self, strMsg, nodeName):
        unicastSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        record = self.routingDB[nodeName]
        ip_addr = record[0]
        unicastSock.sendto(strMsg, ip_addr)

def main():
    hostname = socket.gethostname()
    host = socket.gethostbyname(hostname)
    networkname = sys.argv[2].replace('network', '')
    
    if(not networkname.isdigit()):
        print("Please enter a valid network name")
        exit(1)

    node = Node(host, MCAST_DISC_PORT, hostname, networkname)
    
    node.start(str(sys.argv[1]))

    # Testing internetwork connection
    node.gatewaysock.sendto(b"InterNetwork", (host, constants.INTERNETWORK_PORT))

    while True:
        pass
    
if __name__ == '__main__':
    main()
    
