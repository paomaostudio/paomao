# encoding:utf-8
import os
import sys
from sys import argv
from os import path
import time
from art import tprint
from subprocess import call, Popen
from rich import print
from rich.panel import Panel
from rich.console import Console
from rich.status import Status
from rich.table import Table
from rich.logging import RichHandler
import subprocess
import re
import keyboard
import toml
import argparse
import logging
from rimage import Rimage
import webbrowser
import base64
from playsound import playsound


WorkingDirectory = (path.dirname(path.realpath(argv[0])))  # 当前脚本工作路径
os.chdir(WorkingDirectory)
log_file_path = WorkingDirectory + "\\log.txt"
debug = False  # 测试模式
handbrake = "HandBrakeCLI.exe" 
ffmpeg = 'ffmpeg.exe'
ffprobe = 'ffprobe.exe'
rimg = Rimage("rimage.exe")

with open('config.toml', 'r', encoding="utf-8") as toml_file:
    config = toml.load(toml_file)

# 创建一个日志记录器
logging.basicConfig(
    level="NOTSET", format="%(message)s", datefmt="[%X]", handlers=[RichHandler()]
)
logger = logging.getLogger("rich")
logging.getLogger('playsound').setLevel(logging.CRITICAL)
# 调试信息开关
debug_mode = config["config"]["debug"]  # 将这个变量设置为 False 来关闭调试信息

# 根据开关设置日志级别
if debug_mode:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.WARNING)

def parse_arguments():
    """解析命令行参数并返回解析结果。

    Returns:
        argparse.Namespace: 包含命令行参数的Namespace对象。
    """
    parser = argparse.ArgumentParser(description="抛锚工具箱")
    parser.add_argument('--queue', '-q', nargs='+', help='添加到文件队列')
    parser.add_argument('--input', '-i', help='输入文件')
    parser.add_argument('--preset', '-p', help='预设')
    parser.add_argument('--custom-mode', '-m', help='自定义模式')

    args = parser.parse_args()
    return args



def decode(encoded_text):
    encoded_bytes = encoded_text.encode('utf-8')
    text_bytes = base64.b64decode(encoded_bytes)
    return text_bytes.decode('utf-8')

def init_greeting():
    if config["config"]["vip"] == 1:
        vip = True
        vip_name = decode(config["config"]["vip_name"])
        greeting = f"欢迎使用 [#ffd700]抛锚工具箱 {version} 至尊版 [/#ffd700]感谢[#ffd700]{vip_name}[/#ffd700]对本项目的大力支持！！"
    else:
        greeting = f"欢迎使用 [yellow]抛锚工具箱 {version}[/yellow] "
    return greeting




# 定义一个函数，用于处理队列中的文件
def queue_file_handler(file):
        file_name = str(path.split(file)[1])
        file_split = path.splitext(file)    # 文件名和后缀分割开
        
        if preset_arg == 'mp3':
            output_file = file_split[0] + "_pm.mp3"
        elif preset_arg in ['rimage','rimage2']:
            logger.debug("rimage模式")
            output_file = file_split[0] + "_pm.jpg"
        else:
            output_file = file_split[0] + ext
        
        return file_name, output_file


def run_handbrake(cmd, log_file_path, status):
    with open(log_file_path, 'w', encoding='utf-8', errors='ignore') as log_file:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, encoding='utf-8', errors='ignore')
        
        # 正则表达式匹配 "Encoding" 开头的行
        pattern = re.compile(r'^Encoding:.*$', re.M)
        pattern2 = re.compile(r'^size.*$', re.M)
        while True:
            line = process.stdout.readline()
            if not line:
                break
            log_file.write(line)  # 写入日志文件
            if pattern.match(line):
                status.update(line)
            elif pattern2.match(line):
                status.update(line)
                #print(line, end='') 
                

        process.wait()


def build_command(input_file, output_file, preset_arg):
    """
    根据输入文件、输出文件和预设参数构建命令字符串。
    """
    if preset_arg == "mp3":
        cmd = f"{ffmpeg} -i \"{input_file}\" \"{output_file}\""
    elif preset_arg == "rimage":
        cmd = rimg.converter(input_file)
    elif preset_arg == "rimage2":
        cmd = rimg.resizer(input_file, width=image_width)
    else:
        cmd = f"{handbrake} -i \"{input_file}\" -o \"{output_file}\""
    return cmd


def MediaConverter(encode_arg):
    if preset_arg == "mp3":
        cmd = ffmpeg + " -i \"%s\" %s \"%s\" " % (input_file, encode_arg, output_file)
    elif preset_arg == "rimage":
        cmd =rimg.converter(input_file)
    elif preset_arg == "rimage2":
        cmd =rimg.resizer(input_file, width=image_width)
    else:
        cmd = (handbrake + " -i \"%s\" -o \"%s\"%s" %
            (input_file, output_file, encode_arg))
        
    logger.debug(cmd)
    if not args.queue or len(args.queue) == 1:
        print(Panel(cmd))
    with console.status("[bold green]正在转码...") as status:
        run_handbrake(cmd, "log.txt",status)
        pass


def file_exists(output_file):
    if os.path.exists(output_file):
        music = 'Congrats.mp3'
        console.print(Panel(f"[yellow] [bright_cyan]{output_file} [/bright_cyan]转完啦!![/yellow]"))       
    else:
        music = 'error.mp3'
        text = f"[yellow]出事儿啦！检测不到视频文件 [bright_cyan]{output_file}[/bright_cyan] ，是不是出问题了？\n可以考虑联系开发者飘渺酱!\
                \n把日志文件 [bright_cyan]%s[/bright_cyan]\n发送到邮箱： [bright_cyan]paomao@paomao.cc[/bright_cyan] 并附上自己的联系方式，来获取帮助[/yellow]" % (log_file_path)
        console.print(Panel(text))
    return music

