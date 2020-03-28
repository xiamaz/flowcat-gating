from collections import defaultdict
from flowcat import io_functions, utils, seed as fc_seed

INPUT = {
    "data": utils.URLPath("/data/flowcat-data/mll-flowdata/decCLL-9F"),
    "meta": utils.URLPath("/data/flowcat-data/mll-flowdata/decCLL-9F.2019-10-29.meta/train.json.gz"),
    "meta_test": utils.URLPath("/data/flowcat-data/mll-flowdata/decCLL-9F.2019-10-29.meta/test.json.gz"),
}

train_dataset = io_functions.load_case_collection(INPUT["data"], INPUT["meta_test"])
sorted_cases = sorted(train_dataset, key=lambda c: c.infiltration if c.infiltration > 0.0 else 1000)

perc01_count = 0
group_count = defaultdict(int)
for case in sorted_cases[:100]:
    print("Minimal infiltration sample:", case, case.infiltration)
    if case.infiltration == 0.1:
        perc01_count += 1
        group_count[case.group] += 1

print(perc01_count)
print(group_count)
