from lxml import etree
import webbrowser
import gzip
import shutil
import tempfile
import os

FilePath=r"D:\海豹粥-hand in hand1.prproj"

def open_file(path):# 打开文件，并解析
    global filename
    tmp = tempfile.mkdtemp()
    filename = os.path.splitext(os.path.basename(path))[0] #文件名，不含后缀
    temp_fichier = tmp + '/' + filename

    if path: #Si un fichier est choisi
        with gzip.open(path, 'rb') as f_in:
            with open(temp_fichier, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        return etree.parse(temp_fichier)
    else: return None

def convert_data(projectFile, versionToConvert):
    global filename
    for project in (projectFile.xpath("/PremiereData/Project")):
        if project.get('Version'):
            project.set('Version', versionToConvert)
            return etree.tostring(projectFile, encoding="utf-8", pretty_print=True)

def write_output_file(data): #确认输出文件名，然后输出
    output_file = (filename)
    if output_file: # asksaveasfile return `None` if dialog closed with "cancel".
        if not output_file.endswith(".prproj"):
            output_file = output_file+".prproj"
        with gzip.open(output_file, 'wb') as f:
            f.write(data)
        
    else: return

def get_src_version(projectFile):
    for project in (projectFile.xpath("/PremiereData/Project")):
        if project.get('Version'):
            return project.get('Version')

def get_src_file(): #初始化变量
    global src_filename
    global projectFile
    src_filename = FilePath
    projectFile = open_file(src_filename)
    if projectFile:
        src_version = get_src_version(projectFile)
        print("当前版本是"+src_version)

def convert():
    
    if version and projectFile:
        write_output_file(convert_data(projectFile, version))
    else:
        print("出事啦！")


def textToVersion(argument):
    version = ""
    switcher = {
        "兼容模式" : "1",
        "CC 2018 (v12.0)" : "34",
        "CC 2018 (v12.1)" : "35",
        "CC 2019 (v13.0)" : "36",
    }
    return switcher.get(argument, version)

get_src_file()
print(get_src_version(projectFile))
print(textToVersion("CC 2018 (v12.0)"))

def select():
    version=input("输入要转换的版本：")
    