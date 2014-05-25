#! /usr/bin/env python

#coding=utf-8
import time, socket, thread
from SocketServer import TCPServer
from MyRequestHandler import MyRequestHandler
import global_var as glb
import psutil

def main():
    host = ''
    port = 2048
    addr = (host, port)
    thread.start_new_thread(timer_thread, ())
    server = TCPServer(addr, MyRequestHandler)
    server.serve_forever()

def timer_thread():
    while True:
        netcount_before = psutil.network_io_counters()
        time.sleep(1)
        netcount_after = psutil.network_io_counters()
        glb.network_send_speed = netcount_after.bytes_sent - netcount_before.bytes_sent
        glb.network_recv_speed = netcount_after.bytes_recv - netcount_before.bytes_recv

main()
