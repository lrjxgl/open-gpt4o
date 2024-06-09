import gradio as gr
from PIL import Image
import torch
 
from transformers import AutoModel, AutoTokenizer 
modle_dir="openbmb/MiniCPM-V-2"
model = AutoModel.from_pretrained(modle_dir, trust_remote_code=True, torch_dtype=torch.bfloat16)
# For Nvidia GPUs support BF16 (like A100, H100, RTX3090)
model = model.to(device='cuda', dtype=torch.float16)
# For Nvidia GPUs do NOT support BF16 (like V100, T4, RTX2080)
#model = model.to(device='cuda', dtype=torch.float16)
# For Mac with MPS (Apple silicon or AMD GPUs).
# Run with `PYTORCH_ENABLE_MPS_FALLBACK=1 python test.py`
#model = model.to(device='mps', dtype=torch.float16)

tokenizer = AutoTokenizer.from_pretrained(modle_dir, trust_remote_code=True)
model.eval()

def numpy_to_pil_rgb(numpy_image):
    # 如果numpy_image是从OpenCV读取的，需要将BGR转为RGB
    if numpy_image.shape[2] == 3:  # 检查是否为三通道图像
        numpy_image = numpy_image[:, :, ::-1]  # 将BGR转为RGB

    # 将NumPy数组转换为PIL Image对象
    pil_image = Image.fromarray(numpy_image)
    
    # 转换图像模式为RGB（如果原始不是RGB的话，这一步可能不是必须的）
    pil_image_rgb = pil_image.convert('RGB')
    
    return pil_image_rgb


def ocr_uploaded_image(image,prompt):
    print(image)
    #image = Image.open(img).convert('RGB')
    image=numpy_to_pil_rgb(image)
    if prompt is None:
        prompt='What is in the image?'
    else:
        question = prompt
    msgs = [{'role': 'user', 'content': question}]

    res, context, _ = model.chat(
        image=image,
        msgs=msgs,
        context=None,
        tokenizer=tokenizer,
        sampling=True,
        temperature=0.7
    )
    text = res
    return text

iface = gr.Interface(
    fn=ocr_uploaded_image,
    inputs=[gr.Image(label="Upload an image for OCR"),"text"],
    outputs="text",
    title="OCR Image Recognition"
)

iface.launch(server_port=7861)