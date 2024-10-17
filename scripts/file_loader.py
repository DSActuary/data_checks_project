import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# TODO add custom logic for each file.
# TODO fix date path logic

class FileLoader:
    def __init__(self, file_info, valuation_date):
        self.file_name = file_info['file_name']
        self.file_path_template = file_info['file_path']
        self.valuation_date = datetime.strptime(valuation_date, "%Y-%m-%d")
        self.file_path = self._generate_file_path()

    def _generate_file_path(self):
        """generate file path by replacing date placeholders"""
        # create prior quarter end
        curr_qtr_start_month = (self.valuation_date.month - 1) // 3 * 3 + 1
        prior_qtr = datetime(self.valuation_date.year, curr_qtr_start_month, 1) - timedelta(days = 1)

        # create prior month end
        prior_mnth = self.valuation_date.replace(day = 1) - timedelta(days = 1) # subtract a day to get prior month end

        # month format for paths /2. February/
        valuation_month_number = self.valuation_date.strftime('%-m')  # Without leading zero (e.g., 4)
        valuation_month_name = self.valuation_date.strftime('%B')      # Full month name (e.g., "April")
        month_folder = f"{valuation_month_number}. {valuation_month_name}" # will turn path into "4. April"

        # Replace placeholders in the file path template
        file_path = self.file_path_template \
            .replace("YYYY-MM-DD", self.valuation_date.strftime('%Y-%m-%d')) \
            .replace("YYYY-MM", self.valuation_date.strftime('%Y-%m')) \
            .replace("YYYY", str(self.valuation_date.year)) \
            .replace("MM", self.valuation_date.strftime('%m')) \
            .replace("DD", self.valuation_date.strftime('%d')) \
            .replace("Q#", "Q" + str((self.valuation_date.month - 1) // 3 + 1)) \
            .replace("PRIOR_QTR", prior_qtr.strftime('%Y%m')) \
            .replace("PRIOR_MNTH", prior_mnth.strftime('%Y%m')) \
            .replace("MONTH_FOLDER", month_folder)

        return file_path

    def load_file(self, sheet_name=None):
        """main method to load file based on its type."""
        if self.file_name.startswith('file_one'):
            return self._load_file_one() # assume this one is a csv
        elif self.file_name.startswith('file_two'):
            return self._load_file_two(sheet_name)
        elif self.file_name.startswith('file_three'):
            return self._load_file_three(sheet_name)
        else:
            raise ValueError(f"Unknown file type: {self.file_name}. Ensure file has file_loader logic.")
        
    def _load_file_one(self, sheet_name=None):
        """Logic required to read in file one."""
        try: 
            if sheet_name:
                df = pd.read_excel(self.file_path, sheet_name = sheet_name)
            else:
                df = pd.read_csv(self.file_path)
            return df
        except Exception as e:
            print(f"Error loading {self.file_name}: {e}")
            return None
        
    def _load_file_two(self, sheet_name):
        """Logic required to read in file two."""
        if sheet_name == "Current":
            try: 
                df = pd.read_excel(self.file_path, sheet_name = sheet_name, skiprows = 4)
                #df.drop(index = 5, inplace = True) # drop the blank row of data
                #df.reset_index(drop = True, inplace = True)
                df.rename(columns={df.columns[0]: 'element_type'}, inplace = True)
                return df
            except Exception as e:
                print(f"Error loading {self.file_name}: {e}")
                return None
        elif sheet_name == "Diff":
            try: 
                df = pd.read_excel(self.file_path, sheet_name = sheet_name, header=0, skiprows=range(1,4))
                df.rename(columns={df.columns[0]: 'group_type'}, inplace = True)
                return df
            except Exception as e:
                print(f"Error loading {self.file_name}, tab {sheet_name}: {e}")
                return None
        else:
            print(f"Error loading {self.file_name}, tab {sheet_name}. Sheet name logic not included in _load_file_three.")
            return None
        
    def _load_file_three(self, sheet_name):
        """Logic required to read in file three."""
        try: 
            df = pd.read_excel(self.file_path, sheet_name = sheet_name, skiprows=5)
            
            # there is data in column 1 that are "groups". Take those and make them a data element on each row it pertains to.
            rows_with_identifiers = []
            current_identifer = None

            # TODO fix logic so that the identifers get placed as a new data column
            #      identifers are specific to certain rows of data. 
            #      
            
            # iterate through rows
            """
            for index, row in df.iterrows():
                identifer = row[0]

                if pd.notna(identifer):
                    current_identifer = identifer
                else:
                    if current_identifer is None:
                        continue

                rows_with_identifiers.append([current_identifer] + row.tolist())

            identifer_df = pd.DataFrame(rows_with_identifiers)
            """
            # delete 2nd column which is empty
            df.drop(df.columns[1], axis=1, inplace=True)

            return df
        except Exception as e:
            print(f"Error loading {self.file_name}, tab {sheet_name}: {e}")
            return None
        
    def _load_file_four(self, sheet_name):
        """Logic required to read in file four."""
        try: 
            df = pd.read_excel(self.file_path, sheet_name = sheet_name)
            # put the custom logic here
            return df
        except Exception as e:
            print(f"Error loading {self.file_name}: {e}")
            return None
        