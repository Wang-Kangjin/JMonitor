#! /usr/bin/env python

#coding=utf-8
import time, socket
import xml.dom.minidom as xml

def main():
    while True:
        dom = xml.parse("config.xml")
        root = dom.documentElement
        for node in root.childNodes:
            if node.nodeType == node.ELEMENT_NODE:
                print node.nodeName
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                print node.getAttribute('ip')
                s.connect((node.getAttribute('ip'), 2048))
                s.send(node.getAttribute('id'))
                result = s.recv(1024)
                print result

main()
