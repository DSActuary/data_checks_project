import json
import pandas as pd

config_file_path = "..\config.json"

# load json file
with open(config_file_path, "r") as f:
    config = json.load(f)

# extract valuation date
valuation_date = config['valution_date']

# function to laod files
def load_file(file_info):
    file_path = file_info['file_path'].replace("YYYY-MM-DD", valuation_date) \
                                    .replace("YYYY", valuation_date[:4]) \
                                    .replace("MM", valuation_date[5:7]) \
                                    .replace("Q#", "Q" + str((int(valuation_date[5:7])-1)//3 + 1))

    try:
        df = pd.read_excel(file_path)
        print(f"Loaded {file_info['file_name']} from {file_path}.")
        return df
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")

# function to run tests for one ore more steps
def run_steps(step_names):
    required_files = set() # keep track of all files needed for the steps

    # collect required files for each step
    for step_name in step_names:
        if step_name in config['steps']:
            step = config['steps'][step_name]
            for test in step['tests']:
                required_files.update(test['required_files']) 
        else:
            print(f"Step {step_name} not found.")

    # load only the files needed for the steps
    data_files = {}
    for file_name in required_files:
        file_info = next((f for f in config['files'] if f['file_name'] == file_name), None)    
        if file_info:
            data_files[file_name] = load_files(file_info)

    # Run tests for each step
    for step_name in step_names:
        if step_name in config['steps']:
            step = config['steps'][step_name]
            for test in step['tests']:
                test_name = test['test_name']
                print(f"Running {test_name} for {step_name}...")

                # load required data for the test
                test_data = {name: data_files[name] for name in test['required_files'] if name in data_files}

                # TODO add test logic
                print(f"Files for {test_name}: {list(test_data.keys())}")

            else:
                print(f"step {step_name} not found.")

# examples
run_steps(["comm_trueup"])
run_steps(["comm_trueup", "inv_income"])
