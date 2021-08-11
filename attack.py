#! /usr/bin/python3
from vigenere import decode
from constants import alphabet, NormalIC_en, NormalIC_pt, char_distribution_en, char_distribution_pt
from strUtils import processStringAndRemoveNonLetters
from attackUtils import groupChars, getOccurences, getCI, getCILevels, getChardistribution, getChiSquaredScore, getOffsetCharOccurences

def guessKeylen(message_in, max_level, target):
  message = processStringAndRemoveNonLetters(message_in)
  CI_levels = getCILevels(message, max_level)
  margins = []

  # check how close to target CI all guesses went
  for level, ci in CI_levels:
    margins.append((level, abs(target-ci)))

  # sort by closest to target, and return top result
  margins.sort(key=lambda x:x[1])
  keylenGuess = margins[0][0]
  return keylenGuess

def guessKey(message_in, key_length, expected_char_dist):
  # process input and separate chars into groups
  message = processStringAndRemoveNonLetters(message_in)
  groups = groupChars(message, key_length)

  # array of key characters
  keyArr = []

  # for every group of chars
  for i, group in groups.items():
    # get the occurences of characters in the group
    char_occurences = getOccurences(group)

    # iterate through the alphabet, and get the chi-square scores of each letter
    keyCharChances = []
    for offset in range(len(alphabet)):
      # compare how closely the char distribuition using this offset maps onto the expected distribuition 
      offsetOcc = getOffsetCharOccurences(char_occurences, offset)
      score = getChiSquaredScore(offsetOcc, len(message), expected_char_dist)
      keyCharChances.append((alphabet[offset], score))
      # print(f'[{i}] for character {offset} ({alphabet[offset]}) the chi-squared ccore is {score}')

    keyCharChances.sort(key=lambda x:x[1])
    # print(f'possible chars for position {i} of key: {keyCharChances}\n')
    keyArr.append(keyCharChances[0][0])
  
  keyGuess = "".join(keyArr)
  return keyGuess
