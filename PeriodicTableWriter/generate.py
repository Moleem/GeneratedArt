ELEMENTS_FILE_NAME = 'periodic_table.csv'
WORD_LIST_FILE_NAME = 'word_list.txt'

ELEMENTS = list()
WORDS = list()

def read_elements():
  with open(ELEMENTS_FILE_NAME, 'r') as element_file:
    for line in element_file:
      atomic_number, element, symbol, atomic_mass, _ = line.split(',', 4)
      ELEMENTS.append({
        'atomic_number': atomic_number.strip(),
        'element': element.strip(),
        'symbol': symbol.strip().lower(),
        'atomic_mass': atomic_mass.strip()
      })
  
  # sorting elements by descending length,
  # so longer element symbols deserve priority
  ELEMENTS.sort(reverse=True, key=lambda e: len(e['symbol']))

def read_words():
  with open(WORD_LIST_FILE_NAME, 'r') as word_file:
    for line in word_file:
      WORDS.append(line.strip())

def generate_element_word(word):
  results = list()

  while word != '':
    start_element = next(
      (element['symbol'] for element in ELEMENTS
      if word.startswith(element['symbol'])),
      None
    )
    
    if start_element is not None:
      results.append(start_element)
      word = word[len(start_element):]
    else:
      raise Exception('Invalid word: {}'.format(word))
  
  return results

def generate_element_words():
  for word in WORDS:
    yield generate_element_word(word)

def main():
  read_elements()
  read_words()
  element_words = list(generate_element_words())
  print(element_words)

if __name__ == '__main__':
  main()