import matplotlib
matplotlib.use("Agg")

from flowcat import io_functions, utils
from flowcat.plots import som as fc_somplot

LOGPATH = utils.URLPath("logs/visualize_datasets_{utils.create_stamp()}.log")

LOGGER = utils.logs.setup_logging(LOGPATH, "visualize_datasets")
OUTPUT = utils.URLPath("output/visualization/soms-ungated")

# OUTPUT.mkdir()
# 
# som_dataset = io_functions.load_case_collection(utils.URLPath("output/classifier_ungated/som"))
# 
# # testsample = som_dataset[0].samples[0]
# 
# for case in som_dataset.filter(groups=["CLL"]):
#     testsample = case.get_tube("1", kind="som")
#     LOGGER.info(testsample)
#     somdata = testsample.get_data()
#     fig = fc_somplot.plot_som_grid(somdata, channels=["SS INT LIN", "CD45-KrOr", None])
#     fig.savefig(str(OUTPUT / f"test_{case.id}.png"))

OUTPUT = utils.URLPath("output/visualization/soms-original")
som_dataset = io_functions.load_case_collection(utils.URLPath("/data/flowcat-data/paper-cytometry/som/train"), utils.URLPath("/data/flowcat-data/paper-cytometry/som/train.json.gz"))
OUTPUT.mkdir()
for case in som_dataset.filter(groups=["CLL"]):
    testsample = case.get_tube("1", kind="som")
    LOGGER.info(testsample)
    somdata = testsample.get_data()
    fig = fc_somplot.plot_som_grid(somdata, channels=["SS INT LIN", "CD45-KrOr", None])
    fig.savefig(str(OUTPUT / f"test_{case.id}.png"))
