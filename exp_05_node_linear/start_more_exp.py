import subprocess
import os

# Название папки с экспериментом
abs_path = os.path.abspath(__file__)
dir_path = os.path.dirname(abs_path)
HEADER = os.path.basename(dir_path)

variables = [
    {"name": "8" ,"node_linear": [-1, 8 ]},
    {"name": "16" ,"node_linear": [-1, 16 ]},
    {"name": "32" ,"node_linear": [-1,  32 ]},
    {"name": "64" ,"node_linear": [-1,  64 ]},

    {"name": "16_8" ,"node_linear": [-1, 16, 8 ]},
    {"name": "32_16" ,"node_linear": [-1, 32, 16 ]},
    {"name": "64_32" ,"node_linear": [-1, 64, 32 ]},
    {"name": "128_64" ,"node_linear": [-1, 128, 64 ]},

    {"name": "16_8_4" ,"node_linear": [-1, 16, 8, 4 ]},
    {"name": "32_16_8" ,"node_linear": [-1, 32, 16, 8 ]},
    {"name": "64_32_16" ,"node_linear": [-1, 64, 32, 16 ]},
    {"name": "128_64_32" ,"node_linear": [-1, 128, 64, 32 ]},
    
]


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
        linear = str(exp['node_linear'])
        with open(file_, 'w') as f:
            f.write(f"""
import sys, os
sys.path.append("..")
from exp_00_base import *

EXPERIMENT_PARAMS["NodeLinear"] = {linear}
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