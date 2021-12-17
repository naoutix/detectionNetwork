from pathlib import Path
import os
import subprocess

IMAGE_DIR = Path('animals/luc')
LABEL_DIR = Path('animals/luc/yolo_labels')
OUTPUT_DIR = Path('animals/luc/labelled_img')

labelled_img_list = [x.stem for x in LABEL_DIR.iterdir() if not x.is_dir()]

for img in IMAGE_DIR.iterdir():
    if not img.is_dir():
        if img.stem in labelled_img_list:
             
            status = subprocess.call(f'cp {img} {OUTPUT_DIR.joinpath(img.name)}', shell=True)