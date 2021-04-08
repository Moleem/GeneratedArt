from PIL import Image, ImageDraw, ImageFont

ELEMENTS_FILE_NAME = 'periodic_table.csv'
WORD_LIST_FILE_NAME = 'word_list.txt'

CANVAS_W, CANVAS_H = 4000, 1000
CANVAS_BG = 'orange'

ELEMENT_W, ELEMENT_H = 700, 800
ELEMENT_GAP = 50
ELEMENT_BORDER_W = 50
ELEMENT_BORDER_BG = 'black'
ELEMENT_BG = 'white'

TEXT_FONT_TYPE = '/usr/share/fonts/freefont/FreeSansBold.ttf'
TEXT_SIZE_SMALL = 100
TEXT_SIZE_LARGE = 300
TEXT_FONT_SMALL = ImageFont.truetype(TEXT_FONT_TYPE, TEXT_SIZE_SMALL)
TEXT_FONT_LARGE = ImageFont.truetype(TEXT_FONT_TYPE, TEXT_SIZE_LARGE)
TEXT_MARGIN = 70
TEXT_PADDING = 10
TEXT_COLOR = 'black'

ELEMENTS = list()
WORDS = list()

def read_elements():
  with open(ELEMENTS_FILE_NAME, 'r') as element_file:
    for line in element_file:
      atomic_number, element, symbol, atomic_mass, _ = line.split(',', 4)
      ELEMENTS.append({
        'atomic_number': atomic_number.strip(),
        'name': element.strip(),
        'symbol': symbol.strip(),
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
      (element for element in ELEMENTS
      if word.startswith(element['symbol'].lower())),
      None
    )
    
    if start_element is not None:
      results.append(start_element)
      word = word[len(start_element['symbol']):]
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

def add_element_frame(start_x, start_y, img):
  img.rectangle(
    [start_x, start_y, ELEMENT_W + start_x, ELEMENT_H + start_y],
    fill=ELEMENT_BG, outline=ELEMENT_BORDER_BG, width=ELEMENT_BORDER_W
  )

def add_atomic_number(atomic_number, start_x, start_y, img):
  target_x = start_x + TEXT_MARGIN
  target_y = start_y + TEXT_MARGIN
  img.text((target_x, target_y), atomic_number, TEXT_COLOR, TEXT_FONT_SMALL)

def add_symbol(symbol, start_x, start_y, img):
  small_text_w, small_text_h = img.textsize(symbol, TEXT_FONT_SMALL)
  text_w, text_h = img.textsize(symbol, TEXT_FONT_LARGE)
  target_x = start_x + (ELEMENT_W-text_w)/2
  target_y = start_y + TEXT_MARGIN + small_text_h + TEXT_PADDING + (ELEMENT_H - 2*TEXT_MARGIN - 3*TEXT_PADDING - 3*small_text_h - text_h)/2
  
  img.text((target_x, target_y), symbol, TEXT_COLOR, TEXT_FONT_LARGE)

def add_name(name, start_x, start_y, img):
  text_w, text_h = img.textsize(name, TEXT_FONT_SMALL)
  target_x = start_x + (ELEMENT_W-text_w)/2
  target_y = start_y + ELEMENT_H - TEXT_MARGIN - 2*text_h - TEXT_PADDING
  img.text((target_x, target_y), name, TEXT_COLOR, TEXT_FONT_SMALL)

def add_atomic_mass(atomic_mass, start_x, start_y, img):
  text_w, text_h = img.textsize(atomic_mass, TEXT_FONT_SMALL)
  target_x = start_x + (ELEMENT_W-text_w)/2
  target_y = start_y + ELEMENT_H - TEXT_MARGIN - text_h
  img.text((target_x, target_y), atomic_mass, TEXT_COLOR, TEXT_FONT_SMALL)

def draw_element(start_x, start_y, element, canvas):
  element_img = ImageDraw.Draw(canvas)
  add_element_frame(start_x, start_y, element_img)
  print(element)  
  add_atomic_number(element['atomic_number'], start_x, start_y, element_img)
  add_symbol(element['symbol'], start_x, start_y, element_img)
  add_name(element['name'], start_x, start_y, element_img)
  add_atomic_mass(element['atomic_mass'], start_x, start_y, element_img)
  

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