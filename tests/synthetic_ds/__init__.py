import pickle
from collections import OrderedDict


def load_dataset(ds_name='60_13'):
    with open(ds_name + '.pkl', 'rb')as file:
        curr_dataset = pickle.load(file)
        sort_kes = []
        for key in curr_dataset:
            sort_kes.append(key)
        sort_kes.sort()
        data = OrderedDict()
        for key in sort_kes:
            data[key] = curr_dataset[key]
        return data
