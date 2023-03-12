# Mivoden Trading Card Automator
This Python script creates stylized trading cards from a spreadsheet. It was created for [Camp Mivoden](https://www.mivoden.com/) to create staff trading cards for summer 2023.

<div style="display:flex; justify-content: space-between">
  <img src="https://i.imgur.com/b4K55e3.png" width="24%" />
  <img src="https://i.imgur.com/PZ312i7.png" width="24%" />
  <img src="https://i.imgur.com/GruGh5Z.png" width="24%" />
  <img src="https://i.imgur.com/gd0zLR9.png" width="24%" />
</div>
<br>

## Instructions
1. Create a csv file with the following values in the following order:

    | image | name | positions | years | department | question 1 | answer 1 | question 2 | answer 2 | question 3 | answer 3 | question 4 | answer 4|
    | -------- | -------- | -------- | -------- | -------- | -------- | -------- | -------- | -------- | -------- | -------- | -------- | -------- |
    | luke.png | Luke Irvine | Assistant Directior; Boat Driver | 8 | leadership | Favorite Bible Verse | John 3:16 | question 2 | answer 2 | question 3 | answer 3 | question 4 | answer 4 |
    
    ### Other Rules for data:
    - If there are multiple positions, they must be separated by a semi-colon and space `"; "`
    - The years column must have integers, nothing else (whole numbers), and be 12 or less.
    - The department must be in this list and spelled correctly with no caps:
      ```
      leadership, extreme, housekeeping, office, waterfront, activities, art, challenge, comms, dt, equestrian, kitchen, maintenance, survival, ultimate
      ```
    - All 4 questions and answers must be present
2. Clone this repo onto your local machine. 
    - [Learn how to clone](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) 
    - [Get git](https://git-scm.com/downloads)
3. Add the csv file to the root directory and label it `data.csv`
    - Note: you can get this from any spreadsheet by exporting it as a `csv`
4. Add images for the cards to a directory titled `images` in the root directory.
    - Your images need to have an aspect ratio of `5:7` or it will be distorted. `500x700px` is recommended
    - Make sure an image exists for every entry to the `image` column in `data.csv` and that they are spelled correctly and case sensitive.
5. Open a terminal in the root directory and run:
      ```
      python3 main.py
      ```
    This of course assumes you have python downloaded on your machine. If you don't have python, [get it here](https://www.python.org/downloads/).
6. The script will ask you if you'd like to save plain images or wrap the images in a border used for printing.
7. The script should let you know if any of the above rules are broken.
8. Once the script has finished, your images will appear in the `output` folder. 
    - Be sure to empty this folder before running the script again as it will write over files with the same name without warning.