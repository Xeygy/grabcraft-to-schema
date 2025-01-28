import grabcraft_to_schema as gts
import blockmodel_avg_mapper as bam
import json
import PIL
from PIL import Image
import numpy as np
from pathlib import Path

'''
Script to automatically download image schematics from grabcraft
'''
MODEL_URLS = [
    "https://www.grabcraft.com/minecraft/gothic-medieval-church/churches#model3d",
    "https://www.grabcraft.com/minecraft/rustic-medieval-church/churches",
    "https://www.grabcraft.com/minecraft/tauren-longhouse/other-193",
]

# Load the block map
gts.load_block_map("data/blockmap.csv")

def batch_save(urls):
    for url in urls:
        get_and_save_slices(url)

def get_and_save_slices(url):
    schem = gts.url_to_render_object_data(url)
    print(f"Done downloading {url}\n")

    img, name, dims = gts.render_object_to_png_slice(schem, with_metadata=True)
    width, height, length = dims
    save_dir = name
    Path(save_dir).mkdir(parents=True, exist_ok=True)

    # check if directory is empty 
    if any(Path(save_dir).iterdir()):
        print(f"Directory {save_dir} is already populated, skipping...")
        return

    for i in range(length):
        # crop pil image (left, up, right, down)
        left_border, right_border = i * width, (i + 1) * width
        img.crop((left_border, 0, right_border, height)).save(f"{save_dir}/{name}_{i}.png")

for url in MODEL_URLS:
    get_and_save_slices(url)