import pandas as pd 
from selenium import webdriver 
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.common.exceptions import NoSuchElementException
 
driver = webdriver.Chrome(ChromeDriverManager().install())
news_links = open('news_links.txt', 'r').read().splitlines()

def extractContentFromNew():
    contents = [e.text for e in driver.find_elements_by_css_selector("div.text p")]
    contents = contents[1:] #remove datetime, which is into paragraph
    return [i for i in contents if i not in ['', ' ']]

def cleanContents(contents, maxlength=500):
    contents = [' '.join(i.split()) for i in contents]
    return [x.lower() for x in contents if len(x.split()) <= maxlength]

items = []
for new_link in news_links:
    driver.get(new_link)

    while True:
        try:
            contents = extractContentFromNew()
            if contents:
                items += cleanContents(contents)
                [print(c) for c in contents]
                print('\n\n')
            break
        except NoSuchElementException:
            pass

print('\n\ntotal extracted:',len(items))

data = {'index_name': 'neo_news', 'items': items}
pd.DataFrame(data).to_csv('neo_news.csv', sep=';', index=False, encoding='utf-8')