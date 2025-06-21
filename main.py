import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_news():
    url = 'https://udn.com/news/index'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    news_data = []
    titles = soup.select('span.breaking-news__title, span.tab-link__title')

    for title in titles[:10]:
        parent_a = title.find_parent('a')
        if parent_a and parent_a.has_attr('href'):
            link = parent_a['href']
            full_link = 'https://udn.com' + link if link.startswith('/') else link
            news_data.append({'標題': title.text.strip(), '連結': full_link})

    return news_data

def send_discord_message(content, webhook_url):
    data = {"content": content}
    response = requests.post(webhook_url, json=data)
    return response.status_code

def save_to_excel(news_list, filename='news.xlsx'):
    df = pd.DataFrame(news_list)
    df.to_excel(filename, index=False)

def main():
    webhook_url = "https://discord.com/api/webhooks/1386009648162799707/77YSs30HPRZJ5RQ0G8onesRDjgP5g-WSRVBqjkbiuNAd605Elpv0zPuk2O6N7sE_8oIB"
    news_list = fetch_news()

    if not news_list:
        print("沒抓到新聞")
        return


    message = "**📰 今日新聞標題整理：**\n"
    for news in news_list:
        message += f"• [{news['標題']}]({news['連結']})\n"
    message += "\n資料來源：聯合新聞網"


    status = send_discord_message(message, webhook_url)
    print(f"✅ 已推送到 Discord，狀態碼：{status}")

    save_to_excel(news_list)
    print("✅ 已成功存成 news.xlsx")

if __name__ == "__main__":
    main()
