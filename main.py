from PIL import Image, ImageDraw, ImageFont
import datetime
import textwrap
import os
import json

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

# Set the position of the name on the card
name_position = (50, 50)

# Set the color of the name text
name_color = (255, 255, 255)

# Open data JSON file
with open('data.json', 'r') as f:
  data = json.load(f)

data = data.values()

# Loop through all the images in the folder
for card_data in data:
  # create a new image
  canvas = Image.new("RGB", (500, 700), color=(255, 255, 255))

  # Load the image
  image = Image.open(os.path.join("images", card_data['img']))

  # Resize the image to fit the canvas
  image = image.resize((500, 700))

  # Paste the image onto the card canvas
  canvas.paste(image, (0, 0))

  # Paste the border onto the card
  border = Image.open("materials/border.png")
  paste_alpha = border.split()[-1]
  canvas.paste(border, (0, 0), mask=paste_alpha)

  # Add the name to the card
  texts = [{
    "text": position,
    "size": 24,
    "width": 30,
    "margin_bottom": 0
  } for position in card_data['positions']]
  texts.insert(0, {
    "text": card_data['name'],
    "size": 70,
    "width": 12,
    "margin_bottom": 5
  })
  add_front_text(canvas, texts)

  # add stars
  add_stars(canvas, card_data['years'])

  # Get date for folder name
  current_datetime = datetime.datetime.now()
  formatted_datetime = current_datetime.strftime("%m-%d-%Y-%H%M-%S")

  # Create the folder to save the image
  # folder_path = "results/" + formatted_datetime
  folder_path = "results"
  if not os.path.exists(folder_path):
    os.makedirs(folder_path)

  # Save the trading card as a PNG image
  canvas.save(f"{folder_path}/{card_data['img'].split('.')[0]}_card.png")