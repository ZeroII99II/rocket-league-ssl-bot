@echo off
setlocal

REM Activate venv
call .venv\Scripts\activate

REM Use fewer threads if CPU is choking
set OMP_NUM_THREADS=4
set KMP_DUPLICATE_LIB_OK=TRUE

python train_v2.py