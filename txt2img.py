import torch
import torchvision.transforms as T
import os
from diffusers import StableDiffusionPipeline
import argparse
import matplotlib.pyplot as plt
from IPython.display import Image
from utils import save_img
from image import display_images_sorted, display_images_in_grid
from preview_decoder import ApproximateDecoder
from scheduler import Schedulers

Scheduler = Schedulers()

def load(model_id="runwayml/stable-diffusion-v1-5", from_single_file=False):
    pipe = None
    if from_single_file is True:
        pipe = StableDiffusionPipeline.from_single_file(model_id, torch_dtype=torch.float16, safety_check=None, use_safetensors=True)
    else:
        pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16, safety_check=None, use_safetensors=True)
    pipe = pipe.to("cuda")
    pipe.enable_xformers_memory_efficient_attention()
    return pipe

def gen(pipe, prompt, negative_prompt, num_inference_steps=50, scheduler_name="DPM++ 2M", use_karras_sigmas=False):
    def display_latents_callback(step: int, timestep: int, latents: torch.FloatTensor):
        approximateDecoder = ApproximateDecoder.for_pipeline(pipe)
        latents_image = approximateDecoder(latents.squeeze(0))

        # แสดงรูปภาพพร้อม title เป็น step
        plt.figure(figsize=(6, 6))
        plt.imshow(latents_image)
        plt.title(f"Step {step}")
        plt.axis('off')
        plt.show()
    
    pipe.scheduler = Scheduler(scheduler_name).from_config(pipe.scheduler.config, use_karras_sigmas=use_karras_sigmas)
    p = pipe(prompt=prompt, negative_prompt=negative_prompt ,num_inference_steps=num_inference_steps, callback=display_latents_callback)
    images = p.images
    for image in images:
        save = save_img(image, "outputs/txt2img")
    # display_images_sorted(os.path.dirname(save), num_cols=5, image_width=4)
    display_images_in_grid(images)
