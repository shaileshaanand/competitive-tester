#!/usr/bin/python3
import argparse
import json
import subprocess
import os


parser = argparse.ArgumentParser(
    description="A tester to test your comepitive coding solution against test cases")
language = parser.add_mutually_exclusive_group()

parser.add_argument('program_file',
                    help="path to the program", type=str)
language.add_argument('--python', action='store_true',
                      help="call program by 'python3 filename.py', (default)")
language.add_argument('--exe', action='store_true',
                      help="call program by './filename'")
parser.add_argument('-t', '--test-file',
                    help="path to the tests json file", required=True, type=open)
parser.set_defaults(python=True)
args = parser.parse_args()
test_cases = json.loads(args.test_file.read())
total_cases = len(test_cases)
failed_cases = 0
for i, test_case in enumerate(test_cases, 1):
    input_data = "\n".join(test_case["input"])
    required_output = "\n".join(test_case["output"])
    if args.python:
        process = subprocess.run(["python", args.program_file],
                                 input=input_data.encode(),
                                 capture_output=True)

    elif args.exe:
        process = subprocess.run([f".{os.path.sep}args.program_file"],
                                 input=input_data.encode(),
                                 capture_output=True)
    actual_output = process.stdout.decode().strip().replace('\r','')
    if process.returncode == 0 and required_output == actual_output:
        print(f"Test Case {i} Passed  ✅")
    else:
        failed_cases += 1
        print(f"Test Case {i} Failed ❎")
        if process.returncode == 0:
            print(f"Required Output:\n{required_output}\n---------------")
            print(f"Actual Output:\n{actual_output}\n---------------\n")
        else:
            failed_cases += 1
            print("---------------")
            print("Runtime Error:")
            print(process.stderr.decode().strip())
            print("---------------\n")
if failed_cases == 0:
    print("All tests passed successfully. ✅")
else:
    print(f"{failed_cases}/{total_cases} Test Cases Failed ❎")
