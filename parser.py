import requests
from bs4 import BeautifulSoup
import fake_useragent
import get_url
import csv

user = fake_useragent.UserAgent().random
headers = {
    'user-agent': user}
urls = get_url.get_url()


def save(features, features_text, reasons, reasons_text, items):  # !!!!!!!!!!
    with open('web_design_industry.csv', 'a', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        for item in items:
            writer.writerow([item['hero_title'], item['hero_subtitle'], item['text_one'], item['section_one_hero'],
                             item['section_one_subhero'],
                             item['section_one_text'], features[0], features_text[0], features[1], features_text[1],
                             features[2], features_text[2], features[3], features_text[3], features[4],
                             features_text[4], features[5], features_text[5], features[6], features_text[6],
                             features[7], features_text[7],
                             features[8], features_text[8], item['section_two_hero'], item['section_two_subhero'],
                             item['section_two_text'], reasons[0], reasons_text[0],
                             reasons[1], reasons_text[1], reasons[2], reasons_text[2], reasons[3], reasons_text[3],
                             reasons[4], reasons_text[4], reasons[5], reasons_text[5]])


def parse():
    sites = 0
    for url in urls:
        sites += 1
        print(sites)
        try:
            items = []
            features = []
            features_text = []
            reasons = []
            reasons_text = []
            response = requests.get(url, headers=headers).text
            soup = BeautifulSoup(response, 'html.parser')
            hero_title = soup.find('h1', class_='entry-title').get_text(strip=True)
            hero_subtitle = soup.find('header', class_='entry-header').find('h2').get_text(strip=True)
            text_ones = soup.find('div', 'fl-row-content-wrap').findAll('div', class_='fl-rich-text')
            text_one = ''
            for txt in text_ones:
                text_one += txt.get_text(strip=True)
            sections = soup.findAll('div', class_='fl-row-bg-none')
            section_one_hero = sections[1].find('h2', class_='fl-heading').get_text(strip=True)
            print(section_one_hero)
            try:
                section_one_subhero = sections[1].find('p', style='text-align: center;').get_text(strip=True)
            except AttributeError:
                section_one_subhero = sections[1].find('span', style='color:#738942;font-size:18px;').get_text(
                    strip=True)
            try:
                section_one_text = sections[1].findAll('div', class_='fl-rich-text')[1].get_text(strip=True)
            except IndexError:
                section_one_text = 'empty'
            features_bad = sections[2].findAll('span', style='color: #85985a;')
            counter = 0
            for feature in features_bad:
                while counter != 9:
                    counter += 1
                    try:
                        features.append(feature.get_text(strip=True))
                        features_text.append(
                            sections[2].findAll('div', class_='fl-module-rich-text')[counter].get_text(strip=True))
                        print(features_text)

                    except IndexError:
                        features.append(' ')
                        features_text.append(' ')
            try:
                section_two_hero = sections[3].find('h2', style='text-align: center;').get_text(strip=True)
            except AttributeError:
                section_two_hero = sections[3].find('span', style='color:#433f34;').get_text(strip=True)
                print(section_two_hero)

            try:
                section_two_subhero = sections[3].find('span', style='color: #738942; font-size: 18px;').get_text(
                    strip=True)
            except AttributeError:
                section_two_subhero = sections[3].find('span', style='color:#738942;font-size:18px;').get_text(
                    strip=True)
            try:
                try:
                    section_two_text = sections[3].find('span', style='font-weight: 400;').get_text(strip=True)
                except AttributeError:
                    section_two_text = 'empty'
            except AttributeError:
                section_two_text = sections[3].find('span', style='font-weight:400;').get_text(strip=True)

            try:
                reasons_bad = sections[4].findAll('span', style='color: #6a8338;')
            except AttributeError:
                reasons_bad = sections[4].findAll('span', style='color:#6a8338;')
            counter = 0

            for reason in reasons_bad:
                while counter != 6:
                    counter += 1
                    try:
                        reasons.append(reason.get_text(strip=True))
                        reasons_text.append(
                            sections[4].findAll('p')[counter - 1].get_text(strip=True))
                    except IndexError:
                        reasons.append(' ')
                        reasons_text.append(' ')

            items.append({
                'hero_title': hero_title,
                'hero_subtitle': hero_subtitle,
                'text_one': text_one,
                'section_one_hero': section_one_hero,
                'section_one_subhero': section_one_subhero,
                'section_one_text': section_one_text,
                'section_two_hero': section_two_hero,
                'section_two_subhero': section_two_subhero,
                'section_two_text': section_two_text
            })
            save(features, features_text, reasons, reasons_text, items)
        except AttributeError:
            items = []
            features = []
            features_text = []
            reasons = []
            reasons_text = []
            response = requests.get(url, headers=headers).text
            soup = BeautifulSoup(response, 'html.parser')
            hero_title = soup.find('div', class_='fl-rich-text').find('h2').get_text(strip=True)
            hero_subtitle = soup.find('div', class_='fl-rich-text').find('p').get_text(strip=True)
            text_ones = soup.find('article', class_='toggle').findAll('section')
            text_one = ''
            for txt in text_ones:
                text_one += txt.get_text(strip=True)
            sections = soup.findAll('div', class_='fl-row-bg-none')
            section_one_hero = sections[1].find('span', class_='fl-heading-text').get_text(strip=True)
            try:
                section_one_subhero = sections[1].find('div', class_='fl-rich-text').get_text(strip=True)
            except AttributeError:
                section_one_subhero = 'empty'
            section_one_text = 'empty'
            reasons_bad = sections[1].findAll('div', class_='fl-icon-text fl-icon-text-wrap')
            counter = 0
            for reason in reasons_bad:
                while counter != 6:
                    counter += 1
                    try:
                        reasons.append(reason.find('h4').get_text(strip=True))
                        unwanted = reason.find('h4')
                        unwanted.extract()
                        reasons_text.append(reason.get_text(strip=True))
                    except AttributeError:
                        reasons.append(' ')
                        reasons_text.append(' ')
            section_two_text = sections[5].find('div', class_='fl-rich-text').get_text(strip=True)
            features_bad = sections[5].findAll('div', class_='fl-rich-text')[1:]
            counter = 0
            for feature in features_bad:
                while counter != 9:
                    counter += 1
                    try:
                        features.append(feature.find('h4').get_text(strip=True))
                        features_text.append(feature.find('p').get_text(strip=True))
                        print(features_text)
                    except AttributeError:
                        features.append(' ')
                        features_text.append(' ')

            items.append({
                'hero_title': hero_title,
                'hero_subtitle': hero_subtitle,
                'text_one': text_one,
                'section_one_hero': section_one_hero,
                'section_one_subhero': section_one_subhero,
                'section_one_text': section_one_text,
                'section_two_hero': ' ',
                'section_two_subhero': ' ',
                'section_two_text': section_two_text
            })
            save(features, features_text, reasons, reasons_text, items)


parse()


#
