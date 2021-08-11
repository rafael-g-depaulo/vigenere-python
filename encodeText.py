#! /usr/bin/python3

import sys
from vigenere import encode

# usage:
#  chmod +x encodeText.py
#  ./encodeText.py ./textToEncode.txt encriptionkey ./encodedText.txt

if __name__ == "__main__":
  inputFilename = sys.argv[1]
  key = sys.argv[2]
  outputFilename = sys.argv[3]

  print(f'Text to encode is in file: {inputFilename}')
  print(f'Key is: {key}')
  print(f'File to store encoded text is: {outputFilename}')

  inputFile = open(inputFilename, 'r', encoding='utf-8')
  messageStr = inputFile.read()
  inputFile.close()
  
  encodedText = encode(messageStr, key)
  outputFile = open(outputFilename, 'w', encoding='utf-8')
  outputFile.write(encodedText)
  outputFile.close()

  print(f'The encoded text has been written to {outputFilename}')
