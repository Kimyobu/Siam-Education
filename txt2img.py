import torch
import os
from diffusers import StableDiffusionPipeline
import argparse
from IPython.display import Image
from utils import save_img
from image import display_images_sorted

parser = argparse.ArgumentParser(description="")
parser.add_argument("--prompt", type=str)

args = parser.parse_args()

pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16, safety_check=None)
pipe = pipe.to("cuda")
pipe.enable_xformers_memory_efficient_attention()

prompt = args.prompt
image = pipe(prompt).images[0]
save = save_img(image, "outputs/txt2img")
display_images_sorted(os.path.dirname(save), num_cols=5, image_width=4)

del pipe
torch.cuda.empty_cache()