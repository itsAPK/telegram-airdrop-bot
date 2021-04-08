# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw, ImageFont
from ...config import Config
import random
import itertools 
import os

def generate_image(emoji):
    emojifont=os.path.join('')
    fnt = ImageFont.truetype('G:\\BOT\\airdropbot\\bot\\plugins\\utils\\fonts\\AppleColorEmoji.ttf', size=109, layout_engine=ImageFont.LAYOUT_RAQM)
    im = Image.open(r'G:\\BOT\\airdropbot\\bot\\plugins\\utils\\image\\f.jpg')
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype("G:\\BOT\\airdropbot\\bot\\plugins\\utils\\fonts\\Aaargh.ttf", 28)
    draw.text((0,0),Config.BOT_NAME,font=font)
    width=[266,450,27,104,358,182]
    height=[176,261,100,168,240,35]
    for (i,w,h) in zip(emoji,width,height):
        draw.text((w,h), i, fill="white", embedded_color=True, font=fnt)
    im.save(f"G:\\BOT\\airdropbot\\bot\\plugins\\utils\\image\\testemoji.png")


"""def emoji_markup(generated_emoji):
    random_emoji=random.sample(emoji,10)
    random_emoji.extend(generated_emoji)
    random.shuffle(random_emoji)
    print(random_emoji)"""
    
