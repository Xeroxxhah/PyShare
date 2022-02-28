from core.server import Server
from core.scan import Scan
from core.client import Client
from multiprocessing import Process
import os , sys

def main():
    buddies = []
    try:
        srv = Server()
        scan = Scan()
        client = Client()
        srv.srvstatus = True
        lsrvproc = Process(target=srv.SrvListen)
        rsrvproc = Process(target=srv.RecvData)
        lsrvproc.start()
        rsrvproc.start()
    except Exception as e:
        print(e)



    while True:
        if srv.srvstatus:
            print('+ Server Listening +')
        else:
            print('- Server not Listening -')

        print('1:Scan for buddies')
        print('2:Stop Server')
        print('3:Send File')
        print('4:Use cached ips')
        print('5:Clear Cache')
        print('6:Restart Server')
        print('7:Ping Buddy')
        print('q:Quit')

        print('--->')
        choice = input()
        if choice == '1':
            scan.look4buddies()
            scan.storeCache()
            buddies = scan.buddies
            if len(buddies) > 0:
                print('+Buddies+')
                for host in buddies:
                    print(f'{scan.buddiesWithName.get(host)} ({host})')
            else:
                print('No buddies found...')
        elif choice == 'q':
            lsrvproc.terminate()
            rsrvproc.terminate()
            print('Good Bye...')
            break
        elif choice == '2':
            print("Shuting Down server, now your buddies won't be able to find you :(")
            srv.srvstatus = False
            lsrvproc.terminate()
            rsrvproc.terminate()
        elif choice == '3':
            host_no = 0
            if len(scan.buddies) > 0:
                for host in scan.buddies:
                    print(f"{host_no}: {host.strip('')}")
                    host_no += 1
                user = int(input('Choose a host no to send:'))
                file = input('Enter file path:')
                user_ip = scan.buddies[user]
                try:
                    client.send(file, user_ip)
                except Exception as e:
                    print(e)
                else:
                    print('File Sent Successfully...')
            else:
                print('No buddies found, First scan for buddies')
        elif choice == '4':
            try:
                with open('ip.cache', 'r') as rf:
                    data = rf.read()
                    data = data.splitlines()
                    for i in data:
                        scan.buddies.append(i)
                        scan.buddies = list(dict.fromkeys(scan.buddies))
                rf.close()
            except FileNotFoundError:
                print('No cache Found')
        elif choice == '5':
            try:
                os.remove('ip.cache')
            except FileNotFoundError:
                pass
        elif choice == '6':
            if srv.srvstatus:
                print('Server Already Running...')
            else:
                srv = Server()
                srv.srvstatus = True
                lsrvproc = Process(target=srv.SrvListen)
                rsrvproc = Process(target=srv.RecvData)
                lsrvproc.start()
                rsrvproc.start()
                print('+Server Started+')
        elif choice == '' or choice == ' ' or choice == '\n':
            pass
        elif choice == '7':
            if len(scan.buddies) > 0:
                try:
                    scan.showBuddies()
                    user = int(input('Enter user no:'))
                    try:
                        host = scan.buddies[user]
                    except IndexError:
                        print('Wrong User')
                        break
                    client.sendping(host)
                except Exception as e:
                    print(e)
            else:
                print('No buddies found..')
        else:
            print('Wrong Option')
    lsrvproc.terminate()
    rsrvproc.terminate()
    sys.exit()

main()
