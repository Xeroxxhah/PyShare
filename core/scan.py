import socket
import tqdm

def getip():
    sok = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sok.connect(('8.8.8.8',53))
    return sok.getsockname()[0]


class Scan():
    def __init__(self):
        self.ip = getip()
        self.buddies = []

    def storeCache(self):
        with open('ip.cache', 'w') as wf:
            for host in self.buddies:
                wf.write(host+'\n')
        wf.close()


    def look4buddies(self):
        try:
            for i in tqdm.tqdm(range(254), f"Scaning", unit="B", unit_scale=True, unit_divisor=1024):
                tempsok = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                socket.setdefaulttimeout(0.2)
                tmpvar = self.ip
                tmpvar = tmpvar.split('.')[0] + '.' + tmpvar.split('.')[1] + '.' + tmpvar.split('.')[2] + '.' + str(i)
                try:
                    if tempsok.connect_ex((tmpvar, 5656)) == 0:
                        tempsok.send('wdap, u there???'.encode('utf8'))
                        msg = tempsok.recv(1024).decode('utf8')
                        if msg == 'Yeee':
                            self.buddies.append(tmpvar)
                        tempsok.close()

                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)

    def getbuddies(self):
        if len(self.buddies):
            return self.buddies
        else:
            return None


