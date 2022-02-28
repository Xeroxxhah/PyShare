import socket
import tqdm
import os
import hashlib
from plyer import notification

def getip():
    sok = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sok.connect(('8.8.8.8',53))
    return sok.getsockname()[0]

def calcSha256(file):
    if os.path.exists(file):
        with open(file, 'rb') as f:
            data = f.read()
            return str(hashlib.sha256(data).hexdigest())
    else:
        print('File Does not exist...')

def notify(host):
    notification.notify(title = host,message="Hi There..." ,timeout=5)

def gethostname():
    return str(socket.gethostname())

class Server():
    def __init__(self) -> None:
        self.srvstatus = False
        self.srvhost = str(getip())
        self.srvport = 5656
        self.srvsok = socket.socket(socket.AF_INET ,socket.SOCK_STREAM)

    def SrvListen(self):
        self.srvstatus = True
        try:
            self.srvsok.bind((self.srvhost ,self.srvport))
            self.srvsok.listen(5)
            

            while True:
                con ,addr = self.srvsok.accept()
                data = con.recv(1024).decode('utf8')
                if 'wdap, u there???' in data:
                    con.send(f'Yeee:{gethostname()}'.encode('utf-8'))
                elif 'ping' in data:
                    notify(data.split(':')[1])
        except Exception as e:
            print(e)
        except KeyboardInterrupt:
            quit()

    def RecvData(self):
        recv_port = 2022
        recvsok = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            recvsok.bind((self.srvhost, recv_port))
            recvsok.listen(5)
            con, addr = recvsok.accept()
            tmpdata = con.recv(1024).decode()
            filename, filesize, checksum = tmpdata.split('<SEP>')
            filesize = int(filesize)
            progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)

            with open(filename, 'wb') as wf:
                while True:
                    data = con.recv(4096)
                    if not data:
                        break
                    wf.write(data)
                    progress.update(len(data))
            if calcSha256(filename) != checksum:
                print('Checksum Error: File Corrupted')
            con.close()
            recvsok.close()
        except Exception as e:
            print(f"Following Error Ocurred: {e}")
        finally:
            recvsok.close()
            return True

    def kill(self):
        self.srvsok.close()
