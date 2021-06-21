from PIL import Image, ImageFont, ImageDraw
import requests
import os
import textwrap
from colorsys import rgb_to_hsv, hsv_to_rgb
from io import BytesIO

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
RESOURCE_PATH = os.path.join(BASE_PATH, "resources")


class Color:
    DarkBlue = (66, 135, 245)
    LightBlue = (92, 198, 255)

    DarkGreen = (47, 148, 54)
    LightGreen = (70, 212, 80)

    White = (250, 250, 250)
    Black = (20, 20, 20)

    Tomato = (219, 50, 50)
    Orange = (255, 123, 0)

    Grey = (150, 150, 150)


fontP = os.path.join(RESOURCE_PATH, "Staatliches-Regular.ttf")


class TextEngine:
    def __init__(self):
        pass

    
    def find_font_size(self, text, font, tested_font_size, image, target_width_ratio):
        tested_font = ImageFont.truetype(font, tested_font_size)
        observed_width, observed_height = self.get_text_size(
            text, image, tested_font)
        estimated_font_size = tested_font_size / ((observed_width / target_width_ratio) / (image.width )) 
        return round(estimated_font_size)

    def get_text_size(self, text, image, font):
        im = Image.new('RGB', (image.width, image.height))
        draw = ImageDraw.Draw(im)
        return draw.textsize(text, font)



class ImageEngine:
    def __init__(
        self, 
        text_top, 
        text_bottom, 
        randomColor = False,
        topColor = False,
        bottomColor = False
        ):
        self.font_size_t = 1  # default
        self.font_size_b = 1
        self.font_t = ImageFont.truetype(fontP, self.font_size_t)
        self.font_b = ImageFont.truetype(fontP, self.font_size_b)
        self.txtTop = text_top
        self.txtBottom = text_bottom

        self.width_ratio = 0.75
        self.padding = 10
        self.line_width = 50

        self.textEngine = TextEngine()
        self.colorEngine = ColorEngine()

        self.randomColor= randomColor
        self.topColor= topColor
        self.bottomColor= bottomColor

    def get_text_dimensions(self, text_string, font):
        descent = font.getmetrics()[1]

        text_width = font.getmask(text_string).getbbox()[2]
        text_height = font.getmask(text_string).getbbox()[3] + descent

        return [text_width, text_height]

    def update_font_size_t(self, text: str) -> None:

        font_size_t = self.textEngine.find_font_size(
            text, fontP, self.font_size_t, self.image, self.width_ratio)
        self.font_t = ImageFont.truetype(fontP, font_size_t)

    def update_font_size_b(self, text: str) -> None:
        font_size_b =  self.textEngine.find_font_size(
            text, fontP, self.font_size_b, self.image, self.width_ratio)
        self.font_b = ImageFont.truetype(fontP, font_size_b)


    def draw_top(self):
        imageWidth, imageHeight = self.get_image_dimensions(self.image)
        lines = textwrap.wrap(self.txtTop, width=self.line_width)
        
        self.update_font_size_t(lines[0])
        TopY = self.padding  # imageHeight - 800  # imageHeight / 2
        
    
        for line in lines:
            fWidth, fHeight = self.font_t.getsize(line)
            self.drawText(
                (((imageWidth / 2) - (fWidth / 2)) , TopY), 
                line, self.color, self.font_t
                )
            TopY += fHeight

    def draw_bottom(self):
        imageWidth, imageHeight = self.get_image_dimensions(self.image)
        lines = textwrap.wrap(self.txtBottom, width= self.line_width)
        lines.reverse()
        
        self.update_font_size_b(lines[0])   
        

        textPadding = self.font_b.getsize(lines[0])[1]
        BottomY = imageHeight - textPadding - self.padding   # imageHeight - 800  # imageHeight / 2
        
        for line in lines:
            fWidth, fHeight = self.font_b.getsize(line)
            centerX = (imageWidth / 2) - (fWidth / 2) # 780  # imageWidth / 2
            self.drawText((centerX, BottomY), line, self.color, self.font_b)
            BottomY -= fHeight 
        
    def get_image_dimensions(self, Image):
        return Image.size

    def drawText(self, position, text, color, font):
        self.imageEditable.text(position, text, color, font)

    def get_Image(self, url):
        """ Gets images from URL """
        self.image = Image.open(requests.get(url, stream=True).raw)
        self.imageEditable = ImageDraw.Draw(self.image)
        self.color = self.colorEngine.get_colors(self.image) if self.randomColor else Color.White

    def draw(self, url) -> BytesIO:
        bio = BytesIO()
        self.get_Image(url)
        self.draw_top()
        self.draw_bottom()

        bio.name = 'meme.png'
        self.image.save(bio, 'png')
        bio.seek(0)
        return bio

    def test(self, url):
        self.get_Image(url)
        self.draw_top()
        self.draw_bottom()
        self.image.show()


class ColorEngine:
    def __init__(self):
        pass

    def get_colors(self, image: Image.Image) -> tuple:
        avgCol = self.compute_average_image_color(image)

        aR = avgCol[0]
        aG = avgCol[1]
        aB = avgCol[2]
        if aR > 125 and aG > 125 and aB > 125: return (20, 20, 20)
        else: return (250, 250, 250)

    
    def compute_average_image_color(self, img):
        width, height = img.size

        r_total = 0
        g_total = 0
        b_total = 0

        count = 0
        for x in range(0, width):
            for y in range(0, height):
                r, g, b = img.getpixel((x,y))
                r_total += r
                g_total += g
                b_total += b
                count += 1

        return (round(r_total/count), round(g_total/count), round(b_total/count))

    def get_complementary(self, r, g, b):
        """returns RGB components of complementary color"""
        hsv = rgb_to_hsv(r, g, b)
        return hsv_to_rgb((hsv[0] + 0.5) % 1, hsv[1], hsv[2])

if __name__ == "__main__":
    text1 = input("Text on Top: ")
    text2 = input("text on Bottom: ")

    ImageEngine(text1, text2).test("https://api.telegram.org/file/bot1809224835:AAHPUiSp8C2wWwlUqeQtBUCEqabLs9t5eWQ/photos/file_5.jpg")
