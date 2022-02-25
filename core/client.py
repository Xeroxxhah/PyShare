import socket
import os
import tqdm
import hashlib

def calcSha256(file):
    if os.path.exists(file):
        with open(file, 'rb') as f:
            data = f.read()
            return str(hashlib.sha256(data).hexdigest())
    else:
        print('File Does not exist...')

class Client():

    def __init__(self):
        self.sok = socket.socket()

    def send(self, file, to):
        try:
            checksum = calcSha256(file)
            sok = socket.socket()
            sok.connect((to, 2022))
            if os.path.exists(file):
                filename = os.path.basename(file)
                filesize = os.path.getsize(file)
                sok.send(f"{filename}<SEP>{filesize}<SEP>{checksum}".encode())
                progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
                with open(file, 'rb') as f:
                    while True:
                        data = f.read(1024)
                        if not data:
                            break
                        sok.sendall(data)
                        progress.update(len(data))
                sok.close()
            else:
                print('Please enter a valid file path')
        except Exception as e:
            print(e)
    
    def sendping(self,host):
        pingsok = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        pingsok.connect((host,5656))
        pingsok.send('ping'.encode('utf-8'))
        pingsok.close()
