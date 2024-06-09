import re
from threading import Thread
from transformers import TextIteratorStreamer
from transformers import AutoModelForCausalLM, AutoTokenizer
device = "cuda" # the device to load the model onto
 
dir="Qwen/Qwen1.5-0.5B-Chat-GPTQ-Int4"
model = AutoModelForCausalLM.from_pretrained(
    dir,
    torch_dtype="auto",
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained(dir)
def chat(messages):
    
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(device)

    generated_ids = model.generate(
        model_inputs.input_ids,
        max_new_tokens=20480
    )
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

    return response
    
def stream_chat(messages):
    
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(device)
    streamer = TextIteratorStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)

    generation_kwargs = dict(model_inputs, streamer=streamer, max_new_tokens=512)
    thread = Thread(target=model.generate, kwargs=generation_kwargs)
    thread.start()

    
    return streamer 
def askai(prompt):
    print("问：",prompt)
    try:
        messages=[]
        messages.append({"role": "user", "content": prompt})
        # messages.append({"role": "assistant", "content": "好的"})
        # messages.append({"role": "user", "content": prompt})
        # content=chat(messages)
        for stream_content in stream_chat(messages):
            content=stream_content
            yield content  
        print("答：",content)
    except:
        content=prompt
    yield content    
