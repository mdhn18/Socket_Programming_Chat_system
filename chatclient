#!/usr/bin/python3
import socket
import select
import sys
import re


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) != 3:
    print("please use this Format: chatclient,HOST IP address:port NO, Nickname")
    sys.exit(1)
args = str(sys.argv[1]).split(':')
host = str(args[0])
port = int(args[1])
nick = str(sys.argv[2])
s.connect((host, port))
MESSAGE= s.recv(1024).decode('utf-8')
print(MESSAGE)
s.sendall(('NICK '+nick).encode('utf-8'))
ok = s.recv(1024).decode('utf-8')
if re.search('Error',ok) or re.search('ERROR',ok):
    print(ok)
    sys.exit()
print(ok)
while True:
    sockets = [sys.stdin, s]
    read_sockets,write_sockets, error_sockets = select.select(sockets, [], [])
    for sock in read_sockets:
        if sock == s:
            message = sock.recv(2048).decode('utf-8')
            if re.search(r'Error',message) or re.search(r'ERROR',message):
                print (message)
            else:
                message = message[4:]#stripping the message removing MSG and giving it to print out as per the protocol
                print (message)
        else:
            message = sys.stdin.readline()
            if message == '\n':
                continue
            else:
                s.sendall(('MSG '+message).encode('utf-8'))
s.close()
