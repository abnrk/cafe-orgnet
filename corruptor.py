import os
import random
import tempfile

def bit_not(n, numbits=8):
    return (1 << numbits) - 1 - n

def corrupt(data, level, skip, amount, intensity, expression="randByte()"):
  #fp = tempfile.TemporaryFile()
  #fp.write(data)
  #fileSize = len(fp.read())
  data = list(data)
  fileSize = len(data)
  repeat = 10 * level
  not_intensity = bit_not(intensity)
  print(not_intensity)
  for i in range(amount):
    rand = random.randint(skip,int(fileSize)-1)
    if random.randint(0,not_intensity) < level:
      oldByte = data[rand]
      newByte = evalByte(oldByte, i, expression)
      #fp.write(newByte)
      data[rand] = list(newByte)[0]
    print("Corrupting... " + "(" + str(i) + "/" + str(amount) + ")")
  #fp.seek(0)
  #newData = fp.read()
  newData = bytes(data)
  #fp.close()
  return newData

def evalByte(byte, t, expression):
  return bytes([eval(expression)])

def randByte():
  return random.randint(0,255)

def getCorruptedByte(byte, operand=0, mode="#"):
  if mode == "#":
    return bytes([random.randint(0,255)])
  if mode == "+":
    return bytes([(byte+operand)%256])
  if mode == "-":
    return bytes([(byte-operand)%256])
  if mode == "*":
    return bytes([(byte*operand)%256])
  if mode == "/":
    return bytes([(byte/operand)%256])
  if mode == "<<":
    return bytes([(byte<<operand)%256])
  if mode == ">>":
    return bytes([(byte>>operand)%256])
  if mode == "^":
    return bytes([(byte^operand)%256])
  if mode == "&":
    return bytes([(byte&operand)%256])
  if mode == "|":
    return bytes([(byte|operand)%256])
  if mode == "~":
    return bytes([bit_not(byte,8)])
  if mode == "%":
    return bytes([(byte%operand)%256])