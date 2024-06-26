import gradio as gr
import os
# os.system('pip install --force-reinstall torch==2.0.1')
import torch
print(torch.__version__)
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoModel
from openxlab.model import download


base_path = './repo'
os.system('git lfs install')
os.system(f'git clone https://code.openxlab.org.cn/kafm/self-perception.git {base_path}')
os.system(f'cd {base_path} && git lfs pull')

tokenizer = AutoTokenizer.from_pretrained(base_path,trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(base_path,trust_remote_code=True, torch_dtype=torch.float16).cuda()
print('model path' + base_path)

def chat(message,history):
    for response,history in model.stream_chat(tokenizer,message,history,max_length=2048,top_p=0.7,temperature=1):
        yield response

gr.ChatInterface(chat,
                 title="InternLM2实战营自我认知模型",
                description="""
InternLM is mainly developed by Shanghai AI Laboratory.  
                 """,
                 ).queue(1).launch()
