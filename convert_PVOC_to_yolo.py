import glob
import os
import pickle
import xml.etree.ElementTree as ET
from os import listdir, getcwd
from os.path import join

classes = ['hamster', 'loup', 'leopard', 'chat', 'lynx', 'chimpanze', 'cerf',
'orang outan', 'coyote', 'chien', 'renard', 'souris', 'oiseau', 'tigre', 'lapin',
'lion']

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

def convert_annotation(dir_path, output_path, image_path):
    basename = os.path.basename(image_path)
    basename_no_ext = os.path.splitext(basename)[0]

    in_file = open(dir_path + '/' + basename_no_ext + '.xml')
    out_file = open(output_path + basename_no_ext + '.txt', 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):

        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

FichList = [ f for f in os.listdir('/Users/alicepigneux/Desktop/Cours_3A/IA/labelled_PASCAL_VOC/') if not os.path.basename(f).startswith('.')]
for Fich in FichList:
    # print('/Users/alicepigneux/Desktop/Cours_3A/IA/labelled_PASCAL_VOC/'+Fich)
    convert_annotation('/Users/alicepigneux/Desktop/Cours_3A/IA/labelled_PASCAL_VOC/', '/Users/alicepigneux/Desktop/Cours_3A/IA/labelled_YOLO/', '/Users/alicepigneux/Desktop/Cours_3A/IA/labelled_PASCAL_VOC/'+Fich)