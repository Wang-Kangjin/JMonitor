#! /usr/bin/env python

#coding=utf-8
import psutil
import time, json, os, statvfs
from SocketServer import TCPServer, BaseRequestHandler
import global_var as glb
class MyRequestHandler(BaseRequestHandler):
    def __init__(self, request, client_address, server):
        BaseRequestHandler.__init__(self, request, client_address, server)


    def handle(self):
        data = self.request.recv(1024).strip()
        print data
        status_dict = {}
        status_dict["local_time"] = self.get_time()
        status_dict["cpu_percent"] = str(self.get_cpu_percent())
        status_dict["mem_used"] = str(self.get_memory())
        status_dict["send_speed"] = self.get_net_send_speed()
        status_dict["recv_speed"] = self.get_net_recv_speed()
        status_dict["total_capacity"] = self.get_total_capacity()
        status_dict["available_capacity"] = self.get_available_capacity()
        self.request.sendall(json.dumps(status_dict))

    def bytes2human(self, n):
        """
        >>> bytes2human(10000)
        '9.8 K'
        >>> bytes2human(100001221)
        '95.4 M'
        """
        symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
        prefix = {}
        for i, s in enumerate(symbols):
            prefix[s] = 1 << (i+1)*10
        for s in reversed(symbols):
            if n >= prefix[s]:
                value = float(n) / prefix[s]
                return '%.2f %s' % (value, s)
        return '%.2f B' % (n)

    def bytes2G(self, n):
        res = float(n)/(1024*1024*1024)
        return '%.2f' % res

    def bytes2K(self, n):
        res = float(n)/1024
        return '%.2f' % res

    def get_cpu_percent(self):
        p = psutil.cpu_percent()
        return p

    def get_memory(self):
        mem_state = psutil.virtual_memory()
        return mem_state.percent

    def get_time(self):
        time_format = '%Y-%m-%d %H-%M-%S'
        struct_time = time.localtime(time.time())
        time_stamp = time.strftime( time_format, struct_time)
        return time_stamp

    def get_net_send_speed(self):
        send_speed = self.bytes2K(glb.network_send_speed)
        return send_speed

    def get_net_recv_speed(self):
        recv_speed = self.bytes2K(glb.network_recv_speed)
        return recv_speed

    def get_total_capacity(self):
        vfs=os.statvfs("/")
        capacity=vfs[statvfs.F_BLOCKS]*vfs[statvfs.F_BSIZE]
        return self.bytes2G(capacity)

    def get_available_capacity(self):
        vfs=os.statvfs("/")
        available=vfs[statvfs.F_BAVAIL]*vfs[statvfs.F_BSIZE]
        return self.bytes2G(available)
