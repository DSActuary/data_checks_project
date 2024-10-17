from datetime import datetime
# TODO make the test results more useful. If fails, output the results / definition of test
# TODO definition of test hasn't been added to the config yet
# TODO figure out a better way to refer to files / data (confusing data1 vs file1 etc)

def test_one(data, valuation_date=None):
    """Run test one"""
    file1 = data.get("file_one")
    file2 = data.get("file_two")

    if not (file1["col3"] == "yes").any():
        return False
    if file2[["col1", "col2", "col3"]].sum().sum() == 0:
        return True
    else:
        return False

# TODO look into if there a way to make the number of files being read in dynamic
def test_two(data, valuation_date):
    """Run test two"""
    file1 = data.get("file_one")
    file2 = data.get("file_two")
    file3 = data.get("file_three")

    col_val_date = datetime.strptime(valuation_date, "%Y-%m-%d").strftime("%m/%d/%Y")
    data1 = file1.loc[file1["element_type"] == "test_row", "Current"]

    filtered_data3 = file3[file3[file3.columns[0]] == "a"]
    if col_val_date in file3.columns:
        data3 = filtered_data3[col_val_date].sum()
    else:
        raise ValueError(f"Column '{col_val_date}' not found in {file3}")

    # check that the data from the two files match. Ensure col1 - 3 are zero2
    if data1 != data3:
        return False
    if file2[["col1", "col2", "col3"]].sum().sum() == 0:
        return True
    else:
        return False

def test_three(file1, file2, valuation_date):
    """Run test three"""
    col_val_date = valuation_date.strftime("%m/%d/%Y")

    # check that the two tabs added together are less than 1000
    if col_val_date in file1.columns and col_val_date in file2.columns:
        # Step 2: Sum the values from both files and check if their sum is less than 1000
        data3 = file1[col_val_date].sum() + file2[col_val_date].sum() < 1000
        return data3
    else:
        raise ValueError(f"Column '{col_val_date}' not found in {file1, file2}")

