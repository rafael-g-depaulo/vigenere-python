#! /usr/bin/python3
from vigenere import decode
from constants import alphabet, comAcentos, semAcentos, NormalIC_en, NormalIC_pt, char_distribution_en, char_distribution_pt
from strUtils import processStringAndRemoveNonLetters

# separate message into groups by key char and return them
# example: "abcdefg" in 2 groups would result in { [0]: "aceg", [1]: "bdf" }
def groupChars(input_str, group_num):
  groups = {}
  for i in range(len(input_str)):
    groups[i % group_num] = groups.get(i % group_num, "") + input_str[i]
  return groups

# count the occurence of each char in string
def getOccurences(input_str):
  occurences = {}
  for char in input_str:
    occurences[char] = occurences.get(char, 0) + 1
  return occurences

def getCI(message_in, key_len):
  # separate chars in groups by key_len
  message_groups = groupChars(message_in, key_len)

  # create dictionaries and total numbers for all groups
  occurences = []
  totals = []
  for i in range(key_len): 
    occurences.append(getOccurences(message_groups[i]))
    totals.append(len(message_groups[i]))

  # calculate IC's for all groups and average them
  IC = [0] * key_len
  for i in range(key_len):
    for occ in occurences[i].values():
      IC[i] += occ * (occ - 1) / (totals[i] * (totals[i] - 1))
  
  IC_average = sum(IC) / key_len
  return IC_average


def getCILevels(message_in, max_level):
  # create a list of tuples (key_length, CI) for every length from 2 to max_level
  table = []
  for i in range(2, max_level):
    table.append((i, getCI(message_in, i)))
  return table

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

def getChardistribution(occurences, total_chars):
  distributions = {}
  for char, occ in occurences.items():
    distributions[char] = occ / total_chars
  return distributions

def getChiSquaredScore(occurences, message_length, target_distribuition):
# def getChiSquaredScore(given_distribuition, target_distribuition):
  chiSquaredScore = {}
  for char in target_distribuition.keys():
    expected_frequency = target_distribuition[char]
    expected_occ = expected_frequency * message_length
    char_occ = occurences.get(char, 0)
    occ_error = char_occ - expected_occ
    normalized_error = occ_error * occ_error / expected_occ
    chiSquaredScore[char] = normalized_error

  totalScore = 0
  for charScore in chiSquaredScore.values():
    totalScore += charScore

  return totalScore

def getOffsetCharOccurences(char_occurences, offset):
  offset_occurences = {}
  for char, occ in char_occurences.items():
    char_i = alphabet.find(char)
    offset_char = alphabet[(char_i + offset) % len(alphabet)]
    offset_occurences[offset_char] = occ
  return offset_occurences

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
