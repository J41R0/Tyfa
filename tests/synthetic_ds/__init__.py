import os
import pickle
from collections import OrderedDict


def load_dataset(ds_name='60_13'):
    my_dataset = ''
    if os.path.exists(ds_name + '.pkl'):
        my_dataset = ds_name + '.pkl'
    if os.path.exists('synthetic_ds/' + ds_name + '.pkl'):
        my_dataset = 'synthetic_ds/' + ds_name + '.pkl'
    if os.path.exists('tests/synthetic_ds/' + ds_name + '.pkl'):
        my_dataset = 'tests/synthetic_ds/' + ds_name + '.pkl'
    if my_dataset == '':
        raise Exception('Cannot find dataset')
    with open(my_dataset, 'rb')as file:
        curr_dataset = pickle.load(file)
        sort_kes = []
        for key in curr_dataset:
            sort_kes.append(key)
        sort_kes.sort()
        data = OrderedDict()
        for key in sort_kes:
            data[key] = curr_dataset[key]
        return data
