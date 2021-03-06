import socket
import sys
import getch
from scapy.all import *
from struct import *
from socket import *
from select import select

#Consts
TIME_OUT = 10
UDP_PORT = 13117 # change to 13117
BUFFER_SIZE = 1024
COOKIE = 0xabcddcba
MSG_TYPE = 0x2
TEAM_NAME = "Dothraki"
ETHERNET = "eth2" # to chagne to eht2 in testing


#colors for fun
BOLD = '\033[1m'
RED = '\033[91m'
PURPLE = '\033[95m'
BLUE = '\033[94m'
RESET = "\x1b[0m"


def mainF():
    myIp = get_if_addr(ETHERNET)
    UDPclient = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP) # UDP
    UDPclient.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)
    UDPclient.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    UDPclient.bind((myIp, UDP_PORT))
    while True: # serching for connections
        print(BLUE+"\nClient started, listening for offer requests...\n"+RESET)
        data, addr = UDPclient.recvfrom(BUFFER_SIZE)
        try:
            cookie, msg_type, tcp_port = unpack('LBH',data)
            if(cookie != COOKIE or msg_type != MSG_TYPE):
                raise "m"
            print(BOLD+"Received offer from {0}, attempting to connect...".format(addr[0])+RESET)
            TCPclient = socket(AF_INET, SOCK_STREAM) # create tcp socket
            toConnectTo = (addr[0],tcp_port)
            TCPclient.connect(toConnectTo)
            TCPclient.send(TEAM_NAME.encode()) # sends team name over tcp
            msg = TCPclient.recv(BUFFER_SIZE).decode() # get message from server + question
            print(msg)
            game(TCPclient)
            print(RED + "Server disconnected, listening for offer requests..." + RESET)

        except error:
            print(error)
            print(RED+"socket error, searching for another connection\n\n"+RESET)

        except:
            print(BOLD+"Received offer from {0}".format(addr[0])+RESET)
            print(RED+"Message is not supported ! "+RESET)



def game(TCPsocket):
    try:
        reads, out, e = select([sys.stdin, TCPsocket], [], [], TIME_OUT) # waits timeout time for input from the client
        if(sys.stdin in reads):
        # Means we got input from stdin, we should write it to the socket
            answer = sys.stdin.readline()[0].encode()
            TCPsocket.send(answer) # sends answer
        response = TCPsocket.recv(BUFFER_SIZE).decode() # get final message from the server
        print(response)
    except:
        TCPsocket.close()
        print(RED+"Something went wrong in the answerQuestion method"+RESET)

if __name__ == "__main__":
    mainF()
