#!/usr/bin/python3
import argparse
import re
import subprocess

# gets output from stderr if stdout is empty
# `gcc -v` writes output to stderr
# output is split into a list of lines
def run_shell_command(command):
    try:
        # Run the command in the shell
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        # Check if the command was successful
        if result.returncode == 0:
            # Return the output
            if result.stdout:
                return result.stdout.strip().split('\n')
            else:
                return result.stderr.strip().split('\n')
        else:
            # If the command failed, print error message
            print("Error:", result.stderr.strip().split('\n'))
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

def get_compiler():
    output = run_shell_command("gcc -v")
    if output is not None:
        return output[0]

def get_compiler_default_opts():
    compiler_opts = []
    build_command = "gcc -v hello.c -o hello"
    output = run_shell_command(build_command)
    if output is not None:
        remove_command = "rm -f hello"
        run_shell_command(remove_command)
        opts = output[4].split()
        for opt in opts:
            if opt.startswith('-'):
                compiler_opts.append(opt)
        return compiler_opts
        
def get_makefile_opts(makefile):
    # Extract compiler options
    enabled_options = extract_compiler_options(makefile)

    # Print the enabled compiler options
    print("Enabled Compiler Options:")
    # TODO: add the default enabled compiler options in the set as well
    # TODO: mention the version of gcc/clang being used in the project
    # gcc -v hello.c -o hello; rm -f hello
    for option in enabled_options:
        print(option)
    print(get_compiler_default_opts())


def main():
    # Argument parser setup
    parser = argparse.ArgumentParser(description='Extract enabled compiler options from a Makefile')
    parser.add_argument('--compiler', help='Print compiler', required=False)
    parser.add_argument('--default-opts', help='Print compiler default options', required=False)
    parser.add_argument('--makefile', help='Path to the Makefile', required=True)
    args = parser.parse_args()

    get_makefile_opts(args.makefile)

if __name__ == "__main__":
    main()

# TODO: check if it starts with '-' each compiler option
