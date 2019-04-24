#!/usr/bin/env python
# coding: utf-8

# In[6]:


from bs4 import BeautifulSoup as bs
import pandas
from splinter import Browser
import time


# In[7]:
def init_browser(): 
        executable_path = {'executable_path': '/Users/psaha/Anaconda3/chromedriver'}
        return Browser('chrome', **executable_path, headless=False)


# In[8]:


mars_data = {}


# In[9]:


#Part-1
def scrape_news():
        try:
                browser = init_browser()
                url = 'https://mars.nasa.gov/news/'
                browser.visit(url)



# In[10]:


                html = browser.html
                soup = bs(html, 'html.parser')


# In[12]:


                news_title = soup.find('div', class_="article_teaser_body").text
                news_p =  soup.find('div', class_='content_title').text


# In[13]:


                mars_data['News_Title'] = news_title
                mars_data['News_Parag'] = news_p


# In[14]:
        finally:
                browser.quit()



# In[15]:
def scrape_image():
        try:
                browser = init_browser()

                url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
                browser.visit(url)


# In[16]:


                time.sleep(3)
                html = browser.html
                soup = bs(html, 'html.parser')


# In[17]:


                browser.click_link_by_id('full_image')


# In[18]:


                time.sleep(3)
                html = browser.html
                soup = bs(html, 'html.parser')


# In[19]:


                featured = soup.find('div', class_="fancybox-inner fancybox-skin fancybox-dark-skin fancybox-dark-skin-open")


# In[20]:


                link = featured.find('img')['src']



# In[21]:


                base_url = 'https://www.jpl.nasa.gov'
                full_url = base_url + link
                full_url


# In[22]:


                mars_data['featured_image'] = full_url


# In[23]:


        finally:
                browser.quit()


# In[29]:
def scrape_weather():
        try:
                browser = init_browser()

#Part-3
                url = 'https://twitter.com/marswxreport?lang=en'
                browser.visit(url)


# In[30]:


                html = browser.html
                soup = bs(html, 'html.parser')


# In[31]:


                results = soup.find_all('div', class_='js-tweet-text-container')
                list_tweets = []
                for result in results:
                        if 'InSight' in result.text:
                                tweets = result.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')
                                stripped_tweets = tweets.text.lstrip()
                                tweet = stripped_tweets[:-26]
                                list_tweets.append(tweet)
        


# In[32]:


                mars_data['weather'] = list_tweets[0]


# In[33]:

        finally:
                browser.quit()




# In[34]:
def scrape_facts():
        try:
                browser = init_browser()

#Part-4
                url = 'https://space-facts.com/mars/'
                browser.visit(url)


# In[35]:


                html = browser.html
                soup = bs(html, 'html.parser')


# In[36]:


                import pandas as pd
                import numpy as np


# In[37]:


                tables = pd.read_html(url)

# In[39]:


                df = tables[0]
                df.columns = ['Planet facts', 'Measurements']
                df.set_index('Planet facts', inplace = True)


# In[44]:


                data = df.to_html()


# In[45]:


                mars_data['Mars_Facts'] = data


# In[46]:
        finally:
                browser.quit()





# In[49]:
def scrape_hemispheres():
        try:
                browser = init_browser()


#Part-5
                url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
                browser.visit(url)


# In[50]:


                html = browser.html
                soup = bs(html, 'html.parser')


# In[51]:


                partial_text = []
                texts = soup.find_all('h3')
                for x in texts:
                        partial_text.append(x.text)


                links = []
                for x in partial_text:
                        browser.click_link_by_partial_text(x)
                        time.sleep(6)
                        html = browser.html
                        soup = bs(html, 'html.parser')
                        link = soup.find('div', class_='wide-image-wrapper').find('a')['href']
                        links.append(link)
                        time.sleep(6)
                        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
                        browser.visit(url)
                        time.sleep(6)
                        html = browser.html
                        soup = bs(html, 'html.parser')



                keys = ['title', 'img_url']
    


# In[59]:


                hemisphere_image_urls = [{key:'' for key in keys} for link in links]
                hemisphere_image_urls


                x = 0
                for text in partial_text:
                        hemisphere_image_urls[x]['title'] = text
                        x += 1


# In[61]:


                x = 0
                for link in links:
                        hemisphere_image_urls[x]['img_url'] = link
                        x += 1



                mars_data['Hemispheres'] = hemisphere_image_urls

        finally:
                browser.quit()

# In[64]:
        return mars_data


# In[ ]:




