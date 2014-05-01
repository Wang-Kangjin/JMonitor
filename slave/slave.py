#! /usr/bin/env python

#coding=utf-8
import time, socket
from SocketServer import TCPServer
from MyRequestHandler import MyRequestHandler

def main():
    host = ''
    port = 2048
    addr = (host, port)
    server = TCPServer(addr, MyRequestHandler)
    server.serve_forever()

main()
