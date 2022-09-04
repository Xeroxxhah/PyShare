import socket
import os
import tqdm
import hashlib
import shutil

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
            shutil.make_archive(dst,'zip',src)
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
                        data = f.read(4096)
                        if not data:
                            break
                        sok.sendall(data)
                        progress.update(len(data))
                sok.close()
            else:
                print('Please enter a valid file path')
        except Exception as e:
            print(e)
    
    def sendDir(self, dir, to):
        try:
            shutil.make_archive(dir,'zip',dir)
            dir_zip = f'{dir}.zip'                
            checksum = calcSha256(dir_zip)
            sok = socket.socket()
            sok.connect((to, 2022))
            if os.path.exists(dir_zip):
                dirname = os.path.basename(dir_zip.replace('.zip', ''))
                dirsize = os.path.getsize(dir_zip)
                sok.send(f"{dirname}<SEP>{dirsize}<SEP>{checksum}".encode())
                progress = tqdm.tqdm(range(dirsize), f"Sending {dirname}", unit="B", unit_scale=True, unit_divisor=1024)
                with open(dir_zip, 'rb') as f:
                    while True:
                        data = f.read(4096)
                        if not data:
                            break
                        sok.sendall(data)
                        progress.update(len(data))
                sok.close()
                os.remove(dir_zip)
            else:
                print('Please enter a valid file path')
        except Exception as e:
            print(e)
        except FileNotFoundError:
            print(f'{dir} not found...')
    
    def sendping(self,host):
        pingsok = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        pingsok.connect((host,5656))
        pingsok.send(f'ping:{str(socket.gethostname())}'.encode('utf-8'))
        pingsok.close()
