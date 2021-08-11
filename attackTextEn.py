#! /usr/bin/python3

import sys

from vigenere import decode
from attack import guessKeylen, guessKey
from constants import NormalIC_en, char_distribution_en

# usage:
#  chmod +x attackTextEn.py
#  ./attackTextEn.py 15 ./englishCodedText.txt ./crackedText.txt

if __name__ == "__main__":
  max_level = int(sys.argv[1])
  inputFilename = sys.argv[2]
  outputFilename = sys.argv[3]

  inputFile = open(inputFilename, 'r', encoding='utf-8')
  encodedMessage = inputFile.read()
  inputFile.close()
  
  print(f'Encoded is in file: {inputFilename}')
  print(f'File to store decoded text is: {outputFilename}')

  keylen = guessKeylen(encodedMessage, max_level, NormalIC_en)
  print(f'i guess that the key length is {keylen}.')

  key = guessKey(encodedMessage, keylen, char_distribution_en)
  print(f'i guess that the key is {key}.')

  decodedText = decode(encodedMessage, key)
  outputFile = open(outputFilename, 'w', encoding='utf-8')
  outputFile.write(decodedText)
  outputFile.close()
  
  print(f'The text from {inputFilename} has been decoded using {key} and the result was written to {outputFilename}')
