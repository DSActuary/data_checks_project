import json
from .file_loader import FileLoader
from .tests.test_comm_trueup import test_one, test_two, test_three

class TestManager:
    def __init__(self, config_file_path):
        self.config = self.load_config(config_file_path)
        self.valuation_date = self.get_valuation_date()
        self.test_function = {
            "test_one": test_one,
            "test_two": test_two,
            "test_three": test_three,
        }
    
    def load_config(self, config_file_path):
        """Loads the config from a JSON file."""
        try:
            with open(config_file_path, 'r') as f:
                return json.load(f)  # Load the JSON content into a dictionary
        except FileNotFoundError:
            print(f"Error: Config file {config_file_path} not found.")
            raise
        except json.JSONDecodeError:
            print("Error: Config file is not in proper JSON format.")
            raise

    def get_valuation_date(self):
        """Extracts the valuation date from the config file."""
        date_str = self.config.get("valuation_date")
        if date_str:
            return date_str
        else:
            raise ValueError("Valuation date not found in config")

    def load_files_for_tests(self, required_files):
        """load all rquired files for specific test"""
        data_files = {}

        for file_info in required_files:
            file_name = file_info['file_name']
            sheet_name = file_info['sheet_name']
            file_path = self.get_file_info(file_name)

            if file_path:
                loader = FileLoader(file_path, self.valuation_date)
                loaded_files = loader.load_file(sheet_name)
            else:
                print(f"Error: file '{file_name}' not found in config.")

            key = f"{file_name}_{sheet_name}" if sheet_name else file_name
            data_files[key] = loaded_files

        return data_files
    
    def get_file_info(self, file_name):
        """Helper method to get the file info from the config."""
        for file in self.config['files']:
            if file['file_name'] == file_name:
                return file
        raise ValueError(f"File '{file_name}' not found in config.")
    
    def run_tests(self, step_names):
        """Run specific test in a step"""
        # store a dictionary with file name / sheet combinations
        required_files = [] 

        for step_name in step_names:
            step = self.config['steps'][step_name]
            if not step:
                raise ValueError(f"Step '{step_name}' not found in config.")
            
            for test in step['tests']:
                # extract file names and sheet names from required_files
                for file_info in test['required_files']:
                    required_files.append({
                        'file_name': file_info['file_name'],
                        'sheet_name': file_info.get('sheet_name', None) # defaults to none if there isn't a sheet name
                    })
            
        # Load files needed for the tests
        data_files = self.load_files_for_tests(required_files)
        print("Printing data files:")
        for key, df in data_files.items():
            print(f"{key}: {df.head()}") # print the first couple rows of each DF

        # fun tests for each step
        for step_name in step_names:
            step = self.config['steps'][step_name]
            if not step:
                raise ValueError(f"Step '{step_name}' not found in config.")

            for test in step['tests']:
                test_name = test['test_name']
                print(f"Running {test_name} for {step_name}...")

                # TODO fix the way the name in the dictionaries so that each test data set gets assigned data1 ... dataN
                # then each test can all be structured as data1 ... dataN
                test_data = []
                for file_info in test['required_files']:
                    file_name = file_info['file_name']
                    sheet_name = file_info.get('sheet_name')
                    key = f"{file_name}_{sheet_name}" if sheet_name else file_name

                    print(f"Key -- {key}")
                    print()
                    if key in data_files:
                        test_data.append(data_files[key])
                    else:
                        print(f"Warning: {key} not found in data_files.")
                
                print()
                for index, df in enumerate(test_data):
                    print(f"Data {index + 1}:\n {df.head()}") 
                print()
                #print(f"Test: {test, required_files}")

                if test_name in self.test_function:
                    result = self.test_function[test_name](*test_data, self.valuation_date)
                    print(f"Result of {test_name}: {result}")
                else:
                    print(f"Error: Unknown test '{test_name}'")