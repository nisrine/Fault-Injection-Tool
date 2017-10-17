#!/bin/python

"""
 Fault Injection Tool
 Authors: Nisrine jafri, Thomas Given-Wilson
 Contact: nisrine.jafro@inria.fr 
"""

# Required imports
import mmap
import sys, getopt
import os.path
import argparse
from argparse import RawTextHelpFormatter,SUPPRESS

"""
 Fault Models Functions
"""

"""
Function ZeroByteFM(infile,outfile,position)
	* Geneate the mutant of the input object file by setting one byte to zero
	* Zero the "position" Byte
	* Create the Mutant as outfile
"""
def ZeroByteFM(values,outfile,position):
  values[int(position)]=0x00
  store = open(outfile, 'wb')
  store.write(values)
  store.close()


"""
Function ZeroOneWordFM(infile,outfile,position,wordsize)
	* Geneate the mutant of the input object file by setting eight consecutive bytes to zero
	* Zero the wordsize number of bytes starting from position
	* Create the Mutant as outfile
"""
def ZeroOneWordFM(values,outfile,position,wordsize):
  for i in range(0,wordsize):
    values[int(position)+i]=0x00
  store = open(outfile, 'wb')
  store.write(values)
  store.close()


"""
Function NopByteFM(infile,outfile,position)
	* Geneate the mutant of the input object file by setting the byte at position to 0x90
	* Nop the "position" Byte 
	* Create the Mutant as outfile
"""
def NopByteFM(values,outfile,position):
  values[int(position)]=0x90
  store = open(outfile, 'wb')
  store.write(values)
  store.close()

 
"""
Function FlipBitFM(infile,outfile,position,subposition)
	* Geneate the mutant of the input object file by flipping a bit 
	* flip the "subposition" bit in the "position" Byte
	* Create the Mutant as outfile
"""
def FlipBitFM(values,outfile,position,subposition):
  mask = 1 << (7-int(subposition))
  values[int(position)] = values[int(position)] ^ mask
  store = open(outfile, 'wb')
  store.write(values)
  store.close()


"""
Function ByteChangeFM(infile,outfile,position,value)
	* Geneate the mutant of the input object file by changing the byte
	* at position to be value
	* Create the Mutant as outfile
"""
def ByteChangeFM(values,outfile,position,value):
  values[int(position)] = int(value)
  store = open(outfile, 'wb')
  store.write(values)
  store.close()


"""
Function JMPFM(infile,outfile,position,target)
	* Generate the mutant of the input object file by changing the target
	* of the jump at position to go to target
	* Create the Mutant as outfile
"""
def JMPFM(values,outfile,position,target):
    if (values[int(position)] == 0xEB) or (values[int(position)] == 0x76):
      # check the value of the target
      if (target > 127 or target < -128):
        print "Invalid value for jump target type "+str(values[int(position)])+", must be in range [-128,127]"
        exit(11)
      abstarget = position + target
      if (abstarget < 0 or abstarget >= len(values)):
        print "Invalid absolute target for jump ("+ str(abstarget) +")"
        exit(12)
      values[int(position)+1]=int(target)
    elif values[int(position)] == 0xE9:
      if (target > 2147483647 or target < -2147483648):
        print "Invalid value for jump target type 0xE9, must be in range [-2147483648,2147483647]"
        exit(11)
      abstarget = position + target
      if (abstarget < 0 or abstarget >= len(values)):
        print "Invalid absolute target for jump ("+ str(abstarget) +")"
        exit(12)
      # Note that disassembly may offset by 5 to account for EIP!
      # Add the following line if you wish to use disassembly instead of true values
      # Alternatively, comment out the following line to use true values of disassembly values
      # target = target - 5
      bytes=SeparateValue(getHexValue(str(target)))
      for i in range(0,4):
        if (i < len(bytes)):
          values[position+i+1]=int(bytes[i],16)
        else:
          values[position+i+1]=0x00
    elif ((values[int(position)] == 0x0F) and (values[int(position)+1] == 0x86)): 
      if (target > 2147483647 or target < -2147483648):
        print "Invalid value for jump target type 0x0F86, must be in range [-2147483648,2147483647]"
        exit(11)
      abstarget = position + target
      if (abstarget < 0 or abstarget >= len(values)):
        print "Invalid absolute target for jump ("+ str(abstarget) +")"
        exit(12)
      # Note that disassembly may offset by 5 to account for EIP!
      # Add the following line if you wish to use disassembly instead of true values
      # Alternatively, comment out the following line to use true values of disassembly values
      # target = target - 5
      bytes=SeparateValue(getHexValue(str(target)))
      for i in range(0,4):
        if (i < len(bytes)):
          values[position+i+2]=int(bytes[i],16)
        else:
          values[position+i+2]=0x00
    else:
      print("Address is not a valid jump instruction, supported instructions are 0xEB, 0x76, 0xE9, and 0x0F86")
      exit(13)
    store = open(outfile, 'wb')
    store.write(values)
    store.close()



"""
  Supporting functions
"""

"""
  * Splits a string of hex values into a array of bytes
"""
def SeparateValue(string):
  bytes=[]
  i = len(string)
  while (i >= 0):
    if (i-2 < 0):
      bytes.append("0x0"+string[i-1:i])
    else:
      bytes.append("0x"+string[i-2:i])
    i=i-2
  return bytes

