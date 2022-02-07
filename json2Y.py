import json
import os
from pathlib import Path
import numpy as np
from PIL import Image


def convert(file, path_anno_yolo):
    
    # load JSON
    with open(file) as f:
        data = json.load(f)  
        
        
    # json to yolo (x1,x2,y1,y2 -> xc,yx,w,h)
    nb_detection = len(data)
    liste_txt = np.zeros((nb_detection,5))
    for i in range(nb_detection):
        data_i = data[i]
        label = data_i["label"]
        x1 = data_i["xmin"]
        x2 = data_i["xmax"]
        y1 = data_i["ymin"]
        y2 = data_i["ymax"]
        liste_txt[i][1] = (x1 + x2) / 2
        liste_txt[i][2] = (y1 + y2) / 2
        liste_txt[i][3] = (x2 - x1)
        liste_txt[i][4] = (y2 - y1)
        
        if label=="Chat":
            label = 0
        elif label=="Chimpanzé":
            label=1
        elif label=="Coyote":
            label=2
        elif label=="Hamster" or label=="Cochon d'Inde":
            label=3
        elif label=="Guépard" or label=="Jaguar":
            label=4
        elif label=="Loup":
            label=5
        elif label=="Lynx":
            label=6
        else:
            label=7
        
        with open(path_anno_yolo, 'a') as f2:
            coordonnees = f'{label} {liste_txt[i][1]} {liste_txt[i][2]} {liste_txt[i][3]} {liste_txt[i][4]}'
            f2.write(str(coordonnees)+"\n")
        
    
    
    f2.close()
    f.close()

annotations = os.listdir("donnees_tests/anno_json/")
for anno in annotations:  
     anno_json = os.path.join("donnees_tests/anno_json/",anno)
     anno_yolo = os.path.splitext(anno)
     anno_yolo = anno_yolo[0]
     anno_yolo = anno_yolo + ".txt"
     anno_yolo = os.path.join("donnees_tests/anno_yolo/",anno_yolo)
     convert(anno_json, anno_yolo)