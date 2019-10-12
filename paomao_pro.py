# encoding:utf-8
import os
import sys
from sys import argv
from os import path,system
import time
from art import *
import ui
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import colorama
from colorama import Fore, Back, Style
from subprocess import call,Popen

pygame.mixer.init()
colorama.init(autoreset=True)
#git推送
tprint('PAOMAO',font='slant')

#print(argv[0])          #argv[0] 类似于shell中的$0,但不是脚本名称，而是脚本的路径   
#rint(argv[1])          #argv[1] 表示传入的第一个参数，既 hell

WorkingDirectory= (path.dirname(path.realpath(argv[0]))) #当前脚本工作路径

os.chdir(WorkingDirectory)

platform=sys.platform
if platform == "darwin":

    print('当前系统是MacOS')

    handbrake="./HandBrakeCLI"   #handbrake路径

    ffmpeg='./ffmpeg'

    ffprobe='./ffprobe'

    print(Fore.YELLOW + '抛锚工具箱2.0 beta\n' )
    input_file=input("您现在使用的是手动导入模式，可以把文件拖拽进本窗口并按回车键:\n") .strip()
    print('即将转码的文件是：'+path.split(input_file)[1]+'\n')#路径和文件名分开，取文件名
    classical_mode=False
    time.sleep(0.1)
    
elif platform == "win32":
    
    print("当前系统是Windows")

    if len(argv) > 2:
        print(Fore.CYAN+'抛锚工具箱2.0 beta 经典模式\n')
        classical_mode=True
        input_file=argv[1]
        print('即将转码的文件是：'+path.split(input_file)[1])

    elif len(argv) < 2:
        print(Fore.YELLOW + '抛锚工具箱2.0 beta\n' )
        input_file=input("您现在使用的是手动导入模式，可以把文件拖拽进本窗口并按回车键(如果路径左右两边有引号，请手动去掉引号):\n") 
        print('即将转码的文件是：'+path.split(input_file)[1]+'\n')#路径和文件名分开，取文件名
        classical_mode=False
        time.sleep(0.1)

    else:
        print(Fore.YELLOW + '抛锚工具箱2.0 beta\n' )
        input_file=argv[1]
        print('即将转码的文件是：'+path.split(input_file)[1]+'\n')
        classical_mode=False
        time.sleep(0.1)

    handbrake="HandBrakeCLI.exe"   #handbrake路径

    ffmpeg='ffmpeg.exe'

    ffprobe='ffprobe.exe'
else:
    print('\n\n\n\n\n\n不支持当前系统\n\n\n\n\n\n')

file_split=path.splitext(input_file)    #文件名和后缀分割开

def show_prompt(preset_name):
    prompt='\n当前转码预设：'+Fore.YELLOW+preset_name+Fore.RESET+' \n即将开始转码~\n'
    print(prompt)

def getLength(input_video):
    #print(input_video)
    cmd = '%s -i \"%s\" -show_entries format=duration -v quiet -of csv="p=0"' %(ffprobe,input_video)
    output =os.popen(cmd,'r')
    output = output.read()
    return output


output_file=file_split[0]+"_pm"+".mp4"

encode_arg=" -e x264 --encoder-tune psnr --encoder-preset slow -X 1920 --encoder-level 4.0 -2 -T -R 44.1 --vb 5800"
prompt='当前转码参数：Bilibili 6000K Slow\n即将开始转码~'

def paomao(encode_arg):

    cmd = (handbrake+" -i \"%s\" -o \"%s\"%s"%(input_file,output_file,encode_arg))
    
    print(cmd)

    time.sleep(0.1)

    call(cmd,shell=True)
    
slow='标准版(在合理的转码速度下获得不错的画质，推荐大多数情况下使用)'

slower='高画质版(比标准版更慢的转码速度，更好的画质，推荐时间充裕的时候使用)'

game='高速版(比标准版更高的转码速度，合理的画质)'

wechat='微信版(把视频暴力压缩到25m以下，视频时长越长，画质越差)'

demo="DEMO版(高速，画质一般，文件小，适合压成demo给客户看)"

user="自定义预设(高级功能，如果懂得如何使用命令行版handbrake就自己设置吧！)"

audio="音频提取(把音轨提取出来转成320k的mp3)"

if classical_mode:
    preset=slow
