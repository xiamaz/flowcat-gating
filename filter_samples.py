#!/usr/bin/env python3
# pylint: skip-file
# flake8: noqa
"""
This script will use the training dataset to subsample a 100 samples and put
them into the output directory.
Logs generated in the process will be saved to filter_samples_date.log
"""
import logging
from flowcat import io_functions, utils, seed as fc_seed


def create_logging_handlers(logging_path):
    """Create logging to both file and stderr."""
    return [
        utils.logs.create_handler(logging.FileHandler(str(logging_path))),
        utils.logs.create_handler(utils.logs.print_stream()),
    ]


def setup_logging(logging_path, name):
    logging_path.parent.mkdir()

    logger = logging.getLogger(name)
    handlers = create_logging_handlers(logging_path)
    utils.logs.add_logger(logger, handlers)
    return logger


INPUT = {
    "data": utils.URLPath("/data/flowcat-data/mll-flowdata/decCLL-9F"),
    "meta": utils.URLPath("/data/flowcat-data/mll-flowdata/decCLL-9F.2019-10-29.meta/train.json.gz"),
}

OUTPUT = utils.URLPath("output/samples")

LOGPATH = utils.URLPath(f"logs/filter_samples_{utils.create_stamp()}.log")

LOGGER = setup_logging(LOGPATH, "filter_samples")

fc_seed.set_seed(42)
OUTPUT.mkdir()
train_dataset = io_functions.load_case_collection(INPUT["data"], INPUT["meta"])
LOGGER.log(logging.DEBUG, train_dataset)


FILTER_COUNT = 100
LOGGER.info("Sampling %d samples from each group in dataset", FILTER_COUNT)
filtered_dataset = train_dataset.sample(FILTER_COUNT)

LOGGER.info("Saving filtered samples to %s", OUTPUT)
io_functions.save_case_collection_with_data(filtered_dataset, OUTPUT)
LOGGER.info("Filtered ids are: %s", filtered_dataset.labels)
