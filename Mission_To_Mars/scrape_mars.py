import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    # browser = init_browser()
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Create blank dictionary
    mars_information = {}

    # Visit URL
    url = 'https://redplanetscience.com/'   
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # Blank list and dictionary for storing news information
    news_list = []
    news_dict = {}

    # Pull Titles and Preview paragraphs from the html link. Store the first title and preview text
    news_title = soup.find_all('div', class_='content_title')[0].text
    news_p = soup.find_all('div', class_='article_teaser_body')[0].text

    # Store in sub dictionary "news_dict"
    news_dict['title'] = news_title
    news_dict['paragraph'] = news_p
    news_list.append(news_dict)

    # Visit URL for webpage
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)
    browser.click_link_by_partial_text('FULL IMAGE')

    # Parse through HTML code with BeautifulSoup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Pull all images from webpage into list
    images = soup.find_all('img')

    # Pull the link to the feature image
    for image in images:
        if 'feature' in image['src']:
            image_url = image['src']

    # Create full link to the featured image
    featured_image_url = url + image_url

    # Read all tables from url into pandas
    url = 'https://galaxyfacts-mars.com'
    mars_table = pd.read_html(url)

    # Convert each table into a separate dataframe
    mars_df1 = mars_table[0]
    mars_df2 = mars_table[1]

    # Convert dataframes to HTML table string
    html_table1 = mars_df1.to_html()
    html_table2 = mars_df2.to_html()
    mars_html_list = [html_table1, html_table2]

    # Visit URL
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # Parse through HTML code with BeautifulSoup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Pull all divs in the HTML code with the class item. All hemisphere info is stored here
    results = soup.find_all('div', class_='item')

    # Create blank dictionary and list
    hemispheres_dict = {}
    hemispheres_list = []

    # Iterate through all divs from above and pull the title and image link
    for result in results:
        title = result.find('h3').text
        link_temp = result.find('a')['href']
        link = url + link_temp
        
        # Store in a dictionary and append each dictionary to a list
        hemispheres_dict['title'] = title
        hemispheres_dict['img_url'] = link
        hemispheres_list.append(hemispheres_dict)

    # Quit the browser
    browser.quit()
    
    # Store all information in main dictionary "mars_information"
    mars_information['Mars_News'] = news_list
    mars_information['Mars_Photo'] = featured_image_url
    mars_information['Mars_Stats'] = mars_html_list
    mars_information['Mars_Hemispheres'] = hemispheres_list

    return mars_information