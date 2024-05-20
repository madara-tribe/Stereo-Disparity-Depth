#!/bin/sh
find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf
find . -name '.DS_Store' -type f -ls -delete
mkdir -p bp bp/qtWidgets bp/data/images bp/yolov7s data
mkdir -p bp/qtWidgets/img bp/qtWidgets/vid
cp *.onnx *.py *.sh bp/
cp -r qtWidgets/img/*.py bp/qtWidgets/img/
cp -r qtWidgets/vid/*.py bp/qtWidgets/vid/
cp yolov7s/*.py bp/yolov7s/
cp -r data/left bp/data/
cp -r data/right bp/data/
