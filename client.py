import socket
#import threading
import sys
import os
import re
import time
import hashlib
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

class client_socket():
    def __init__(self,ip,port):
        self.host = ''
        self.port = port
        self.ip = ip
        self.auth()
        self.sockets()
        self.starter()

    def get_key(password):

        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(password)
        return base64.urlsafe_b64encode(digest.finalize())

    def encrypt(password, token):
        f = Fernet(get_key(password))
        return f.encrypt(token)

    def decrypt(password, token):
        f = Fernet(get_key(password))
        return f.decrypt(token)

    def auth(self):
        flag = 0
        tries = 0
        while (tries <= 5):
            i = 0
            username = input("Username: ")
            password = input("Password: ")
            self.username = username
            self.password = password
            fh = open("dfc.conf", "r")
            for line in fh:
                linesplit = line.split()
                try:
                    if i == 1:
                        if password == linesplit[1]:
                            #socke = client_socket(ip, port, username, password)
                            flag = 1
                            print("Authenticated")
                            return
                        else:
                            i = 0
                            continue
                    elif linesplit[1] == username:
                        i = 1
                    else:
                        print("Try again")
                        continue
                except Exception as e:
                    print(e)
            fh.close()
            tries = tries + 1
            if flag == 1:
                break
        if flag == 0:
            print("Wrong credentials")
            self.Els()
            sys.exit(0)

    def sockets(self):
        i = 1
        while(i<5):
            fh = open("dfc.conf", "r")
            for line in fh:
                try:
                    line1 = re.search(r'DFS' + str(i) + r'\s(.*)', line)
                    try:
                        det = line1.group(1)
                        if (line1.group(1) != "None"):
                            self.create_socket(det,i)
                            print("socket created")
                            break
                    except:
                        print("failed")
                        continue
                except Exception as e:
                    print(e)
            fh.close()
            i = i + 1

    def create_socket(self, det, number):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ipi,porti = det.split(":")
        portint = int(porti)
        sock.connect((ipi, portint))
        if number == 1:
            self.sock1 = sock
            print("Server 1 connected")
        elif number == 2:
            self.sock2 = sock
            print("Server 2 connected")
        elif number == 3:
            self.sock3 = sock
            print("Server 3 connected")
        else:
            self.sock4 = sock
            print("Server 4 connected")


    def starter(self):
        userInput = "NULL"
        while (userInput != "exit"):  # loop for user input
            print("1:get[file_name] \n2:put[file_name] \n3:list \n4:exit")
            userInput = input("Please enter the command:")
            if userInput[:3] == "get":
                self.getFile(userInput)
            elif userInput[:3] == "put":
                self.putFile(userInput)
            elif userInput[:] == "list":
                self.lst(userInput)
            elif userInput[:] == "exit":
                self.ext(userInput)
            else:
                self.Els(userInput)
        exit(1)



    def checkfile(self, fileparts):
        if len(fileparts) == 4:
            return "yes"
        else:
            return "no"


    def getFile(self,userInput):
        fileparts = ["hello"," its", "me", "..."]
        funct, filename = userInput.split()
        i = 0
        filepartnum = []
        self.auth()
        try:
            self.sock1.send((self.username + " " + self.password).encode())
            self.sock1.send((userInput).encode())
        except:
            print("0")
        try:
            a = self.sock1.recv(1024)
            a = a.decode()
            print(a)
            if a == "sending":
                k = self.sock1.recv(1024)
                k = k.decode()
                if not k == "Incomplete":
                    j = 0
                    while j < 2:
                        val = self.sock1.recv(10)
                        val = val.decode()
                        valu = int(val)
                        if not valu in filepartnum:
                            filepartnum.append(valu)
                            msg = self.sock1.recv(65535)
                            fileparts[valu-1] = msg
                            i = i + 1
                        j = j + 1
            else:
                print("File not found on server 1")
        except Exception as e:
            print(e)
            print("File not received from server 1")

        #11111111111111

        try:
            self.sock3.send((self.username + " " + self.password).encode())
            self.sock3.send((userInput).encode())
        except:
            print("0")
        try:
            a = self.sock3.recv(1024)
            a = a.decode()
            if a == "sending":
                k = self.sock3.recv(1024)
                k = k.decode()
                if not k == "Incomplete":
                    j = 0
                    while j < 2:
                        val = self.sock3.recv(10)
                        val = val.decode()
                        val = int(val)
                        if not val in filepartnum:
                            filepartnum.append(val)
                            msg = self.sock3.recv(65535)
                            fileparts[val-1] = msg
                            i = i + 1
                        j = j + 1
                check = self.checkfile(fileparts)
                if check == "yes":
                    fh = open(filename, "wb+")
                    for part in fileparts:
                        fh.write(part)
                        time.sleep(0.05)
                    fh.close()
                    return
            else:
                print("File not found on server 3")
        except Exception as e:
            print(e)
            print("File not received from server 3")


        try:
            self.sock2.send((self.username + " " + self.password).encode())
            self.sock2.send((userInput).encode())
        except:
            print("0")
        try:
            a = self.sock2.recv(1024)
            a = a.decode()
            if a == "sending":
                k = self.sock2.recv(1024)
                k = k.decode()
                if not k == "Incomplete":
                    j = 0
                    while j < 2:
                        val = self.sock2.recv(10)
                        val = val.decode()
                        val = int(val)
                        if not val in filepartnum:
                            filepartnum.append(val)
                            msg = self.sock2.recv(65535)
                            fileparts[val-1] = msg
                            i = i + 1
                        j = j + 1
                    check = self.checkfile(fileparts)
                    if check == "yes":
                        fh = open(filename, "wb+")
                        for part in fileparts:
                            fh.write(part)
                            time.sleep(0.05)
                        fh.close()
            else:
                print("File not found on server 2")
        except Exception as e:
            print(e)
            print("File not received from server 2")


        try:
            self.sock4.send((self.username + " " + self.password).encode())
            self.sock4.send((userInput).encode())
        except:
            print("0")
        try:
            a = self.sock4.recv(1024)
            a = a.decode()
            if a == "sending":
                k = self.sock4.recv(1024)
                k = k.decode()
                if not k == "Incomplete":
                    j = 0
                    while j < 2:
                        val = self.sock4.recv(10)
                        val = int(val)
                        if not val in filepartnum:
                            filepartnum.append(val)
                            msg = self.sock4.recv(65535)
                            fileparts[val-1] = msg
                            i = i + 1
                        j = j + 1
                    check = self.checkfile(fileparts)
                    if check == "yes":
                        fh = open(filename, "wb+")
                        for part in fileparts:
                            fh.write(part)
                            time.sleep(0.05)
                        fh.close()
                    else:
                        print("File not available")
            else:
                print("File not found on server 4")
        except Exception as e:
            print(e)
            print("File not received from server 4")
        return



    def putFile(self,userInput):
        self.auth()
        try:
            self.sock1.send((self.username + " " + self.password).encode())
            self.sock1.send((userInput).encode())
        except:
            print("0")
        try:
            self.sock2.send((self.username + " " + self.password).encode())
            self.sock2.send((userInput).encode())
        except:
            print("0")
        try:
            self.sock3.send((self.username + " " + self.password).encode())
            self.sock3.send((userInput).encode())
        except:
            print("0")
        try:
            self.sock4.send((self.username + " " + self.password).encode())
            self.sock4.send((userInput).encode())
        except:
            print("0")
        funct, filename = userInput.split()
        if (os.path.isfile(filename)):
            fh = open(filename, 'rb')  # open file in read mode
            msg = fh.read()
            y = hashlib.md5(msg)
            y.hexdigest()
            val = int(y.hexdigest(), 16) % 4
            siz = len(msg)
            print(type(siz))
            file1 = msg[:int(siz/4)]
            file2 = msg[int(siz/4):int(siz/2)]
            file3 = msg[int(siz/2):int(3*siz/4)]
            file4 = msg[int(3*siz/4):]
            if val == 0:
                try:
                    self.sock1.send("0".encode())
                    time.sleep(0.05)
                    self.sock1.send(file1)
                    time.sleep(0.05)
                    self.sock1.send(file2)
                except:
                    print("File not saved on server 1")
                try:
                    self.sock2.send("0".encode())
                    time.sleep(0.05)
                    self.sock2.send(file2)
                    time.sleep(0.05)
                    self.sock2.send(file3)
                except:
                    print("File not sent on server 2")
                try:
                    self.sock3.send("0".encode())
                    time.sleep(0.05)
                    self.sock3.send(file3)
                    time.sleep(0.05)
                    self.sock3.send(file4)
                except:
                    print("File not sent on server 3")
                try:
                    self.sock4.send("0".encode())
                    time.sleep(0.05)
                    self.sock4.send(file4)
                    time.sleep(0.05)
                    self.sock4.send(file1)
                except:
                    print("File not sent on server 4")
            elif val == 1:
                try:
                    self.sock1.send("1".encode())
                    time.sleep(0.05)
                    self.sock1.send(file4)
                    time.sleep(0.05)
                    self.sock1.send(file1)
                except:
                    print("File not sent on server 1")
                try:
                    self.sock2.send("1".encode())
                    time.sleep(0.05)
                    self.sock2.send(file1)
                    time.sleep(0.05)
                    self.sock2.send(file2)
                except:
                    print("File not sent on server 2")
                try:
                    self.sock3.send("1".encode())
                    time.sleep(0.05)
                    self.sock3.send(file2)
                    time.sleep(0.05)
                    self.sock3.send(file3)
                except:
                    print("File not sent on server 3")
                try:
                    self.sock4.send("1".encode())
                    time.sleep(0.05)
                    self.sock4.send(file3)
                    time.sleep(0.05)
                    self.sock4.send(file4)
                except:
                    print("File not sent on server 4")
            elif val == 2:
                try:
                    self.sock1.send("2".encode())
                    time.sleep(0.05)
                    self.sock1.send(file3)
                    time.sleep(0.05)
                    self.sock1.send(file4)
                except:
                    print("File not sent on server 1")
                try:
                    self.sock2.send("2".encode())
                    time.sleep(0.05)
                    self.sock2.send(file4)
                    time.sleep(0.05)
                    self.sock2.send(file1)
                except:
                    print("File not sent on server 2")
                try:
                    self.sock3.send("2".encode())
                    time.sleep(0.05)
                    self.sock3.send(file1)
                    time.sleep(0.05)
                    self.sock3.send(file2)
                except:
                    print("File not sent on server 3")
                try:
                    self.sock4.send("2".encode())
                    time.sleep(0.05)
                    self.sock4.send(file2)
                    time.sleep(0.05)
                    self.sock4.send(file3)
                except:
                    print("File not sent on server 4")
            else:
                try:
                    self.sock1.send("3".encode())
                    time.sleep(0.05)
                    self.sock1.send(file2)
                    time.sleep(0.05)
                    self.sock1.send(file3)
                except:
                    print("File not sent on server 1")
                try:
                    self.sock2.send("3".encode())
                    time.sleep(0.05)
                    self.sock2.send(file3)
                    time.sleep(0.05)
                    self.sock2.send(file4)
                except:
                    print("File not sent on server 2")
                try:
                    self.sock3.send("3".encode())
                    time.sleep(0.05)
                    self.sock3.send(file4)
                    time.sleep(0.05)
                    self.sock3.send(file1)
                except:
                    print("File not sent on server 3")
                try:
                    self.sock4.send("3".encode())
                    time.sleep(0.05)
                    self.sock4.send(file1)
                    time.sleep(0.05)
                    self.sock4.send(file2)
                except:
                    print("File not sent on server 4")
        else:
            print("no such file")
            return



    def lst(self,userInput):
        files = []
        filess = []
        complete = []
        incomplete = []
        self.auth()
        self.sock1.send((self.username + " " + self.password).encode())
        time.sleep(0.05)
        self.sock1.send((userInput).encode())
        funct= userInput.split()
        name1 = self.sock1.recv(2048)
        named1 = name1.decode()
        while named1 != "done":
            filename1 = named1.split(".")
            filenamee1 = filename1[0]+"."+filename1[1]
            if not filenamee1 in files:
                files.append(filenamee1)
            filess.append(named1)
            name1 = self.sock1.recv(2048)
            named1 = name1.decode()
        self.sock2.send((self.username + " " + self.password).encode())
        time.sleep(0.05)
        self.sock2.send((userInput).encode())
        name2 = self.sock2.recv(2048)
        named2 = name2.decode()
        while named2 != "done":
            filename2 = named2.split(".")
            filenamee2 = filename2[0] + "." + filename2[1]
            if not filenamee2 in files:
                files.append(filenamee2)
            filess.append(named2)
            name2 = self.sock2.recv(2048)
            named2 = name2.decode()
        self.sock3.send((self.username + " " + self.password).encode())
        time.sleep(0.05)
        self.sock3.send((userInput).encode())
        name3 = self.sock3.recv(2048)
        named3 = name3.decode()
        while named3 != "done":
            filename3 = named3.split(".")
            filenamee3 = filename3[0] + "." + filename3[1]
            if not filenamee3 in files:
                files.append(filenamee3)
            filess.append(named3)
            name3 = self.sock3.recv(2048)
            named3 = name3.decode()
        self.sock4.send((self.username + " " + self.password).encode())
        time.sleep(0.05)
        self.sock4.send((userInput).encode())
        name4 = self.sock4.recv(2048)
        named4 = name4.decode()
        while named4 != "done":
            filename4 = named4.split(".")
            filenamee4 = filename4[0] + "." + filename4[1]
            if not filenamee4 in files:
                files.append(filenamee4)
            filess.append(named4)
            name4 = self.sock4.recv(2048)
            named4 = name4.decode()
        print(files)
        for file in files:
            print(file)
            i = 0
            j = 0
            k = 0
            l = 0
            m = 0
            n = 0
            for filena in filess:
                if filena != "done" and i != 4:
                    fina = filena.split(".")
                    print(fina)
                    fina1 = fina[0] + "." + fina[1]
                    if fina1 == file:
                        if fina[2] == "1" and k == 0:
                            i = i + 1
                            k = k + 1
                        elif fina[2] == "2" and l == 0:
                            i = i + 1
                            l = l + 1
                        elif fina[2] == "3" and m == 0:
                            i = i + 1
                            m = m + 1
                        elif fina[2] == "4" and n == 0:
                            i = i + 1
                            n = n + 1
                        else:
                            continue
                print(i , file)
                if i == 4 and j == 0:
                    complete.append(file)
                    j = j + 1
            if i<4:
                incomplete.append(file)
        print("Complete available files")
        for file in complete:
            print(file + '\n')
        print("Incomplete files")
        for file in incomplete:
            print(file + '\n')
        return



    def ext(self,userInput):
        sys.exit(1)



    def Els(self,userInput):
        self.auth()
        print("enter a valid command")
        return


if __name__ == '__main__':
    ip = "127.0.0.1"
    port = 10000
    socke = client_socket(ip, port)
