import os
import random
import csv
import argparse
from pymatgen.core.structure import Structure
from pymatgen.io.cif import CifWriter
import copy
import math

def save_csv(path: str, head: list, data_list: list):
    # Create CSV file and write data
    with open(path, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        # Write header
        writer.writerow(head)
        # Write data
        writer.writerows(data_list)
    print(f"CSV file saved, {len(data_list)} rows, located at {path}")

def read_csv(file_path):
    data_list = []
    with open(file_path, "r", newline="") as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            data_list.append(row)
    return data_list

def main(cif_dir, dataset_name):
    idx = 0
    head = ',Unnamed: 0,material_id,formation_energy_per_atom,band_gap,pretty_formula,e_above_hull,elements,cif,spacegroup.number,spacegroup.number.conv,cif.conv'.split(',')
    data_list = []

    cif_names = os.listdir(cif_dir)

    for name in cif_names:
        try:
            cif_path = os.path.join(cif_dir, name)
            cif_id = name
            crystal = Structure.from_file(cif_path)
            atom_types = crystal.atomic_numbers

            cif_writer = CifWriter(crystal)
            cif_string = str(cif_writer)

            random_number = random.random()
            formation_energy_per_atom = 0
            line = [idx, 
                    random_number, 
                    cif_id, 
                    0,
                    0, 
                    crystal.composition.reduced_formula, 
                    0, 
                    f"{[str(e) for e in crystal.elements]}",
                    cif_string,
                    0,
                    0,
                    cif_string]

            data_list.append(line)
            idx += 1
        except Exception as e:
            print(f"Error processing {name}: {e}")

    test_data = []
    val_data = []
    train_data = []
    for i in range(1):
        test_data += data_list[:1000]
        val_data += data_list[:1000]
    if len(data_list) <= 10000:
        repeat_times = math.ceil( 10000 / len(data_list) )
    else:
        repeat_times = 1
    for i in range(repeat_times):
        train_data += data_list

    output_dir = os.path.join(os.getcwd(), 'data', dataset_name)
    os.makedirs(output_dir, exist_ok=True)

    test_csv = os.path.join(output_dir, 'test.csv')
    valid_csv = os.path.join(output_dir, 'val.csv')
    train_csv = os.path.join(output_dir, 'train.csv')
    data_csv = os.path.join(output_dir, 'data_materials.csv')

    random.shuffle(test_data)
    random.shuffle(val_data)
    random.shuffle(train_data)

    def set_idx(data_list):
        new_data = []
        for idx, data in enumerate(data_list):
            data[0] = idx
            new_data.append(copy.deepcopy(data))
        return new_data

    save_csv(path=data_csv, head=head, data_list=set_idx(data_list))
    save_csv(path=test_csv, head=head, data_list=set_idx(test_data))
    save_csv(path=valid_csv, head=head, data_list=set_idx(val_data))
    save_csv(path=train_csv, head=head, data_list=set_idx(train_data))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process CIF files and generate CSV datasets.")
    parser.add_argument("--cif_dir", type=str, help="Directory containing CIF files")
    parser.add_argument("--dataset_name", type=str, help="Name of the dataset")

    args = parser.parse_args()

    main(args.cif_dir, args.dataset_name)