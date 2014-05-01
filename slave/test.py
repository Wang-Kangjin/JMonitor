import socket, json
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.64.131", 2048))
s.send("test")
result = s.recv(1024)
print result
