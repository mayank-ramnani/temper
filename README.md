# Temper
Compiler Hardening for C/C++ based on the [OpenSSF Compiler Hardening Guide](https://best.openssf.org/Compiler-Hardening-Guides/Compiler-Options-Hardening-Guide-for-C-and-C++.html)


## Usage
Run this in your build environment, otherwise might give inaccurate results due to compiler being different than the one used in production
```sh
python3 temper.py --makefile <path-to-project-makefile>
```

## Options
```sh
  -h, --help            show this help message and exit
  -m MAKEFILE, --makefile MAKEFILE
                        Path to Makefile to analyse and get recommendations
  -i INPUT_JSON_PATH, --input-json-path INPUT_JSON_PATH
                        Path to input json generated from tool to get recommendations
  -o, --output          Store analysed options in json output file
  --apply               Apply recommended options to Makefile
  -l, --list            List compiler options in OpenSSF database
  --show                Show configured options in Makefile
```

## Example
```sh
╰─ temper -m example-makefiles/Makefile.OpenWAF
Write compiler options in json: output-1713221129.json
Found in configured opts:  -Wall
Recommendations:
[
    {
        "opt": "-O2",
        "desc": "Optimize compilation - Level 2"
    },
    {
        "opt": "-Wformat",
        "desc": "Check calls to printf and scanf, etc., to make sure that the arguments supplied have types appropriate to the format string specified"
    },
    {
        "opt": "-fstack-protector-strong",
        "desc": "Enable run-time checks for stack-based buffer overflows. Can impact performance."
    }
]
```
