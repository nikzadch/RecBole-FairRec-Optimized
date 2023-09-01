import os
import subprocess
import datetime
import time

MODEL = ['ItemKNN', 'PFCN_DMF', 'PFCN_biasedMF', 'NFCF', 'FOCF', 'FairGo_PMF', 'FairGo_GCN', 'PFCN_PMF', 'NGCF', 'SGL', 'LightGCN', 'DMF', 'NeuMF', 'NNCF', 'DGCF']
CONFIG = [('ML', 'ml-1M'), ('LFM', 'LastFM-100K'), ('BR', 'BookRec-100K')]

log_dir = '~/work/code-results/'

for config in CONFIG:
    for model in MODEL:
        output_file = f"Run {datetime.datetime.now().strftime('%H,%M')}@{model}-{config[1]}.log"
        command = f"python3 run_recbole.py --model={model} --config=Configuration{config[0]}.yaml --dataset={config[1]} > {output_file} 2>&1"
                
        # Run the script and capture the output
        # completed_process = subprocess.run(command, shell=True, text=True, capture_output=True)
        process = subprocess.Popen(command, shell=True)
        process.wait()
        # output = '\n'.join(completed_process.stdout.splitlines()[-14:])
        
        # Write the output to a file
        # os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
        # with open(log_dir + output_file, 'w') as f:
        #     f.write(output)
        
        # Wait for 1 second before starting the next iteration
        time.sleep(1)
