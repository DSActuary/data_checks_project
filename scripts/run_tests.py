import json
import pandas as pd
from datetime import datetime
from file_loader import FileLoader

def load_config(config_file_path):
    """Load the configuration file."""
    try:
        with open(config_file_path, "r") as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print(f"Error: Config file {config_file_path} not found.")
        return None
    except json.JSONDecodeError:
        print("Error: Config file is not in proper JSON format.")
        return None

# function to laod files
def load_files_for_test(required_files, config, valuation_date):
    """Load all required files for specific tests"""
    loaded_files = {}

    for file_name in required_files:
        # get file info from config.json
        file_info = next((f for f in config['files']  if f['file_name'] == file_name), None)
    
        if file_info:
            # pass config and valuation date to the FileLoader
            loader = FileLoader(file_info, valuation_date)
            sheet_name = file_info.get('sheet_name')
            loaded_files[file_name] = loader.load_file(sheet_name)
        else:
            print(f"Errror: File {file_name} not found in config.")
    
    return loaded_files


# function to run tests for one ore more steps
def run_tests(step_names, config, valuation_date):
    """Run tests for one or more steps."""
    required_files = set() # keep track of all files needed for the steps

    # collect required files for each step
    for step_name in step_names:
        if step_name in config['steps']:
            step = config['steps'][step_name]
            for test in step['tests']:
                required_files.update(test['required_files']) 
        else:
            print(f"Step {step_name} not found in config file.")

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
