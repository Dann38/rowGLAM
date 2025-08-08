import re
import matplotlib.pyplot as plt
import os

def extract_metrics_from_file(file_content):
    """
    Извлекает метрики F1 (IoU=0.50 и IoU=0.95), mAP и время из текста файла.
    
    Args:
        file_content (str): Содержимое файла с метриками.
    
    Returns:
        dict: Словарь с извлеченными метриками.
            {
                "F1_0.50": float,
                "F1_0.95": float,
                "mAP": float,
                "time": float
            }
    """
    metrics = {
        "F1_0.50": None,
        "F1_0.95": None,
        "mAP": None,
        "time": None
    }
    
    # Извлекаем F1 (IoU=0.50)
    f1_50_match = re.search(r"F1 \(IoU=0\.50\):\s+([0-9.]+)", file_content)
    if f1_50_match:
        metrics["F1_0.50"] = float(f1_50_match.group(1))
    
    # Извлекаем F1 (IoU=0.95)
    f1_95_match = re.search(r"F1 \(IoU=0\.95\):\s+([0-9.]+)", file_content)
    if f1_95_match:
        metrics["F1_0.95"] = float(f1_95_match.group(1))
    
    # Извлекаем mAP
    map_match = re.search(r"mAP@IoU\[0\.50:0\.95\]\s*=\s*([0-9.]+)", file_content)
    if map_match:
        metrics["mAP"] = float(map_match.group(1))
    
    # Извлекаем время
    time_match = re.search(r"mean time:\s+([0-9.]+)\s*sec", file_content)
    if time_match:
        metrics["time"] = float(time_match.group(1))
    
    return metrics

def read_res_test(header, name):
    with open(os.path.join(header, name, 'test_result.txt')) as f:
         return extract_metrics_from_file(f.read())


def print_exp(dir_):
    print("="*50+ "\n"+dir_ + '\n'+"*"*50)
    print("exp \t\t F1_0.50 \t F1_0.95 \t mAP")
    exps = [exp for exp in os.listdir(dir_) if os.path.isdir(os.path.join(dir_, exp))]
    exps.sort()
    for exp in exps:
        try:
            name = [" " for i in range(15)]
            for i, s in enumerate(exp):
                if i > 14:
                    break
                name[i] = s

            name = ''.join(name)
            print(name, end='\t')
            r = read_res_test(dir_, exp)
            print(f'{r['F1_0.50']}\t{r['F1_0.95'] }\t{r['mAP']}')
        except:
            print()
    print()

print_exp('exp_01_balans')
print_exp('exp_02_lr_and_epochs')
print_exp('exp_03_K_count_tag')
print_exp('exp_04_neural_size')
print_exp('exp_05_node_linear')
print_exp('exp_06_batch_epochs')
print_exp('exp_07_edge_linear')
print_exp('exp_08_loss')
print_exp('exp_09_linear_cl')