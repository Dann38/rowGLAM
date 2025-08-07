import subprocess

def start_new_exp(name):
    subprocess.run(["python", f"{name}/start_more_exp.py"])

# start_new_exp("exp_00_base")
start_new_exp("exp_01_balans")
start_new_exp("exp_02_lr_and_epochs")
start_new_exp("exp_03_K_count_tag")
start_new_exp("exp_04_neural_size")
start_new_exp("exp_05_node_linear")