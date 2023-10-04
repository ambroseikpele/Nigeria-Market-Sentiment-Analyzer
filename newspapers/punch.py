import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

date_list=[]
headline_list=[]
link_list=[]

def scrape():
    r= requests.get('https://punchng.com/topics/business/', headers=headers)
    soup= BeautifulSoup(r.content, 'html.parser')
    news_date= soup.find_all('article', {'class':'entry-item-simple'})

    for element in news_date:
        news= element.find('h3').text.strip()
        date= element.find('div').text.strip()
        if date.find('s')==1:
            date= date.replace('th', '').replace('st', '').replace('nd', '').replace('rd', '')
        else:
            date= date.replace('th', '').replace('nd', '').replace('rd', '')
        date= datetime.strptime(date, '%d %B %Y')
        date= date.strftime('%d/%m/%Y')
        link= element.find('a')['href']

        date_list.append(date)
        headline_list.append(news)
        link_list.append(link)


    news_date= soup.find_all('div', class_='post-content')


    for element in news_date:
        news= element.find(class_='post-title').find('a').text.strip()

        try:
            date= element.find('span', {'class':'post-date'}).text.strip()
            if date.find('s')==1:
                date= date.replace('th', '').replace('st', '').replace('nd', '').replace('rd', '')
            else:
                date= date.replace('th', '').replace('nd', '').replace('rd', '')
            date= datetime.strptime(date, '%d %B %Y')
            date= date.strftime('%d/%m/%Y')
        except:
            date=None
        link= element.find('a')['href']

        date_list.append(date)
        headline_list.append(news)
        link_list.append(link)

    df= pd.DataFrame({
        'headline':headline_list,
        'date':date_list,
        'link':link_list
    })
    return df
