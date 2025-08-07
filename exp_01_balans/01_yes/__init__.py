
import sys, os
sys.path.append("..")
from exp_00_base import *

EXPERIMENT_PARAMS["loss_params"]["publaynet_imbalance"] = [1.57, 0.03, 0.81, 2.39, 0.18]
EXPERIMENT_PARAMS["loss_params"]["edge_imbalance"] =  0.41
