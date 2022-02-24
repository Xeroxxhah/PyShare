import socket
import tqdm


def getip():
    sok = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sok.connect(('8.8.8.8',53))
    return sok.getsockname()[0]

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
            con ,addr = self.srvsok.accept()

            while True:
                data = con.recv(1024).decode('utf8')
                if 'wdap, u there???' in data:
                    con.send('Yeee'.encode('utf-8'))
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
            filename, filesize = tmpdata.split('<SEP>')
            filesize = int(filesize)
            progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)

            with open(filename, 'wb') as wf:
                while True:
                    data = con.recv(1024)
                    if not data:
                        break
                    wf.write(data)
                    progress.update(len(data))
            con.close()
            recvsok.close()
        except Exception as e:
            print(f"Following Error Ocurred: {e}")
        finally:
            recvsok.close()
            return True

    def kill(self):
        self.srvsok.close()
