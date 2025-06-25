import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
from fake_useragent import UserAgent
from time import sleep



def get_html(url):
  ua = UserAgent()
  headers = {'User-Agent': ua.random}

  # Make request with fake user-agent
  r = requests.get(url, headers=headers)
  sleep(1)
  return r.content


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

date_list=[]
headline_list=[]
link_list=[]




def scrape(page=1):
    r= requests.get(f'https://punchng.com/topics/business/{page}/', headers=headers)
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

def scrape_date(dt):
    base_url = 'https://punchng.com/topics/business/' #update
    #dt = datetime.strptime(dt, '%d/%m/%Y').date()
    # Step 1: Get base link and max page number
    soup = BeautifulSoup(get_html(base_url))
    link = soup.find_all('li', {'class': 'page-item'})[-1].find('a')['href'].strip('/')

    max_page = int(link[link.rfind('/') + 1:])
    print("max_page : ", max_page)
    #link = link.replace(str(max_page), '')

    # Normalize dt
    if isinstance(dt, str):
        dt = pd.to_datetime(dt).date()

    def get_page_date_range(page):
        
        df = scrape(page)
        print(df)
        df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y').dt.date
        #print(df)
        #print(page_url)
        if df.empty:
            return None, None, df
        return df['date'].min(), df['date'].max(), df

    # Binary search to find the first page that contains the date
    low = 1
    high = max_page
    first_page_with_dt = None

    while low <= high:
        mid = (low + high) // 2
        min_date, max_date, df = get_page_date_range(mid)

        if df.empty:
            high = mid - 1
            continue

        if min_date <= dt <= max_date:
            first_page_with_dt = mid
            high = mid - 1  # keep looking to the left
        elif dt < min_date:
            high = mid - 1
        else:
            low = mid + 1

    if first_page_with_dt is None:
        return pd.DataFrame()

    # Start scraping from the first matching page forward
    all_data = []
    for page in range(first_page_with_dt, max_page + 1):
        _, _, df = get_page_date_range(page)
        if df.empty:
            continue
        # Stop if we passed the date
        if df['date'].min() > dt:
            break
        all_data.append(df[df['date'] == dt])

    if all_data:
        return pd.concat(all_data, ignore_index=True)
    else:
        return pd.DataFrame()
