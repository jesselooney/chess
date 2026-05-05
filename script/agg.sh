#!/bin/bash

for f in results/matchups-tenfold/slurm-*/run.out; do
    grep "white=" "$f"
done | tee data/results.dkvp

