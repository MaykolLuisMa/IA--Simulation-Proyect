import numpy as np
def normal_variation(value : float, variation = 0.03):
    return np.random.normal(value, value*variation, None)

def random_up(value : int, porcent = 0.05):
    high = int(value * (1 + porcent))
    return np.random.randint(value,high)

def random_down(value : int, porcent = 0.05):
    low = int(value * (1 - porcent))
    low = max(0,low)
    return np.random.randint(low,value)