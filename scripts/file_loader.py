import pandas as pd

# TODO Add custom logic needed
# TODO fix sheet name pulling as it'll likely need to know which test is being ran to know what sheet to pull

class FileLoader:
    def __init__(self, file_info, valuation_date):
        self.file_name = file_info['file_name']
        self.file_path_template = file_info['file_path']
        self.valuation_date = valuation_date
        self.file_path = self._generate_file_path()

    def _generate_file_path(self):
        """generate file path by replacing date placeholders"""
        return self.file_path_template.replace("YYYY-MM-DD", valuation_date) \
                                    .replace("YYYY", valuation_date[:4]) \
                                    .replace("MM", valuation_date[5:7]) \
                                    .replace("Q#", "Q" + str((int(valuation_date[5:7])-1)//3 + 1))

    def load_file(self):
        """main method to load file based on its type."""
        if self.file_name == 'file_one':
            return._load_file_one()
        elif self.file_name == 'file_two':
            return self._load_file_two()
        elif self.file_name == 'file_three':
            return self._load_file_three()
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
        
    def _load_file_two(self):
        """Logic required to read in file two"""
        try: 
            df = pd.read_excel(self.file_path, sheet_name = "Sheet1"))
            # put the custom logic here
            return df
        except Exception as e:
            print(f"Error loading {self.file_name}: {e}")
            return None
        
    def _load_file_three(self):
        """Logic required to read in file three"""
        try: 
            df = pd.read_csv(self.file_path)
            # put the custom logic here
            return df
        except Exception as e:
            print(f"Error loading {self.file_name}: {e}")
            return None
        
    def _load_file_four(self):
        """Logic required to read in file four"""
        try: 
            df = pd.read_excel(self.file_path, sheet_name = "Sheet1"))
            # put the custom logic here
            return df
        except Exception as e:
            print(f"Error loading {self.file_name}: {e}")
            return None
        