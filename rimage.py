class Rimage:
    """
    Rimage类提供了对图片进行转换和调整大小的功能。
    
    使用Rimage路径初始化Rimage实例，并可选地指定文件名后缀。
    
    Attributes:
        suffix (str): 生成文件的后缀名，默认为"_pm"。
        rimage_path (str): Rimage工具的路径。
        
    Methods:
        converter(input_file, quality=75):
            对指定的图片文件进行转换，可以指定转换的质量。
            
        resizer(input_file, width, quality=75):
            调整指定图片的宽度，并可以指定转换的质量。
    """
    
    def __init__(self, rimage_path, suffix="_pm"):
        """
        初始化Rimage类的一个实例。
        
        Parameters:
            rimage_path (str): Rimage工具的路径。
            suffix (str, optional): 生成文件的后缀名。默认为 "_pm"。
        """
        self.suffix = suffix
        self.rimage_path = rimage_path

    def converter(self, input_file, quality=75):
        """
        生成一个用于转换图片质量的命令字符串。
        
        Parameters:
            input_file (str): 需要转换的图片文件路径。
            quality (int, optional): 转换后的图片质量，默认为75。
            
        Returns:
            str: 完成转换的命令字符串。
        """
        arg = f"{self.rimage_path} -q {quality} -s {self.suffix} {input_file}"
        return arg
    
    def resizer(self, input_file, width, quality=75):
        """
        生成一个用于调整图片宽度的命令字符串。
        
        Parameters:
            input_file (str): 需要调整大小的图片文件路径。
            width (int): 调整后的图片宽度。
            quality (int, optional): 调整大小后的图片质量，默认为75。
            
        Returns:
            str: 完成调整大小的命令字符串。
        """
        arg = f"{self.rimage_path} -q {quality} -s {self.suffix} --width {width} {input_file}"
        return arg


'''
使用方法：rimage [选项] <文件>...

参数：
<文件>... 要处理的输入文件

选项：
-h, --help 打印帮助信息
-V, --version 打印版本信息

通用：
-q, --quality <质量> 优化图片质量，在使用 Jpegxl 格式时禁用
[范围：1 - 100] [默认：75]
-f, --codec <编解码器> 使用的图像编解码器
[默认：jpg] [可选值：png, oxipng, jpegxl, webp, avif]
-o, --output <目录> 将输出文件写入 <目录>，如果未使用 "-r" 选项
-r, --recursive 保存输出文件时保留文件夹结构
-s, --suffix [<后缀>] 给输出文件名添加后缀
-b, --backup 在输入文件扩展名后添加 ".backup" 后缀
-t, --threads 使用的线程数，更多线程运行更快，但太多可能会导致崩溃
[范围：1 - 16] [仅限整数] [默认：核心数]

量化：
--quantization [<质量>] 启用量化，可选择质量
[范围：1 - 100] [默认：75]
--dithering [<质量>] 启用抖动，可选择质量
[范围：1 - 100] [默认：75]

调整大小：
--width <宽度> 指定宽度调整图片大小
[仅限整数]
--height <高度> 指定高度调整图片大小
[仅限整数]
--filter <滤镜> 用于图片调整大小的滤镜
[可选值：point, triangle, catrom, mitchell] [默认：lanczos3]
'''