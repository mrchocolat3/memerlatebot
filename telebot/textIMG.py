from PIL import Image, ImageDraw, ImageFont
import textwrap

def draw_multiple_line_text(image, text, font, text_color, text_start_height):
    '''
    From unutbu on [python PIL draw multiline text on image](https://stackoverflow.com/a/7698300/395857)
    '''
    draw = ImageDraw.Draw(image)
    image_width, image_height = image.size
    y_text = text_start_height
    lines = textwrap.wrap(text, width=round(0.0625 * image.width))
    for line in lines:
        line_width, line_height = font.getsize(line)
        draw.text(((image_width - line_width) / 2, y_text), 
                  line, font=font, fill=text_color)
        y_text += line_height


def main():
    '''
    Testing draw_multiple_line_text
    '''
    #image_width
    image = Image.new('RGB', (1000, 600), color = (0, 0, 0))
    fontsize = 40  # starting font size
    font = ImageFont.truetype("resources/Staatliches-Regular.ttf", fontsize)
    text1 = "I try to add text at the bottom of image and actually I've done it, but in case of my text is longer then image width it is cut from both sides, to simplify I would like text to be in multiple lines if it is longer than image width."
    text2 = "You could use textwrap.wrap to break text into a list of strings, each at most width characters long"

    text_color = (200, 200, 200)
    text_start_height = 0
    draw_multiple_line_text(image, text1, font, text_color, text_start_height)
    draw_multiple_line_text(image, text2, font, text_color, 400)
    image.save('pil_text.png')

if __name__ == "__main__":
    main()