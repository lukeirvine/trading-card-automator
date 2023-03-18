import os
import csv
import shutil

# Set the path to the directory containing the files to be renamed
input_dir = "imgs"

# Set the path to the directory where new files will be saved
output_dir = "results"

# Set the path to the CSV file containing the new names
csv_path = "names.csv"

# Check if the new directory already exists
if not os.path.exists(output_dir):
  # If it doesn't exist, create the directory
  os.makedirs(output_dir)

# Open the CSV file and read the contents
new_names = []
with open(csv_path, 'r') as csv_file:
  csv_reader = csv.reader(csv_file)
  for row in csv_reader:
     new_names.append(row[0])

# Sort the file names
filenames = sorted(os.listdir(input_dir))
index = 0
for filename in filenames:
  if os.path.isfile(os.path.join(input_dir, filename)):  # check if the file exists
    # get the file extension
    input_path = os.path.join(input_dir, filename)
    ext = os.path.splitext(input_path)[1]

    # Construct new filename based on index
    output_path = os.path.join(output_dir, str(new_names[index]) + ext)

    # Copy the input file to the output folder with a different name
    shutil.copyfile(input_path, output_path)
    
    index += 1  # increment the index
