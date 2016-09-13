## Outcome  
This Crawler is specific to antaranews's bussiness category: http://www.antaranews.com/en/business/

## How to use

create a dir named news to store the download result.
```
mkdir news
```

open a python3 shell beside this dir
import crawler than call the functions. for example:  
```
import crawler
crawler.save_articles_from_page(1, 10)
```

## dogged_get(url)

In this method, we add multiple trying times and decent wait upon requests.get()  
Notice that we set a global var to record request_times in method dogged_get(), and will print out in the end of save_articles_from_page(start_page, end_page) method.

## guess_the_final_page()

This case the web would not show 404, so we have identify the final page by list_link.  
The method to try out the final page, in the first part, we let guess_num * 2 every guessing.  

If the guess_page is greatter than final_page, we decrease the add_value, and re-add again until guess_page is smaller than final_page.  
ps: at the early test we found the final_page is 845.

## get_articles_by_url(url)

input: url  
output: A string parsed by BeautifulSoup from HTML  

## save_articles_from_page(start_page, end_page)

input: start_page, end_page  
output: save files into the news directary  

