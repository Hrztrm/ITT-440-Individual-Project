import socket

s = socket.socket()
serv_ip = "192.168.56.104"
port = 8888
command = 5
hostname = "www.youtube.com"
ip = "8.8.8.8"
buf = 4096
try:
    s.connect((serv_ip,port))
except socket.error as e:
    print(str(e))
print (s.recv(buf).decode('utf-8'))
print("Command sent: {}".format(command))
s.sendall(str.encode(str(command)))
print("Hostname sent: {}".format(hostname))
s.sendall(str.encode(hostname))
if command == 2 or command == 4:
    try:
        ip = input("Enter IP: ")
        s.sendall(str.encode(ip))
    except:
        print("Sending IP failed")
        quit()
if command == 1:
    ip = s.recv(buf).decode('utf-8')
    print("IP address for {}: {}".format(hostname, ip))
elif command == 4:
    hostname = s.recv(buf).decode('utf-8')
    print("Hostname for IP address {}: {}".format(ip, hostname))
else:
    print (s.recv(buf).decode('utf-8'))
s.close()
