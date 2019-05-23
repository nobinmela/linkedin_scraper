import csv
import parameters
from parsel import Selector
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def validate_field(field):
    if field:
        pass
    else:
        field = ''
    return field


writer = csv.writer(open('H1', 'w'))
writer.writerow(['Name', 'Job Title', 'School', 'Location', 'URL'])

driver = webdriver.Chrome('../chromedriver')
driver.get('https://www.linkedin.com')

username = driver.find_element_by_class_name('login-email')
username.send_keys(parameters.linkedin_username)
sleep(0.5)

password = driver.find_element_by_id('login-password')
password.send_keys(parameters.linkedin_password)
sleep(0.5)

sign_in_button = driver.find_element_by_xpath('//*[@type="submit"]')
sign_in_button.click()
sleep(5)

driver.get('https://www.google.com')
sleep(3)

search_query = driver.find_element_by_name('q')
# driver.current_url (bash)
search_query.send_keys(parameters.search_query)
sleep(0.5)

# from selenium.webdriver.common.keys import Keys (bash)
search_query.send_keys(Keys.RETURN)
sleep(3)

# linkedin_urls = driver.find_elements_by_tag_name('cite')
linkedin_urls = driver.find_elements_by_xpath(
    '//cite[contains(text(),"linkedin")]')
# len(linkedin_urls)  (Bash)
# linkedin_urls[0].text
linkedin_urls = [url.text for url in linkedin_urls]
sleep(0.5)

for linkedin_url in linkedin_urls:
    driver.get(linkedin_url)
    sleep(5)

    sel = Selector(text=driver.page_source)

    name = sel.xpath('//h1[contains(@class,"name")]/text()').extract_first()
    if name:
        name = name.strip()

        # For removing "\n      " and "\n    " from "'\n      Paul Garner(name)\n    '" we use strip()

    job_title = sel.xpath(
        '//h2[contains(@class,"headline")]/text()').extract_first()
    if job_title:
        job_title = job_title.strip()

    school = sel.xpath(
        '//h3[contains(@class,"school-name")]/text()').extract_first()

    location = sel.xpath(
        '//h3[contains(@class,"location")]/text()').extract_first()
    if location:
        location = location.strip()

    linkedin_url = driver.current_url

    name = validate_field(name)
    job_title = validate_field(job_title)
    school = validate_field(school)
    location = validate_field(location)
    linkedin_url = validate_field(linkedin_url)

    print('\n')
    print('Name: ' + name)
    print('Job Title: ' + job_title)
    print('School: ' + school)
    print('Location: ' + location)
    print('URL: ' + linkedin_url)
    print('\n')

    writer.writerow([name.encode('utf-8'),
                     job_title.encode('utf-8'),
                     school.encode('utf-8'),
                     location.encode('utf-8'),
                     linkedin_url.encode('utf-8')])

    try:
        driver.find_element_by_xpath(
            '//button[@aria-label="More actions"]').click()
        sleep(3)

        driver.find_element_by_xpath('//span[text()="Connect"]').click()
        sleep(3)

        driver.find_element_by_xpath('//button[text()="Send now"]').click()
        sleep(3)

    except:
        pass


driver.quit()
