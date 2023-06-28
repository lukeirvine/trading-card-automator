from PIL import Image, ImageDraw, ImageFont
import datetime
import os
import functions
import sys
from fpdf import FPDF

folder_path = "input-images"

# Check if the folder path exists
if not os.path.exists(folder_path):
  print("Folder path does not exist.")
  sys.exit()

image_names = []

# Get the list of files in the folder and sort them alphabetically
file_list = sorted(os.listdir(folder_path))

# Loop through files in the folder
for index, filename in enumerate(file_list):
  # Process the image (replace this with your desired logic)
  image_name = filename
  # Your logic to process the image goes here
  if index % 2 == 0:
    image_names.append([])
  image_names[len(image_names) - 1].append(image_name) 


for pair in image_names:
  print(pair[0])
  canvas_front = Image.new("RGB", (750, 1050), color=(60, 64, 42))
  image_front = Image.open(os.path.join(folder_path, pair[0]))
  image_front = image_front.resize((675, 945))
  canvas_front.paste(image_front, (38,38))

  canvas_back = Image.new("RGB", (750, 1050), color=(255, 255, 255))
  image_back = Image.open(os.path.join(folder_path, pair[1]))
  image_back = image_back.resize((750, 1050))
  canvas_back.paste(image_back, (0,0))

  path_front = pair[0].lower().replace(" ", "_") + "_front.png"
  canvas_front = functions.add_print_border(canvas_front, (60, 64, 42), pair[0])
  canvas_front.save(f"print-border-output/{pair[0]}")

  path_back = pair[0].lower().replace(" ", "_") + "_back.png"
  canvas_back = functions.add_print_border(canvas_back, (221, 219, 215), pair[1])
  canvas_back.save(f"print-border-output/{pair[1]}")

pdf = FPDF(format=(500, 700))
print("Making pdf")
images = []
# Get the list of files in the folder and sort them alphabetically
file_list = sorted(os.listdir("print-border-output"))
for filename in file_list:
  # Open the image using PIL
  # image_path = os.path.join("print-border-output", filename)
  # image = Image.open(image_path)
  # image = image.resize((750, 1050))
  
  # # Convert the image to PDF and add it to the PDF object
  # pdf.add_page()
  # pdf.image(image_path, 0, 0)
  image = Image.open(os.path.join("print-border-output", filename))
  images.append(image)

images[0].save(
  "print-border-pdfs/aaa.pdf", "PDF", resolution=100.0, save_all=True, append_images=images[1:]
)
  