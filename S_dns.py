import socket
import dns.resolver
import os

def menu(i):
    menul = "DNS Server\n1. Search for IP address\n2. Add record\n3. Remove record\n4. Reverse DNS lookup\n5. Shutdown"
    if i == 0:
        print(menul)
    else:
        client_s.sendall(str.encode(menul))

name_serv = socket.gethostname()
ip_serv = socket.gethostbyname_ex(name_serv)
s = socket.socket()
port = 8888
buf_size = 4096
if not os.path.isfile('IP_list.txt'):
    with open('IP_list.txt', 'w') as f:
        f.write("Name and IP\n")
        f.close()
try:
    s.bind(('', port))
except socket.error as e:
    print(str(e))
print("DNS server with IP address {} is online".format(ip_serv[2]))
i = 0
menu(i)
print("Waiting for Client...")
s.listen(5)

def find_ip(hostname): #Find the IP address of host
    try:
        ipaddress = socket.gethostbyname(hostname)
        return ipaddress
    except:
        return False

def find_host(ip): #Find the host of the IP address
    try:
        host, alias, addresslist = socket.gethostbyaddr(ip)
        return host
    except:
        return False

def save_ip(hostname, ip): #Appends the new IP address into the text file
    try:
        with open('IP_list.txt', 'a') as f:
            f.write(hostname)
            f.write(" ")
            f.write(ip)
            f.write("\n")
            f.close()
    except:
        print("Saving failed")

def com1(dec_hostname): #Finds the IP address of host
    found = 0
    with open('IP_list.txt') as f: #Searches the text file for same domain name, if not found then found = 0
        try:
            for line in f:
                if dec_hostname in line:
                    client_s.sendall(str.encode(line[len(dec_hostname) + 1:]))
                    print("IP address for {}: {}".format(dec_hostname, line[len(dec_hostname) + 1:]))
                    found = 1
                    break
        except:
            print("Command 1 failed")
        f.close()
    if found != 1: #When found = 0, then do the find_IP function to search the IP address
        try:
            ipaddress = find_ip(dec_hostname)
            found_ip = "IP address for {}: {}".format(dec_hostname, ipaddress)
            print(found_ip)
            client_s.sendall(str.encode(ipaddress))
            save_ip(dec_hostname, ipaddress)
        except:
            print("Failed to find IP of {}".format(hostname))
            fail = "Failed to find IP"
            client_s.sendall(str.encode(fail))

def com2(hostname, ip): #Manually add a record from Client
    same = 0
    try:
        with open('IP_list.txt', 'r') as f:
            try:
                for line in f:
                    if dec_hostname in line:
                        same = 1
                        break
            except:
                same = 0
            f.close()
        if same != 1:
            save_ip(hostname, ip)
            print("{} with IP address {} added".format(hostname,ip))
            client_s.sendall(str.encode("Record Added"))
        else:
            print("{} with IP address {} not added".format(hostname,ip))
            client_s.sendall(str.encode("Record Already Exist"))
    except:
        print("Command 2 failed")

def com3(hostname): #Deletes a record based on Client request
    try:
        with open("IP_list.txt", "r") as f:
            lines = f.readlines()
        with open("IP_list.txt", "w") as f:
            for line in lines:
                name = line[:len(hostname)]
                if name != hostname:
                    f.write(line)
        print("{} is deleted from record".format(hostname))
        client_s.sendall(str.encode("{} is deleted from record".format(hostname)))
    except:
        print("Command 3 failed")

def com4(ip): #Carry out reverse DNS look up
    try:
        host = find_host(ip)
        complete = "Host for IP {}: {}".format(ip,host)
        print(complete)
        client_s.sendall(str.encode(host))
    except:
        fail = "Failed to find host"
        client_s.sendall(str.encode(fail))

while True: #This is where the commands are accepted
    i = 1
    client_s, addr = s.accept()
    menu(i)
    print("Connected to " + str(addr))
    command = client_s.recv(buf_size)
    dec_command = command.decode('utf-8')
    print("Command Recevied: {}".format(dec_command))
    hostname = client_s.recv(buf_size)
    dec_hostname = hostname.decode('utf-8')
    print("Hostname Received: {}".format(dec_hostname))
    if dec_command == '2' or dec_command == '4':
        ip = client_s.recv(buf_size)
        dec_ip = ip.decode('utf-8')
        print("IP received: {}".format(dec_ip))
    if dec_command == '1': #Search IP Address
        com1(dec_hostname)
    elif dec_command == '2': #Add Record 
        com2(dec_hostname, dec_ip)
    elif dec_command == '3': #Deletes Record
        com3(dec_hostname)
    elif dec_command == '4': #Reverse DNS lookup
        com4(dec_ip)
    elif dec_command == '5': #Shuttsdown the server
        client_s.sendall(str.encode("Shutting Down..."))
        print("Shutting Down...")
        client_s.close()
        s.close()
        break
    client_s.close()
s.close()
