from PIL import Image, ImageDraw, ImageFont
import datetime
import textwrap
import os
import json
import functions

PRINT = True

# Colors for border based on department
border_colors = {
  'leadership': (60, 89, 115),
  'extreme': (56, 65, 42),
  'housekeeping': (59, 41, 58),
  'office': (49, 47, 89),
  'waterfront': (111, 166, 119),
  'activities': (177, 74, 53),
  'art': (146, 67, 83),
  'challenge': (89, 155, 152),
  'comms': (186, 118, 48),
  'dt': (126, 46, 46),
  'equestrian': (25, 89, 65),
  'kitchen': (76, 20, 17),
  'maintenance': (78, 78, 80),
  'survival': (140, 88, 58),
  'ultimate': (217, 109, 85)
}

# Get data for the cards
with open('data.json', 'r') as f:
  data = json.load(f)

data = data.values()

data = functions.read_csv_file()

outputs = []

for card_data in data:
  border_color = border_colors[card_data['department']]
  # Front of Card ==================================

  # create a new image
  canvas = Image.new("RGB", (500, 700), color=(255, 255, 255))

  # Load the image
  image = Image.open(os.path.join("images", card_data['img']))

  # Resize the image to fit the canvas
  image = image.resize((500, 700))

  # Paste the image onto the card canvas
  canvas.paste(image, (0, 0))

  # Paste the border onto the card
  border = functions.set_border_color("materials/border.png", border_color)
  paste_alpha = border.split()[-1]
  canvas.paste(border, (0, 0), mask=paste_alpha)

  # Paste the logo
  logo = Image.open("materials/logo.png")
  logo = logo.resize((95, 80))
  paste_alpha = logo.split()[-1]
  canvas.paste(logo, (10, 20), mask=paste_alpha)

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
  functions.add_front_text(canvas, texts)

  # add stars
  functions.add_stars(canvas, card_data['years'])

  # Back of Card ==================================

  # Create canvas
  canvas_back = Image.new("RGB", (500, 700), color=border_color)

  # Add brand
  brand = Image.open("materials/full-logo.png")
  brand = brand.resize((300, 75))
  paste_alpha = brand.split()[-1]
  canvas_back.paste(brand, (100, 50), mask=paste_alpha)

  # Add text
  functions.add_back_text(canvas_back, card_data['info'])

  # Save both sides ===============================

  # add print borders
  if PRINT:
    canvas = functions.add_print_border(canvas, border_color)
    canvas_back = functions.add_print_border(canvas_back, border_color)

  outputs.append({
    "front": canvas,
    "back": canvas_back,
    "name": card_data['name']
  })

  # Save the trading card as a PNG image
  # canvas.save(f"{folder_path}/{card_data['img'].split('.')[0]}_front.png")
  # canvas_back.save(f"{folder_path}/{card_data['img'].split('.')[0]}_back.png")
  print("card made for " + card_data['name'])

# print all the made files at once
for output in outputs:
  # Get date for folder name
  current_datetime = datetime.datetime.now()
  formatted_datetime = current_datetime.strftime("%m-%d-%Y-%H%M-%S")

  # Create the folder to save the image
  # folder_path = "results/" + formatted_datetime
  folder_path = "output"
  if not os.path.exists(folder_path):
    os.makedirs(folder_path)

  # make name lowercase with underscores
  name = output['name'].lower().replace(" ", "_")

  # save files
  output['front'].save(f"{folder_path}/{name}_front.png")
  output['back'].save(f"{folder_path}/{name}_back.png")
  print("cards printed for " + name)