from constants import comAcentos, semAcentos, alphabet

def processString(input_str):
  res = input_str.upper()
  for i in range(len(comAcentos)):
    res = res.replace(comAcentos[i], semAcentos[i])
  return res

def processStringAndRemoveNonLetters(input_str):
  processed = processString(input_str)
  res = ""
  for char in processed:
    if alphabet.find(char) != -1:
      res = res + char
  return res
