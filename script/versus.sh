#!/bin/bash

cd /home/jlooney27/chess
source .venv/bin/activate
python -m chess_engine.versus "$1" "$2"

