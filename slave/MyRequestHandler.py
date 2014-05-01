#! /usr/bin/env python

#coding=utf-8
import psutil
import time, json
from SocketServer import TCPServer, BaseRequestHandler
class MyRequestHandler(BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024).strip()
        print data
        status_dict = {}
        status_dict["local_time"]= time = self.get_time()
        status_dict["cpu_percent"] = str(self.get_cpu_percent())
        status_dict["mem_used"] = str(self.get_memory()) + '%'
        status_dict["send_speed"] = self.get_net_send_speed()
        status_dict["recv_speed"] = self.get_net_recv_speed()
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

    def get_cpu_percent(self):
        p = psutil.cpu_percent()
        return p

    def get_memory(self):
        mem_state = psutil.virtual_memory()
        return mem_state.percent

    def get_time(self):
        time_format = '%Y-%m-%d-%H-%M-%S'
        struct_time = time.localtime(time.time())
        time_stamp = time.strftime( time_format, struct_time)
        return time_stamp

    def get_net_send_speed(self):
        netcount_before = psutil.network_io_counters()
        time.sleep(1)
        netcount_after = psutil.network_io_counters()
        send_speed = self.bytes2human(netcount_after.bytes_sent - netcount_before.bytes_sent)
        return send_speed + '/s'

    def get_net_recv_speed(self):
        recv_before = psutil.network_io_counters()
        time.sleep(1)
        recv_after = psutil.network_io_counters()
        recv_speed = self.bytes2human(recv_after.bytes_recv - recv_before.bytes_recv)
        return recv_speed + '/s'
