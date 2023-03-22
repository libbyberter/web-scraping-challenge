from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


def scrape_info():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    time.sleep(1)
    # SCRAPE 1

    # Visit webpage
    url = "https://redplanetscience.com/"
    browser.visit(url)
    #read webpage
    html = browser.html
    soup = bs(html, 'html.parser')
    time.sleep(1)
    # Scrape page into Soup
    result = soup.find('div',class_='list_text')
    news_title = result.find(class_='content_title').text.strip()
    news_article = result.find(class_='article_teaser_body').text.strip()


    # SCRAPE 2
    # Visit webpage
    url2 = "https://spaceimages-mars.com/"
    browser.visit(url2)
    #read webpage
    html = browser.html
    soup = bs(html, 'html.parser')
    time.sleep(1)
    # Scrape page into Soup
    result = soup.find('div',class_='floating_text_area')
    featured_image = result.find('a')['href']
    featured_image_url = ('https://spaceimages-mars.com/' + featured_image)


    # SCRAPE 3
    # Visit webpage
    url3 = "https://galaxyfacts-mars.com"
    #read webpage
    web_table = pd.read_html(url3)
    time.sleep(1)
    # Format table
    df = web_table[0]
    df.columns = ['Description', 'Mars', 'Earth']
    df = df.iloc[1:]
    df.set_index('Description', inplace=True)
    mars_table = df.to_html()
    mars_table = mars_table.replace('<table border="1" class="dataframe"',\
        '<table border="1" class="table  table-sm table-striped  w-auto" style="text-align: center"')


    # SCRAPE 4
    #Website info
    hemispheres_url = "https://marshemispheres.com/"
    browser.visit(hemispheres_url)
    #read webpage
    html = browser.html
    soup = bs(html, 'html.parser')
    time.sleep(1)

    # Scrape page into Soup
    #list for hemispheres
    hemi_list=[]
    #dictionary for hemisphere data
    hemi_dict_list=[]
    #get links for the hemispheres
    hemispheres = soup.find_all('div', class_='description')
    for hemisphere in hemispheres:
        a = hemisphere.find('a')
        href = a['href']
        link = (hemispheres_url + href)
        hemi_list.append(link)

    for i in hemi_list:
    #get hemishphere info
        hemi_url = i
        browser.visit(hemi_url)
        #read webpage
        html = browser.html
        soup = bs(html, 'html.parser')
        time.sleep(1)
        #image
        result = soup.find('div', id="wide-image", class_="wide-image-wrapper")
        result_image = result.find(class_='wide-image')['src']
        result_image_url = (hemispheres_url + result_image)
        #title
        result_title = soup.find('div', class_="cover")
        result_title_text = result_title.find('h2', class_='title').text.strip()
        hemi_dict = ({"title": result_title_text, "img_url": result_image_url})
        hemi_dict_list.append(hemi_dict)


    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_article": news_article,
        "featured_image": featured_image,
        "featured_image_url": featured_image_url,
        "mars_table": mars_table,
        "hemispheres": hemi_dict_list
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
