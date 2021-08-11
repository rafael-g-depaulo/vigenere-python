#! /usr/bin/python3

import sys
from vigenere import decode

# usage:
#  chmod +x decodeText.py
#  ./decodeText.py ./textToDecode.txt encriptionkey ./decodedText.txt

if __name__ == "__main__":
  inputFilename = sys.argv[1]
  key = sys.argv[2]
  outputFilename = sys.argv[3]

  print(f'Text to decode is in file: {inputFilename}')
  print(f'Key is: {key}')
  print(f'File to store decoded text is: {outputFilename}')

  inputFile = open(inputFilename, 'r', encoding='utf-8')
  messageStr = inputFile.read()
  inputFile.close()
  
  decodedText = decode(messageStr, key)
  outputFile = open(outputFilename, 'w', encoding='utf-8')
  outputFile.write(decodedText)
  outputFile.close()

  print(f'The decoded text has been written to {outputFilename}')
