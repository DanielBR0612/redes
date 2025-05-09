import socket
import subprocess

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind(("0.0.0.0", 5005))
    while True:
        data, addr = sock.recvfrom(1024)
        print(data, " recebido de", addr)
        subprocess.run(["powershell", "Stop-Process -Name \"chrome\" -Force"], shell=False, stdout=subprocess.PIPE)
except KeyboardInterrupt:
    print("Fechando...")