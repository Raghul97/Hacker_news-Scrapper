#https://news.ycombinator.com/
import requests
from bs4 import BeautifulSoup
import re
import time


def page_response(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    news = soup.select('.storylink')
    count_block = soup.select('.subtext')
    return news, count_block, soup


def data_parser(links, title, counts, news, count_block):
    for i, data in enumerate(news):
        links.append(data['href'])
        title.append(data.text)
        try:
            counts.append(int(count_block[i].find(attrs={'class':'score'}).get_text().split()[0]))
        except:
            counts.append(0)
    return title, links, counts

def creating_datastructure(title, links, counts):
    mass_data = list()
    for i in range(len(title)):
        mass_data.append({'Title': title[i], 'Link': links[i], 'Count': counts[i]})
    return mass_data

def extracting_news(mass_data):
    required_data = list()
    pattern = re.compile('python')
    for data in mass_data:
        if pattern.search(data['Title'].lower()):
            required_data.append(data)
    return required_data

def sorting_required_data(required_data):
    sorted_required_data = sorted(required_data, key=lambda k: k['Count'], reverse=True)
    return sorted_required_data

def get_next_page(soup):
    try:
        more = soup.find(attrs={'class':'morelink'})['href']
        next_page = True
    except:
        more = ''
        next_page = False
    return next_page, more


def main_function(url, links, title, counts):
    next_page = True
    more = ''
    while next_page:
        news, count_block, soup = page_response(url + more)
        title, links, counts = data_parser(links, title, counts, news, count_block)
        next_page, more = get_next_page(soup)
        time.sleep(2)
    mass_data = creating_datastructure(title, links, counts)
    required_data = extracting_news(mass_data)
    sorted_required_data = sorting_required_data(required_data)
    return sorted_required_data

def print_output(sorted_required_data):
    for data in sorted_required_data:
        print('*'*35)
        print(f'Title: {data["Title"]}')
        print(f'Link: {data["Link"]}')
        print(f'Count: {data["Count"]}')
    print('*'*35)

if __name__ == '__main__':
    links = list()
    title = list()
    counts = list()
    url = 'https://news.ycombinator.com/'
    sorted_required_data = main_function(url, links, title, counts)
    print_output(sorted_required_data)


