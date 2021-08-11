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

def determineKey(message_in, key_length, expected_char_dist):
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

encoded_msg = "N UQQVM CAE FEMF PN OVREM QQ IUTQAQEQ, PAZA GAQMF MF OVREMF BBXVMYRNNRFVONE, R PVESMEOND NE SDRCHQAOVMF PNE YQGDNE QA GQKFB BYMAA, B CHQ VZGQERRDR OBY N MCXVONONA QUEQGM QM NZNXVER PR REQDGRZPUN, BBD RJRYCXB, ER B SAE M YQGDN YNUF REQDGRZGQ RY HY GQKFB-OVREM PGWA GQKFB BYMAA REGM RY VZTXRE, R BBEFUIQY EHECQVFND DGR B PAEDRECAAPR M R, BBDDGR Q R M YQGDN YNUF REQDGRZGQZQAFR GFMQM RY VZTXRE"

max_level = 10

keylenPt = guessKeylen(encoded_msg, max_level, NormalIC_pt)
keylenEn = guessKeylen(encoded_msg, max_level, NormalIC_en)

print(f'i guess that the key length is {keylenPt} if the text is in portuguese')
print(f'i guess that the key length is {keylenEn} if the text is in english')

keyPt = determineKey(encoded_msg, keylenPt, char_distribution_pt)
keyEn = determineKey(encoded_msg, keylenEn, char_distribution_en)

print(f'i guess the key is {keyPt} if the text is in portuguese')
print(f'i guess the key is {keyEn} if the text is in english')

decodedPt = decode(encoded_msg, keyPt)
decodedEn = decode(encoded_msg, keyEn)

print(f'the decoded portuguese message is {decodedPt}')
print(f'the decoded english message is {decodedEn}')
