import torch
import torchvision.transforms as T
import os

import diffusers
import transformers

import argparse

import matplotlib.pyplot as plt
from IPython.display import Image
from utils import save_img
from image import display_images_sorted, display_images_in_grid
from preview_decoder import ApproximateDecoder
from scheduler import Schedulers

Scheduler = Schedulers()

def load(model_id="runwayml/stable-diffusion-v1-5", from_single_file=False, device="cuda"):
    pipe = None
    if from_single_file is True:
        pipe = diffusers.StableDiffusionPipeline.from_single_file(model_id, torch_dtype=torch.float16, safety_checker=None, use_safetensors=True, requires_safety_checker=False)
    else:
        pipe = diffusers.StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16, safety_checker=None, use_safetensors=True, requires_safety_checker=False)
    pipe = pipe.to(device)
    pipe.enable_xformers_memory_efficient_attention()
    return pipe

def gen(model_id: str, pipe: diffusers.StableDiffusionPipeline, prompt: str, negative_prompt: str, num_inference_steps=50, scheduler_name="DPM++ 2M", use_karras_sigmas=False, clip_skip=2, size=(512,512), cfg_scale=7.5, generator=["cuda", -1]):
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
    pipe.text_encoder = transformers.CLIPTextModel.from_pretrained(model_id, num_hidden_layers=12 - (clip_skip - 1), torch_dtype=torch.float16)
    seed = generator[1]
    seed = torch.randint(0, 244536412, (1,)).item() if seed == -1 else seed
    generator = torch.Generator(device=generator[0]).manual_seed(seed)
    p = pipe(
        prompt=prompt,
        negative_prompt=negative_prompt,
        num_inference_steps=num_inference_steps, 
        callback=display_latents_callback,
        width=size[0],
        height=size[1],
        guidance_scale=cfg_scale,
        generator=generator
    )
    images = p.images
    for image in images:
        save = save_img(image, "outputs/txt2img")
    # display_images_sorted(os.path.dirname(save), num_cols=5, image_width=4)
    display_images_in_grid(images)
