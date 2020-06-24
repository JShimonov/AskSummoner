import requests
from bs4 import BeautifulSoup

name = input('in-game name: ')
URL = 'https://na.op.gg/summoner/userName=' + name
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

results = soup.find(class_='MostChampionContent')

champs = results.find_all('div', class_='ChampionBox Ranked')

for champ in champs:
    champion = champs.find()
    kda = champs.find()
    win_rate = champs.find()

    print('Champion : ' + champion)
    print('kda : ' + kda)
    print('Win Rate : ' + win_rate)

print(champs)
