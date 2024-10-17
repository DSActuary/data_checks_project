import argparse
from scripts.test_manager import TestManager

# TODO fix config to have a definition. This definition explains each test and can be printed when the test fails

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

    # Initialize the TestManager with the config
    test_manager = TestManager(config_file_path)

    print(f"is test as list: {isinstance(args.tests, list)}")

    # Run specified tests
    try:
        print(f"Running test '{args.tests}'")
        test_manager.run_tests(args.tests)
    except ValueError as e:
        print(f"Error running test {args.tests}: {e}")


'''    # Run specified tests
    for test in args.tests:
        print(f"in loop, is test a string: {isinstance(test, str)}")
        try:
            print(f"Running test '{test}'")
            test_manager.run_tests(test)
        except ValueError as e:
            print(f"Error running test {test}: {e}")'''

if __name__ == "__main__":
    main()
