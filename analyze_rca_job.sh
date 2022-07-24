#!/bin/bash
#SBATCH --time=20:00
#SBATCH --nodes=1 --ntasks-per-node=14
#SBATCH --output=logs/%j.log
#SBATCH --account=PAS0409

set -x  # for displaying the commands in the log for debugging

data_analyzer_path=~/palm/palm_wrapper/analyze_rca.py

working_dir=$1
job_name=$2
working_dir_output=$working_dir/$job_name/OUTPUT

python $data_analyzer_path --input_dir $working_dir --output_dir $working_dir_output --job_name $job_name
