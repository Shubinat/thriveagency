import requests
from bs4 import BeautifulSoup
import fake_useragent
import get_url

user = fake_useragent.UserAgent().random
headers = {
    'user-agent': user}
urls = get_url.get_url()


def parse():
    for url in urls:
        features = []
        features_text = []
        reasons = []
        response = requests.get(url, headers=headers).text
        soup = BeautifulSoup(response, 'html.parser')
        hero_title = soup.find('h1', class_='entry-title').get_text(strip=True)
        hero_subtitle = soup.find('header', class_='entry-header').find('h2').get_text(strip=True)
        text_ones = soup.find('div', 'fl-row-content-wrap').findAll('div', class_='fl-rich-text')
        text_one = ''
        for txt in text_ones:
            text_one += txt.get_text(strip=True)

        section_one_hero = soup.find('h2', class_='fl-heading').get_text(strip=True)
        subheroes = soup.findAll('span', style='color: #738942; font-size: 18px;')
        texts = soup.findAll('p', style='text-align: center;')
        section_one_subhero = subheroes[0].get_text(strip=True)
        section_one_text = texts[1].get_text(strip=True)
        features_bad = soup.findAll('span', style = 'color: #85985a;')
        count = 0
        for feature in features_bad:
            features.append(feature.get_text(strip=True))
            count +=1
        features_bad_text = soup.findAll('p')
        
        print(features_bad_text)
        # for feature_texts in features_bad_text:
        #     #features_text.append(feature_texts.findAll('p')[3:])
        #     print(feature_texts.findAll('p')[1].get_text(strip=True))
parse()
