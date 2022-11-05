to_batch=${1:-true}

if [[ $to_batch = true ]]
then
  batch='-b'
else
  batch=''
fi

echo $batch