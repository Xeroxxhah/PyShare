import socket
import os
import tqdm

class Client():

    def __init__(self):
        self.sok = socket.socket()

    def send(self, file, to):
        try:
            sok = socket.socket()
            sok.connect((to, 2022))
            if os.path.exists(file):
                filename = os.path.basename(file)
                filesize = os.path.getsize(file)
                sok.send(f"{filename}<SEP>{filesize}".encode())
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
