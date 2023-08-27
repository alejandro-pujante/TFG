#!/bin/bash

cd meshes/2D/
python3 data_preprocessing.py
cd ../../

for i in $(seq 1 $1)

do
    sfepy-run problem-descriptions/2D/main.py > bin.log

    cd outputs/test
    python3 data_processing.py

    cd ../../

    echo 'La simulación' $i 'ha finalizado'
done

cd outputs/test

python3 results.py

rm q_values.csv

rm error_values.csv

echo 'Todas las simulaciones han finalizado'