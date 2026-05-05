#!/bin/bash

for f in results-addendum/addendum/slurm-*/run.out; do
    grep "white=" "$f"
done | tee -a data/results.dkvp

