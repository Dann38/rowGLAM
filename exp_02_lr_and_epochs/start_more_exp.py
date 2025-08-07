import subprocess
import os

# Название папки с экспериментом
abs_path = os.path.abspath(__file__)
dir_path = os.path.dirname(abs_path)
HEADER = os.path.basename(dir_path)

variables = [
    {"name": "lr05_ep20", "learning_rate": 0.5, "epochs": 20},
    {"name": "lr01_ep20", "learning_rate": 0.1, "epochs": 20},
    {"name": "lr005_ep20", "learning_rate": 0.05, "epochs": 20},
    {"name": "lr001_ep20", "learning_rate": 0.01, "epochs": 20},
    {"name": "lr0005_ep30", "learning_rate": 0.005, "epochs": 30},
    {"name": "lr0001_ep30", "learning_rate": 0.001, "epochs": 30},
    {"name": "lr00005_ep50", "learning_rate": 0.0005, "epochs": 50},
    {"name": "lr00001_ep50", "learning_rate": 0.0001, "epochs": 50},
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
        with open(file_, 'w') as f:
            f.write(f"""
import sys, os
sys.path.append("..")
from exp_00_base import *

EXPERIMENT_PARAMS["learning_rate"] = {exp['learning_rate']}
EXPERIMENT_PARAMS["epochs"] =  {exp['epochs']}
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