import torch
from  util.utils import *

def pool2d(tensor, type= 'max'):
    sz = tensor.size()
    if type == 'max':
        x = torch.nn.functional.max_pool2d(tensor, kernel_size=(int(sz[2]/8), sz[3]))
    if type == 'mean':
        x = torch.nn.functional.mean_pool2d(tensor, kernel_size=(int(sz[2]/8), sz[3]))
    x = x[0].cpu().data.numpy()
    x = np.transpose(x,(2,1,0))[0]
    return x   