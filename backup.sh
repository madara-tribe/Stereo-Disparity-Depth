#!/bin/sh
find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf
find . -name '.DS_Store' -type f -ls -delete
mkdir -p bp/data/left bp/data/right 
mkdir -p bp/yolov7s
mkdir -p bp/qtWidgets/img bp/qtWidgets/vid
cp *.onnx *.py *.sh *.yaml bp/
cp -r qtWidgets/img/*.py bp/qtWidgets/img/
cp -r qtWidgets/vid/*.py bp/qtWidgets/vid/
cp yolov7s/*.py bp/yolov7s/
cp -r data/left/image_050.png bp/data/left/
cp -r data/right/image_050.png bp/data/right/
