import configparser
import os
from os import path,system
from sys import argv


cf = configparser.ConfigParser()
WorkingDirectory= (path.dirname(path.realpath(argv[0]))) #当前脚本工作路径

os.chdir(WorkingDirectory)
cf.read("config.ini")
sections = cf.sections()
print (sections)