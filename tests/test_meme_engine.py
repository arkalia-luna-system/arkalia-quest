import os
import sys
sys.path.append('.')
from mission_utils.meme_engine import generer_meme
import pytest

def test_generer_meme_cree_fichier():
    # Créer une image de test simple
    from PIL import Image
    test_img = Image.new('RGB', (300, 200), color='black')
    test_img.save('static/base_meme.jpg')
    
    sortie = generer_meme("Test Meme")
    assert os.path.exists(sortie)
    
    # Nettoyer
    if os.path.exists('static/base_meme.jpg'):
        os.remove('static/base_meme.jpg')
    if os.path.exists(sortie):
        os.remove(sortie) 