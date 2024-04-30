#!/usr/bin/python3
import argparse
import re
import subprocess
import json
import time
from tabulate import tabulate
import art # ascii art

output_db = {}

# gets output from stderr if stdout is empty
# gets output from stdout if stderr is empty
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
            if result.stderr:
            # If the command failed, print error message
                return result.stderr.strip().split('\n')
            else:
                return result.stdout.strip.split('\n')
    except Exception as e:
        print("Error:", e)
        return None


def print_list_of_dicts_as_table(list_of_dicts):
    # Extract headers from the keys of the first dictionary
    headers = list(list_of_dicts[0].keys())

    # Extract data from each dictionary and convert it into a list of lists
    table_data = [[row[key] for key in headers] for row in list_of_dicts]

    # Print table
    # print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
    # print(tabulate(table_data, headers=headers, tablefmt="orgtbl"))
    # print(tabulate(table_data, headers=headers, tablefmt="presto"))
    print(tabulate(table_data, headers=headers, tablefmt="psql"))
    # print(tabulate(table_data, headers=headers, tablefmt="rst"))

def extract_compiler_options(makefile_path):
    print("Makefile path: ", makefile_path)
    compiler_options = set()

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
        for line in output:
            if "version" in line:
                print(line)
                return line

def get_compiler_default_opts(compiler):
    compiler_opts = []
    build_command = compiler + " -v assets/hello.c -o hello"
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

def extract_cc_value(makefile_lines):
    compiler_options = set()

    for line in makefile_lines:
        # Match lines starting with "CC"
        match = re.match(r'^\s*(CC)\s*.?[=]?=\s*(.+)', line)
        if match:
            cc_value = match.group(2).strip()
            print(cc_value) 
            return cc_value

def get_configured_compiler(makefile_lines):
    # Find the configured compiler
# get value of CC
    cc_value = extract_cc_value(makefile_lines)
    if not cc_value:
        default_make_output = run_shell_command("make -p")
# if it is not defined, run `make -p` and get its value from the default set
# run `$CC --version` to find the compiler being used

    # parser.add_argument('--compiler', help='Print compiler', required=False, action='store_true')
    # parser.add_argument('--default-opts', help='Print compiler default options', 
    # required=False, action='store_true')
def main():
    print(art.text2art("temper"))
    parser = argparse.ArgumentParser(description="Temper: Harden your C/C++\
                                     projects - Analyse and find secure\
                                     compiler options for your makefile")
    parser.add_argument('-m', '--makefile', help='Path to Makefile to analyse\
                        and get recommendations',
                        required=False)
    parser.add_argument('-i', '--input-json-path', help='Path to input json\
                        generated from tool to get recommendations',
                        required=False)
    parser.add_argument('-o', '--output', help='Store analysed\
                        options in json output file', required=False, action='store_true')
    parser.add_argument('--apply', help='Apply recommended options to\
                        Makefile', required=False, action='store_true')
    parser.add_argument('-l', '--list', help='List compiler options in OpenSSF database',
                        required=False, action='store_true')
    parser.add_argument('-d', '--debug', help='Debug mode',
                        required=False, action='store_true')
    parser.add_argument('--show', help='Show configured options in\
                        Makefile', required=False, action='store_true')
    # parser.add_argument('-o', '--output', help='Output', required=True)
    args = parser.parse_args()

    # if args.compiler:
    #    get_compiler()
    # if args.default_opts:
    #    get_compiler_default_opts()
    if args.makefile:
        # read makefile and pass the lines for processing
        with open(args.makefile, 'r') as f:
            output_db["makefile"] = args.makefile
            timestamp = int(time.time())
            output_db["timestamp"] = timestamp
            makefile_lines = f.readlines()
            # get_configured_compiler(lines)
            cc_value = ""
            for line in makefile_lines:
                # Match lines starting with "CC"
                match = re.match(r'^\s*(CC)\s*.?[=]?=\s*(.+)', line)
                if match:
                    cc_value = match.group(2).strip()
                    # print(cc_value) 
            if not cc_value:
                # print("didn't find compiler in makefile")
                # need to specify argument of makefile to make the command not
                # error out
                default_make_output = run_shell_command("make -p " +
                                                        args.makefile)
                for line in default_make_output:
                    # Match lines starting with "CC"
                    match = re.match(r'^\s*(CC)\s*.?[=]?=\s*(.+)', line)
                    if match:
                        cc_value = match.group(2).strip()
                        # print(cc_value) 
                        # TODO: get full path of the compiler, currently output
                        # is just "cc". might be able to run which "cc"

            output_db["compiler"] = cc_value
            # 3. get default opts
            default_opts = get_compiler_default_opts(cc_value)
            output_db["default_opts"] = default_opts

            # 4. get configured opts
            configured_opts = set()

            for line in makefile_lines:
                # Match lines starting with "CFLAGS", "CXXFLAGS", or "CPPFLAGS"
                # match = re.match(r'^\s*(CFLAGS|CXXFLAGS|CPPFLAGS)\s*[:]?=\s*(.+)', line)
                match = re.match(r'^\s*(CFLAGS|CXXFLAGS|CPPFLAGS)\s*.?[=]?=\s*(.+)', line)
                if match:
                    options = match.group(2).strip().split()
                    for option in options:
                        configured_opts.add(option)
            output_db["configured_opts"] = list(configured_opts)
            # set is not directly serializable in python
            output_file = "output-" + str(timestamp) + ".json"
            if args.debug:
                with open(output_file, 'w') as fp:
                    json_formatted_str = json.dumps(output_db, indent=4)
                    print("Write compiler options in json:", output_file)
                    # print(json_formatted_str)
                    fp.write(json_formatted_str)
            
            db_json = {}
            with open("assets/db.json", 'r') as db:
                db_json = json.load(db)
            
            input_json = {}
            # with open(output_file, 'r') as ij:
            #    input_json = json.load(ij)
            input_json = output_db
            
            default_opts = input_json["default_opts"]
            configured_opts = input_json["configured_opts"]

            recommended_opts = db_json["options"]["recommended"]
            recommendations = []
            for opt in recommended_opts:
                if opt["opt"] in default_opts:
                    print("Found in default opts: ", opt["opt"])
                elif opt["opt"] in configured_opts:
                    print("Found in configured opts: ", opt["opt"])
                else: # recommend addition
                    recommendations.append(opt)

            print("Recommendations:")
            # print(json.dumps(recommendations, indent=4))
            print_list_of_dicts_as_table(recommendations)
            
    if args.input_json_path:
        db_json = {}
        with open("db.json", 'r') as db:
            db_json = json.load(db)
        
        input_json = {}
        with open(args.input_json_path, 'r') as ij:
            input_json = json.load(ij)
        
        default_opts = input_json["default_opts"]
        configured_opts = input_json["configured_opts"]

        recommended_opts = db_json["options"]["recommended"]
        recommendations = []
        for opt in recommended_opts:
            if opt["opt"] in default_opts:
                print("Found in default opts: ", opt["opt"])
            elif opt["opt"] in configured_opts:
                print("Found in configured opts: ", opt["opt"])
            else: # recommend addition
                recommendations.append(opt)

        print("Recommendations:")
        # print(json.dumps(recommendations, indent=4))


if __name__ == "__main__":
    main()

# TODO: check if it starts with '-' each compiler option
# TODO: add ascii art
    # TODO: add the default enabled compiler options in the set as well
    # TODO: mention the version of gcc/clang being used in the project
    # TODO: reformat code, make everything functional
