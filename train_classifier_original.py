"""
Train a flowcat classifier including SOMs for the given dataset.

USE the original data from paper-cytometry, since we are hunting a bug in classification.
"""
from flowcat import io_functions, utils, flowcat, constants
from flowcat.seed import set_seed

SEED = 42
OUTPUT = utils.URLPath("output/classifier_original")
LOGDIR = utils.URLPath(f"logs/train_classifier_original_{utils.create_stamp()}")

LOGGER = utils.setup_logging(LOGDIR, "train_classifier_original")

set_seed(SEED)

dataset = io_functions.load_case_collection(
    utils.URLPath("/data/flowcat-data/paper-cytometry/som/train"),
    utils.URLPath("/data/flowcat-data/paper-cytometry/som/train.json.gz")
)

dataset = dataset.sample(100)
reference = io_functions.load_casesom(utils.URLPath("/data/flowcat-data/paper-cytometry/reference"), **constants.DEFAULT_TRANSFORM_SOM_ARGS)


# train, test = dataset.create_split(0.9)
# print(train.group_count)
# print(test.group_count)
# io_functions.save_json(train.labels, OUTPUT / "train_ids.json")
# io_functions.save_json(test.labels, OUTPUT / "test_ids.json")

model = flowcat.FlowCat(reference=reference)
args = constants.DEFAULT_TRAIN_ARGS
args["classifier"]["balance"] = None
args["classifier"]["split_ratio"] = 0.9
args["classifier"]["config"].tubes = ["1", "2"]
args["classifier"]["config"].train_epochs = 100
test = model._train_classifier(dataset, args["classifier"])
print(len(test))

predictions = model.predict_dataset(test)
preds = model.predictions_to_metric(predictions, OUTPUT / "preds")
