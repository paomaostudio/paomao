from gooey import Gooey,GooeyParser
import paomao_pro as pm
import os
import sys


#from argparse import ArgumentParser
#初始化
version="抛锚工具箱 2.2.2"
WorkingDirectory= (os.path.dirname(os.path.realpath(sys.argv[0]))) #当前脚本工作路径
print (WorkingDirectory)
os.chdir(WorkingDirectory)#切换工作目录到脚本文件夹
def os_check():
        global OS
        global handbrake
        global ffmpeg
        global ffprobe
        platform=sys.platform
        if platform == "darwin":

            print('当前系统是MacOS\n')
            
            OS="macos"

            handbrake="./HandBrakeCLI"   #handbrake路径

            ffmpeg='./ffmpeg'

            ffprobe='./ffprobe'

            print(Fore.YELLOW + '%s\n'%(version) )
            classical_mode=False
            time.sleep(0.1)
            
        elif platform == "win32":
            
            print("当前系统是Windows\n")
            
            OS="windows"
            handbrake="HandBrakeCLI.exe"   #handbrake路径

            ffmpeg='ffmpeg.exe'

            ffprobe='ffprobe.exe'
        else:
            print('\n\n\n\n\n\n不支持当前系统\n\n\n\n\n\n')

os_check()
print(OS,handbrake,ffmpeg,ffprobe)

@Gooey(
language='chinese',
advanced=True,
program_name=version,       # Defaults to script name
program_description="抛锚",       # Defaults to ArgParse Description
default_size=(800, 700),
)
def main():
    
    parser = GooeyParser(description="工具箱模式") 

    parser.add_argument('data',
                            action='store',
                            help="Source directory that contains Excel files")

    parser.add_argument('-d', help='Start date to include')
    args = parser.parse_args()
    print(args.data)
    pm.main()
if __name__ == '__main__':
    main()