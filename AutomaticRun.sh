#!/bin/bash

MODEL=("ItemKNN" "PFCN_DMF" "PFCN_biasedMF" "NFCF" "FOCF" "FairGo_PMF" "FairGo_GCN" "PFCN_PMF" "NGCF" "SGL" "LightGCN" "DMF" "NeuMF" "NNCF" "DGCF")
CONFIG=("ML,ml-1M" "LFM,LastFM-100K" "BR,BookRec-100K")

# LOG_DIR is the directory you'd like to save the results, e.g:
LOG_DIR="~/work/code-results/"

for config in ${CONFIG[@]}; do
    IFS=',' read -r -a config_arr <<< "$config"
    
    for model in ${MODEL[@]}; do
        output_file="${LOG_DIR}Run_$(date +'%H%M')_${model}-${config_arr[1]}.log"
        command="python3 run_recbole.py --model=${model} --config=Configuration${config_arr[0]}.yaml --dataset=${config_arr[1]} > ${output_file} 2>&1"
    
        # Start timer
        start=$(date +%s)
        
        # Run the script in the background
        eval $command &
        
        # Get the process ID of the background task
        pid=$!
        
        # Display progress dots
        echo -n "Running $model-$config_arr[1]..."
        
        # Check the status of the process every second
        while ps -p $pid > /dev/null; do
            echo -n "."
            sleep 1
        done
        
        # Calculate the duration
        end=$(date +%s)
        duration=$((end - start))
        
        # Convert duration to MM:SS format
        minutes=$((duration / 60))
        seconds=$((duration % 60))
        time_taken=$(printf "%02d:%02d" $minutes $seconds)
        
        # Output time taken to run the code
        echo ""
        echo "Code with $output_file took $time_taken to run."
        
        # Save only the last 20 lines of the log file
        command2="tail -n 20 $output_file > ${output_file}.tmp && mv ${output_file}.tmp $output_file"
        eval $command2 &
        
        # Wait for 1 second before starting the next iteration
        sleep 1
    done
done
