
import socket
import threading
import time

class TelloConnection:

    def __init__(self):
        self.serverAddressPort = ("192.168.10.1", 8889)
        self.bufferSize = 1024
        self.TIME_OUT = 5

        #Create a UDP socket at client side
        self.local_ip = ''
        self.local_port = 8889
        self.UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.UDPClientSocket.bind((self.local_ip, self.local_port))

        #set up listener thread
        self.thread = threading.Thread(target=self._ResponseListener)
        self.thread.daemon = True   #daemon = True makes it so that self.thread shutsdown when main thread is shutting down
        self.thread.start()     #starts _ResponseListener

        #Send the following commands
        commands = ["command", "land"]
        for command in commands:
            if isinstance(command, int) == True:
                time.sleep(command)
            else:
                self.sendCommand(command)

        #idle while _ResponseListener runs in background
        time.sleep(self.TIME_OUT)
        self.sendCommand("emergency") #shutsdown all motors
        print("TIME OUT of %s has been reached, shutting down.." % self.TIME_OUT)

        time.sleep(3)

    def sendCommand(self, command):
        bytesToSend = str.encode(command) #the command "command" sets Tello in a state in which it will listen to further commands
        self.UDPClientSocket.sendto(bytesToSend, self.serverAddressPort)
        print('sending command: %s to %s' % (command, self.serverAddressPort))

    def _ResponseListener(self):
        while True:
            self.response, ip = self.UDPClientSocket.recvfrom(self.bufferSize)
            print('from %s: %s' % (ip, self.response))

if __name__ == "__main__":
    tello = TelloConnection()
