做一个类似gpt4o的聊天机器人，支持语音对话，图像对话，视频对话。暂时只是demo.

## 语音识别
   语音识别采用faster-whisper来实现，支持中文和英文识别，速度快。
   https://github.com/SYSTRAN/faster-whisper


## 文本对话
    文本对话采用千问模型，支持中文和英文对话。
    https://modelscope.cn/models/qwen/Qwen1.5-0.5B-Chat-GPTQ-Int4/summary

## 语音合成
    语音合成采用百度paddlespeech,用api来实现，支持中文和英文合成，缺点速度慢。
    https://github.com/PaddlePaddle/PaddleSpeech 
    使用说明 
        安装好paddlespeech，然后运行 g-speech.py

## 图像识别
    图像识别采用MiniCPM-V-2
    https://modelscope.cn/models/iic/MiniGPT-v2/summary 
    使用说明
        运行 python g-img2text.py 

## 屏幕录制
    屏幕录制采用pyautogui来实现，支持linux和windows，支持录制屏幕和窗口。
    运行 g-screen-capture.py

# 安装方法

    环境依赖

    py310+pytorch 

    https://pytorch.org/get-started/locally/ 

    git clone https://github.com/lrjxgl/gpt4o.git

    cd gpt4o

    pip install -r requirements.txt

# 运行方法

    python gradio_app.py