#!/bin/bash

find . -name "__pycache__" -exec rm -r "{}" \;
rm -rf stage/ output/ perflogs/ reframe.log
