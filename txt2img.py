import torch
import os
from diffusers import StableDiffusionPipeline, VQModel
import argparse
import matplotlib.pyplot as plt
from IPython.display import Image
from utils import save_img
from image import display_images_sorted, display_images_in_grid

def tensor_to_image(tensor):
    # ใช้ transform ใน torchvision เพื่อแปลง tensor เป็นรูปภาพ
    transform = T.ToPILImage()

    # ถ้า tensor มี batch dimension (batch_size > 1) ให้ใช้ลูปเพื่อแปลงและแสดงรูปภาพแต่ละรายการใน batch
    if len(tensor.shape) == 4:
        images = [transform(t) for t in tensor]
    # ถ้า tensor ไม่มี batch dimension (batch_size=1) ให้แปลงและคืนเป็นรูปภาพเดียวในรูปแบบของ list ที่มีรายการเดียว
    else:
        images = [transform(tensor.squeeze(0))]
    
    return images

def display_latents_callback(step: int, timestep: int, latents: torch.FloatTensor):
    # แปลง latents เป็นรูปภาพ
    tensor = VQModel.forward(sample=latents).latents
    latents_image = tensor_to_image(tensor)

    # แสดงรูปภาพพร้อม title เป็น step
    plt.figure(figsize=(6, 6))
    plt.imshow(latents_image)
    plt.title(f"Step {step}")
    plt.axis('off')
    plt.show()

def load(model_id="runwayml/stable-diffusion-v1-5"):
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16, safety_check=None)
    pipe = pipe.to("cuda")
    pipe.enable_xformers_memory_efficient_attention()
    return pipe

def gen(pipe, prompt, negative_prompt, num_inference_steps=50):
    images = pipe(prompt=prompt, negative_prompt=negative_prompt ,num_inference_steps=num_inference_steps, callback=display_latents_callback)
    save = save_img(image, "outputs/txt2img")
    # display_images_sorted(os.path.dirname(save), num_cols=5, image_width=4)
    display_images_in_grid(images)
