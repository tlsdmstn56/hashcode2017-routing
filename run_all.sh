#!/bin/bash
inputs=( me_at_the_zoo trending_today videos_worth_spreading kittens )
for file in "${inputs[@]}"; do
echo "Running $file"
./run.sh $file
done
