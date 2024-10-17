import json
import pandas as pd
from datetime import datetime
from .file_loader import FileLoader
from .tests.test_comm_trueup import test_one, test_two, test_three # TODO update this when a better way to call tests

# TODO is this needed if the json is being read in the early test_manager step
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
            print(f"Error: File {file_name} not found in config.")
    
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
    data_files = load_files_for_test(required_files, config, valuation_date)

    # Run tests for each step
    for step_name in step_names:
        if step_name in config['steps']:
            step = config['steps'][step_name]
            for test in step['tests']:
                test_name = test['test_name']
                print(f"Running {test_name} for {step_name}...")

                # load required data for the test
                test_data = {name: data_files[name] for name in test['required_files'] if name in data_files}

                # TODO fix this to call things dynamically so as the tests scale adjustments don't need to be made here
                if test_name == "test_one":
                    result = test_one(test_data['file1'], test_data['file2'])
                elif test_name == "test_two":
                    result = test_two(test_data['file1'], test_data['file2'], test_data['file3'], valuation_date)
                elif test_name == "test_three":
                    result = test_three(test_data['file1'], test_data['file2'], valuation_date)
                else:
                    print(f"Error: Unknown test '{test_name}'")
                    continue
                
                print(f"Result of {test_name}: {result}")

            else:
                print(f"step {step_name} not found.")
