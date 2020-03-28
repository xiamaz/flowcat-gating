"""
Generate plots based on randomized experiments.
"""
from dataclasses import dataclass
import pandas as pd
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt

import seaborn as sns
import scipy.stats as sst

from flowcat import utils, io_functions

NAME = "result_analysis"

RESULTS = {
    "path": utils.URLPath("output"),
    "names": ["classifier_ungated", "classifier_gated_single"],
}

OUTPUT = utils.URLPath(f"output/{NAME}")

LOGGER = utils.setup_logging(utils.URLPath(f"logs/{NAME}_{utils.create_stamp()}"), NAME)

def get_result_dirs(path: utils.URLPath, names: list):
    """Get result directories for individual iterations from given path and names"""
    result_dirs = {
        name: Metrics(list(map(Result, path.glob(f"./{name}*")))) for name in names
    }
    return result_dirs


@dataclass
class Result:
    path: utils.URLPath

    @property
    def json_results(self):
        print(self.path)
        return io_functions.load_json(self.path / "preds" / "validation_metrics.json")

    @property
    def confusion_matrix(self):
        return pd.read_csv(str(self.path / "preds" / "validation_confusion.csv"))


class Metrics:

    def __init__(self, data):
        self.data = data
        self.metrics = [d.json_results for d in self.data]

    @property
    def dataframe(self):
        data = pd.DataFrame(self.metrics)
        return data

OUTPUT.mkdir()

result_dirs = get_result_dirs(**RESULTS)
LOGGER.info(result_dirs["classifier_ungated"].metrics)
LOGGER.info(result_dirs["classifier_gated_single"].metrics)

ungated = result_dirs["classifier_ungated"].dataframe.stack().reset_index()
ungated["gated"] = "no"
gated = result_dirs["classifier_gated_single"].dataframe.stack().reset_index()
gated["gated"] = "yes"

data = pd.concat([ungated, gated]).drop("level_0", axis=1).reset_index(drop=True)
data.columns = ["Type", "Score", "Gated"]
LOGGER.info(data)

sns.set(style="whitegrid")
ax = sns.boxplot(x="Type", y="Score", hue="Gated",
                 data=data, linewidth=2.5)
plt.savefig(str(OUTPUT / "boxplot.png"))

for stat_type in ("f1_avg", "f1_weighted", "balanced", "mcc"):
    stat_type = "f1_avg"
    stat_data = data.loc[data["Type"] == stat_type, :]
    ungated_data = stat_data.loc[data["Gated"] == "no", "Score"]
    gated_data = stat_data.loc[data["Gated"] == "yes", "Score"]
    LOGGER.info("Ungated: %s", ungated_data)
    LOGGER.info("Gated: %s", gated_data)
    res = sst.ttest_rel(ungated_data, gated_data)
    LOGGER.info("paired t-Test (ungated vs gated) on %s: %s", stat_type, res)
