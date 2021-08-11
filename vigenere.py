#! /usr/bin/python3
import math
from constants import alphabet, comAcentos, semAcentos
from strUtils import processString

def encode(message, key):
  message_str = processString(message)
  key_str = processString(key)
  key_len = len(key_str)
  encoded_message = []

  # encode message
  key_i = 0
  for i in range(len(message_str)):
    # if char isn't in alphabet, add it unchanged
    if (alphabet.find(message_str[i]) == -1):
      encoded_message.append(message_str[i])
      continue
    
    # transform message and key characters to number (a -> 0, z -> 25)
    mchar_num = alphabet.find(message_str[i])
    kchar_num = alphabet.find(key_str[key_i % key_len])
    key_i += 1

    # calculate encoded char
    encoded_num = (mchar_num - kchar_num) % len(alphabet)
    encoded_char = alphabet[encoded_num]

    # add to message
    encoded_message.append(encoded_char)

  # transform encoded message from array to string, and return
  encoded_str = "".join(encoded_message)
  return encoded_str

def decode(message, key):
  message_str = processString(message)
  key_str = processString(key)
  key_len = len(key_str)
  decoded_message = []

  # decode message
  key_i = 0
  for i in range(len(message_str)):
    # if char isn't in alphabet, add it unchanged
    if (alphabet.find(message_str[i]) == -1):
      decoded_message.append(message_str[i])
      continue
    
    # transform message and key characters to number (a -> 0, z -> 25)
    mchar_num = alphabet.find(message_str[i])
    kchar_num = alphabet.find(key_str[key_i % key_len])
    key_i += 1

    # calculate decoded char
    decoded_num = (mchar_num + kchar_num) % len(alphabet)
    decoded_char = alphabet[decoded_num]

    # add to message
    decoded_message.append(decoded_char)

  # transform decoded message from array to string, and return
  decoded_str = "".join(decoded_message)
  return decoded_str
