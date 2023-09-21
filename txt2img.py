import torch
from diffusers import StableDiffusionPipeline
import argparse
from IPython.display import display

parser = argparse.ArgumentParser(description="")
parser.add_argument("prompt", type=str)

args = parser.parse_args()

pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16)
pipe = pipe.to("cuda")
pipe.enable_xformers_memory_efficient_attention()

prompt = args.prompt
image = pipe(prompt).images[0]
display(image)