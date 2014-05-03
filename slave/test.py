import socket, json
import MySQLdb as db
g_conn = db.connect(host='localhost',user='root',passwd='wkj',db='jmonitor',port=3306,charset='utf8')
sql = 'select sv_name from ServerRuntime where sv_id=' + "1"
print sql
cur = g_conn.cursor()
cur.execute(sql)
print cur.__methods__()
