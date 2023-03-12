import json

# Open a JSON file and load its contents into a Python object
with open('test.json', 'r') as f:
  data = json.load(f)

# Print the contents of the Python object
for key in data:
  print(data[key]['positions'][0])
