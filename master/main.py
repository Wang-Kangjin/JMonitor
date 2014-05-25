#! /usr/bin/env python

#coding=utf-8
import time, socket
import xml.dom.minidom as xml
import MySQLdb as db

global g_conn

def main():

    try:
        dom = xml.parse("config.xml")
        #get "config" element
        xml_config = dom.documentElement

        for node in xml_config.childNodes:
            #find "slave_cluster" node
            if node.nodeName == "slave_cluster":
                xml_slave_cluster = node
            if node.nodeName == "db_config":
                xml_db_config = node

        db_pwd = raw_input("Please type your DB password:")
        db_user = xml_db_config.getAttribute("user")
        db_name = xml_db_config.getAttribute("db_name")
        init(db_user, db_pwd, db_name)
        # request slave server
        while True:
            poll(xml_slave_cluster)
            time.sleep(1)
    except KeyboardInterrupt, e:
        print "Exit! Bye~"
        g_conn.close


def init(db_user, db_pwd, db_name):
    global g_conn
    # init mysql connection
    #g_conn = db.connect(host='localhost',user='root',passwd='wkj',db='jmonitor',port=3306,charset='utf8')
    g_conn = db.connect(host='localhost',user=db_user,passwd=db_pwd,db=db_name,port=3306,charset='utf8')

def poll(cluster):
    for node in cluster.childNodes:
        if node.nodeType == node.ELEMENT_NODE:
            print node.nodeName
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                node_ip = node.getAttribute('ip')
                node_id = int(node.getAttribute('id'))
                node_name = node.getAttribute('name')
                print node_name+":"+node_ip
                #connect to a slave server
                s.connect((node_ip, 2048))
                s.send(str(node_id))
                response_data = s.recv(1024)
                update_runtime_status([node_id, node_name, response_data])
                save_history_status([node_id, node_name, response_data, get_time()])
                on_recv_response(response_data)
                print response_data
                s.close

            except socket.error, e:
                s.close
                print "Error Code:"+ str(e.args[0])+ " Detial:"+str(e.args[1])
                print "Warning!!!" + str(node_id) + " is not availabel !"
            print "==============================="

def get_time():
    time_format = '%Y-%m-%d %H-%M-%S'
    struct_time = time.localtime(time.time())
    time_stamp = time.strftime( time_format, struct_time)
    return time_stamp

def on_recv_response(data):
    pass
def update_runtime_status(values):
    global g_conn
    print values[0]
    sql_is_exist = 'select count(sv_name) from ServerRuntime where sv_id=' + str(values[0])
    sql_insert = 'insert into ServerRuntime values(%s,%s,%s)'
    sql_update = 'update ServerRuntime set status=%s where sv_id=' + str(values[0])
    cur = g_conn.cursor()
    cur.execute(sql_is_exist)
    row_count = cur.fetchall()[0][0]
    print row_count
    if row_count == 0:
        #dont exsit ,insert
        effect_row = cur.execute(sql_insert,values)
        if effect_row == 1:
            print "Runtime insert success!"
        else:
            print "Runtime insert FAIL!!"
    else:
        #exsit ,update
        effect_row = cur.execute(sql_update,values[2])
        if effect_row == 1:
            print "Runtime update success!"
        else:
            print "Runtime update FAIL!!"
    g_conn.commit()


def save_history_status(values):
    global g_conn
    print type(values[0])
    sql_insert_history = 'insert into History values(%s, %s, %s, %s)'
    cur = g_conn.cursor()
    cur.execute(sql_insert_history, values)
    g_conn.commit()

main()
