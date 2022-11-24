from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pandas as pd
import re
import time
import datetime
from webdriver_manager.chrome import ChromeDriverManager


category = ['Politics','Economic','Social','Culture','World','IT']
pages = [101,101,101,71,94,73]
url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100#&date=%2000:00:00&page=2'

options = webdriver.ChromeOptions()
# options.add_argument('headless')
options.add_argument('lang=kr_KR')
driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)

df_titles = pd.DataFrame()
for i in range(0,1):        #section
    titles = []
    for j in range(1,pages[i]):     #page
        url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=10{}#&date=%2000:00:00&page={}'.format(i,j)
        driver.get(url)
        time.sleep(0.2)
        for k in range(1,9):        #x_path
            for l in range(1,5):    #x_path
                x_path = '//*[@id="main_content"]/div/div[2]/div[1]/div[{}]/div[1]/ul/li[{}]/div[2]/a'.format(k,l)
                try:
                    title = driver.find_element('xpath',x_path).text
                    title = re.compile('[^가-힣 ]').sub(' ',title)
                    titles.append(title)
                except NoSuchElementException as e :
                    x_path = '//*[@id="main_content"]/div/div[2]/div[1]/div[{}]/div[1]/ul/li[{}]/div/a'.format(k,l)
                    title = driver.find_element('xpath',x_path).text
                    title = re.compile('[^가-힣 ]').sub(' ', title)
                    titles.append(title)
                except :
                    print('error', i,j,k,l)

        df_section_title = pd.DataFrame(titles, columns=['titles'])
        df_section_title['category'] = category[i]
        df_titles = pd.concat([df_titles, df_section_title], ignore_index=True)
        df_titles.to_csv('./crawling_data/crawling_data_main_{}.csv'.format(category[i]),
                             index = False)
        titles = []

    # df_section_title = pd.DataFrame(titles, columns = ['titles'])
    # df_section_title['category'] = category[i]
    # df_titles = pd.concat([df_titles, df_section_title], ignore_index= True)
# print(df_titles.head())
# print(df_titles.category.value_counts())
