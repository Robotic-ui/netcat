import socket 
import threading

target_host = 'www.google.com'
target_port = 80

# socket object 
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

 #client connection
client.connect((target_host, target_port))

client.send(b"GET / HTTP\r\nHost: google.com\r\n\r\n")

reponse = client.recv(4096)

print(reponse.decode)
client.close()