import requests
import base64
import wave
def create_empty_wave(file_name):
    sample_rate = 44100  # 采样率，每秒样本数，标准CD音质为44100
    channel_num = 1  # 声道数，1为单声道，2为立体声
    sample_width = 2  # 采样宽度，单位字节，常见的有1（8位）、2（16位）
    duration_seconds = 0.3  # 文件时长，秒
    with wave.open(file_name, 'wb') as wave_file:
        # 设置参数
        wave_file.setparams((channel_num, sample_width, sample_rate, 
                            duration_seconds * sample_rate, 'NONE', 'not compressed'))
def tts(word,outfile):
    # 目标URL
    url = "http://127.0.0.1:8000/tts"
    # 设置查询参数
    params = {"word": word}
    
    try:
        # 发送GET请求
        response = requests.get(url, params=params)
        
        # 检查响应状态码是否为200（成功）
        if response.status_code == 200:
            # 解析JSON响应内容
            res = response.json()
            if res is None:
                create_empty_wave(outfile)
                return outfile
            # 打印或处理音频文件路径
            base64_string=res["audio"]
            audio_binary = base64.b64decode(base64_string)
            with open(outfile, 'wb') as audio_file:
                audio_file.write(audio_binary)
            return outfile
        else:
            print(f"请求失败，状态码：{response.status_code}")
            create_empty_wave(outfile)
            return outfile
    except requests.exceptions.RequestException as e:
        print(f"请求过程中发生错误：{e}")
        create_empty_wave(outfile)
        return outfile