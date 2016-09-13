import requests
from bs4 import BeautifulSoup
import time
import datetime

# Crawler for http://news.pia.gov.ph/archives/current/1
# We can go to next page by adding 15 at the last part of url
# also be able jump to the final page directly by click button

# add multiple trying times and decent wait upon requests.get()
# notice that we set a global var to record request_times in method dogged_get()
request_times = 0
def dogged_get(url):
    global request_times

    # empty in, empty out
    if url == '':
        return('')

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

# news in pia seperate 3 parts by year 2014 to year 2016
# we set the defalt to 2016(current)  
def get_news_links_list_by_page(page):

    # process the special page
    if page == 1:
        page = 1
    else:
        page = (page - 1) * 15
    
    url = 'http://news.pia.gov.ph/archives/current/' + str(page)
    r  = dogged_get(url)
    # dogged_get has a decent wait

    soup = BeautifulSoup(r.text, 'html.parser')
    all_news_title_h4 = soup.find_all('h4', class_='')

    link_list = []
    for h4 in all_news_title_h4:
        link_list.append(h4.a.get('href'))
    return(link_list)

def get_articles_by_url(url):

    r = dogged_get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    all_article_contents = soup.find('div', class_='col-md-12 margin-bottom-10')

    return(str(all_article_contents))

def save_articles_from_page(start_page, final_page):

    for page in range(start_page-1, final_page):

        with open('news/' + str(page+1) + '.txt', 'w') as f:

            print('page:', page+1)
            print(datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'))
            one_page_link_list = get_news_links_list_by_page(page+1)

            for url in one_page_link_list:
                f.write(url + '\n')
                f.write(get_articles_by_url(url) + '\n\n')

# 1. get the final page
# final_page = 1160


# print(get_news_links_list_by_page(1))
save_articles_from_page(1159, 1160)


print('program end! requests with', request_times, 'times.')
