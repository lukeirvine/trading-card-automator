from PIL import Image, ImageDraw, ImageFont
import textwrap
import csv
import os
from datetime import datetime

def add_front_text(canvas, texts, outline_color):
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
      fill_color = (255, 255, 255)
      width = 2
      # draw outline
      draw.text((x_pos + width, y), line, fill=outline_color, font=font)
      draw.text((x_pos - width, y), line, fill=outline_color, font=font)
      draw.text((x_pos, y + width), line, fill=outline_color, font=font)
      draw.text((x_pos, y - width), line, fill=outline_color, font=font)
      # draw main text
      draw.text((x_pos, y), line, fill=fill_color, font=font)
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
  y_start = 150
  y = y_start
  title_size = 30
  title_wrap_width = 25
  text_size = 22
  text_wrap_width = 40
  drawing = False
  done = False

  # this loop will shrink font sizes until everything fits on the card
  while not done:
    for pair in info:
      title = pair['title']
      title = title.upper()
      title_font = ImageFont.truetype("fonts/TiltWarp-Regular.ttf", title_size)
      title_wrapper = textwrap.TextWrapper(width=title_wrap_width)
      title_wrapped_text = title_wrapper.wrap(title)

      text = pair['text']
      text_font = ImageFont.truetype("fonts/TiltWarp-Regular.ttf", text_size)
      text_wrapper = textwrap.TextWrapper(width=text_wrap_width)
      text_wrapped_text = text_wrapper.wrap(text)

      for line in title_wrapped_text:
        line_width = draw.textsize(line, font=title_font)[0]
        x_pos = (canvas.width - line_width) / 2
        if drawing:
          draw.text((x_pos, y), line, fill=(255, 255, 255), font=title_font)
        y += title_font.getsize(line)[1]
      # margin below title
      y += 5

      for line in text_wrapped_text:
        line_width = draw.textsize(line, font=text_font)[0]
        x_pos = (canvas.width - line_width) / 2
        if drawing:
          draw.text((x_pos, y), line, fill=(255, 255, 255), font=text_font)
        y += text_font.getsize(line)[1]
      # margin below text
      y += 20
    # determine next action based on how low we went
    if drawing:
      done = True
    if y > 700:
      title_size -= 1
      title_wrap_width += 2
      text_size -= 2
      text_wrap_width += 5
    else:
      drawing = True
    # reset y
    y = y_start
    
def add_print_border(card, color, path):
  canvas = Image.new("RGB", (666, 915), color=color)

  # add the print border
  border = Image.open("materials/print-border.png")
  paste_alpha = border.split()[-1]
  canvas.paste(border, (0, 0), mask=paste_alpha)

  # add the card
  canvas.paste(card, ((666 - 500) // 2, (915 - 700) // 2))

  # add time
  font = ImageFont.truetype("fonts/PTMono-Regular.ttf", 13)
  draw = ImageDraw.Draw(canvas)
  now = datetime.now()
  formatted_time = now.strftime("%m/%d/%y  %I:%M:%S %p")
  time_width = draw.textsize(formatted_time, font=font)[0]
  time_height = font.getsize(formatted_time)[1]
  x = canvas.width - time_width - 10
  y = canvas.height - time_height - 10
  draw.text((x, y), formatted_time, fill=(0, 0, 0), font=font)

  # add file name
  draw.text((10, y), path, fill=(0, 0, 0), font=font)

  return canvas


def read_csv_file():
  data = []
  with open('staff.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')

    # consume the first row (header)
    header = next(reader)

    # Iterate through subsequent rows
    i = 0
    for row in reader:
      # check that years is an integer
      if not row[3].isdigit():
        raise RuntimeError(f"The value in the years column at row {i + 2} is not an integer.")
      try:
        positions = row[2].split('; ')
        data.append({
          "img": row[0],
          "name": row[1],
          "positions": positions,
          "years": int(row[3]),
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
      except IndexError:
        raise RuntimeError(f"Your csv file is missing some values on line {i + 2}. Check the readme file for required columns")
      i += 1
  return data

def check_data(data, border_colors):
  i = 0
  errors = []
  for card in data:
    # check that image exists
    img_path = card['img']
    if not os.path.exists('images/' + img_path):
      errors.append(f"IMAGE ERROR {i + 2}: The image \"{card['img']}\" for {card['name']} doesn't exist. Check line {i + 2} in the csv file.")
    
    # check that name is valid
    if "/" in card['name']:
      errors.append(f"The name column on row {i + 2} should not contain '/'")
    
    # check that years is 12 or less
    if card['years'] > 12:
      errors.append(f"12 is the maximum number of stars allowed. Check row {i + 2} in the csv file.")

    # check that department is valid
    if card['department'] not in border_colors:
      error = f"The department \"{card['department']}\" is not valid. Valid departments are:\n"
      for dep in border_colors.keys():
        error += dep + "\n"
      error += f"This error occurred in line {i + 2} of the csv file."
      errors.append(error)
    
    i += 1
  if len(errors) > 0:
    error_str = "\n"
    for error in errors:
      error_str = error_str + "\n" + error
    raise RuntimeError(f"There were {len(errors)} errors with your data:" + error_str)
  
def print_pdfs(folder_path, file_counts):
  print("\nSaving PDFs...")

  # create pdf folder path if it doesn't exist
  pdf_folder = f"{folder_path}/pdfs"
  if not os.path.exists(pdf_folder):
    os.makedirs(pdf_folder)

  pdf_path = f'{pdf_folder}/mivoden-trading-cards.pdf'
  pdf_rarity_path = f'{pdf_folder}/mivoden-trading-cards-with-rarity.pdf'

  # add images
  images = []
  rarity_images = []
  for file_prefix in file_counts.keys():
    front = Image.open(f"{file_prefix}_front.png")
    back = Image.open(f"{file_prefix}_back.png")
    images.append(front)
    images.append(back)
    for i in range(file_counts[file_prefix]):
      rarity_images.append(front)
      rarity_images.append(back)
  images[0].save(
    pdf_path, "PDF", resolution=100.0, save_all=True, append_images=images[1:]
  )
  rarity_images[0].save(
    pdf_rarity_path, "PDF" ,resolution=100.0, save_all=True, append_images=rarity_images[1:]
  )
  print("Print PDFs saved")