"""
  * strips the "0x" from string representations of hex values
"""
def getHexValue(string):
  for i in range(0, len(string)):
    if string[i] == "x":
      return string[i+1:len(string)]
  return ""


"""
  FOLLOWING FUNCTIONS NOT USED, BUT LEFT FOR REFERENCE/FUTURE USE
"""

"""
FindJumpAdress(filename,  start, size)
	*Takes as an entry the file name and the .text position in the file 
	*Parse the file looking for the jump instruction
	*return a list containing the location of the jump instruction
"""
def FindJumpAdress(values):
  JumpAddresses = []
  j=0
  while (j < len(values)-1):
      if (values[j] == 0xEB) or (values[j] == 0xE9) or (values[j] == 0x76):
         JumpAddresses.append(int(j))
      if (values[j] == 0x0F) and (values[j+1] == 0x86):
         JumpAddresses.append(int(j))
      j=j+1
  return JumpAddresses


"""
  Main functionality
"""

parser = argparse.ArgumentParser(description='Fault injection tool\nUsage:\tfaultinject.py [-h] -f {zerobyte,zeroword,nop,flip,tamper,jump} -a ADDRESS [-b [0-7]] [-t TARGET] [-v [0-255]] -o OUTFILE -i INFILE', formatter_class=RawTextHelpFormatter, usage=SUPPRESS)
parser.add_argument('-a','--address', type=int, help='the address to implement the fault injection in the input file', required=True)
parser.add_argument('-b','--bit', type=int, choices=range(0,8) , metavar='[0-7]',  help='the bit of the byte to flip (required for flip fault model, otherwise ignored)', required=False)
parser.add_argument('-f','--faultmodel', choices=['zerobyte','zeroword','nop','flip','tamper','jump'],  help="* zerobyte: sets the specified <address> byte to zero.\n* zeroword: sets the specified <address> word to zero.\n* nop: sets the specified <address> byte to the x86 NOP code (0x90).\n* flip: flips the specified <address> byte\'s <bit>.\n* tamper: changes the value of a byte to <value>.\n* jump: sets the specified <address> jump to jump to <target> location.", required=True)
parser.add_argument('-i','--infile', type=str, metavar='INFILE', help='the input file', required=True)
parser.add_argument('-o','--outfile', help='the output mutant file name', required=True)
parser.add_argument('-t','--target', type=int, help='the target relative address to jump to (required for jump fault model, otherwise ignored)', required=False)
parser.add_argument('-v','--value', choices=range(0,256), type=int, metavar='[0-255]', help='the value to set the byte to (required for tamper fault model only, otherwise ignored)', required=False)
parser.add_argument('-w','--wordsize', choices=range(1,9), type=int, metavar='[1-8]', help='the size (in bytes) of the word (required for zerobyte fault model only, otherwise ignored)', required=False)
args=parser.parse_args()



if __name__ == "__main__":
  inpufile = args.infile
  outputfile = args.outfile
  faultmodel = args.faultmodel
  address = args.address
  bit = args.bit
  target = args.target
  value = args.value
  wordsize = args.wordsize
  binaryfile=[]
  
  if (os.path.exists(inpufile)):
    # Input file exits we can proceed, check it is readable
    with open(inpufile, "r+b") as f:
      mm = mmap.mmap(f.fileno(), 0)
      binaryfile = bytearray(mm)
      sizefile=len(binaryfile)
    if ( os.path.exists(outputfile) ):
      # If output file exists, confirm overwrite, or abort
      proceed=False
      while(not proceed):
        response = raw_input("The output file "+outputfile+" already exists. Do you want to overwrite it [y/n]?)").lower().strip()
        if (response == 'n'):
          exit(0)
        elif (response == 'y'):
          proceed = True
    # Sanity check address
    if not (address >= 0 and address <= sizefile):
      # invalid address specified
      print('Address '+str(address)+' out of valid range (0-'+str(sizefile)+')')
      exit(5)
    if faultmodel == 'zerobyte':
        # check that address is valid here
        ZeroByteFM(binaryfile,outputfile,address)
    elif faultmodel == 'zeroword':
        # check that address is valid here
        if wordsize == None:
          print('Requires -w/--wordsize [1-8] argument')
          exit(9)
        ZeroOneWordFM(binaryfile,outputfile,address,wordsize)
    elif faultmodel == 'nop':
        # check that address is valid here
        NopByteFM(binaryfile,outputfile,address)
    elif faultmodel == 'flip':
        # check that address is valid here
        if bit == None:
          print('Requires -b/--bit [0-7] argument')
          exit(6)
        # check that bit is valid here
        FlipBitFM(binaryfile,outputfile,address,bit)
    elif faultmodel == 'tamper':
        # check that address is valid here
        if value == None:
          print('Requires -v/--value [0-255] argument')
          exit(7)
        # check that value is valid here
        ByteChangeFM(binaryfile,outputfile,address,value)
    elif faultmodel == 'jump':
        # check that address is valid here
        if target == None:
          print('Requires -t/--target argument')
          exit(8)
        # check that target is valid here
        JMPFM(binaryfile,outputfile,address,target)
  else:
    if (not os.path.exists(inpufile)):
      print("The inputfile "+inpufile+" not found, aborting.")
      exit(4)

