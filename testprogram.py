#!/usr/bin/python3
import argparse
import json
import subprocess
import os
import sys
import time


parser = argparse.ArgumentParser(
    description="A tester to test your comepitive coding solution against test cases")
language = parser.add_mutually_exclusive_group(required=True)

parser.add_argument('program_file',
                    help="path to the program", type=str)
language.add_argument('--python', action='store_true',
                      help="call program by 'python3 filename.py', (default)")
language.add_argument('--exe', action='store_true',
                      help="call program by './filename'")
language.add_argument('--java', action='store_true',
                      help="call program by 'java classname'")
language.add_argument('--pypy', action='store_true',
                      help="call program by 'pypy3 filename'")
parser.add_argument('-t', '--test-file',
                    help="path to the tests json file", required=True, type=open)
args = parser.parse_args()
if args.java:
    subprocess.run(["javac", f"{args.program_file}.java"])
test_cases = json.loads(args.test_file.read())
total_cases = len(test_cases)
failed_cases = 0
for i, test_case in enumerate(test_cases, 1):
    input_data = "\n".join(test_case["input"]).encode()
    required_output = "\n".join(test_case["output"])
    start_time = time.time()
    process = None
    if args.exe:
        if sys.platform == 'linux':
            process = subprocess.run([f".{os.path.sep}{args.program_file}"],
                                     input=input_data,
                                     capture_output=True)
        elif sys.platform == 'win32':
            process = subprocess.run([f"{args.program_file}"],
                                     input=input_data,
                                     capture_output=True,
                                     shell=True)
    elif args.python:
        if sys.platform == 'linux':
            process = subprocess.run(["python3", args.program_file],
                                     input=input_data,
                                     capture_output=True)
        elif sys.platform == 'win32':
            process = subprocess.run(["python", args.program_file],
                                     input=input_data,
                                     capture_output=True,
                                     shell=True)
    elif args.pypy:
        if sys.platform == 'linux':
            process = subprocess.run(["pypy3", args.program_file],
                                     input=input_data,
                                     capture_output=True)
        elif sys.platform == 'win32':
            process = subprocess.run(["pypy", args.program_file],
                                     input=input_data,
                                     capture_output=True,
                                     shell=True)
    elif args.java:
        if sys.platform == 'linux':
            process = subprocess.run(["java", f"{args.program_file}"],
                                     input=input_data,
                                     capture_output=True,)
        elif sys.platform == 'win32':
            process = subprocess.run(["java", f"{args.program_file}"],
                                     input=input_data,
                                     capture_output=True,
                                     shell=True)
    time_taken = time.time()-start_time
    actual_output = process.stdout.decode().strip().replace('\r', '')
    if process.returncode == 0 and required_output == actual_output:
        print(f"Test Case {i} Passed and took {time_taken:.3f} seconds  ✅")
    else:
        failed_cases += 1
        print(f"Test Case {i} Failed ❎")
        if process.returncode == 0:
            print(f"Required Output:\n{required_output}\n---------------")
            print(
                f"Actual Output:\n{actual_output}\n---------------\n(took {time_taken:.3f} seconds)\n")
        else:
            failed_cases += 1
            print("---------------")
            print(f"Runtime Error: (took {time_taken:.3f} seconds)")
            print(process.stderr.decode().strip())
            print("---------------\n")
if failed_cases == 0:
    print("All tests passed successfully. ✅")
else:
    print(f"{failed_cases}/{total_cases} Test Cases Failed ❎")
