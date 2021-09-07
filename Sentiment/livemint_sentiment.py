# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 02:40:44 2021

@author: User
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 00:28:12 2021

@author: Ashu Prakash 
"""
import pandas as pd
import numpy as np

def senti_livemint(page):
    
    import re
    import bs4
    import requests
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    
    def cleanhtml(raw_html):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext
    
    url = 'https://www.livemint.com/market/stock-market-news/page-'+str(page)
    request = requests.get(url)
    soup = bs4.BeautifulSoup(request.text, 'html.parser')
    url_list = []
    headline_list = []
    news_list = []
    time_list = []
    
    all_links = soup.find_all('h2', {'class':'headline'}) 
    
    for x in all_links:
        headline_list.append(x.get_text().split('\n')[2].lstrip())
        url_list.append('https://www.livemint.com/'+ x.find_all('a')[0].get('href'))
        
    for this_url in url_list:
        temp_request = requests.get(this_url)
        temp_soup = bs4.BeautifulSoup(temp_request.text, 'html.parser')
            
        news = temp_soup.find_all('p')
        for para in reversed(news):
            if 'Never miss a story!' in str(para):
                k = news.index(para)
        
        temp = ''
        for i in range(1,k):
            temp = temp + str(news[i])
            temp = cleanhtml(temp)
            temp = temp.replace('\n',' ').replace('\t','')
        
        news_list.append(temp)
        
        time = str(temp_soup.find_all('span', {'class':'articleInfo pubtime'})[0]).split('Updated')[-1]
        time = cleanhtml(time)
        time = time.lstrip(':')
        time_list.append(time)
    
    # Creating a DataFrame
    news_df = pd.DataFrame({
        'Date':time_list,
        'Headline':headline_list,
        'News':news_list
        })
    
    # Sentiment Analysis
    analyser = SentimentIntensityAnalyzer()
    
    def comp_score(text):
        return analyser.polarity_scores(text)["compound"]   
      
    news_df["Sentiment"] = news_df["News"].apply(comp_score)
    
    return news_df

# Getting News and Sentiments for multiple pages
df_all = pd.DataFrame()
for i in range(1,11):
    df = senti_livemint(i)
    df_all = pd.concat([df_all, df], axis=0)

df_all.index = np.arange(1, len(df_all)+1)
        

    
