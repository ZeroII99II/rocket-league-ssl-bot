#!/bin/bash

# Activate virtual environment
source .venv/bin/activate

# Set environment variables for better performance
export OMP_NUM_THREADS=4
export KMP_DUPLICATE_LIB_OK=TRUE

# Run training
python train_v2.py