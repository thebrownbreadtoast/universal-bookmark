#!/bin/bash

if [ $(uname) == "Darwin" ]; then
    NUM_CPU=`sysctl -n hw.physicalcpu`
else
    NUM_CPU=`nproc`
fi

NUM_WORKERS=$(( 2 * NUM_CPU + 1))

uvicorn src.main:app --host 0.0.0.0 --port 4444 --workers $NUM_WORKERS --reload
