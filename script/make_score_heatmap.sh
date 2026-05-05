#!/bin/bash

mlr --d2c --from=data/processed.dkvp stats1 -a mean -g white,black -f score > data/heatmap_score_mean.csv

