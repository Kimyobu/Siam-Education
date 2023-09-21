import torch
import os
from diffusers import StableDiffusionPipeline
import argparse
from IPython.display import Image
from utils import save_img
from image import display_images_sorted, display_images_in_grid

def load(model_id="runwayml/stable-diffusion-v1-5"):
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16, safety_check=None)
    pipe = pipe.to("cuda")
    pipe.enable_xformers_memory_efficient_attention()
    return pipe

def gen(pipe, prompt):
    images = pipe(prompt)
    save = save_img(image, "outputs/txt2img")
    # display_images_sorted(os.path.dirname(save), num_cols=5, image_width=4)
    display_images_in_grid(images)
