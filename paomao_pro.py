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


            
            #input_file=input("您现在使用的是手动导入模式，可以把文件拖拽进本窗口并按回车键:\n") .strip()
            #input_file=input_file.replace("\\","")
            #print('即将转码的文件是：'+path.split(input_file)[1]+'\n')#路径和文件名分开，取文件名
            

            # if len(argv) > 2:
            #     print(Fore.CYAN+'%s 经典模式\n'%(version))
            #     classical_mode=True
            #     input_file=argv[1]
            #     print('即将转码的文件是：'+path.split(input_file)[1])

            # elif len(argv) < 2:
            #     print(Fore.YELLOW + '%s\n'%(version) )
            #     input_file=input("您现在使用的是手动导入模式，可以把文件拖拽进本窗口并按回车键(如果路径左右两边有引号，请手动去掉引号):\n") 
            #     print('即将转码的文件是：'+path.split(input_file)[1]+'\n')#路径和文件名分开，取文件名
            #     classical_mode=False
            #     time.sleep(0.1)

            # else:
            #     print(Fore.YELLOW + '%s\n'%(version) )
            #     input_file=argv[1]
            #     print('即将转码的文件是：'+path.split(input_file)[1]+'\n')
            #     classical_mode=False
            #     time.sleep(0.1)
def getLength(input_video):
    #print(input_video)
    cmd = '%s -i \"%s\" -show_entries format=duration -v quiet -of csv="p=0"' %(ffprobe,input_video)
    output =os.popen(cmd,'r')
    output = output.read()
    return output

slow=('标准模式',
'(在合理的转码速度下获得不错的画质，符合bilibili不二压标准，推荐大多数情况下使用)',
" -e x264 --encoder-tune psnr --crop 0:0:0:0 --encoder-preset slow -X 1920 --encoder-level 4.0 -2 -T -R 44.1 --vb 5800")



slower=('超清模式',
'(比标准版更慢的转码速度，更好的画质，推荐时间充裕的时候使用)',
" -e x264 --encoder-tune psnr --crop 0:0:0:0 --encoder-preset slower -X 1920 --encoder-level 4.0 -2 -T -R 44.1 --vb 5800")


game=('高速模式',
   '(比标准版更高的转码速度，合理的画质)',
   " -e x264 --encoder-tune psnr --crop 0:0:0:0 --encoder-preset normal -X 1920 --encoder-level 4.0 -2 -T -R 44.1 --vb 5800")
   

wechat=('微信模式',   
'(把视频暴力压缩到25m以下，视频时长越长，画质越差)',
)


demo=('演示模式',
   '(高速，画质一般，文件小，适合给客户看的DEMO)',
   ' -e x264 --encoder-tune psnr --crop 0:0:0:0 --encoder-preset medium -X 960 --encoder-level 4.0 -R 44.1 --ab 32 --vb 1500'
)


user=('专家模式' ,  '(高级功能，如果懂得如何使用命令行版handbrake就自己设置吧！)'
)

audio=('音频提取'   '(把音轨提取出来转成320k的mp3)'
)

def wechat_check(input_file):
    print (input_file)
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
    
    if 0 < videobitrate <= 10:
        videobitrate=20*8/duration*1024-10
        ab=10
    elif videobitrate < 1:
        print("视频时长过长，无法转换，我崩溃了")
        input()
        exit(0)
    elif 10<videobitrate<64:
        print(Fore.RED+'!!!!视频时长过长，画质可能会惨不忍睹!!!!'+Fore.RESET)
        pass
    elif videobitrate>2000:
        videobitrate=2000
        pass
    else:
        pass
        
    if duration>1000:
        print ("警告：视频时长较长，画质可能会惨不忍睹")
    return (" -e x264 --encoder-tune psnr --crop 0:0:0:0 --encoder-preset slow -X 640 --encoder-level 4.0 -2 -T --ab %s -R 44.1 --vb "%(ab)+str(videobitrate))       
            
def main():
        
    pygame.mixer.init()
    colorama.init(autoreset=True) 
    #argv[0] 脚本的路径
    #argv[1] 表示传入的第一个参数

    file_split=path.splitext(input_file)    #文件名和后缀分割开

    def show_prompt(preset_name):
        prompt='\n当前转码预设：'+Fore.YELLOW+preset_name+Fore.RESET+' \n即将开始转码~\n'
        print(prompt)

    


    output_file=file_split[0]+"_pm"+".mp4"

    encode_arg=" -e x264 --encoder-tune psnr --crop 0:0:0:0 --encoder-preset slow -X 1920 --encoder-level 4.0 -2 -T -R 44.1 --vb 5800"
    prompt='当前转码参数：Bilibili 6000K Slow\n即将开始转码~'

    def paomao(encode_arg):

        cmd = (handbrake+" -i \"%s\" -o \"%s\"%s"%(input_file,output_file,encode_arg))
        
        print(cmd)

        time.sleep(0.1)

        call(cmd,shell=True)
        


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
        
        #encode_arg=
        show_prompt('超清版')
        paomao(encode_arg)

    elif preset == wechat:
        
        encode_arg=" -e x264 --encoder-tune psnr --crop 0:0:0:0 --encoder-preset slow -X 640 --encoder-level 4.0 -2 -T --ab %s -R 44.1 --vb "%(ab)+str(videobitrate)
        output_file=file_split[0]+"_wechat"+".mp4"
        show_prompt('微信版')
        paomao(encode_arg)

    elif preset == game:
        encode_arg=" -e x264 --encoder-tune psnr --crop 0:0:0:0 --encoder-preset medium -X 1920 --encoder-level 4.0 -2 -T -R 44.1 --vb 5800"
        show_prompt('高速版')
        paomao(encode_arg)

    elif preset == demo:
        encode_arg=" -e x264 --encoder-tune psnr --crop 0:0:0:0 --encoder-preset medium -X 960 --encoder-level 4.0 -R 44.1 --ab 32 --vb 1500"
        show_prompt('DEMO')
        paomao(encode_arg)

    elif preset == audio:
        output_file=file_split[0]+"_pm"+".mp3"
        cmd=ffmpeg+" -i \"%s\" -f mp3 -vn -b:a 320k \"%s\" " %(input_file,output_file)
        show_prompt('音频提取')
        call(cmd,shell=True)

    elif preset == user:
        #encode_arg=" -e x264 --encoder-tune psnr --crop 0:0:0:0 --encoder-preset medium -X 960 --encoder-level 4.0 -R 44.1 --ab 32 --vb 1500"
        print('默认参数是:',Fore.CYAN+encode_arg+Fore.RESET+'\n')
        print('您可以复制并修改上面的参数，或查询官方文档',Fore.CYAN+r'https://handbrake.fr/docs/en/1.2.0/cli/command-line-reference.html'+Fore.RESET,'\n')
        encode_arg = input('请输入参数(第一个参数前需要加空格)：\n')
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
