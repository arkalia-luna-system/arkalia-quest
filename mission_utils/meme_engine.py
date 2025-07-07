import os
from PIL import Image, ImageDraw, ImageFont

def generer_meme(texte, image_path="static/base_meme.jpg", sortie="static/meme_result.jpg"):
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()

    largeur, hauteur = img.size
    bbox = draw.textbbox((0, 0), texte, font=font)
    texte_largeur = bbox[2] - bbox[0]
    texte_hauteur = bbox[3] - bbox[1]
    position = ((largeur - texte_largeur) // 2, hauteur - 50)

    draw.text(position, texte, font=font, fill="white")
    img.save(sortie)
    return sortie 