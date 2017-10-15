#!/bin/python

"""
 Fault Injection Tool
 Authors:
 Licence:
"""

# Required imports
import mmap
import sys, getopt
import os.path
#import subprocess
#import random
#from subprocess import Popen,PIPE,STDOUT
#from joblib import Parallel, delayed
#import threading
import argparse

"""
 Fault Models
"""

"""
Enumerate the different Fault Model
	flipBit = 0
	zeroByte = 1
	zeroTwoByte = 2
	nopeByte = 3
	jmpAdress = 4
	jbeAdress = 5
"""
class FaultModel:
  zeroByte = 0
  zeroTwoByte = 1
  nopeByte = 2
  flipBit = 3
  bytechange = 4
  jmpAdress = 5
  jbeAdress = 6


"""
Function ZeroByteFM(infile,outfile,position)
	*Geneate the mutant of the input object file by setting one byte to zero
	*Zero the "position" Byte
	*Create the Mutant as outfile
"""
def ZeroByteFM(infile,outfile,position):
  with file(infile, 'r+b') as fh:
    data =fh.read()
    store = open(outfile, 'wb')
    store.write(data)
    store.seek(int(position))
    store.write(b'\x00')
    store.close()

"""
Function ZeroOneWordFM(infile,outfile,position)
	*Geneate the mutant of the input object file by setting eight consecutive bytes to zero
	*Zero the eight bytes starting from position
	*Create the Mutant as outfile
"""
def ZeroOneWordFM(infile,outfile,position):
  with open(infile, "r+b") as f:
    mm = mmap.mmap(f.fileno(), 0)
    values = bytearray(mm)
    values[int(position)]=0x00
    values[int(position)+1]=0x00
    values[int(position)+2]=0x00
    values[int(position)+3]=0x00
    values[int(position)+4]=0x00
    values[int(position)+5]=0x00
    values[int(position)+6]=0x00
    values[int(position)+7]=0x00
    store = open(outfile, 'wb')
    store.write(values)
    store.close()
    mm.close()


"""
Function NopByteFM(infile,outfile,position)
	*Geneate the mutant of the input object file by setting the byte at position to 0x90
	*Nop the "position" Byte 
	*Create the Mutant as outfile
"""
def NopByteFM(infile,outfile,position):
  with file(infile, 'r+b') as fh:
    data =fh.read()
    store = open(outfile, 'wb')
    store.write(data)
    store.seek(int(position))
    store.write(b'\x90')
    store.close()

 
"""
Function FlipBitFM(infile,outfile,position,subposition)
	*Geneate the mutant of the input object file by flipping a bit 
	*flip the "subposition" bit in the "position" Byte
	*Create the Mutant as outfile
"""
def FlipBitFM(infile,outfile,position,subposition):
  values = []
  with open(infile, "r+b") as f:
    mm = mmap.mmap(f.fileno(), 0)
    values = bytearray(mm)
    mask = 1 << (7-int(subposition))
    values[int(position)] = values[int(position)] ^ mask
    store = open(outfile, 'wb')
    store.write(values)
    store.close()
    mm.close()


"""
Function ByteChangeFM(infile,outfile,position,value)
	*Geneate the mutant of the input object file by changing the byte
	*at position to be value
	*Create the Mutant as outfile
"""
def ByteChangeFM(infile,outfile,position,value):
  values = []
  with open(infile, "r+b") as f:
    mm = mmap.mmap(f.fileno(), 0)
    values = bytearray(mm)
    values[int(position)] = int(value)
    store = open(outfile, 'wb')
    store.write(values)
    store.close()
    mm.close()



"""
Function JMPFM(infile,outfile,position,target)
	* Generate the mutant of the input object file by changing the target
	* of the jump at position to go to target
	*Create the Mutant as outfile
"""
def JMPFM(infile,outfile,position,target):
  values=[]
  with open(infile, "r+b") as f:
    mm = mmap.mmap(f.fileno(), 0)
    data =f.read()
    values = bytearray(mm)
    if values[int(position)] == 0xEB:
      values[int(position)+1]=int(target)
    elif values[int(position)] == 0xE9: 
      position=int(position)
      JumpAdress=int(target)
      JumpAdress=hex(JumpAdress-5)
      JumpAdress=getHexValue(str(JumpAdress))
      Byte=SeparateValue(JumpAdress) 
      for i in range(0,4):
        if (i < len(Byte)):
          values[position+i+1]=int(Byte[i],16)
        else:
          values[position+i+1]=0x00
    elif (values[int(position)] == 0x76):
      values[int(position)+2]=int(target)
    elif ((values[int(position)] == 0x0F) and (values[int(position)+1] == 0x86)): 
      position=int(position)
      JumpAdress=int(target)
      JumpAdress=hex(JumpAdress-5)
      JumpAdress=getHexValue(str(JumpAdress))
      Byte=SeparateValue(JumpAdress) 
      for i in range(0,4):
        if (i < len(Byte)):
          values[position+i+2]=int(Byte[i],16)
        else:
          values[position+i+2]=0x00
    else:
      print("Jump address badly specified!")
      mm.close()
    store = open(outfile, 'wb')
    store.write(values)
    store.close()
    mm.close()


"""
  Supporting functions
"""

"""
  * Splits a string of hex values into a array of bytes
"""
def SeparateValue(string):
  Byte=[]
  i = len(string)
  while (i >= 0):
    if (i-2 < 0):
      Byte.append("0x0"+string[i-1:i])
    else:
      Byte.append("0x"+string[i-2:i])
    i=i-2
  #Byte = [string[i:i+2] for i in range(len(string),0,2)]
  return Byte

