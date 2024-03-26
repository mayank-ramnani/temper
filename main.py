#!/usr/bin/python3
import argparse
import re
import subprocess

def run_shell_command(command):
    try:
        # Run the command in the shell
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        # Check if the command was successful
        if result.returncode == 0:
            # Return the output
            return result.stdout.strip()
        else:
            # If the command failed, print error message
            print("Error:", result.stderr.strip())
            return None
    except Exception as e:
        print("Error:", e)
        return None


def extract_compiler_options(makefile_path):
    print("Makefile path: ", makefile_path)
    compiler_options = set()

    with open(makefile_path, 'r') as f:
        lines = f.readlines()

    for line in lines:
        # Match lines starting with "CFLAGS", "CXXFLAGS", or "CPPFLAGS"
        # match = re.match(r'^\s*(CFLAGS|CXXFLAGS|CPPFLAGS)\s*[:]?=\s*(.+)', line)
        match = re.match(r'^\s*(CFLAGS|CXXFLAGS|CPPFLAGS)\s*.?[=]?=\s*(.+)', line)
        if match:
            options = match.group(2).strip().split()
            for option in options:
                compiler_options.add(option)

    return compiler_options

def main():
    # Argument parser setup
    parser = argparse.ArgumentParser(description='Extract enabled compiler options from a Makefile')
    parser.add_argument('--makefile', help='Path to the Makefile', required=True)
    args = parser.parse_args()

    # Extract compiler options
    enabled_options = extract_compiler_options(args.makefile)

    # Print the enabled compiler options
    print("Enabled Compiler Options:")
    # TODO: add the default enabled compiler options in the set as well
    # TODO: mention the version of gcc/clang being used in the project
    # gcc -v hello.c -o hello; rm -f hello
    for option in enabled_options:
        print(option)

if __name__ == "__main__":
    build_command = "gcc -v hello.c -o hello"
    remove_command = "rm -f hello"
    output = run_shell_command(build_command)
    if output is not None:
        print(output)

    run_shell_command(remove_command)
    # main()
