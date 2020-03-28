# pylint: skip-file
# flake8: noqa
from flowcat import utils, io_functions
from fcg_logging import create_logging_handlers, setup_logging


LOGPATH = utils.URLPath("logs/assess_quality_{utils.create_stamp()}.log")
LOGGER = setup_logging(LOGPATH, "assess_quality")

ungated_samples = list(utils.URLPath("output/ungated/data").glob("**/*.LMD"))
ungated_sample_count = len(ungated_samples)
gated_samples = list(utils.URLPath("output/gated_single/data").glob("**/*.LMD"))
gated_sample_count = len(gated_samples)

LOGGER.info("Gated/Ungated successful FCS count: %d/%d (%s %%)", gated_sample_count, ungated_sample_count, gated_sample_count / ungated_sample_count)

sample_dataset = io_functions.load_case_collection(utils.URLPath("output/samples"))

LOGGER.info(sample_dataset)

def foldername(path):
    return str(utils.URLPath(path.parent.name, path.name))

def ppp(v):
    LOGGER.info(v)
    return v

gated_samples_names = list(map(lambda p: foldername(p), gated_samples))
missing_paths = list(filter(lambda p: foldername(p) not in gated_samples_names, ungated_samples))
LOGGER.info("Missing paths: %s", missing_paths)

def has_path(case):
    sample_paths = list(map(lambda p: str(p.path), case.samples))
    return any(map(lambda p: foldername(p) in sample_paths, missing_paths))

associated_cases = list(filter(lambda c: has_path(c), sample_dataset))
LOGGER.info("Associated missing cases: %s", associated_cases)
for case in associated_cases:
    LOGGER.info("ID %s: infiltration %s", case.id, case.infiltration)
