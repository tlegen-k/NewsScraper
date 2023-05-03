from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime

"""
This code scrapes headlines of latest news in French and Spanish from following links: www.LeMonde.fr, www.elMundo.es.  
"""


def scrape_french(url):
    print('Extracting French news')
    french_cnt = ''
    french_cnt += '<b>French Top Stories:</b>\n'+'<br>'+'-'*50+'<br>'

    # Going into headless mode
    # No instance of Chrome will be opened to imitate session
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1200")

    # Starting the session
    driver = webdriver.Chrome(options=options)
    # Take action on browser
    driver.get(url)
    # waiting for articles links to load
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="gdpr-lmd-button gdpr-lmd-button--big gdpr-lmd-button--main"]'))).click()
        
        # Take a screenshot of main page
        driver.save_screenshot('lemonde-1.png')

        # wait to load
        WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'article__title'))
            )
        
        # Take a screenshot of main page after accepting cookies
        driver.save_screenshot('lemonde-2.png')

        # find main article url and title
        main_article_url = driver.find_element(by=By.XPATH, value='//div[@class="article article--main"]//a')
        main_article_title = driver.find_element(by=By.XPATH, value='//div[@class="article article--main"]//p[@class="article__title-label"]')

        urls_list = []
        titles_list = []

        # append main article information
        urls_list.append(main_article_url.get_attribute("href"))
        titles_list.append(main_article_title.text)

        # find other top articles
        article_urls   = driver.find_elements(by=By.XPATH, value='//div[@class="article article--headlines"]//a')
        article_titles = driver.find_elements(by=By.XPATH, value='//div[@class="article article--headlines"]//p[@class="article__title"]')

        for url in range(len(article_urls)):
            urls_list.append(article_urls[url].get_attribute("href"))

        for title in range(len(article_titles)):
            titles_list.append(article_titles[title].text)

        for i in range(len(titles_list)):
            french_cnt += str(i+1) + ' :: ' + titles_list[i] + ' (' + urls_list[i] + ')' + "\n" + '<br>'
    
    # close connection
    finally:
        driver.quit()

    return french_cnt

def scrape_spanish(url):
    print('Extracting Spanish news')
    spanish_cnt = ''
    spanish_cnt += '<b>Spanish Top Stories:</b>\n' + '<br>' + '-' * 50 + '<br>'

    # Going into headless mode
    # No instance of Chrome will be opened to imitate session
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1200")

    # Starting the session
    driver = webdriver.Chrome(options=options)
    # Take action on browser
    driver.get(url)
    # waiting for articles links to load
    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'ue-c-cover-content__link'))
        )
        # Take a screenshot of main page
        driver.save_screenshot('elmundo.png')

        article_urls = driver.find_elements(by=By.XPATH, value='//a[@class="ue-c-cover-content__link"][not(@cmp-ltrk="Bloque Apertura")]')
        article_titles = driver.find_elements(by=By.XPATH,
                                              value='//a[@class="ue-c-cover-content__link"]//h2[@class="ue-c-cover-content__headline"]')

        urls_list = []
        for url in range(len(article_urls)):
            urls_list.append(article_urls[url].get_attribute("href"))

        titles_list = []
        for title in range(len(article_titles)):
            titles_list.append(article_titles[title].text)

        # taking only first 3 news
        for i in range(3):
            spanish_cnt += str(i + 1) + ' :: ' + article_titles[i].text + ' (' + article_urls[i].get_attribute(
                "href") + ')' + "\n" + '<br>'
    # close connection
    finally:
        driver.quit()

    return spanish_cnt

if __name__ == "__main__":
    # current time
    now = datetime.datetime.now()

    content = ''

    url_french = 'https://www.lemonde.fr/'
    french_cnt = scrape_french(url_french)
    content += french_cnt

    content += '<br>' + '-' * 50 + '<br>'

    url_spanish = 'https://www.elmundo.es/'
    spanish_cnt = scrape_spanish(url_spanish)
    content += spanish_cnt
    content += '<br><br>End of Message'

    print('Composing Email...')
    SERVER = 'smtp.gmail.com'
    PORT = 587
    FROM = 'FROM-EMAIL'
    TO = 'TO-EMAIL'
    PASS = 'PASSWORD'

    msg = MIMEMultipart()
    msg['Subject'] = 'French and Spanish Top News [Automated Email]' + ' ' + str(now.day) + '-' + str(now.month) + '-' + str(
        now.year)
    msg['From'] = FROM
    msg['To'] = TO

    msg.attach(MIMEText(content, 'html'))
    print('Initiating Server...')
    # initialize server
    server = smtplib.SMTP(SERVER, PORT)
    server.set_debuglevel(1)
    # initialize transaction
    server.ehlo()
    server.starttls()
    server.login(FROM, PASS)
    server.sendmail(FROM, TO, msg.as_string())

    print('Email Sent...')
    server.quit()