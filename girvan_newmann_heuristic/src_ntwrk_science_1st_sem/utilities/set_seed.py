import os
import random
import numpy as np

def set_seed(seed):
    # Set random seed for reproducibility
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)

