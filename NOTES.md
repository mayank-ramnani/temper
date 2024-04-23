- `make -p` gives the default variables supplied by the make tool to a Makefile
    + For example, CC is supplied by it
- Compiler options can be specified in other variables that are later included in the compilation command
    + For example, `$(CC) -c $(CPPFLAGS) $(ALL_CFLAGS)`
- Dry run make: `make -f Makefile -n | grep ^($CC)`
- Check binutils version: `ld -v`, `ar --version`

