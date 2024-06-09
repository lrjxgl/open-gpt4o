import time
from PIL import ImageGrab
import pyautogui

def screen_capture(interval=1, duration=5, filename_prefix='screenshot'):
    """
    每隔interval秒进行一次屏幕截图，总共持续duration秒。
    
    :param interval: 截图间隔时间（秒）
    :param duration: 总持续时间（秒）
    :param filename_prefix: 图片文件名前缀
    """
    start_time = time.time()
    count = 1
    
    while time.time() - start_time < duration:
        # 截取整个屏幕
        image = pyautogui.screenshot()
        
        # 使用PIL的ImageGrab模块也可以实现类似功能，例如：image = ImageGrab.grab()
        
        # 构造文件名，确保文件名唯一
        filename = f"output/capture/{filename_prefix}_{count}.png"
        
        # 保存截图
        image.save(filename)
        print(f"已保存截图：{filename}")
        
        count += 1
        time.sleep(interval)  # 等待指定的间隔时间

# 调用函数，每隔1秒截图，持续5秒
screen_capture(interval=1, duration=5)