#coding=utf-8
import sys
import xmlrpclib
from AppiumLibrary import AppiumLibrary
from Selenium2Library import Selenium2Library
from RequestsLibrary import RequestsLibrary
from MacacaLibrary import MacacaLibrary
from EasyLibrary import EasyLibrary



class CloudLibrary():
	def  __init__(self):
		self.appium=AppiumLibrary()
		self.selenium=Selenium2Library()
		self.request=RequestsLibrary()
		self.macaca=MacacaLibrary()
		self.easy=EasyLibrary()



	def get_library(self,library):    
    			
		if library=="appium":
			return self.appium


		elif library=="selenium":
			return self.selenium


		elif library=="request":
			return self.request


		elif library=="macaca":
			return self.macaca


		elif library=="easy":
			return self.easy


		else:
			return self 

    
if __name__ == '__main__':
    from robotcloudserver import RobotCloudServer
    RobotCloudServer(CloudLibrary(),"192.168.1.1",8270,None)

