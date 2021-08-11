#! /usr/bin/python3
from vigenere import decode

# alphabet with all valid chars
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

comAcentos = "ÄÅÁÂÀÃÉeËÈÍÎÏÌÖÓÔÒÕÜÚÛÇ"
semAcentos = "AAAAAAEEEEIIIIOOOOOUUUC"

# normal Indexes of Coincidence of languages
NormalIC_pt = 0.072723
NormalIC_en = 0.065601

# char distribuition for english and portuguese
char_distribution_pt = {
  'A': 0.1463,
  'B': 0.0104,
  'C': 0.0388,
  'D': 0.0499,
  'E': 0.1257,
  'F': 0.0102,
  'G': 0.0130,
  'H': 0.0128,
  'I': 0.0618,
  'J': 0.0040,
  'K': 0.0002,
  'L': 0.0278,
  'M': 0.0474,
  'N': 0.0505,
  'O': 0.1073,
  'P': 0.0252,
  'Q': 0.0120,
  'R': 0.0653,
  'S': 0.0781,
  'T': 0.0434,
  'U': 0.0463,
  'V': 0.0167,
  'W': 0.0001,
  'X': 0.0021,
  'Y': 0.0001,
  'Z': 0.0047,
}

char_distribution_en = {
  'A': 0.08167,
  'B': 0.01492,
  'C': 0.02782,
  'D': 0.04253,
  'E': 0.12702,
  'F': 0.02228,
  'G': 0.02015,
  'H': 0.06094,
  'I': 0.06966,
  'J': 0.00153,
  'K': 0.00772,
  'L': 0.04025,
  'M': 0.02406,
  'N': 0.06749,
  'O': 0.07507,
  'P': 0.01929,
  'Q': 0.00095,
  'R': 0.05987,
  'S': 0.06327,
  'T': 0.09056,
  'U': 0.02758,
  'V': 0.00978,
  'W': 0.02360,
  'X': 0.00150,
  'Y': 0.01974,
  'Z': 0.00074,
}

def processString(input_str):
  temp = input_str.upper()
  for i in range(len(comAcentos)):
    temp = temp.replace(comAcentos[i], semAcentos[i])
  res = ""
  for char in temp:
    if alphabet.find(char) != -1:
      res = res + char
  return res

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
  # process input and separate chars in groups by key_len
  message = processString(message_in)
  message_groups = groupChars(message, key_len)

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
  message = processString(message_in)
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
  message = processString(message_in)
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
