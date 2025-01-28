import grabcraft_to_schema as gts
import blockmodel_avg_mapper as bam
import json
import PIL
from PIL import Image
import numpy as np

# Load the block map
gts.load_block_map("data/blockmap.csv")

# A demo link that you can try to use:
# "https://www.grabcraft.com/minecraft/gothic-medieval-church/churches#model3d"
schem = gts.url_to_render_object_data(input("Enter the link to the build: "))
print("Done downloading!\n")

match input("Would you like to save it as\n\t(1) A litematica schematic\n\t(2) RenderObject json\n\t(3) PNG slice\n\t(4) Multiple PNG slices\n"):
    case "1": # Litematica
        schem = gts.render_object_to_schema(schem)
        # Save the schem as litematica
        schem.save(f"{ input('Enter what you want to name the litematic: ') }.litematic")
    case "2": # RenderObject
        # Save the schem as render object json
        with open(f"{ input('Enter what you want to name the Render Object: ') }.json", 'w') as f:
            f.write(json.dumps(schem.__dict__))
    case "3": # PNG slice
        gts.render_object_to_png_slice(schem).save(f"{ input('Enter what you want to name the png slice: ') }.png")
    case "4": # Multiple PNG slices
        img, name, dims = gts.render_object_to_png_slice(schem, with_metadata=True)
        width, height, length = dims
        for i in range(length):
            # crop pil image (left, up, right, down)
            left_border, right_border = i * width, (i + 1) * width
            img.crop((left_border, 0, right_border, height)).save(f"{name}_{i}.png")
    case _:
        print("That's an invalid option!")