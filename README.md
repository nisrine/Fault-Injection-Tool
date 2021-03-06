# SimFI : Simulation-Fault-Injection-Tool
             

What is it?

Fault Injection Tool for Binaries. It simulates variety of the fault injection attacks. 

Documentation:

Usage:	faultinject.py [-h] -f {zerobyte,zeroword,nop,armnop,flip,tamper,jump} -a ADDRESS [-b [0-7]] [-t TARGET] [-v [0-255]] -o OUTFILE -i INFILE 

optional arguments: 

- -h, --help            : Show this help message and exit
- -a ADDRESS, --address ADDRESS : The position of the byte to implement the fault injection in the input file
- -b [0-7], --bit [0-7] : The bit of the byte to flip (required for flip fault model, otherwise ignored)
- -f {zerobyte,zeroword,nop,flip,tamper,jump}, --faultmodel {zerobyte,zeroword,nop,flip,tamper,jump}:
   - zerobyte: sets the specified  address  byte to zero.
   - zeroword: sets the specified  address  word to zero.
   - nop: sets the specified  address  byte to the x86 NOP code (0x90).
   - armnop: sets the specified address byte and the next byte to the ARM NOP (0x00BF)
   - flip: flips the specified  address  byte s  bit .
   - tamper: changes the value of a byte to  value .
   - jump: sets the specified  address  jump to jump to  target  location.
- -i INFILE, --infile INFILE : The input file
- -o OUTFILE, --outfile OUTFILE : The output mutant file name
- -t TARGET, --target TARGET :  The target relative address to jump to (required for jump fault model, otherwise ignored)
- -v [0-255], --value [0-255] : The value to set the byte to (required for tamper fault model only, otherwise ignored)
- -w [1-8], --wordsize [1-8] : The size (in bytes) of the word (required for zeroword fault model only, otherwise ignored)

