import argparse
import json
from scripts.test_manager import TestManager  # Import your TestManager class or equivalent

def choose_config(product):
    """Based on arguments, select the correct configuration file."""
    if product == "prod1":
        return "config.json"
    elif product == "prod2":
        return "config2.json"
    elif product == "prod3":
        return "config3.json"
    else:
        raise ValueError(f"Unknown product type: {product}. Program supports 'prod1', 'prod2', 'prod3'.")

def load_config(config_file_path):
    """Load configuration from a JSON file."""
    with open(config_file_path, 'r') as f:
        return json.load(f)

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Run data checks on Excel files.")
    parser.add_argument('-p', '--product', type=str, required=True, 
                        help='The product you are running tests on.')
    parser.add_argument('-t', '--tests', nargs='+', required=True, 
                        help='List of tests to run (e.g., comm_trueup inv_income).')
    
    args = parser.parse_args()

    # Choose configuration
    config_file_path = choose_config(product=args.product)

    # Load configuation
    config = load_config(config_file_path)

    # Initialize the TestManager with the config
    test_manager = TestManager(config)

    # Run specified tests
    for test in args.tests:
        try:
            test_manager.run_test(test)  # Implement this method in your TestManager
        except ValueError as e:
            print(f"Error running test {test}: {e}")

if __name__ == "__main__":
    main()
