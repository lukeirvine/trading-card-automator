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
# Loop through files in the folder
for index, filename in enumerate(os.listdir(folder_path)):
  # Process the image (replace this with your desired logic)
  image_name = filename
  # Your logic to process the image goes here
  if index % 2 == 0:
    image_names.append([])
  image_names[len(image_names) - 1].append(image_name) 


for pair in image_names:
  print(pair[0])
  canvas_front = Image.new("RGB", (500, 700), color=(255, 255, 255))
  image_front = Image.open(os.path.join(folder_path, pair[0]))
  image_front = image_front.resize((500, 700))
  canvas_front.paste(image_front, (0,0))

  canvas_back = Image.new("RGB", (500, 700), color=(255, 255, 255))
  image_back = Image.open(os.path.join(folder_path, pair[1]))
  image_back = image_back.resize((500, 700))
  canvas_back.paste(image_back, (0,0))

  path_front = pair[0].lower().replace(" ", "_") + "_front.png"
  canvas_front = functions.add_print_border(canvas_front, (255, 255, 255), pair[0])
  canvas_front.save(f"print-border-output/{pair[0]}")

  path_back = pair[0].lower().replace(" ", "_") + "_back.png"
  canvas_back = functions.add_print_border(canvas_back, (255, 255, 255), pair[1])
  canvas_back.save(f"print-border-output/{pair[1]}")

pdf = FPDF(format=(500 / 72, 700 / 72))
print("Making pdf")
for filename in os.listdir("print-border-output"):
  # Open the image using PIL
  image_path = os.path.join("print-border-output", filename)
  image = Image.open(image_path)
  image = image.resize((500, 700))
  
  # Convert the image to PDF and add it to the PDF object
  pdf.add_page()
  pdf.image(image_path, 0, 0)

pdf.output("print-border-pdfs/aaa.pdf")