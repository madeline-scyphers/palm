#!/bin/bash

job_name=$1
run_time=${2:-900}
to_batch=${3:--b}
io_config=${4:-'"d3#"'}

palmrun -r $job_name -c default -X48 -T24 -q parallel -t $run_time -a $io_config $to_batch -v -m 4315
