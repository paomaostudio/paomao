# encoding:utf-8
from sys import argv
from os import path,system
import time
from pyfiglet import Figlet
f = Figlet(font='slant')
print (f.renderText('PAOMAO'))
#print(argv[0])          #argv[0] 类似于shell中的$0,但不是脚本名称，而是脚本的路径   
#rint(argv[1])          #argv[1] 表示传入的第一个参数，既 hell
if len(argv) < 2:
    file=input("没有成功导入文件，可以把文件拖拽进本窗口并按回车键:\n") 
    print('即将转码的文件是：'+path.split(file)[1])#路径和文件名分开，取文件名
    time.sleep(1)
else:
    #print(argv[1])
    file=argv[1]
    print('即将转码的文件是：'+path.split(file)[1])

c_path= (path.dirname(path.realpath(argv[0]))) #当前脚本工作路径
#print(c_path) #当前工作路径
hb=(c_path+"\handbrakecli.exe")#handbrake路径
#print(hb)
file_split=path.splitext(file)#文件名和后缀分割开
#print(file_split[0]+"分割"+file_split[1])
arg = (" -i "+file+" -o "+file_split[0]+"_pm"+".mp4"+" -e x264 --encoder-tune psnr --encoder-preset slow -X 1920 --encoder-level 4.0 -2 -T --vb 5800")
print('当前转码参数：\n'+arg)
encode = (hb+arg)#handbrake+参数 开始转码
#print (encode)
system(encode)
input("转完啦！")