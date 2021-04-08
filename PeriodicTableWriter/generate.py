from PIL import Image, ImageDraw, ImageFont

ELEMENTS_FILE_NAME = 'periodic_table.csv'
WORD_LIST_FILE_NAME = 'word_list.txt'

CANVAS_W, CANVAS_H = 4000, 1000
CANVAS_BG = 'orange'

ELEMENT_W, ELEMENT_H = 600, 800
ELEMENT_GAP = 100
ELEMENT_BORDER_W = 50
ELEMENT_BORDER_BG = 'black'
ELEMENT_BG = 'white'

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

def create_canvas():
  return Image.new('RGBA', (CANVAS_W, CANVAS_H), CANVAS_BG)

def draw_elements(elements, canvas):
  vertical_padding = (CANVAS_H - ELEMENT_H)/2
  elem_size = len(elements)
  initial_horizontal_padding = (
    CANVAS_W - (elem_size*ELEMENT_W + (elem_size-1)*ELEMENT_GAP)
  ) / 2

  for index, element in enumerate(elements):
    horizontal_padding = initial_horizontal_padding + index*(ELEMENT_W+ELEMENT_GAP)
    draw_element(horizontal_padding, vertical_padding, element, canvas)


def draw_element(start_x, start_y, element, canvas):
  element_frame = ImageDraw.Draw(canvas)
  element_frame.rectangle(
    [start_x, start_y, ELEMENT_W + start_x, ELEMENT_H + start_y],
    fill=ELEMENT_BG, outline=ELEMENT_BORDER_BG, width=ELEMENT_BORDER_W
  )


def generate_image(elements):
  canvas = create_canvas()
  draw_elements(elements, canvas)
  canvas.save('out.png')


def main():
  read_elements()
  read_words()
  element_words = list(generate_element_words())

  generate_image(generate_element_word('genius'))

if __name__ == '__main__':
  main()