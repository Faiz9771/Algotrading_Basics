# Normal scraping doesnt work on websites anymore hence we will try scraping it with selenium 


import requests
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0"}

url = "https://finance.yahoo.com/quote/AAPL/financials/"
page = requests.get(url, headers=headers)

page_content = page.content

soup = BeautifulSoup(page_content,"html.parser")
table = soup.find_all("div",{"class" : "tableBody yf-yuwun0"})