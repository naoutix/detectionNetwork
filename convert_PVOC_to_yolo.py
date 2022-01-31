import glob
import os
import pickle
import xml.etree.ElementTree as ET
from os import listdir, getcwd
from os.path import join
from pathlib import Path 

classes = ['hamster', 'loup', 'leopard', 'chat', 'lynx', 'chimpanze',
'orang outan', 'coyote']

INPUT_DIR = Path('donnees_annotees/labelled_PASCAL_VOC')
OUTPUT_DIR = Path('donnees_annotees/labelled_YOLO_2')

def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(label_file: Path, output_path: Path):
    print(label_file)
    in_file = open(label_file)
    out_file = open(output_path.joinpath(label_file.stem + '.txt'), 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):

        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls.startswith("orang"):
            cls = "orang outan"
            
        if cls.startswith("cochon"):
            cls = 'hamster'
        
            
        if cls not in classes or int(difficult)==1:
            print(f"{cls} not found ({label_file})")
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

for x in INPUT_DIR.iterdir() :
    if not x.is_dir():
        # print(INPUT_DIR+Fich)
        convert_annotation(x, OUTPUT_DIR)