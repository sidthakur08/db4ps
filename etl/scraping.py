from tqdm import tqdm
import requests
from bs4 import BeautifulSoup
import json

urls = [f'https://gamesdb.launchbox-app.com/platforms/games/50%7C{i}' for i in range(1,12)]
l = []

for url in tqdm(urls):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    content = soup.find('body')
    inside_content = content.find_all('div','list-item-wrapper')

    for i in tqdm(inside_content):
        content_dic = {}
        url_i = "https://gamesdb.launchbox-app.com" + i.find('a','list-item').get('href')
        page_i = requests.get(url_i)
        soup_i = BeautifulSoup(page_i.content, 'html.parser')

        content_i = soup_i.find('body').find_all('div','container')[2].find('form').find('table').find_all('tr')

        if content_i[1].find('td','row-header').text == 'Alternate Name':
            content_i.pop(1)
            content_i.pop(1)
            content_i.pop(1)
            content_i.pop(1)

        if content_i[1].find('td','row-header').text == 'Add Alternate Name':
            content_i.pop(1)
            content_i.pop(1)
            content_i.pop(1)
            content_i.pop(1)

        try:
            content_dic['Name'] = content_i[0].find('span','view').text
        except:
            content_dic['Name'] = ''
        try:
            content_dic['Platform'] = content_i[1].find('span','view').text
        except:
            content_dic['Platform'] = ''
        try:
            content_dic['Release Date'] = content_i[2].find('span','view').text
        except:
            content_dic['Release Date'] = ''
        try:
            content_dic['Game Type'] = content_i[3].find('span','view').text
        except:
            content_dic['Game Type'] = ''
        try:
            content_dic['ESRB'] = content_i[4].find('span','view').text
        except:
            content_dic['ESRB'] = ''
        try:
            content_dic['Developers'] = content_i[5].find('span','view').text
        except:
            content_dic['Developers'] = ''
        try:
            content_dic['Publishers'] = content_i[6].find('span','view').text
        except:
            content_dic['Publishers'] = ''
        try:
            content_dic['Genres'] = content_i[7].find('span','view').text
        except:
            content_dic['Genres'] = ''
        try:
            content_dic['Max Players'] = content_i[8].find('span','view').text
        except:
            content_dic['Max Players'] = ''
        try:
            content_dic['Cooperative'] = content_i[9].find('span','view').text
        except:
            content_dic['Cooperative'] = ''
        try:
            content_dic['Community Rating'] = content_i[10].find('span',id='communityRating').text
        except:
            content_dic['Community Rating'] = ''
        try:
            content_dic['Total View'] = content_i[10].find('span',id='totalVotes').text
        except:
            content_dic['Total View'] = ''
        try:
            content_dic['Wikipedia'] = content_i[11].find('span','view').text
        except:
            content_dic['Wikipedia'] = ''
        try:
            content_dic['Video Link'] = content_i[12].find('span','view').text
        except:
            content_dic['Video Link'] = ''
        try:
            content_dic['Overview'] = content_i[13].find('div','view').text
        except:
            content_dic['Overview'] = ''
        
        l.append(content_dic)

with open('games.txt','w') as f:
    json.dump(l,f)