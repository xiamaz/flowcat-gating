# Pregating for flowcat data

## Existing gating and clustering tools

* flowDensity
    * has been used in previous pipeline by [van Gassen et al.](https://onlinelibrary.wiley.com/doi/full/10.1002/cyto.a.22734)
* alternative gating strategies
    * [Review on gating of flow data](https://www.nature.com/articles/nri.2016.56)
        * does not include flowDensity in review
    * [Comparison of clustering methods](https://onlinelibrary.wiley.com/doi/full/10.1002/cyto.a.23030)
        * mainly focused on clustering instead of gating

### Chosen tools

We use flowDensity as it is a published tool for gating closely matching human
gating results.

## Analysis approach

* we assess performance on a smaller subset of training data for performance
  reasons
* compared pipelines are:
1. plain pipeline without preprocessing
2. flowDensity based gating

This will need to resave all FCS files in R.

Put filtered data into `data/samples`

```sh
# filter training dataset to extract 100 samples from each group
$ ./filter_samples.py
```

Gate data on CD45 SS and CD34 SS for B-lymphocyte gate vs ungated (eg load and
save data in R).

```sh
# gate and ungated data
$ Rscript ./gate_samples.R  # save samples to output/gated
$ Rscript ./gate_samples_nogating.R  # samples to output/ungated
```

When doing the analysis, we noted that sequential gating was highly error-prone
in fully-automatic mode, why we switched to using a single gating on SS-/CD45+.

TODO: Test a simple reference gating strategy.

### SOM Generation and Classification

SOM generation used the same standard parameters as outlined in the publication.
Classification was changed to keep the reduced number of samples in mind.
The model was trained for 150 epochs. The number was determined after testing on
a 100 per-group sample with values between 20-200 epochs.

We generate 5 randomized classification runs per dataset, in each iteration both
SOMs and classifications newly generated.

```
# generate SOMs and train classifiers
$ ./run_experiments.sh
```

### Results analysis

F1, accuracy and MCC values generated for all iterations are used to calculate
in a simple statistical significance test for both groups. A box-plot comparison
for each metric is used for visualization of results distribution.

```
# generate result analysis into output/analysis
$ ./result_analysis.py
```

# Reference gating

For speed, this has been only done in 1 replication initially.
