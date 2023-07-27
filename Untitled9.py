#!/usr/bin/env python
# coding: utf-8

# In[42]:


import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd


# In[62]:


def fetch_data(page_url):
    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    return soup

def find_links(soup):
    links = [a['href'] for a in soup.find_all('a', href=True, class_='title')]
    
    return links

def find_info(soup):
    job_titles = soup.find_all('div', id='contenttitle')
    job_titles = [title.text.strip() for title in job_titles]
    descriptions = soup.find_all('div', class_='desc')
    descriptions = [desc.text.strip() for desc in descriptions]
    phone_numbers = soup.find_all('span', class_='mobilestyle')
    phone_numbers = [phone.text.strip() for phone in phone_numbers]
    locations = soup.find_all('div', class_='viewdesc')
    locations = [location.text.replace("位置：", "").strip() for location in locations if "位置：" in location.text]
    times = soup.find_all('div', class_='posttime')
    times = [time.text.split('：')[-1].strip() for time in times]
    return job_titles, descriptions,locations,times,phone_numbers

web_url = "https://www.168worker.com/list/1_0/"
pages = 2  # 抓取的页数


# In[63]:


with open('results.csv', 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerow(['标题', '描述', '位置', '时间', '电话'])

for i in range(1, pages + 1):
    page_url = web_url + str(i)
    data = fetch_data(page_url)
    links = find_links(data)
    for link in links:
        link = requests.compat.urljoin(page_url, link)
        data = fetch_data(link)
        job_titles, descriptions,locations,times,phone_numbers = find_info(data)
        with open('results.csv', 'a', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f,delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for title, desc, location, time, number in zip(job_titles, descriptions, locations, times, phone_numbers):
                writer.writerow([title, desc, location, time, number])


# In[64]:


df = pd.read_csv('results.csv')
df


# In[ ]:




