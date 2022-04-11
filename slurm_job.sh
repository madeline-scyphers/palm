#!/bin/bash
#SBATCH --job-name=test_job
#SBATCH --time=200:00
#SBATCH --nodes=2 --ntasks-per-node=24
#SBATCH --partition=parallel
#SBATCH --output=logs/%j.log
#SBATCH --account=PAS0409

set -x  # for displaying the commands in the log for debugging

job_name=1
input_dir=$TMPDIR/palm_config
output_dir=$TMPDIR/$job_name/OUTPUT

python main.py --input_dir $input_dir --job_name $job_name

cd current_version

palmrun -r $job_name -c default -X48 -T24 -q parallel -t 120 -a "slurm" -v

cd ../data_analyzer

python analyze.py --input_dir $input_dir --output_dir $output_dir

function move_output() {
    cd $SLURM_SUBMIT_DIR
    mkdir -p $SLURM_SUBMIT_DIR/output/$SLURM_JOB_ID
    cp -R $output_dir/r_ca.txt $SLURM_SUBMIT_DIR/output/$SLURM_JOB_ID/r_ca.txt
    cp -R $input_dir $SLURM_SUBMIT_DIR/output/$SLURM_JOB_ID
  exit
}

move_output
trap move_output TERM