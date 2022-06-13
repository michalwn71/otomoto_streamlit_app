import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pickle
import re

def prep_text(text):
    return text.replace('“', '\\"').replace('”', '\\"').replace('"', '\\"') + '\\n'

class car_info_scraper:
    def __init__(self, url) -> None:
        self.url = url
        self.response = requests.get(self.url)
        self.soup = BeautifulSoup(self.response.content, 'html.parser')

    def car_info(self):
        params_dict = {}

        price = self.soup.find('span', {'class':'offer-price__number'})
        params_dict['price'] = re.sub(' +', ' ', price.text.replace('\n',''))

        data_params = self.soup.find_all('li', {'class':'offer-params__item'})
        for item in data_params:
            params_dict[item.contents[1].text] = item.contents[3].text.replace('\n', '').strip()


        data_equip = self.soup.find_all('li', {'class':'parameter-feature-item'})
        eq_list = []
        for eq in data_equip:
            eq_list.append(eq.contents[2].text.strip())
        params_dict['equipment'] = ','.join(eq_list)

        description = self.soup.find('div', {'class':'offer-description__description'})
        params_dict['description'] = description.text

        return params_dict


class Listing_scraper:
    def __init__(self, url) -> None:
        self.url = url
        self.response = requests.get(self.url)
        self.soup = BeautifulSoup(self.response.content, 'html.parser')
    
    def num_pages(self):
        num = self.soup.find_all('a', {"class":"ooa-g4wbjr ekxs86z0"})
        max = 0
        for n in num:
            if int(n.text) > max:
                max = int(n.text)
        return max

    def check_num_of_listings(self):
        num_list_text = self.soup.find('h1', {'class':'e1l24m9v0 ooa-x3g7qd-Text eu5v0x0'})
        num_check = num_list_text.text
        pos1 = num_check.find(' - ')
        pos2 = num_check.find(' ogł')
        return int(num_check[pos1+3:pos2].replace(' ', ''))

    def listing_links(self):
        links = self.soup.find_all('article', {"class":"ooa-rld5ij e1b25f6f18"})
        link_list = []
        for listing in links:
            # link = listing.find('a')
            link = listing.find('a')['href']
            if 'oferta' in link:
                link_list.append(link)
            # print(link['href'])
        return link_list
       
class Make_scraper:
    def __init__(self, url) -> None:
        self.url = url
        self.response = requests.get(self.url)
        self.soup = BeautifulSoup(self.response.content, 'html.parser')
    
    def check_len(self):
        try:
            content = self.soup.find('h1', {"class":"e1l24m9v0 ooa-x3g7qd-Text eu5v0x0"})
            return content.text
        except:
            make = self.url.split('/')
            return make[-1]
       
#loading and saving dictionary of car makes as pickle file
def makes_dict_save(makes_dict):
    with open('makes.pickle', 'wb') as f:
        pickle.dump(makes_dict, f, pickle.HIGHEST_PROTOCOL)

def makes_dict_load():
    with open('makes.pickle', 'rb') as f:
        return pickle.load(f)