#-*- coding:utf-8 -*-
import sys,os
reload(sys)
sys.setdefaultencoding('utf-8')
import time
import json
import socket
import os

arglist=sys.argv
if "-h" in arglist:
  outstr='''
    how to use it
    -h   help
    -p   server port,like 8720
    -c   cloud proxy server,lile 192.168.1.1:8280
    -n   the cloud server name,use to register cloud proxy
  '''
  print outstr
  sys.exit(0)

if "-p" in arglist:
  port=arglist[arglist.index('-p')+1]
else:
  port=8270

if "-c" in  arglist:
  proxy_addr=arglist[arglist.index('-c')+1]
  if "-n" in  arglist:
  	cloud_name=arglist[arglist.index('-n')+1]
  else:
  	"you should input the cloud while you want to register cloud proxy"
  	sys.exit(0) 	
else:
  proxy_addr=None


  


def get_ip():
	iplist=[]
	iplist = socket.gethostbyname_ex(socket.gethostname())
	ip=iplist[2][0]
	return ip

def load(filename):
    with open(filename) as json_file:
        data = json.load(json_file,encoding="utf-8")
        return data

template="""#coding=utf-8
import sys
import xmlrpclib
{import_lib}


class CloudLibrary():
	def  __init__(self):
{instane}


	def get_library(self,library):    
    		{method}
    
if __name__ == '__main__':
    from robotcloudserver import RobotCloudServer
    {register_code}
    RobotCloudServer(CloudLibrary(),"{ip}",{port},None)

"""

register_tmp="""proxy = xmlrpclib.ServerProxy("{proxy_ip}")
    result=proxy.set_register("{cloud_name}","{local_ip}","{local_port}")
    if result:
    	print "register to cloud proxy server:{cloud_name} successed!"
    else:
    	print "it register to cloud proxy server:{cloud_name} failed! please check again or change the cloud_name!"
"""

import_lib=""
method_str=""
instane_str=""

method=""
instane_tmp="""		self.{api}={lib}()
"""	
f_func_tmp='''	
		if library=="{api}":
			return self.{api}
'''
func_tmp='''
		elif library=="{api}":
			return self.{api}
'''

final_tmp='''
		else:
			return self 
'''
report_json =load("lib_config.json")
for rjson in report_json:
	import_lib=import_lib+"from {liby} import {liby}\n".format(liby=rjson["lib"])
	instane_str=instane_str+instane_tmp.format(lib=rjson["lib"],api=rjson["api"])
	if report_json.index(rjson)==0:
		method_str=method_str+f_func_tmp.format(api=rjson["api"],lib=rjson["lib"])+"\n"	
	else:
		method_str=method_str+func_tmp.format(api=rjson["api"],lib=rjson["lib"])+"\n"	
method=method+method_str+final_tmp
if proxy_addr==None:
	libtext=template.format(import_lib=import_lib,method=method,ip=get_ip(),port=port,instane=instane_str,register_code="")
else:
	if "http//" not in proxy_addr:
		proxy_addr="http://"+proxy_addr
	register_str=register_tmp.format(proxy_ip=proxy_addr,cloud_name=cloud_name,local_ip=get_ip(),local_port=port)
	libtext=template.format(import_lib=import_lib,method=method,ip=get_ip(),port=port,instane=instane_str,register_code=register_str)	

f = open("CloudLibrary.py",'wb')
f.write(libtext)
f.close()
print "starting the robotframework cloud now!"
time.sleep(3)
os.system("python CloudLibrary.py")


