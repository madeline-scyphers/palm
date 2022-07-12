#!/bin/bash
#SBATCH --time=12:00:00
#SBATCH --nodes=2 --ntasks-per-node=24
#SBATCH --partition=parallel
#SBATCH --output=logs/%j.log
#SBATCH --account=PAS0409

set -x  # for displaying the commands in the log for debugging

config_file=$1
job_name=$2
run_time=${3:-900}
io_config=${4:-'"d3#"'}
to_batch=${5:-true}

if [[ $to_batch = true ]]
then
  batch='-b'
else
  batch=''
fi

input_dir=$TMPDIR/palm_config
output_dir=$TMPDIR/$job_name/OUTPUT
palm_dir=~/palm
script_path=palm_wrapper/main.py
model_path=~/palm/current_version
data_analyzer_path=palm_wrapper.data_analyzer.analyze

mkdir -p $input_dir
mkdir -p $output_dir

cd $palm_dir

python $script_path --config_file $config_file --input_dir $input_dir --job_name $job_name

cd $model_path

palmrun -r $job_name -c default -X48 -T24 -q parallel -t $run_time -a $io_config $batch -v -m 4315

cd $palm_dir

python -m $data_analyzer_path --input_dir $input_dir --output_dir $output_dir

function move_output() {
    cd $SLURM_SUBMIT_DIR
    mkdir -p $SLURM_SUBMIT_DIR/output/$job_name/output
    cp -R $output_dir/r_ca.json $SLURM_SUBMIT_DIR/output/$job_name/output/r_ca.json
    # cp -R $output_dir $SLURM_SUBMIT_DIR/output/$job_name/output
    cp -R $input_dir $SLURM_SUBMIT_DIR/output/$job_name
  exit
}

move_output
trap move_output TERM