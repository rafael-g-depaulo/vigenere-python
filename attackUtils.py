
from constants import alphabet, comAcentos, semAcentos

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


def getChardistribution(occurences, total_chars):
  distributions = {}
  for char, occ in occurences.items():
    distributions[char] = occ / total_chars
  return distributions

def getChiSquaredScore(occurences, message_length, target_distribuition):
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
