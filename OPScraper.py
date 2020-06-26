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
    played = champ.find('div', class_='Played')

    winRatio = played.find('div', title='Win Ratio')
    totalPlayed = played.find('div', class_='Title')
    # if None in (champion, kda, win_rate):
    #     continue

    champion = champion.text.strip()
    kda = kda.text.strip()
    win_ratio = winRatio.text.strip()
    totalPlayed = totalPlayed.text.strip()

    print("Champion: " + champion)
    print("Your KDA for " + champion + " is " + kda)
    print("Your win ratio for " + champion + " is " + win_ratio)
    print("You have a total of " + totalPlayed + " games on " + champion)
    print()

# print(champs)
