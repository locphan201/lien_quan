import os
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

def get_champs_list():
    url = 'https://lienquan.garena.vn/hoc-vien/tuong-skin/'

    response = requests.get(url)

    if response.ok:
        file = open('heros.txt', 'w', encoding='utf-8')

        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        div = soup.find('div', class_='st-heroes__list')
        heroes_list = div.find_all('a', class_='st-heroes__item')

        for hero in tqdm(heroes_list, total=len(heroes_list), desc='Heroes'):
            dt = hero['data-type'][1:3]
            name = hero.find('h2', class_='st-heroes__item--name').text.strip()
            img_src = hero.find('img')['src']
            file.write(f'{name}|{dt}|{img_src}\n')
            file.flush()

        file.close()

def load_champs_list():
    if not os.path.isfile('heros.txt'):
        get_champs_list()

    with open('heros.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    heros = []
    for line in lines:
        parts = line.split('|')
        heros.append({
            'name': parts[0],
            'type': parts[1],
            'img': parts[2].strip()
        })

    return heros

def load_picked_champs():
    if not os.path.isfile('picked.txt'):
        with open('picked.txt', 'w', encoding='utf-8') as file:
            file.write('')

    with open('picked.txt', 'r', encoding='utf-8') as file:
        lines = [line.strip() for line in file.readlines()]

    return lines

def save_picked_champs(champs):
    try:
        with open('picked.txt', 'w', encoding='utf-8') as file:
            file.write('\n'.join(champs))
        return champs
    except Exception as e:
        print(e)
        return []