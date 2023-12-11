from socket import gethostbyname, gethostname
from socket import socket, AF_INET, SOCK_STREAM
import subprocess

def ip(): return subprocess.check_output(['ipconfig', 'getifaddr', 'en0']).decode().strip('\n')
def ip(): return subprocess.check_output(['hostname','-I']).decode().split(" ")[0]

def Message(addr: str, port: str, message: str):

  clientName = ip()
  serverName = addr
  serverPort = 15000

  print(f"Client: {clientName}")
  print(f"Server: {addr}:{port}")

  try:
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    clientSocket.send(message.encode())

  except ConnectionRefusedError or TimeoutError as e:
    print(e)
    clientSocket.close()
    return -1

  response = clientSocket.recv(2048)
  print(f'From Server: "{response}"')
  clientSocket.close()

  return 0

while True:

  instruction = input()
  Message("10.57.2.41", 15000, instruction)
  if instruction == "a":
    break