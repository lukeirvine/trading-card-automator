from PIL import Image, ImageDraw, ImageFont
import textwrap
import csv
import os
from datetime import datetime
import PyPDF2

CARD_WIDTH = 750
CARD_HEIGHT = 1050

PRINT_WIDTH = 825
PRINT_HEIGHT = 1125
  
from PIL import Image

def resize_and_crop_image(image, new_width, new_height):
  # Get the current width and height
  current_width, current_height = image.size

  # Calculate the aspect ratios
  current_aspect_ratio = current_width / current_height
  new_aspect_ratio = new_width / new_height

  # Calculate the scale factor to resize the image
  if new_aspect_ratio > current_aspect_ratio:
    scale_factor = new_height / current_height
  else:
    scale_factor = new_width / current_width

  # Calculate the new size with the preserved aspect ratio
  resized_width = int(current_width * scale_factor)
  resized_height = int(current_height * scale_factor)

  # Resize the image while maintaining the aspect ratio
  resized_image = image.resize((resized_width, resized_height), Image.ANTIALIAS)

  # Calculate the coordinates for cropping
  left = (resized_width - new_width) / 2
  top = (resized_height - new_height) / 2
  right = (resized_width + new_width) / 2
  bottom = (resized_height + new_height) / 2

  # Crop the image to the desired dimensions
  cropped_image = resized_image.crop((left, top, right, bottom))

  return cropped_image

def add_front_text(canvas, texts, outline_color):
  draw = ImageDraw.Draw(canvas)
  # set base margin
  y = canvas.height - 45

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
      width = 3
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
  star = star.resize((60, 60))
  paste_alpha = star.split()[-1]
  for i in range(years):
    x = 675 - ((i % 6) * 52)
    y = 55 - (i // 6) * 45
    canvas.paste(star, (x, y), mask=paste_alpha)

def set_border_color(path, new_color):
  image = Image.open(path)
  image = image.resize((CARD_WIDTH, CARD_HEIGHT))

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
  y_start = 225
  y = y_start
  title_size = 35
  title_wrap_width = 34
  text_size = 26
  text_wrap_width = 55
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
      y += 7

      for line in text_wrapped_text:
        line_width = draw.textsize(line, font=text_font)[0]
        x_pos = (canvas.width - line_width) / 2
        if drawing:
          draw.text((x_pos, y), line, fill=(255, 255, 255), font=text_font)
        y += text_font.getsize(line)[1]
      # margin below text
      y += 30
    # determine next action based on how low we went
    if drawing:
      done = True
    if y > PRINT_HEIGHT:
      title_size -= 1
      title_wrap_width += 2
      text_size -= 2
      text_wrap_width += 5
    else:
      drawing = True
    # reset y
    y = y_start
    
def add_print_border(card, color, path):
  canvas = Image.new("RGB", (PRINT_WIDTH, PRINT_HEIGHT), color=color)

  # add the print border
  border = Image.open("materials/print-border-5.png")
  border = border.resize((PRINT_WIDTH, PRINT_HEIGHT))
  paste_alpha = border.split()[-1]
  canvas.paste(border, (0, 0), mask=paste_alpha)

  # add the card
  canvas.paste(card, ((PRINT_WIDTH - CARD_WIDTH) // 2, (PRINT_HEIGHT - CARD_HEIGHT) // 2))

  # add time
  font = ImageFont.truetype("fonts/PTMono-Regular.ttf", 19)
  draw = ImageDraw.Draw(canvas)
  now = datetime.now()
  formatted_time = now.strftime("%m/%d/%y  %I:%M:%S %p")
  time_width = draw.textsize(formatted_time, font=font)[0]
  time_height = font.getsize(formatted_time)[1]
  x = canvas.width - time_width - 15
  y = canvas.height - time_height - 15
  # draw.text((x, y), formatted_time, fill=(0, 0, 0), font=font)

  # add file name
  # draw.text((15, y), path, fill=(0, 0, 0), font=font)

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

def save_image(output, folder_path, file_counts):
  # make name lowercase with underscores
  name = output['name'].lower().replace(" ", "_")

  # set frequency
  frequency = 1
  years = output["years"]
  # 8 or more years
  if years >= 8:
    frequency = 1
  # 6 or 7 years
  elif years >= 6:
    frequency = 1
  # 4 or 5 years
  elif years >= 4:
    frequency = 2
  # 3 years
  elif years >= 3:
    frequency = 2
  # 2 years
  elif years >= 2:
    frequency = 3
  # 1st year
  elif years >= 1:
    frequency = 3

  file_prefix = f"{folder_path}/{output['department']}/{name}"
  file_counts[file_prefix] = frequency

  # save files
  output['front'].save(f"{file_prefix}_front.png")
  output['back'].save(f"{file_prefix}_back.png")