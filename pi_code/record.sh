#!/bin/bash

# Clear old data before recording new data
sudo rm ~/Documents/sdc/data/*.png

# Run car in "record" mode
cd src-record
node record.js & python3 record.py
