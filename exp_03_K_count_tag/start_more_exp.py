import subprocess
import os

# Название папки с экспериментом
abs_path = os.path.abspath(__file__)
dir_path = os.path.dirname(abs_path)
HEADER = os.path.basename(dir_path)

neural1 = 64
neural2 = 8
variables = [
    [{"name": f"k{k}t1",  "tags": [
        { "in": -1, "size": neural1, "out": neural2, "k":k}
    ]},
    {"name": f"k{k}t2",  "tags": [
        { "in": -1, "size": neural1, "out": neural1, "k":k},
        { "in": neural1, "size": neural1, "out": neural2, "k":k}
    ]},
    {"name": f"k{k}t3",  "tags": [
        { "in": -1, "size": neural1, "out": neural1, "k":k},
        { "in": neural1, "size": neural1, "out": neural1, "k":k},
        { "in": neural1, "size": neural1, "out": neural2, "k":k}
    ]},
    {"name": f"k{k}t4",  "tags": [
        { "in": -1, "size": neural1, "out": neural1, "k":k},
        { "in": neural1, "size": neural1, "out": neural1, "k":k},
        { "in": neural1, "size": neural1, "out": neural1, "k":k},
        { "in": neural1, "size": neural1, "out": neural2, "k":k}
    ]}] for k in [1, 2, 3, 4, 5]
]
variables = [e for row in variables for e in row]


count_char_in_code = len(str(len(variables))) + 1
name_exps = lambda i : f"{str(i).zfill(count_char_in_code)}_{variables[i]['name']}"
list_num_exp =  [i for i in range(len(variables))]


def created_exps():
    for i in list_num_exp:
        dir_ = os.path.join(HEADER, name_exps(i))
        if os.path.exists(dir_):
            continue
        os.mkdir(dir_)
        file_ = os.path.join(dir_, "__init__.py")
        exp = variables[i]
        tags = ',\n'.join([str(e) for e in exp['tags']])
        with open(file_, 'w') as f:
            f.write(f"""
import sys, os
sys.path.append("..")
from exp_00_base import *

EXPERIMENT_PARAMS["Tag"] = [{tags}]
"""
)
def start_new_exp(name, header=HEADER):
    with open ('.env', 'r') as f:
        old_data = f.read()
    new_data = "\n".join([f'EXPERIMENT="{header}/{name}"']+old_data.split("\n")[1:])
    with open ('.env', 'w') as f:
        f.write(new_data)
    

    subprocess.run(["python", "script_train.py"])
    subprocess.run(["python", "script_test.py"])


    
if __name__ == "__main__":
    created_exps()
    for i in list_num_exp:
        dir_ = os.path.join(HEADER, name_exps(i))
        if not os.path.exists(os.path.join(dir_, 'log.txt')):
            start_new_exp(name_exps(i))