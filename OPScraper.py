import requests
from bs4 import BeautifulSoup

name = input('in-game name: ')
URL = 'https://na.op.gg/summoner/userName=' + name
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

results = soup.find(class_='MostChampionContent')

champs = results.find_all('div', class_='ChampionBox Ranked')

for champ in champs:
    champion = champ.find('div', class_='ChampionName')
    kda = champ.find('span', class_='KDA')
    win_rate = champ.find('div', class_='WinRatio normal tip tpd-delegation-uid-1')

    print(champion)
    print(kda)
    print(win_rate)

print(champs)
