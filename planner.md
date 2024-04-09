# planner
## flow
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
7. 
