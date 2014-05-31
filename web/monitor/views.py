from django.shortcuts import render
from django.template import loader, Context
from django.http import HttpResponse
import MySQLdb as db
from django.conf import settings
import simplejson
from django.contrib.auth.decorators import login_required

# Create your views here.
def login2(req):
    t = loader.get_template('signin.htm')
    c = Context()
    html = t.render(c)
    return HttpResponse(html)

@login_required
def details(req, serverid):
    print serverid
    select_sql = "select * from History where sv_id="+str(serverid)+" and record_time > DATE_SUB(NOW(),INTERVAL 1 MINUTE);"
    username = settings.DATABASES['default']['USER']
    pwd = settings.DATABASES['default']['PASSWORD']
    db_name = settings.DATABASES['default']['NAME']
    conn = db.connect(host='localhost',user=username,passwd=pwd,db=db_name,port=3306,charset='utf8')
    cur = conn.cursor()
    cur.execute(select_sql)
    rows = cur.fetchall()
    cpu_list = []
    mem_list = []
    net_send_list = []
    net_recv_list = []
    used_disk = float()
    avail_disk = float()
    for row in rows:
        json_str = row[2]
        status_dict = simplejson.loads(json_str)
        cpu_list.append(float(status_dict['cpu_percent']))
        mem_list.append(float(status_dict['mem_used']))
        net_send_list.append(float(status_dict['send_speed']))
        net_recv_list.append(float(status_dict['recv_speed']))
        total_disk = float(status_dict['total_capacity'])
        avail_disk = float(status_dict['available_capacity'])
        used_disk = total_disk - avail_disk
    conn.close()
    print "avail_disk:"+str(avail_disk)
    t = loader.get_template('high_detail.html')
    c = Context(
        {
        'cpu_list':cpu_list,
        'mem_list':mem_list,
        'net_send_list':net_send_list,
        'net_recv_list':net_recv_list,
        'avail_disk':avail_disk,
        'used_disk':used_disk,
        'serverid':serverid
        })
    html = t.render(c)
    return HttpResponse(html)

@login_required(login_url="/login")
def index(req):
    t = loader.get_template('list.html')
    sql = "select sv_id, sv_name from ServerRuntime"
    username = settings.DATABASES['default']['USER']
    pwd = settings.DATABASES['default']['PASSWORD']
    db_name = settings.DATABASES['default']['NAME']
    conn = db.connect(host='localhost',user=username,passwd=pwd,db=db_name,port=3306,charset='utf8')
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    server_list = []
    for row in rows:
        server = {"sv_id":row[0],"sv_name":row[1]}
        server_list.append(server)

    conn.close()
    c = Context({
        "server_list": server_list
        })
    html = t.render(c)
    return HttpResponse(html)

def high(req):
    t = loader.get_template('high_detail.html')
    c = Context()
    html = t.render(c)
    return HttpResponse(html)

def get_runtime(req, serverid):
    print serverid
    select_sql = "select * from ServerRuntime where sv_id="+str(serverid)
    username = settings.DATABASES['default']['USER']
    pwd = settings.DATABASES['default']['PASSWORD']
    db_name = settings.DATABASES['default']['NAME']
    conn = db.connect(host='localhost',user=username,passwd=pwd,db=db_name,port=3306,charset='utf8')
    cur = conn.cursor()
    cur.execute(select_sql)
    row = cur.fetchone()
    status_json_str = row[2]
    conn.close()
    return HttpResponse(status_json_str,content_type = "application/json")