"""
  * strips the "0x" from string representations of hex values
"""
def getHexValue(string):
  for i in range(0, len(string)):
    if string[i] == "x":
      return string[i+1:len(string)]
  return ""



"""
Function GenerateMutant(filename.o,  faultmodel, position, subposition)
	*Based on the choosen fault model call the specific function to generate the mutant 
"""
def GenerateMutant(filename, faultmodel, position, subposition, flag):
  if faultmodel == FaultModel.flipBit:
    #call flip one bit fault model
    FlipBitFM(filename,position,subposition,flag)
  if faultmodel == FaultModel.zeroByte:
    #call zero one byte fault model
    ZeroByteFM(filename,position,flag)
  if faultmodel == FaultModel.zeroTwoByte:
    #call zero one word fault model
    ZeroOneWordFM(filename,position,flag)
  if faultmodel == FaultModel.nopeByte:
    #call Nop one byte  fault model
    NopByteFM(filename,position,flag)
  if faultmodel == FaultModel.jmpAdress:
    #call JMP address modification fault model
    JMPFM(filename,position,subposition,flag)
  if faultmodel == FaultModel.jbeAdress: 
    #call JBE address modification fault model
    JBEFM(filename,position,subposition,flag)
  if faultmodel == FaultModel.bytechange: 
    #call JBE address modification fault model
    ByteChangeFM(filename,position,subposition,flag)




"""
  FOLLOWING FUNCTIONS NOT USED, BUT LEFT FOR REFERENCE/FUTURE USE
"""

"""
FindJumpAdress(filename,  start, size)
	*Takes as an entry the file name and the .text position in the file 
	*Parse the file looking for the jump instruction
	*return a list containing the location of the jump instruction
"""
def FindJumpAdress(filename,  start, size):
  JumpAddres = []
  with open(filename, "r+b") as f:
    mm = mmap.mmap(f.fileno(), 0)
    data =f.read()
    values = bytearray(mm)
    j=0
    while (j<=size) :
      if ((values[int(start)+j] == 0xEB) | (values[int(start)+j] == 0xE9) | (values[int(start)+j] == 0x76)):
        JumpAddres.append(start+j)
      if ((values[int(start)+j] == 0x0F) & (values[int(start)+j+1] == 0x86)):
        JumpAddres.append(start+j)
      j=j+1
  mm.close()
  return JumpAddres


"""
  Main functionality
"""

parser = argparse.ArgumentParser(description='Fault injection tool')
parser.add_argument('-f','--faultmodel', choices=['zerobyte','zeroword','nop','flip','tamper','jump'], metavar='', help=
    '''
    * zerobyte: sets the specified <address> byte to zero.\
    * zeroword: sets the specified <address> word to zero.\
    * nop: sets the specified <address> byte to the x86 NOP code (0x90).\
    * flip: flips the specified <address> byte\'s <bit>.\
    * tamper: changes the value of a byte to <value>.\
    * jump: sets the specified <address> jump to jump to <target> location.'''
    , required=True)
parser.add_argument('-a','--address',  help='<address>: \n'
                    'the address to implement the fault injection in the <binary>', required=True)
parser.add_argument('-b','--bit', type=int, choices=range(0,7) , metavar='', help='<bit> (required for flip fault model, otherwise ignored): \n '
                    'the bit of the byte to flip (0-7)', required=False)
parser.add_argument('-t','--target', type=int, metavar='', help='<target> (required for jump fault model, otherwise ignored):\n'
                    'the target relative address to jump to', required=False)
parser.add_argument('-v','--value', choices=range(0,255), type=int, metavar='', help='<value> (required for tamper fault model only, otherwise ignored):\n'
                    'the value to set the byte to', required=False)
parser.add_argument('-o','--outfile', metavar='', help='<outfile>: \n'
                    'the output mutant file name', required=True)
parser.add_argument('-i','--binary', metavar='', help='the input binary file', required=True)
args=parser.parse_args()



if __name__ == "__main__":
  inpufile = args.binary
  outputfile = args.outfile
  faultmodel = args.faultmodel
  address = args.address
  bit = args.bit
  target = args.target
  value = args.value
  answer = 1
  values=[]
  
  if (os.path.exists(inpufile)):
    with open(inpufile, "r+b") as f:
      mm = mmap.mmap(f.fileno(), 0)
      values = bytearray(mm)
      sizefile=len(values)
    if ( os.path.exists(outputfile) ):
      response = raw_input("The output file "+outputfile+" already exists. Do you want to overwrite it [y/n]?)").lower().strip()
      if (response == 'n'):
        exit(0)
    else :
      if faultmodel == 'zerobyte':
        # check that address is valid here
        ZeroByteFM(inpufile,outputfile,address)
        print "create the file"
      elif faultmodel == 'zeroword':
        # check that address is valid here
        ZeroOneWordFM(inpufile,outputfile,address)
      elif faultmodel == 'nop':
        # check that address is valid here
        NopByteFM(inpufile,outputfile,address)
      elif faultmodel == 'flip':
        # check that address is valid here
        # check that bit is valid here
        FlipBitFM(inpufile,outputfile,address,bit)
      elif faultmodel == 'tamper':
        # check that address is valid here
        # check that value is valid here
        ByteChangeFM(inpufile,outputfile,address,value)
      elif faultmodel == 'jump':
        # check that address is valid here
        # check that target is valid here
        JMPFM(inpufile,outputfile,address,target)
  else:
    if (not os.path.exists(inpufile)):
      print("The inputfile "+inpufile+" not found, aborting.")
      exit(4)