else:
    choices = [slow, slower,wechat,game,demo,user,audio]
    preset = ui.ask_choice("选择一个预设", choices=choices)

if preset == slow:
    show_prompt('标准版')
    paomao(encode_arg)
    pass
elif preset == slower:
    
    encode_arg=" -e x264 --encoder-tune psnr --encoder-preset slower -X 1920 --encoder-level 4.0 -2 -T -R 44.1 --vb 5800"
    show_prompt('高画质版')
    paomao(encode_arg)

elif preset == wechat:
    try:
        duration=float(getLength(input_file))
    except:
        print(Fore.RED+'出事啦,无法计算视频长度，请手动输入视频长度，\n默认单位为秒，请直接输入数字\n'+Fore.RESET)

        duration = input()

    else:
        pass


    print( '视频时长为'+str(duration)+'秒' )
    videobitrate=20*8/duration*1024-32
    ab=32
    #print(videobitrate)
    if 0 < videobitrate <= 10:
        videobitrate=20*8/duration*1024-10
        ab=10
        if videobitrate < 1:

            print("视频时长过长，无法转换，我崩溃了")
            input()
            exit(0)
        else:
            pass

    if 10<videobitrate<64:
        print(Fore.RED+'!!!!视频时长过长，画质可能会惨不忍睹!!!!'+Fore.RESET)
        pass
    if duration>1000:
        wechat_choices = ["我不管，我就要！", "害怕！那算了~"]
        warning = ui.ask_choice(
            "温馨提示:\n---------------------------------------------------------------------------------------\n视频时长超过10分钟！\
                微信转码的规则是无论视频多长，都要压缩到25m以内，\n视频文件体积=(音频码率+视频码率) x 时长 / 8\n视频越长画质越差，10分钟以上的视频画质通常惨不忍睹\n确定要继续吗？\
                \n---------------------------------------------------------------------------------------", choices=wechat_choices
                )
        if warning == "我不管，我就要！":
            pass
        else:
            
            exit(0)
    encode_arg=" -e x264 --encoder-tune psnr --encoder-preset slow -X 960 --encoder-level 4.0 -2 -T --ab %s -R 44.1 --vb "%(ab)+str(videobitrate)
    output_file=file_split[0]+"_wechat"+".mp4"
    show_prompt('微信视频')
    paomao(encode_arg)

elif preset == game:
    encode_arg=" -e x264 --encoder-tune psnr --encoder-preset medium -X 1920 --encoder-level 4.0 -2 -T -R 44.1 --vb 5800"
    show_prompt('高速版')
    paomao(encode_arg)

elif preset == demo:
    encode_arg=" -e x264 --encoder-tune psnr --encoder-preset medium -X 960 --encoder-level 4.0 -R 44.1 --ab 32 --vb 1500"
    show_prompt('DEMO')
    paomao(encode_arg)

elif preset == audio:
    output_file=file_split[0]+"_pm"+".mp3"
    cmd=ffmpeg+" -i \"%s\" -f mp3 -vn -b:a 320k \"%s\" " %(input_file,output_file)
    show_prompt('音频提取')
    call(cmd,shell=True)

elif preset == user:
    #encode_arg=" -e x264 --encoder-tune psnr --encoder-preset medium -X 960 --encoder-level 4.0 -R 44.1 --ab 32 --vb 1500"
    print('默认参数是:',Fore.CYAN+encode_arg+Fore.RESET+'\n')
    print('您可以复制并修改上面的参数，或查询官方文档',Fore.CYAN+r'https://handbrake.fr/docs/en/1.2.0/cli/command-line-reference.html'+Fore.RESET,'\n')
    input('请输入参数(第一个参数前需要加空格)：\n')
    show_prompt('用户自定义')
    paomao(encode_arg)

else:
    print ('如果你看到这条消息 说明程序出错了 可以考虑联系飘渺酱')
    exit(0)
    pass

if os.path.exists(output_file):
    music=pygame.mixer.Sound('Congrats.wav')
    music.play()
    input(Fore.GREEN+"\n\n转完啦!!！")
    exit(0)
    
else:
    music=pygame.mixer.Sound('error.wav')
    music.play()
    print(Fore.RED+'\n\n出事儿啦！\n检测不到视频文件，是不是出问题了？可以考虑联系飘渺酱!')
    input()
