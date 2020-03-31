#!/bin/sh
# Repeat experiments multiple times to calculate average
# IMPORTANT: Check that seed is not set in scripts before using this script.

# Also make sure that the datasets sample, gated_single and ungated exist
# beforehand. The sampling and gating are not included in the random repeat
# testing.

ITERATIONS=5

run_iterations() {
	for i in $(seq 1 $ITERATIONS); do
		echo "Running iteration $i"
		$1 $i
	done
}

run_iterations "python3 ./train_classifier_ungated.py"
# run_iterations "python3 ./train_classifier_gated_single.py"
run_iterations "python3 ./train_classifier_gated_removeedge.py"