def file_path_converter(input_file,ext):
    file_name = str(path.split(input_file)[1])  # 包含后缀的文件名
    file_split = path.splitext(input_file)    # 文件名和后缀分割开的列表
    output_file = file_split[0] + ext   # 添加新后缀的文件名
    return file_name, output_file


def select_preset(console):
    # 创建一个表格对象
        table = Table(show_header=False) 

        # 添加表格行
        table.add_row("1", config["hd"]["name"], config["hd"]["summary"], "2", config["4k"]["name"], config["4k"]["summary"])
        table.add_row("3", config["mp3"]["name"], config["mp3"]["summary"], "4", config["demo"]["name"], config["demo"]["summary"])
        table.add_row("5", config["tiny"]["name"], config["tiny"]["summary"],"6", config["user1"]["name"], config["user1"]["summary"])
        table.add_row("7", config["user2"]["name"], config["user2"]["summary"],"8", config["user3"]["name"], config["user2"]["summary"])
        table.add_row("9", config["rimage"]["name"], config["rimage"]["summary"],"0", config["rimage2"]["name"], config["rimage2"]["summary"])
        # 打印表格
        console.print(table)

        
        # 定义功能函数
        def function1():
            global Preset
            Preset = config["hd"]
        def function2():
            global Preset
            Preset = config["4k"]
        def function3():
            global Preset
            global preset_arg
            Preset = config["mp3"]
            preset_arg = "mp3"
        def function4():
            global Preset
            Preset = config["demo"]
        def function5():
            global Preset
            Preset = config["tiny"]
        def function6():
            global Preset
            Preset = config["user1"]
        def function7():
            global Preset
            Preset = config["user2"]
        def function8():
            global Preset
            Preset = config["user3"]
        def function9():
            global Preset
            global preset_arg
            Preset = config["rimage"]
            preset_arg = "rimage"
        def function0():
            global Preset
            global preset_arg
            Preset = config["rimage2"]
            preset_arg = "rimage2"
            
        def function_help():
            webbrowser.open(url)

        # 监听数字键事件
        keyboard.add_hotkey("1", function1)
        keyboard.add_hotkey("2", function2)
        keyboard.add_hotkey("3", function3)
        keyboard.add_hotkey("4", function4)
        keyboard.add_hotkey("5", function5)
        keyboard.add_hotkey("6", function6)
        keyboard.add_hotkey("7", function7)
        keyboard.add_hotkey("8", function8)
        keyboard.add_hotkey("9", function9)
        keyboard.add_hotkey("0", function0,suppress=True)
        keyboard.add_hotkey("h", function_help,suppress=True)
        print("请按下 1 到 0 之间的数字键执行对应功能,按 H 键获取帮助")
        while not Preset:
            event = keyboard.read_event()
            logger.debug(Preset)
            if event.event_type == keyboard.KEY_DOWN and event.name == "q":
                break
        keyboard.unhook_all()
        return Preset
       

        

if __name__ == "__main__":
    version = "2.42"
    os.system('mode con: cols=80 lines=35')
    tprint('PAOMAO', font='slant')
    Preset = False
    args = parse_arguments()
    preset_arg = args.preset
    input_arg = args.input
    url = config["config"]["help_url"]
    greeting = init_greeting()
    console = Console()
    console.print(Panel(greeting))
    ext = "_pm.mp4"

    if debug:
        input_file = r"M:\BaiduNetdiskDownload\节目\龙游晚会录像v2.mp4"
        Preset = config[preset_arg]
        encode_arg = Preset['arg']
        file_name, output_file = file_path_converter(input_file,ext)

    elif args.preset:
        input_file = input_arg
        Preset = config[preset_arg]
        encode_arg = Preset['arg']

        if args.preset == 'mp3':
            ext = "_pm.mp3"
        if args.preset in ['rimage','rimage2']:
            ext = "_pm.jpg"
        
        file_name, output_file = file_path_converter(input_file,ext)    
        console.print(Panel('当前文件：[red]' + file_name +"[/red]"))
        console.print(Panel(f"{Preset['name']}：[red]{Preset['info']}[/red]"))

        MediaConverter(encode_arg)
        music = file_exists(output_file)
        playsound(music)
        input()

    elif args.queue:
        Preset = select_preset(console)
        if preset_arg == "rimage2":
            image_width = input("请输入图片的宽度，按回车键确认: ")

        encode_arg = Preset['arg']
        logger.debug(f"encode_arg: {encode_arg}")
        queue_length = len(args.queue)
        index = 1
        converted_files = []
        console.print(Panel(f"{Preset['name']}：[red]{Preset['info']}[/red]"))

        #print(Preset, preset_arg)
        for file_path in args.queue:
            file_name, output_file = queue_file_handler(file_path)
            logger.debug("文件名：%s, 输出文件：%s, 编码参数：%s", file_name, output_file, encode_arg)
            input_file = file_path
            console.print(Panel(f'{index}/{queue_length} 当前文件：[red]' + file_name +"[/red]"))

            MediaConverter(encode_arg)
            index += 1
            converted_files.append(output_file)

        for file in converted_files:
            music = file_exists(file)
        playsound(music)
        input()

