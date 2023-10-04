import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
today= datetime.today()
r= requests.get('https://guardian.ng/category/business-services/', headers=headers)
soup= BeautifulSoup(r.content, 'html.parser')
news_date= soup.find_all('div', {'class':'item design-article'})
#news_date= [i for i in news_date if 'Business' in i.find('div', {'class':'category'}).text ]

date_list=[]
headline_list=[]
link_list=[]


def scrape():
    for element in news_date:
        news= element.find('span', {'class':'title'}).text.strip()
        date= element.find('div', {'class':'age'}).text.strip()
        
        if 'hours' in date or 'hour' in date:
            hours= date.replace(' hour ago', '')
            hours= hours.replace(' hours ago', '')
            hours=int(hours)
            date= today- timedelta(hours=hours)
        elif 'day' in date or 'days' in date:
            days= date.replace(' day ago', '')
            days= days.replace(' days ago', '')
            days= int(days)
            date= today- timedelta(days=days)
            
        else:
        
            date = datetime.strptime(date, "%d %b")
            date= date.strftime(f'%d/%m/{year}')
        try:
            date= date.strftime('%d/%m/%Y')
        except:
            pass
        year= date[-4:]
        link= element.find('span', {'class':'title'}).find('a')['href']
        
        date_list.append(date)
        headline_list.append(news)
        link_list.append(link)

    df= pd.DataFrame({
        'headline':headline_list,
        'date':date_list,
        'link':link_list
    })
    return df