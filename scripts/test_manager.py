from file_loader import FileLoader

class TestManager:
    def __init__(self, config, valuation_date):
        self.config = config
        self.valuation_date = valuation_date

    def load_files_for_tests(self, required_files):
        """load all rquired files for specific test"""
        loaded_files = {}
        for file_info in required_files:
            file_name = file_info['file_name']
            sheet_name = file_info.get('sheet_name')
            file_loader = FileLoader(self.get_file_info(file_name), self.valuation_date)
            loaded_files[file_name] = file_loader.load_file(sheet_name)
        return loaded_files
    
    def get_file_info(self, file_name):
        """Helper method to get the file info from the config."""
        for file in self.config['files']:
            if file['file_name'] == file_name:
                return file
        raise ValueError(f"File {file_name} not found in config.")
    
    def run_test(self, step_name, test_name)
        """Run specific test in a step"""
        step = self.config['steps'].get(step_name)
        if not step:
            raise ValueError(f"Step {step_name} not found in config.")
        
        test = None
        for t in step ['tests']:
            if t['test_name'] == test_name:
                test = t
                break

        if not test:
            raise ValueError(f"Test {test_name} not found in step {step_name}.")
        
        # load all required files for this test
        required_files = test['required_files']
        loaded_files = self.load_files_for_test(required_files)

