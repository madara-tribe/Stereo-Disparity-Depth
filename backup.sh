#!/bin/sh
find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf
find . -name '.DS_Store' -type f -ls -delete
mkdir -p bp bp/qtWidgets bp/data/images bp/yolov7s
cp *.png *.onnx *.py *.sh bp/
cp qtWidgets/*.py bp/qtWidgets/
cp yolov7s/*.py bp/yolov7s/
cp data/images/* bp/data/images/

