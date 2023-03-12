from PIL import Image, ImageDraw, ImageFont
import textwrap
import csv

def add_front_text(canvas, texts):
  draw = ImageDraw.Draw(canvas)
  # set base margin
  y = canvas.height - 30

  # wrap texts and get starting y
  for text in texts:
    font = ImageFont.truetype("fonts/TiltWarp-Regular.ttf", text['size'])
    text['font'] = font
    wrapper = textwrap.TextWrapper(width=text['width'])
    wrapped_text = wrapper.wrap(text['text'])
    text['wrapped_text'] = wrapped_text
    y -= font.getsize(text['text'])[1] * len(wrapped_text)
    y -= text['margin_bottom']

  # print each set of text
  for text in texts:
    # Set the font type and size for the name
    font = text['font']

    # Get wrapped text
    wrapped_text = text['wrapped_text']

    # Calculate the x and y coordinates for the text to be centered
    text_widths = [draw.textsize(line, font=font)[0] for line in wrapped_text]
    max_text_width = max(text_widths)
    x = (canvas.width - max_text_width) / 2

    # Draw the wrapped text on the image at the centered position
    for line in wrapped_text:
      line_width = draw.textsize(line, font=font)[0]
      x_pos = (canvas.width - line_width) / 2
      draw.text((x_pos, y), line, fill=(255, 255, 255), font=font)
      y += font.getsize(line)[1]
    
    # adjust y for margin
    y += text['margin_bottom']

def add_stars(canvas, years):
  star = Image.open("materials/star.png")
  paste_alpha = star.split()[-1]
  for i in range(years):
    x = 450 - ((i % 6) * 35)
    y = 37 - (i // 6) * 30
    canvas.paste(star, (x, y), mask=paste_alpha)

def set_border_color(path, new_color):
  image = Image.open(path)

  # Convert image to RGB mode if it's in grayscale mode
  if image.mode == 'L':
    image = image.convert("RGB")

  # Replace the pixels of the original image with the new color
  width, height = image.size
  for x in range(width):
    for y in range(height):
      pixel = image.getpixel((x, y))
      if pixel[3] != 0:
        image.putpixel((x, y), new_color)
  
  return image

def add_back_text(canvas, info):
  draw = ImageDraw.Draw(canvas)

  # set starting point
  y = 150

  for pair in info:
    title = pair['title']
    title_font = ImageFont.truetype("fonts/TiltWarp-Regular.ttf", 38)
    title_wrapper = textwrap.TextWrapper(width=25)
    title_wrapped_text = title_wrapper.wrap(title)

    text = pair['text']
    text_font = ImageFont.truetype("fonts/TiltWarp-Regular.ttf", 22)
    text_wrapper = textwrap.TextWrapper(width=40)
    text_wrapped_text = text_wrapper.wrap(text)

    for line in title_wrapped_text:
      line_width = draw.textsize(line, font=title_font)[0]
      x_pos = (canvas.width - line_width) / 2
      draw.text((x_pos, y), line, fill=(255, 255, 255), font=title_font)
      y += title_font.getsize(line)[1]
    # margin below title
    y += 5

    for line in text_wrapped_text:
      line_width = draw.textsize(line, font=text_font)[0]
      x_pos = (canvas.width - line_width) / 2
      draw.text((x_pos, y), line, fill=(255, 255, 255), font=text_font)
      y += text_font.getsize(line)[1]
    # margin below text
    y += 15
    
def add_print_border(card, color):
  canvas = Image.new("RGB", (666, 915), color=color)

  # add the print border
  border = Image.open("materials/print-border.png")
  paste_alpha = border.split()[-1]
  canvas.paste(border, (0, 0), mask=paste_alpha)

  # add the card
  canvas.paste(card, ((666 - 500) // 2, (915 - 700) // 2))

  return canvas


def read_csv_file():
  data = []
  with open('data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')

    # consume the first row (header)
    header = next(reader)

    # Iterate through subsequent rows
    for row in reader:
      positions = row[2].split('; ')
      data.append({
        "img": row[0],
        "name": row[1],
        "positions": positions,
        "years": row[3],
        "department": row[4],
        "info": [
         {
          "title": row[5],
          "text": row[6]
         },
         {
          "title": row[7],
          "text": row[8]
         },
         {
          "title": row[9],
          "text": row[10]
         },
         {
          "title": row[11],
          "text": row[12]
         },
        ]
      })
  return data