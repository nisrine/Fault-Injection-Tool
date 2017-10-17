# Fault-Injection-Tool
Fault Injection Tool for Binaries
                           Fault Injection Tool

What is it?
———————————
Fault Injection Tool simulates variety of the fault injection attacks.

Documentation
—————————————
Usage:	faultinject.py [-h] -f {zerobyte,zeroword,nop,flip,tamper,jump} -a ADDRESS [-b [0-7]] [-t TARGET] [-v [0-255]] -o OUTFILE -i INFILE

optional arguments:
  -h, --help            show this help message and exit
  -a ADDRESS, --address ADDRESS
                        the address to implement the fault injection in the input file
  -b [0-7], --bit [0-7]
                        the bit of the byte to flip (required for flip fault model, otherwise ignored)
  -f {zerobyte,zeroword,nop,flip,tamper,jump}, --faultmodel {zerobyte,zeroword,nop,flip,tamper,jump}
                        * zerobyte: sets the specified <address> byte to zero.
                        * zeroword: sets the specified <address> word to zero.
                        * nop: sets the specified <address> byte to the x86 NOP code (0x90).
                        * flip: flips the specified <address> byte's <bit>.
                        * tamper: changes the value of a byte to <value>.
                        * jump: sets the specified <address> jump to jump to <target> location.
  -i INFILE, --infile INFILE
                        the input file
  -o OUTFILE, --outfile OUTFILE
                        the output mutant file name
  -t TARGET, --target TARGET
                        the target relative address to jump to (required for jump fault model, otherwise ignored)
  -v [0-255], --value [0-255]
                        the value to set the byte to (required for tamper fault model only, otherwise ignored)
  -w [1-8], --wordsize [1-8]
                        the size (in bytes) of the word (required for zerobyte fault model only, otherwise ignored)



