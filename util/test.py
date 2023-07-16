import requests
from PIL import Image

url = 'https://cdn.discordapp.com/attachments/1117475820995350661/1126749160830402611/garrettzhao_3893016642one_year_old_chinese_baby_boy_sitting_on__356021dd-e068-4d35-a5f5-8f29c7f8c34c.png'

data = requests.get(url).content

f = open('img.jpg','wb')
f.write(data)
f.close()

# Opening the saved image and displaying it
img = Image.open('img.jpg')
img.show()

