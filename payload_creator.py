import sys

if len(sys.argv) != 3:
    print("[!] Invalid Argument! Usage: python payload_creator.py <IP> <PORT>")
    exit()

IP = sys.argv[1]
PORT = sys.argv[2]

with open('payload.py', 'r') as file:
    data = "\r" + file.read()
    file.close()

data = data.replace("42069_", IP).replace("42069", PORT)

with open('tempPayload.py', 'w') as tempPayload:
    tempPayload.write(data)
    tempPayload.close()