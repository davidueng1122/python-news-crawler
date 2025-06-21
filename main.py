import requests
from bs4 import BeautifulSoup
import csv


url = 'https://udn.com/news/index'


response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')


news_items = soup.select('div.story-list__news a')


news_data = []
for item in news_items[:10]:  
    title = item.text.strip()
    link = item['href']
    full_link = 'https://udn.com' + link if link.startswith('/') else link
    news_data.append([title, full_link])


with open('news.csv', 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['標題', '連結'])
    writer.writerows(news_data)

print("已成功儲存前10筆新聞到 news.csv")
