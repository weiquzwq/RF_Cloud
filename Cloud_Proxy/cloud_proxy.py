import xmlrpclib
import socket
from SimpleXMLRPCServer import SimpleXMLRPCServer

cloud_dict={}

def is_even(n):
    return n % 2 == 0

def get_ip():
      iplist=[]
      iplist = socket.gethostbyname_ex(socket.gethostname())
      ip=iplist[2][0]
      return ip


def set_register(cloud_name,cloud_addr,cloud_port):
        clo_address="{cloud_addr}:{cloud_port}".format(cloud_addr=cloud_addr,cloud_port=cloud_port)
        try:
            print cloud_dict[cloud_name]
            tmpaddr=cloud_dict[cloud_name]
            print "the cloudname:{cloud_name},ip:{addr} is exist".format(cloud_name=cloud_name,addr=tmpaddr)
            return False
        except:
            cloud_dict[cloud_name]=clo_address
            print cloud_dict[cloud_name]
            print "the cloudname:{cloud_name} register ok,ip:{addr} ".format(cloud_name=cloud_name,addr=clo_address)
            return True

def get_cloud_address(cloud_name,taga=None):
        try:
            print "aaa  "+cloud_dict[cloud_name]
            ipaddr=cloud_dict[cloud_name]
            print "It point to {cloud_name}:{ipaddr}\nImport the lib:{taga} ".format(cloud_name=cloud_name,ipaddr=ipaddr,taga=taga)
            return "http://"+ipaddr
        except:     
            ipaddr="http://"+str(get_ip())
            print "The cloud is not exist,It point to local center cloud:{ipaddr}".format(ipaddr=get_ip())    
            return "error"

ipaddress=get_ip()
server = SimpleXMLRPCServer((ipaddress, 8280))
print "The Cloud Proxy Server Listening on {ip}:{port} ...".format(ip=ipaddress,port=8280)
server.register_function(is_even, "is_even")
server.register_function(get_cloud_address,"get_cloud_address")
server.register_function(set_register,"set_register")

server.serve_forever()
