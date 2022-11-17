from PIL import ImageFont
from PIL import ImageDraw
from PIL import Image as PImage
import math
import textwrap

font = ImageFont.truetype("fonts/OpenSans-ExtraBold.ttf", 100)
fontMono = ImageFont.truetype("fonts/DroidSansMono.ttf", 100)
fontEmoji = ImageFont.truetype("fonts/OpenSansEmoji.ttf", 150)
font_small = ImageFont.truetype("fonts/OpenSans-ExtraBold.ttf", 60)

#def sayEmoji(string):
#    return say_(string, fontEmoji)

def say(string, font=font, align='center'):
    return say_(string, font, align)

def sayM(string, font=fontMono, align='left'):
    return say_(string, font, align)


yodaimg = PImage.open('images/yoda.jpg')
chewimg = PImage.open('images/diego.png')
background = PImage.open('images/background.png')
scale=1.5

def yoda(string):
    return herosay(string, yodaimg)

def chew(string):
    return herosay(string, chewimg)

def wooclap(text = u''):
    return say(u"Wooclap! 👏 %s" % (text), fontEmoji)

def herosay(string, img):    
    fontbbox = font_small.getbbox(string)
    fontsize = (fontbbox[2] - fontbbox[0], fontbbox[3] - fontbbox[1])
    imgcp = img.copy()
    ys = imgcp.size
    imgsize = [int(fontsize[0]*scale), int(fontsize[0] * scale * ys[1] / ys[0])]
    imgcp = imgcp.resize(imgsize)
    draw = ImageDraw.Draw(imgcp)
    draw.text((int(fontsize[0] * (1 - scale/2)),
               int(imgcp.size[1] - fontsize[1]*scale)),
              string,
              (255,255,255,1), 
              font=font_small)
    return imgcp

def say_(string, font, align):
    if len(string) == 0:
        return False

    image = background.copy()
    draw = ImageDraw.Draw(image)
    fontbbox = draw.textbbox((0,0),string,font=font,anchor='mm', align=align)
    #fontbbox = font.getbbox(string) #The size of the font
    fontsize = (fontbbox[2] - fontbbox[0], fontbbox[3] - fontbbox[1])
    emsize = int(fontsize[0] / len(string))
    imgsize = [int(fontsize[0] + 4*emsize), int(fontsize[1] + 2 *emsize)]

    #image = background.copy()
    image = image.resize(imgsize)

    draw = ImageDraw.Draw(image)
    draw.multiline_text((int(imgsize[0] / 2),int(imgsize[1] / 2)), 
                  string, (255,255,255,1), font=font, anchor='mm', align=align)
    return image

def say__(string, font):
    if len(string) == 0:
        return False
    
    fontbbox = font.getbbox(string) #The size of the font
    fontsize = (fontbbox[2] - fontbbox[0], fontbbox[3] - fontbbox[1])
    imgsize = [int(fontsize[0] * scale), int(fontsize[1] * scale)]

    image = PImage.new('RGB', imgsize) #Create the image

    innerColor = [80, 80, 255] # Color at the center
    outerColor = [0, 0, 80] # Color at the corners

    for y in range(imgsize[1]):
        for x in range(imgsize[0]):

            # Find the distance to the corner
            distanceToCorner = math.sqrt((x) ** 2 + (y ) ** 2)

            # Make it on a scale from 0 to 1
            distanceToCenter = float(distanceToCorner) / (1.4142 * imgsize[0])

            # Calculate r, g, and b values
            r = outerColor[0] * distanceToCenter + innerColor[0] * (1 - distanceToCenter)
            g = outerColor[1] * distanceToCenter + innerColor[1] * (1 - distanceToCenter)
            b = outerColor[2] * distanceToCenter + innerColor[2] * (1 - distanceToCenter)


            # Place the pixel        
            image.putpixel((x, y), (int(r), int(g), int(b)))

    draw = ImageDraw.Draw(image)
    draw.text((int(imgsize[0] / 2),int(imgsize[1] / 2)), 
              string, (255,255,255,1), font=font, anchor='mm')
    return image

# http://stackoverflow.com/a/30525061/62365
class DictTable(dict):
    # Overridden dict class which takes a dict in the form {'a': 2, 'b': 3},
    # and renders an HTML Table in IPython Notebook.
    def _repr_html_(self):
        html = ["<table width=100%>"]
        for key, value in self.items():
            html.append("<tr>")
            html.append("<td>{0}</td>".format(key))
            html.append("<td>{0}</td>".format(value))
            html.append("</tr>")
        html.append("</table>")
        return ''.join(html)

class ListDictTable(list):
    def _repr_html_(self):
        html = ["<ul>"]
        for i in self:
            html.append("<li>")
            html.append(DictTable(i)._repr_html_())
            html.append("</li>")
        html.append("</ul>")
        return ''.join(html)

from IPython.display import HTML

def img_to_fixed_width_html_image(img_url, width="100%"):
    text = f'<img width="{width}" src="{img_url}"/>'
    return HTML(text)