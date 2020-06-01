import socket
import sys
import re
import select

# create TCP welcoming socket
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
if len(sys.argv) != 2:
    print("please use this format: python3 chatserver server_addr:port number")
    sys.exit(1)
args = str(sys.argv[1]).split(':')
host = str(args[0])# create TCP welcoming socket
port = int(args[1])
s.bind((host, port))
s.listen(100)
client_list=[]  # creates an array of list of clients to save them
client_list.append(s)
temp_client_list=[]  # creates a array of temporary list which will be proceeded to permanent list if no errors of input
permanent_client_list=[]  # creates a array of permanent list
permanent_client_list_dictionary={}  # creates an array of dictionary of permanent list which will assign the nick to the address

def broadcast(msg,conn):
    for sock in permanent_client_list:
        if sock!= conn:
            print('broadcasting')
            try:
                sock.sendall(msg.encode('utf_8'))
            except:
                sock.close()
                permanent_client_list.remove(sock)
                del permanent_client_list_dictionary[sock]
                client_list.remove(sock)
def main():
    print("HI, server started running on " ,host, port )
    while True:
        readsock,writesock,errorsock=select.select(client_list,[],[])
        for sock in readsock:
            if sock==s:
                newsock,addr=s.accept()
                newsock.sendall('Hello 1'.encode('utf_8'))
                client_list.append(newsock)
                temp_client_list.append(newsock)
            elif sock in temp_client_list:
                try:
                    nick=sock.recv(1024).decode('utf_8')
                    if nick:
                        found=re.search(r'NICK\s(\S*)',nick)
                        name=str(found.group(1))
                        if len(name)>12:
                            sock.sendall('Error : nicknames are limited to 12 characters '.encode('utf_8'))
                        elif re.search(r'!',name) or re.search(r'@',name) or re.search(r'#',name) or re.search(r'\$',name) or re.search(r'%',name) or re.search(r'\*',name) or re.search(r'\^',name):
                            sock.sendall('Error don\'t use special characters in your nick names'.encode('utf_8'))
                        elif found:
                            sock.sendall(('Welcome to chat '+str(name)).encode('utf_8'))
                            permanent_client_list.append(sock)
                            permanent_client_list_dictionary[sock]=name
                            temp_client_list.remove(sock)
                        else:
                            sock.sendall('Error -> BAD COMMAND ACTUAL COMMAND PROTOCOL NICK <nick>'.encode('utf_8'))
                    else:
                        sock.close()
                        client_list.remove(sock)
                        temp_client_list.remove(sock)
                except:
                    continue
            elif sock in permanent_client_list:
                try:
                    msg=sock.recv(1024).decode('utf_8')
                    if msg:
                        found=re.search(r'MSG\s',msg)
                        if len(msg)>259:
                            sock.sendall('Error message length should not exceed 256 characters'.encode('utf_8'))
                        elif found:
                            msg_to_send='MSG '+str(permanent_client_list_dictionary[sock])+': '+msg[4:]
                            broadcast(msg_to_send,sock)
                        else:
                            sock.sendall('Error BAD COMMAND ACTUAL COMMAND MSG <msg>'.encode('utf_8'))
                    else:
                        sock.close()
                        client_list.remove(sock)
                        permanent_client_list.remove(sock)
                        del permanent_client_list_dictionary[sock]
                except:
                    continue

    s.close()
if __name__ == "__main__":
    main()
