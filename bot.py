import tweepy
import markovify
from PIL import Image, ImageDraw, ImageFont
from os import listdir
from os.path import isfile, join 
import glob
import random


# twitter api
auth = tweepy.OAuthHandler("tslbQSOl2fkBolOZNRZFDgA8d", "xJUccg2XgchNGul8US73ZUsxIvlxLPQpT1aDAXd39wNSmuVC4e")
auth.set_access_token("1265363071138066432-wXuasE0KxqBiHEw15hkyH3F33alHo2", "ulsNRtfoPhR4OhZWe9tgzf7YqBtuvfJ0Mc3db4Egcnuy6")
api = tweepy.API(auth)

# try authenticating credentials
try:
	api.verify_credentials()
	print("Authentication OK")
except:
	print("Error during uthentication")

# get array of all images and fonts for later use
imagesDir = "images/"
fontsDir = "font/"
failedDir = "fail/"
imageList = glob.glob(imagesDir+"*.png")
fontsList = glob.glob(fontsDir+"*.ttf")
failList = glob.glob(failedDir+"*.png")


# Get raw text as string.
with open("sample.txt") as f:
    text = f.read()

# Build the model.
text_model = markovify.Text(text)

# generate image with text
imageName = imageList[random.randint(0, len(imageList)-1)]
fontName = fontsList[random.randint(0, len(fontsList)-1)]
image = Image.open(imageName)
image = image.convert('RGB')
draw = ImageDraw.Draw(image)
font = ImageFont.truetype(fontName, size = 30) #use for font
message = "Test text for image"
color = 'rgb(0,0,0)'

#center text on image
tweet = text_model.make_short_sentence(50)
print(tweet)
MAX_W, MAX_H = image.size

#in case of error, tweet out uninspired message
try:
	w, h = draw.textsize(tweet, font=font)
except:
	print("error catch")
	tweet = "Too much clutter to sort through right now #clutteredmind #uninspired" 
	imageName = failList[random.randint(0, len(failList)-1)]
	api.update_with_media(imageName, status=tweet)
	exit()

# now create the image
draw.text(((MAX_W - w) / 2, (MAX_H - h) / 2), tweet, fill=color, font=font)
image.save('nonsense.png')

# Tweet!
tweet += " #nonsense"
api.update_with_media('nonsense.png', status=tweet)