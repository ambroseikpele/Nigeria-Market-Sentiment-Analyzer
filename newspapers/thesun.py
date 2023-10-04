import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
today= datetime.today()
r= requests.get('https://sunnewsonline.com/category/business/', headers=headers)
soup= BeautifulSoup(r.content, 'html.parser')
news_date= soup.find_all('a', {'class':'col-lg-4 archive-grid-single'})

date_list=[]
headline_list=[]
link_list=[]

def scrape():
    for element in news_date:
        print(element)
        print()
        news= element.find('h3', {'class':'archive-grid-single-title'}).text.strip()
        print(news)
        date= element.find('p', {'class':'post-date'}).text.strip()
        # Convert the string into a datetime object
        date_obj = datetime.strptime(date, "%b %d, %Y %I:%M %p")

        # Format the datetime object into the desired format
        date = date_obj.strftime("%d/%m/%Y")
        
        link= element['href']
        
        date_list.append(date)
        headline_list.append(news)
        link_list.append(link)

    df= pd.DataFrame({
        'headline':headline_list,
        'date':date_list,
        'link':link_list
    })
    return df