import lib.grabcraft_to_schema as gts
import lib.blockmodel_avg_mapper as bam
import json
import PIL
from PIL import Image
import numpy as np
from pathlib import Path
import argparse
import hashlib

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

def hash_str(s):
    return str(hashlib.md5(s.encode()).hexdigest())

def get_and_save_slices(url, save_dir):
    schem = gts.url_to_render_object_data(url)
    url_hash = hash_str(url)[1:5] # to avoid name collisions
    print(f"Done downloading {url}\n")

    img, name, dims = gts.render_object_to_png_slice(schem, with_metadata=True)
    name = name.replace(" ", "_")
    width, height, length = dims
    save_dir = save_dir + "/" + name + "_" + url_hash
    Path(save_dir).mkdir(parents=True, exist_ok=True)

    # check if directory is empty 
    if any(Path(save_dir).iterdir()):
        print(f"Directory {save_dir} is already populated, skipping...")
        return

    for i in range(length):
        # crop pil image (left, up, right, down)
        left_border, right_border = i * width, (i + 1) * width
        img.crop((left_border, 0, right_border, height)).save(f"{save_dir}/{name}_{i}.png")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog='Downloader for Grabcraft',
                    description='Creates PNG slices from Grabcraft models',
                    epilog='Text at the bottom of help')
    parser.add_argument('-u', '--urls', help='file with urls of the Grabcraft models', required=True)
    parser.add_argument('-d', '--dir', help='directory to store the data', default='dataset')
    args = parser.parse_args()

    if not Path(args.dir).exists():
        Path(args.dir).mkdir(parents=True, exist_ok=True)

    with open(args.urls, 'r') as f:
        urls = f.readlines()
        for url in urls:
            get_and_save_slices(url.strip(), args.dir)
