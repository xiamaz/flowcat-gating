"""
Train a flowcat classifier including SOMs for the given dataset.

Use the dataset that has been gated a single time on SS INT LIN and CD45 Kr-Or
"""
import sys
from flowcat import io_functions, utils, flowcat, constants
from flowcat.seed import set_seed

IDENTIFIER = sys.argv[1]
NAME = f"classifier_gated_single_{IDENTIFIER}"

def check_dataset(dataset: "CaseCollection"):
    """Check that cases can be loaded."""
    LOGGER.info(dataset)
    case = dataset[0]
    LOGGER.info(case)
    sample = case.get_tube("1")
    LOGGER.info("Tube 1 %s", sample)
    data = sample.get_data()
    LOGGER.info(data)
    LOGGER.info(f"{data.data.shape}, {data.data.min(axis=1)}, {data.data.max(axis=1)}")

def filter_missing_files(dataset: "CaseCollection") -> "CaseCollection":
    LOGGER.info("Before filtering: %s", dataset)

    def all_samples_exist(case: "Case") -> bool:
        return all(s.complete_path.exists() for s in case.samples)

    filtered = dataset.copy()
    filtered.cases = [
        case for case in filtered.cases if all_samples_exist(case)
    ]
    filtered.data_path = dataset.data_path
    LOGGER.info("After filtering only existing: %s", filtered)
    return filtered

SEED = None
OUTPUT = utils.URLPath(f"output/{NAME}")
LOGDIR = utils.URLPath(f"logs/{NAME}_{utils.create_stamp()}")
INPUT = {
    "data": utils.URLPath("output/gated_single/data"),
    "meta": utils.URLPath("output/samples/meta.json.gz"),
}

LOGGER = utils.setup_logging(LOGDIR, NAME)

set_seed(SEED)
dataset = io_functions.load_case_collection(INPUT["data"], INPUT["meta"])

check_dataset(dataset)

# remove all cases without filtered fcs
filtered_dataset = filter_missing_files(dataset)

train, test = filtered_dataset.create_split(0.9)
io_functions.save_json(train.labels, OUTPUT / "train_ids.json")
io_functions.save_json(test.labels, OUTPUT / "test_ids.json")

reference = train.sample(1)
LOGGER.info("Reference dataset: %s", reference)
LOGGER.info("Reference labels: %s", reference.labels)

model = flowcat.FlowCat()
args = constants.DEFAULT_TRAIN_ARGS
args["classifier"]["balance"] = None
args["classifier"]["split_ratio"] = 1.0
args["classifier"]["config"].tubes = ["1", "2"]
args["classifier"]["config"].train_epochs = 150
som_train, som_test = model.train(train, reference, OUTPUT, args=args, validation_data=test)
predictions = model.predict_dataset(som_test)
preds = model.predictions_to_metric(predictions, OUTPUT / "preds")
