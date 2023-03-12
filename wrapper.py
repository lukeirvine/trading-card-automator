from PIL import Image, ImageDraw, ImageFont
import textwrap

# Create a new image
img = Image.new('RGB', (500, 700), color=(255, 255, 255))

# Create a new draw object
draw = ImageDraw.Draw(img)

# Set the font for the text
font = ImageFont.truetype('arial.ttf', 36)

# Define the text to be centered and wrapped
text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed vel nisi elit. Nam pulvinar suscipit mauris, sit amet interdum est."

# Wrap the text to fit within the image
wrapper = textwrap.TextWrapper(width=40)
wrapped_text = wrapper.wrap(text)

# Calculate the x and y coordinates for the text to be centered
text_widths = [draw.textsize(line, font=font)[0] for line in wrapped_text]
max_text_width = max(text_widths)
x = (img.width - max_text_width) / 2
y = (img.height - font.getsize(text)[1] * len(wrapped_text)) / 2

# Ensure that the text doesn't go below 50 pixels from the bottom of the image
min_y = img.height - 50 - font.getsize(wrapped_text[-1])[1]
if y > min_y:
    y = min_y

# Draw the wrapped text on the image at the centered position
for line in wrapped_text:
    line_width = draw.textsize(line, font=font)[0]
    x_pos = (img.width - line_width) / 2
    draw.text((x_pos, y), line, fill=(0, 0, 0), font=font)
    y += font.getsize(line)[1]

# Show the resulting image
img.show()
