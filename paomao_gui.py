from gooey import Gooey,GooeyParser
import paomao_pro as pm
import os
import sys
import time
import argparse

parser = argparse.ArgumentParser()
parser.description='这是程序简介'
parser.add_argument("-n","--normal", help="标准模式",action="store_true")
parser.add_argument("-s","--slow", help="超清模式")
parser.add_argument("-f","--fast", help="高速模式")
parser.add_argument("file", help="默认输入文件，不带参数")
args=parser.parse_args()
normal=args.normal
if args.input:
    input_file=args.input
else:
    input_file=args.file
print(input_file)

if args.normal:
    print (normal)
else:
    print("rua")

#from argparse import ArgumentParser
#初始化
version="抛锚工具箱 2.2.2"
WorkingDirectory= (os.path.dirname(os.path.realpath(sys.argv[0]))) #当前脚本工作路径
print (WorkingDirectory)
os.chdir(WorkingDirectory)#切换工作目录到脚本文件夹
#input_file="D:\\Render2\\C0006(12)_pm.mp4"
input_file="k:\\render\\小初-sweet devil_pm.mp4"


OS,handbrake,ffmpeg,ffprobe=pm.os_check()
slow=('标准模式',
'(在合理的转码速度下获得不错的画质，符合bilibili不二压标准，推荐大多数情况下使用)',
" -e x264 --encoder-tune psnr --crop 0:0:0:0 --encoder-preset slow -X 1920 --encoder-level 4.0 -2 -T -R 44.1 --vb 5800")



slower=('超清模式',
'(比标准版更慢的转码速度，更好的画质，推荐时间充裕的时候使用)',
" -e x264 --encoder-tune psnr --crop 0:0:0:0 --encoder-preset slower -X 1920 --encoder-level 4.0 -2 -T -R 44.1 --vb 5800")


normal=('高速模式',
   '(比标准版更高的转码速度，合理的画质)',
   " -e x264 --encoder-tune psnr --crop 0:0:0:0 --encoder-preset normal -X 1920 --encoder-level 4.0 -2 -T -R 44.1 --vb 5800")
   

wechat=('微信模式',   
'(把视频暴力压缩到25m以下，视频时长越长，画质越差)',
pm.wechat_check(input_file,ffprobe),
)


demo=('演示模式',
   '(高速，画质一般，文件小，适合给客户看的DEMO)',
   ' -e x264 --encoder-tune psnr --crop 0:0:0:0 --encoder-preset medium -X 960 --encoder-level 4.0 -R 44.1 --ab 32 --vb 1500'
)


user=('专家模式' ,  '(高级功能，如果懂得如何使用命令行版handbrake就自己设置吧！)'
)

audio=('音频提取'   '(把音轨提取出来转成320k的mp3)'
)
print(OS,handbrake,ffmpeg,ffprobe)
#pm.wechat_check(input_file,ffprobe)
#print(wechat[2])

@Gooey(
#optional_cols=2,
language='chinese',
#advanced=False,
auto_start=True,
#program_name=version,       # Defaults to script name
#program_description="抛锚",       # Defaults to ArgParse Description
#default_size=(800, 700),
)
def main():
    
    parser = GooeyParser(description="工具箱模式") 
    subs = parser.add_subparsers(help='commands', dest='command')
    flv_parser = subs.add_parser('FLV解封',
         help='curl is a tool to transfer data from or to a server')
    flv_parser.add_argument('data',
                            action='store',
                            help="Source directory that contains Excel files")

    flv_parser.add_argument('-d', help='Start date to include')
    flv_parser.set_defaults(which='flv')
    print('现在是FLv模式')
    #################################
    siege_parser = subs.add_parser(
        '标准模式', help='Siege is an http/https regression testing and benchmarking utility')
    siege_parser.add_argument('--get',
                              help='Pull down headers from the server and display HTTP transaction',
                              type=str)
    siege_parser.set_defaults(which='siege')
    args = parser.parse_args()
    print(args.data)
    print('现在是标准模式')
    #pm.main()
if __name__ == '__main__':
    main()