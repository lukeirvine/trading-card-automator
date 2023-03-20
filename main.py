from PIL import Image, ImageDraw, ImageFont
import PyPDF2
import datetime
import textwrap
import os
import json
import functions

# ask whether we should use print version or not
response = ''
while True:
  response = input("Would you like to use print format? (y/n): ")
  if (response.lower() in ('y', 'n')):
    break
  print("Invalid input. Please enter 'y' or 'n'.")

PRINT = response.lower() == 'y'

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

used_departments = set()

data = functions.read_csv_file()
functions.check_data(data, border_colors)
num_cards = len(data)
done_processing = 0

outputs = []

for card_data in data:
  border_color = border_colors[card_data['department']]

  # Add department to used_departments
  used_departments.add(card_data["department"])

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
  functions.add_front_text(canvas, texts, border_color)

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
    path_front = card_data['name'].lower().replace(" ", "_") + "_front.png"
    path_back = card_data['name'].lower().replace(" ", "_") + "_back.png"
    canvas = functions.add_print_border(canvas, border_color, path_front)
    canvas_back = functions.add_print_border(canvas_back, border_color, path_back)

  outputs.append({
    "front": canvas,
    "back": canvas_back,
    "name": card_data['name'],
    "department": card_data['department'],
    "years": card_data["years"]
  })
  done_processing += 1
  print("\rDone Processing: " + str(done_processing) + "/" + str(num_cards), end="", flush=True)

# new line
print("")

# print all the made files at once
printed = 0
# Create the folder to save the image
# folder_path = "results/" + formatted_datetime
folder_path = "output"
if not os.path.exists(folder_path):
  os.makedirs(folder_path)

# make department folders
for dept in used_departments:
  if not os.path.exists(f"{folder_path}/{dept}"):
    os.makedirs(f"{folder_path}/{dept}")
  
# File counts for pdf
file_counts = {}

# Save the files
for output in outputs:
  # Get date for folder name
  current_datetime = datetime.datetime.now()
  formatted_datetime = current_datetime.strftime("%m-%d-%Y-%H%M-%S")

  # make name lowercase with underscores
  name = output['name'].lower().replace(" ", "_")

  # set frequency
  frequency = 1
  years = output["years"]
  # 8 or more years
  if years >= 8:
    frequency = 2
  # 6 or 7 years
  elif years >= 6:
    frequency = 3
  # 4 or 5 years
  elif years >= 4:
    frequency = 4
  # 2 or 3 years
  elif years >= 2:
    frequency = 5
  # 1st year
  elif years >= 1:
    frequency = 6

  file_prefix = f"{folder_path}/{output['department']}/{name}"
  file_counts[file_prefix] = frequency

  # save files
  output['front'].save(f"{file_prefix}_front.png")
  output['back'].save(f"{file_prefix}_back.png")
  printed += 1
  print("\rPrinted: " + str(printed) + "/" + str(num_cards), end="", flush=True)

# Save images to pdf with duplicates for frequency
# if PRINT:
#   pdf_path = 'mivoden-trading-cards.pdf'
#   pdf = PyPDF2.PdfWriter()

#   # add images
#   for file_prefix in file_counts.keys():
    

# Print new line to end
print("")