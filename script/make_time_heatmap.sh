#!/bin/bash

mlr --d2c --from=data/processed.dkvp put '$time_ratio = $white_clock / $black_clock' then stats1 -a mean -g white,black -f time_ratio > data/heatmap_time_ratio_mean.csv

