import socket
import threading
import sys
import os
#import re
#import hashlib
import time



class Server():
    def __init__(self,port,homedir):
        self.host = ''
        self.port = port
        self.homedir = homedir
        self.threads=[]
        self.create_socket()


    def create_socket(self):
        try:
            sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)#create an INET, STREAMing socket
            sock.bind((self.host,self.port))#bind the socket to a host, and a port
            sock.listen(20)#queue up as many as 250 connect requests
            self.sock=sock
            print("socket running on port:")
            print(self.port)
            self.accept_req()#call accept_req()
        except socket.error as message:
            if sock:
                sock.close()
            print("Could not open socket: %s", str(message) )
            sys.exit(1)



    def accept_req(self):
        while 1:
            try:
                conn,addr=self.sock.accept()#accept Request
                if conn:
                    thr_multiple=Multiple(conn,addr,homedir)
                    thr_multiple.start()
                    self.threads.append(thr_multiple)
                '''for elements in self.threads:
                    elements.join()'''
            except (KeyboardInterrupt, SystemExit):
                sys.exit(1)



class Multiple(threading.Thread):
    def __init__(self,conn,addr,homedir):
        threading.Thread.__init__(self)
        print("client connected at %s",conn)
        self.conn = conn
        self.addr = addr
        self.size = 65535
        self.homedir = homedir


    def run(self):
        while(1):
            cred = self.conn.recv(65535)
            userInput = self.conn.recv(65535)
            userInput = userInput.decode()
            self.auth(cred)
            print("1")
            if userInput[:3] == "get":
                self.getFile(userInput)
            elif userInput[:3] == "put":
                print("put")
                self.putFile(userInput)
            elif userInput[:] == "list":
                self.lst(userInput)
            elif userInput[:] == "exit":
                self.ext(userInput)
            else:
                self.Els(userInput)


    def auth(self,cred):
        self.cred = cred.decode()
        print(self.cred)
        flag = 0
        fh = open("dfs.conf", "r")
        for line in fh:
            if line == self.cred:
                print("Authenticated")
                flag = 1
                #self.conn.send(("Authenticated").encode())
                return
        if flag == 0:
            #self.conn.send(("Invalid username/password").encode())
            print("not authorised")
            self.conn.close()

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


    def putFile(self,userInput):
        funct,filename = userInput.split()
        self.funct = funct
        self.filename = filename
        username,password = self.cred.split()
        direc = self.homedir + "/" + username
        if not os.path.exists(direc):
            print("directory created?")
            os.makedirs(direc)
        direc = direc + "/" + self.filename
        if not os.path.exists(direc):
            os.makedirs(direc)
        filenamee = direc + "/" + self.filename
        valu = self.conn.recv(65535)
        print(valu)
        val = valu.decode()
        if int(val) == 1:
            file1 = self.conn.recv(65535)
            print("tried")
            fh1 = open(filenamee+".1","wb+")
            fh1.write(file1)
            print("written")
            fh1.close()
            file2 = self.conn.recv(65535)
            fh2 = open(filenamee+".2","wb+")
            fh2.write(file2)
            fh2.close()
            print("done")
            return
        elif int(val) == 0:
            file2 = self.conn.recv(65535)
            fh2 = open(filenamee + ".2", "wb+")
            fh2.write(file2)
            fh2.close()
            file3 = self.conn.recv(65535)
            fh3 = open(filenamee + ".3", "wb+")
            fh3.write(file3)
            fh3.close()
            return
        elif int(val) == 3:
            file3 = self.conn.recv(65535)
            fh3 = open(filenamee + ".3", "wb+")
            fh3.write(file3)
            fh3.close()
            file4 = self.conn.recv(65535)
            fh4 = open(filenamee + ".4", "wb+")
            fh4.write(file4)
            fh4.close()
            return
        else:
            file4 = self.conn.recv(65535)
            fh4 = open(filenamee + ".4", "wb+")
            fh4.write(file4)
            fh4.close()
            file1 = self.conn.recv(65535)
            fh1 = open(filenamee + ".1", "wb+")
            fh1.write(file1)
            fh1.close()
            return





    def getFile(self, userInput):
        funct, filename = userInput.split()
        self.funct = funct
        calval = []
        self.filename = filename
        username, password = self.cred.split()
        direc = self.homedir + "/" + username
        if os.path.exists(direc):
            direc = direc + "/" + self.filename
            if os.path.exists(direc):
                self.conn.send("sending".encode())
                time.sleep(0.05)
                files = os.listdir(direc)
                file1 = filename.split(".")
                for file in files:
                    file2 = file.split(".")
                    try:
                        calval.append(int(file2[2]))
                    except:
                        continue
                if calval == [1,2]:                #change for each server
                    self.conn.send("1".encode())
                    time.sleep(0.05)
                elif calval == [1,4]:
                    self.conn.send("2".encode())
                    time.sleep(0.05)
                elif calval == [3,4]:
                    self.conn.send("3".encode())
                    time.sleep(0.05)
                elif calval == [2,3]:
                    self.conn.send("0".encode())
                    time.sleep(0.05)
                else:
                    self.conn.send("Incomplete".encode())
                    time.sleep(0.05)
                    return
                time.sleep(1)
                i = 0
                for file in files:
                    file2 = file.split(".")
                    self.conn.send(file2[2].encode())
                    time.sleep(0.05)
                    fh = open(direc + "/" + file,"rb")
                    msg = fh.read()
                    self.conn.send(msg)
                    time.sleep(0.05)
            else:
                self.conn.send("Not found".encode())
        return


    def lst(self, userInput):
        username, password = self.cred.split()
        direc = self.homedir + "/" + username
        if os.path.exists(direc):
            files = os.listdir(direc)
            print(files)
            for file in files:
                filess = os.listdir(direc + "/" + file)
                print(filess)
                for filee in filess:
                    self.conn.send(filee.encode())
                    print(filee)
                    time.sleep(0.05)
            self.conn.send("done".encode())
        return


    def ext(self, userInput):
        return



if __name__ == '__main__':
    homedir = os.getcwd()
    Server(10002,homedir)       #change for each server
