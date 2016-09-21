import requests
from bs4 import BeautifulSoup
import time
import datetime

request_times = 0

def dogged_get(url):
    global request_times
   
    if url != '':

        for i in range(5):
            
            time.sleep(1.5)
            r = requests.get(url)
            request_times = request_times + 1

            if r.status_code == 200:
                print(r.status_code)
                return(r)
            else:
                print('faild', i+1, 'time(s), keep trying')
                time.sleep(3)

        # empty out after trying 5 times
        return('')

    else:
        # empty in, empty out
        return('')

def print_the_page_information_by_page(page):
    # get the HTML response
    url = 'http://www.antaranews.com/en/business/' + str(page)
    r  = requests.get(url)
    print('page:', page) 
    print(url)
    print('r.status_code:', r.status_code)

    # parse HTML
    soup = BeautifulSoup(r.text, 'html.parser')
    all_news_links = soup.find_all('a', class_='box_link2')

    # save links of this page to list
    link_list = []

    for link in all_news_links:
        link_list.append('http://www.antaranews.com' + link['href'])
    print('len(link_list):', len(link_list))

#### get links_list from page
def get_news_links_list_by_page(page):
    url = 'http://www.antaranews.com/en/business/' + str(page)
    r  = dogged_get(url)
    # dogged_get has a decent wait

    soup = BeautifulSoup(r.text, 'html.parser')
    all_news_links = soup.find_all('a', class_='box_link2')

    link_list = []
    for link in all_news_links:
        link_list.append('http://www.antaranews.com' + link['href'])
    return(link_list)

def guess_the_final_page():
    guess_page = 1

    while len(get_news_links_list_by_page(guess_page))!=0:
        guess_page = guess_page*2
        print('guess_page:', guess_page)

    guess_page = int(guess_page/2)
    mid_bar = int(guess_page)
    add_num = int(guess_page/2)
    max_bar = guess_page*2

    # you can see the thought detail in optimized_page_loader.py
    # ['len(get_news_links_list_by_page(guess_page))!=0']  is equal to ['guess_page < final_page']
    
    # set 2 vars to control connect times and simular value looping
    connect_time = 0
    simular_num = 0

    while len(get_news_links_list_by_page(guess_page))!=0:
        connect_time = connect_time + 1
        guess_page = mid_bar + add_num

        # detect part:
        if connect_time >= 20:
            print('not the best answer, but connect_time is:', connect_time)
            break
        if simular_num == guess_page:
            print('bingo!!!')
            break

        # guessing part
        if len(get_news_links_list_by_page(guess_page))==0:
            print('guess_page > final_page, so change a smaller add_num;', guess_page)

            while len(get_news_links_list_by_page(guess_page))==0:
                add_num = int(add_num/2)
                guess_page = mid_bar + add_num

        if len(get_news_links_list_by_page(guess_page))!=0:
            print('guess_page < final_page, so update a higher mid_bar;', guess_page)
            mid_bar = guess_page

        # set simular_num
        print('set the simular_num')
        simular_num = guess_page

    print('connect_time:', connect_time)
    return(guess_page)

#### ! have to improve parse effect
#### get url and return str
def get_articles_by_url(url):
    r = dogged_get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    content_news = soup.find('div', id='content_news')
    return(str(content_news))

def save_articles_from_page(start_page, end_page):
    
    for page in range(start_page-1, end_page):

        with open('news/' + str(page+1) + '.txt', 'w') as f:

            print('page:', page+1)
            print(datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'))
            one_page_link_list = get_news_links_list_by_page(page+1)

            for url in one_page_link_list:
                f.write(url + '\n')
                f.write(get_articles_by_url(url) + '\n\n')

    print('download finished! requests with', request_times, 'times.')
