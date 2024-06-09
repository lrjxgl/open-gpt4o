import gradio as gr
import io 
import re
import numpy as np
import time
from pydub import AudioSegment
import wave
import soundfile as sf
from faster_whisper import WhisperModel
import lib.text2text_qianwen as askai
from lib.tts import  tts
import pickle
model = WhisperModel("F:/model/faster-whisper-small")
#初始化
with open("out_stream.txt","wb") as f:
    pass

def get_stream():
    out_stream=None
    with open("out_stream.txt","rb") as f:
        serialized_data=f.read()

        if serialized_data:
            out_stream=pickle.loads(serialized_data)
    return out_stream
def save_stream(data):
    """
    将音频流保存到文件
    :param data: 音频流数据
    :return: 无
    """
    sr, y = data
    y = y.astype(np.float32)
    y /= np.max(np.abs(y))
    # h获取历史音频流
    with open("out_stream.txt","rb") as f:
        data_old = f.read()
        
    
        if data_old:
            # 合并两个音频流
            old_stream=pickle.loads(data_old)
            osr, oy = old_stream
            oy = oy.astype(np.float32)
            oy /= np.max(np.abs(oy))
            oy = np.concatenate([oy, y])
            old_stream=(sr,oy)
        else:    
            old_stream = data
    # 将音频流数据写入文件
    with open("out_stream.txt","wb") as f:
        con=pickle.dumps(old_stream)
        f.write(con)
def empty_wav_tuple():
   return wav_to_tuple("static/empty.wav")
def wav_to_tuple(wav_file):
    with wave.open(wav_file, 'rb') as w:
        num_channels = w.getnchannels()
        sample_width = w.getsampwidth()
        framerate = w.getframerate()
        num_frames = w.getnframes()
        
        audio_buffer = w.readframes(num_frames)
        audio_data = np.frombuffer(audio_buffer, dtype=np.int16 if sample_width == 2 else np.int8)
        
        # 如果是多通道，可以单独处理每个通道或将它们组合成更复杂的结构
        if num_channels > 1:
            audio_data = audio_data.reshape(-1, num_channels)
        
        # 封装成元组
        audio_tuple = (framerate,audio_data)
    
    return audio_tuple 

 
def transcribe(stream, new_chunk):
    
    history=open("history.txt","r").read()
    sr, y = new_chunk
    y = y.astype(np.float32)
    y /= np.max(np.abs(y))

    if stream is None:
        #stream = np.concatenate([stream, y])
        stream = y
     
        
    file_stream = "output/audio-stream.wav"
    file_all = "output/audio-all.wav"
    # 最新
    sf.write(file_stream, y, sr)
    

    con=""
    # 判断当前
    segments, info =model.transcribe(
        file_stream,
        beam_size=5,
         
        condition_on_previous_text=False,
        vad_filter=True,
        vad_parameters=dict(min_silence_duration_ms=1000)
    )
    print(segments)
    last=""
    for segment in segments:      
        last=segment.text
    
    out_stream=get_stream()      
    if last=='' or last=='字幕by索兰娅' or last=='by bwd6':
        # 如果遇到暂停 解读完整
        # 全部
        sf.write(file_all, stream, sr)
        segments, info =model.transcribe(
            file_all,
            beam_size=10,
             
            condition_on_previous_text=False,
            vad_filter=True,
            vad_parameters=dict(min_silence_duration_ms=1000)
        )
        last=""
        for segment in segments:
            last+=segment.text
        con=last+"\n"
        if last!='' and last!='字幕by索兰娅' and last!=' by bwd6':
            stream = y   
            messages=[]
            messages.append({"role": "user", "content": last})
            print("问：",last)
            ttsKey=0
            tts_con=""
             
            for cc in askai.stream_chat(messages):
            #for response in askai.stream_chat(messages):
                #print(response)
                #cc=response.output.choices[0]['message']['content']
                ttsKey+=1
                con +=cc
                #print("回答：",cc)
                tts_con += cc
                split_result = re.split(r'[.,，。]', tts_con)
                split_result = [part for part in split_result if part]
                if len(split_result)>1:
                    s1=split_result[:-1]
                    tts_con=",".join(s1)
                    print(tts_con)
                    outfile="output/tts"+str(time.time()+ttsKey)+".wav"
                    tts(tts_con,outfile)
                    out_stream=wav_to_tuple(outfile)
                     
                    tts_con=split_result[-1]
                    #保存
                    save_stream(out_stream)
                    
                    yield stream,con,out_stream
            
            if len(tts_con)>0:
                print("剩下的",tts_con)
                ttsKey+=1
                outfile="output/tts"+str(time.time()+ttsKey)+".wav"
                tts(tts_con,outfile)
                out_stream=wav_to_tuple(outfile)
                save_stream(out_stream)
                
                tts_con=""
            con+="\n"       
            #保存
          
            yield stream,con,out_stream
        else:
              
            con="" 
            stream = np.concatenate([stream, y])
            
                    
            yield stream,con,out_stream
    else:
        stream = np.concatenate([stream, y]) 
        con="" 
         
        yield  stream, con,out_stream  
     
    #return stream, con
    
state1=gr.State() 
state2=gr.State() 
saudio=gr.Audio(sources=["microphone"],streaming=True)
demo = gr.Interface(
    transcribe,
    [state1, saudio],
    [state1, gr.Textbox(placeholder="等待讲话...",lines=6),gr.Audio(autoplay=True, streaming=True)],
    live=True
)
demo.queue(max_size=2)
demo.launch(server_name="0.0.0.0",share=False)