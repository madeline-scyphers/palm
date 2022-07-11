#!/bin/bash
#SBATCH --time=15:00
#SBATCH --nodes=1 --ntasks-per-node=28
#SBATCH --output=logs/%j.log
#SBATCH --account=PAS0409

input_dir=$1
job_name=${2:-1}
output_dir=${3:-$1/$job_name/OUTPUT}

set -x

echo $input_dir
echo $job_name
echo $output_dir

python -m palm_wrapper.data_analyzer.analyze --input_dir $input_dir --output_dir $output_dir --job_name $job_name
