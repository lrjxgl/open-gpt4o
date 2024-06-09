from typing import Union
import time
import base64
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from paddlespeech.cli.tts.infer import TTSExecutor
from paddlespeech.cli.asr.infer import ASRExecutor
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

tts = TTSExecutor()
asr = ASRExecutor()
@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/tts")
def read_item(word: str):
    
    output="output/"+str(time.time())+".wav"
    tts(text=word, output=output)
    con=open(output,"rb").read()
    audio_base64 = base64.b64encode(con)
    # 将字节串转换为字符串以便输出或存储
    audio_base64_str = audio_base64.decode('utf-8')
    return {"audio": audio_base64_str}
    

@app.get("/asr")
def read_asr(audio_file: str):
    result = asr(audio_file=audio_file)
    print(result)
    return {"result":result}