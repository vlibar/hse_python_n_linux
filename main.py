from bs4 import BeautifulSoup
import requests
import urllib.request, urllib.error, urllib.parse
import os
import ssl
import warnings
import sys
context = ssl._create_unverified_context()
warnings.filterwarnings("ignore")


def links_from_website(start_link, deep, links_set=set()):
    res = requests.get(start_link, verify=False) # получаем html страницы
    soup = BeautifulSoup(res.text, 'html.parser') # получаем soup из html страницы
    links_current = set() # текущий список ссылок на данной глубине
    for link in soup.findAll('a'):
        link_nm = link.get('href')
        try:
            # Если ссылка ведёт на дочернюю страницу и её нет в предыдущих ссылках
            if (link_nm.startswith(start_link)) and link_nm not in links_set:
                links_current.add(link_nm.strip().rstrip('/'))
        except AttributeError:
            pass
    links_set.update(links_current)
    if deep == 1:
        return links_set
    else:
        for link in links_current:
            links_from_website(link, deep - 1, links_set)
        return links_set

try:
    links = links_from_website(sys.argv[1], int(sys.argv[2]))

    if not os.path.exists('data'):
        os.makedirs('data')

    f_urls = open('urls.txt', 'w')
    for i, link in enumerate(sorted(links)):
        print(i, link)
        response = urllib.request.urlopen(link, context=context)
        try:
            webContent = response.read().decode('UTF-8')
            f_html = open(f'data/{i}.html', 'w')
            f_html.write(webContent)
            f_html.close
            f_urls.write(str(i) + ' ' + str(link) + '\n')
        except UnicodeDecodeError:
            pass
    f_urls.close()

except IndexError:
    print('Вы передали не все аргументы')

except ValueError:
    print('Вы передали аргументы не в том формате.\nПервым аргументом идёт ссылка на сайт, вторым - глубина')
