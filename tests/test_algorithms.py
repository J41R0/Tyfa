import time
import json

import matplotlib.pyplot as plt

from tests.synthetic_ds import load_dataset
from tyfa import yyc
from tyfa import fastbr
from tyfa import gcreduct


def compare_algorithms(compare_time=False):
    dataset_name = "60_13"
    # dataset_name = "150_15"
    # dataset_name = "250_20"

    density_dataset = load_dataset(dataset_name)

    # define comparison parameter

    sufix = '_hits'
    if compare_time:
        sufix = '_time'
    output_dir = "tests/"
    paht_to_file = output_dir + dataset_name + sufix

    dims = []
    mean_gcreduct_cost = []
    mean_regsearch_cost = []
    mean_fastbr_cost = []
    mean_yyc_cost = []
    res_set = set()
    for density in density_dataset:
        dims.append(density)
        gcreduct_cost = []
        regsearch_cost = []
        fastbr_cost = []
        yyc_cost = []
        for curr_mb in density_dataset[density]:
            res_set.clear()
            start = time.time()
            # cmps, tt_list = RegularSearch.find_tt(curr_mb)
            cmps, tt_list = gcreduct.find_tt(curr_mb)
            end = time.time()
            res_set.add(len(tt_list))
            if compare_time:
                gcreduct_cost.append(end - start)
            else:
                gcreduct_cost.append(cmps)

            # start = time.time()
            # cmps, tt_list = RegularSearch.find_tt(curr_mb, sort='row')
            # end = time.time()
            # res_set.add(len(tt_list))
            # if compare_time:
            #     regsearch_cost.append(end - start)
            # else:
            #     regsearch_cost.append(cmps)

            start = time.time()
            # cmps, tt_list = RegularSearch.find_tt(curr_mb, sort='col')
            cmps, tt_list = fastbr.find_tt(curr_mb)
            end = time.time()
            res_set.add(len(tt_list))
            if compare_time:
                fastbr_cost.append(end - start)
            else:
                fastbr_cost.append(cmps)

            start = time.time()
            cmps, tt_list = yyc.find_tt(curr_mb)
            end = time.time()
            res_set.add(len(tt_list))
            if compare_time:
                yyc_cost.append(end - start)
            else:
                yyc_cost.append(cmps)

            if len(res_set) > 1:
                print(res_set)
                raise Exception("Non equal testor number")
        print(density)
        mean_gcreduct_cost.append(sum(gcreduct_cost) / len(gcreduct_cost))
        # mean_regsearch_cost.append(sum(regsearch_cost) / len(regsearch_cost))
        mean_fastbr_cost.append(sum(fastbr_cost) / len(fastbr_cost))
        mean_yyc_cost.append(sum(yyc_cost) / len(yyc_cost))

    results = {}
    results["FastBR"] = []
    results["GCreduct"] = []
    results["RegularSearch"] = []
    results["YYC"] = []
    for pos in range(len(dims)):
        results["FastBR"].append((dims[pos], mean_fastbr_cost[pos]))
        results["GCreduct"].append((dims[pos], mean_gcreduct_cost[pos]))
        # results["RegularSearch"].append((dims[pos], mean_regsearch_cost[pos]))
        results["YYC"].append((dims[pos], mean_yyc_cost[pos]))

    with open(paht_to_file + '.txt', 'w') as file:
        file.write(json.dumps(results, indent=2))

    plt.plot(dims, mean_fastbr_cost, 'bh-', label="FastBR")
    plt.plot(dims, mean_gcreduct_cost, 'rs-', label="GCreduct")
    # plt.plot(dims, mean_regsearch_cost, 'go-', label="RegularSearch")
    plt.plot(dims, mean_yyc_cost, 'yd-', label="YYC")

    y_label = 'Evaluated sets hits'
    if compare_time:
        y_label = 'Time in seconds'
    plt.ylabel(y_label)
    plt.xlabel("D(1)")
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=4)

    plt.savefig(paht_to_file + '.png')
    plt.close()
    print("END")
