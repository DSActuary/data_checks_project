import pandas as pd

# TODO add custom logic for each file.

class FileLoader:
    def __init__(self, file_info, valuation_date):
        self.file_name = file_info['file_name']
        self.file_path_template = file_info['file_path']
        self.valuation_date = valuation_date
        self.file_path = self._generate_file_path()

    def _generate_file_path(self):
        """generate file path by replacing date placeholders"""
        return self.file_path_template.replace("YYYY-MM-DD", self.valuation_date) \
                                    .replace("YYYY", self.valuation_date[:4]) \
                                    .replace("MM", self.valuation_date[5:7]) \
                                    .replace("Q#", "Q" + str((int(self.valuation_date[5:7])-1)//3 + 1))

    def load_file(self, sheet_name=None):
        """main method to load file based on its type."""
        if self.file_name == 'file_one':
            return self._load_csv_file() # assume this one is a csv
        elif self.file_name == 'file_two':
            return self._load_file_two(sheet_name)
        elif self.file_name == 'file_three':
            return self._load_file_three(sheet_name)
        else:
            raise ValueError(f"Unknown file type: {self.file_name}. Ensure file has file_loader logic")
        
    def _load_file_one(self):
        """Logic required to read in file one"""
        try: 
            df = pd.read_csv(self.file_path)
            # put the custom logic here
            return df
        except Exception as e:
            print(f"Error loading {self.file_name}: {e}")
            return None
        
    def _load_file_two(self, sheet_name):
        """Logic required to read in file two"""
        try: 
            df = pd.read_excel(self.file_path, sheet_name = sheet_name)
            # put the custom logic here
            return df
        except Exception as e:
            print(f"Error loading {self.file_name}: {e}")
            return None
        
    def _load_file_three(self, sheet_name):
        """Logic required to read in file three"""
        try: 
            df = pd.read_excel(self.file_path, sheet_name = sheet_name)
            # put the custom logic here
            return df
        except Exception as e:
            print(f"Error loading {self.file_name}: {e}")
            return None
        
    def _load_file_four(self, sheet_name):
        """Logic required to read in file four"""
        try: 
            df = pd.read_excel(self.file_path, sheet_name = sheet_name)
            # put the custom logic here
            return df
        except Exception as e:
            print(f"Error loading {self.file_name}: {e}")
            return None
        