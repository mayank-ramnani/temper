# planner
## tasks
1. get makefile path from user
    a. write makefile path, timestamp to output json db
2. get the configured compiler - needed to figure out compiler defaults
    a. read it from the makefile $CC argument
    b. else; read it from `make -p` output
    c. add configured compiler to a key "compiler" in the json output db
3. figure out compiler defaults using obtained compiler
    a. compile a simple hello world program
    b. get output of `$CC -v hello.c -o hello`
    c. remove `hello`
    d. split compiler defaults and add them to a key "default_opts" in the json output db
4. figure out configured options in the makefile lines using regex
    a. extract options and then separate out the ones that start with '-'
    b. add the options to an array; add array to a key "configured_opts" in the json output db
5. add timestamp to the output json db - "timestamp"
6. write the json db to file - "options-timestamp.json"
7. add support for giving recommendations
    a. get input json from user
    b. read db.json
    c. diff the options, and give recommendations



8. add more compiler options to the `db.json` - add new types of categories as well
9. add support for the additional arguments - detect makefile automatically, --apply option
10. human readable output by default with an option `-v`? that gives output in json
11. figure out how to deal with group options (O2 is absent, but O3 is present)
12. posix vs gnu make; use spec instead of just regex
13. testing on cmake
14. force make to expand macros before applying regex 
    - make dry run mode to get the configured compiler options and then parse them
15. parse the openssf compiler guide markdown to find options
16. add functions to compare if the required compiler option is applicable with the `required` object
