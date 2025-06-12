import csv
import tensorflow as tf
import time
import csv
from megnet.utils.models import load_model
from pymatgen.core import Structure, Lattice
model_name = '44w_data_model'

model = load_model(model_name)


def read_csv(file_path):
    data_list = []
    
    with open(file_path, "r", newline="") as csv_file:
        reader = csv.reader(csv_file)
        
        for row in reader:
            data_list.append(row)
    
    return data_list

def save_csv(path:str, head:list, data_list:list):
    
    
    with open(path, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        
        
        writer.writerow(head)
        
        
        writer.writerows(data_list)

    print(f"CSV文件已保存,{len(data_list)}条， 位置在", path)

def load_cif_to_str(cif_path):
    with open(cif_path, "r") as cif_file:
        cif_str = cif_file.read()
    return cif_str
import os
data = []
prediction_list = []
target_list = []

cif_dir = ''
run_name = ''

cif_file_paths = [os.path.join(cif_dir, name) for name in os.listdir(cif_dir) ]
cif_name_list = []

t1 = time.time()
for idx, path in enumerate (cif_file_paths):
    
    try:
        cif_name = path.split('/')[-1]
        if 'cif' in path:
            cif_str = load_cif_to_str(path)
            
            structure = Structure.from_str(cif_str, fmt='cif')
        else:
            structure = Structure.from_file(path)
        
       
        if model_name.startswith("log"):
            prediction = 10 ** model.predict_structure(structure).ravel()[0]
        else:
            prediction = model.predict_structure(structure).ravel()[0]
        
        cif_name_list.append(cif_name)
        prediction_list.append( prediction )
        data.append([cif_name,prediction])
        
        t2 = time.time()
        print(idx, f'using time: {(t2-t1)/60:.3f} min', f' finsh target need {(10*10**4-idx)*(t2-t1)/((idx+1)*60):.3f} min')
    except Exception as e:
        print(e)


save_csv(path=f'./{run_name}_{model_name}.csv', head=['file_name','formation_energy'], data_list=data)
