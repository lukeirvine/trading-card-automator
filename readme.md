# Mivoden Trading Card Automator

## Instructions
1. Create a csv file with the following values in the following order:

    | image | name | positions | years | department | question 1 | answer 1 | question 2 | answer 2 | question 3 | answer 3 | question 4 | answer 4|
    | -------- | -------- | -------- | -------- | -------- | -------- | -------- | -------- | -------- | -------- | -------- | -------- | -------- |
    | luke.png | Luke Irvine | Assistant Directior; Boat Driver | 8 | leadership | Favorite Bible Verse | John 3:16 | question 2 | answer 2 | question 3 | answer 3 | question 4 | answer 4 |
    
    ### Other Rules for data:
    - If there are multiple positions, they must be separated by a semi-colon and space `"; "`
    - The years column must have integers, nothing else (whole numbers)
    - The department must be in this list and spelled correctly with no caps:
      ```
      leadership, extreme, housekeeping, office, waterfront, activities, art, challenge, comms, dt, equestrian, kitchen, maintenance, survival, ultimate
      ```
    - All 4 questions and answers must be present
2. Add the csv file to the root directory and label it `data.csv`
3. Add images for the cards to a directory titled `images` in the root directory.
    - Make sure an image exists for every entry to the `image` column in `data.csv` and that they are spelled correctly and case sensitive.
4. Open a terminal in the root directory and run:
      ```
      python3 main.py
      ```
    This of course assumes you have python downloaded on your machine. If you don't have python, [get it here](https://www.python.org/downloads/).
5. The script will ask you if you'd like to save plain images or wrap the images in a border used for printing.
6. The script should let you know if any of the above rules are broken.
7. Once the script has finished, your images will appear in the `output` folder. 
    - Be sure to empty this folder before running the script again as it will write over files with the same name without warning.