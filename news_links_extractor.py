import time, os
from selenium import webdriver 
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.common.exceptions import NoSuchElementException
  
driver = webdriver.Chrome(ChromeDriverManager().install())
main_page = f"https://www.neoenergia.com/pt-br/sala-de-imprensa/noticias/Paginas/default.aspx#k="  

def extractNewsLinks():
    while True:
        try:
            elements = driver.find_elements_by_xpath('//a[@id="undefined_itemTitleLink"]')
            return [e.get_attribute('href') for e in elements]
        except NoSuchElementException:
            pass

def goToNextPage():
    while True:
        try:
            driver.find_element_by_css_selector("a#PageLinkNext").click()
            time.sleep(2.5)
            break
        except NoSuchElementException:
            pass

news_links = []
num_pages = 37
for i in range(num_pages):
    driver.get(main_page)
    news_links += extractNewsLinks()

    if i < 36:
        goToNextPage()

def saveNewsLinksAt(filename, folder=''):
    if '.txt' not in filename:
        filename += '.txt'
    
    if folder:
        if not os.path.exists(folder):
            os.makedirs(folder)

    path = f'{folder}/{filename}' if folder else filename
    with open(path, 'w') as file:
        [file.write(url+'\n') for url in news_links]

saveNewsLinksAt('news_links.txt')