import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

options = Options()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=Service(), options=options)
driver.maximize_window()
driver.get("https://books.toscrape.com/")

with open('books.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Title', 'Price', 'Availability', 'Rating', 'UPC', 'Price (Excl. Tax)', 'Price (Incl. Tax)', 'Tax', 'Number of Reviews'])

    while True:
        books = driver.find_elements(By.CSS_SELECTOR, 'li.col-xs-6.col-sm-4.col-md-3.col-lg-3')
        for book in books:
            book_page_link = book.find_element(By.CSS_SELECTOR, 'h3 a').get_attribute('href')
            driver.get(book_page_link)

            title = driver.find_element(By.CSS_SELECTOR, 'div.product_main h1').text
            price = driver.find_element(By.CSS_SELECTOR, 'p.price_color').text
            availability = driver.find_element(By.CSS_SELECTOR, 'p.instock.availability').text.split()[0]
            rating = driver.find_element(By.CSS_SELECTOR, 'p.star-rating').get_attribute('class').split()[-1]
            upc = driver.find_element(By.CSS_SELECTOR, 'table.table-striped tr:nth-child(1) td').text
            price_excl_tax = driver.find_element(By.CSS_SELECTOR, 'table.table-striped tr:nth-child(3) td').text
            price_incl_tax = driver.find_element(By.CSS_SELECTOR, 'table.table-striped tr:nth-child(4) td').text
            tax = driver.find_element(By.CSS_SELECTOR, 'table.table-striped tr:nth-child(5) td').text
            number_of_reviews = driver.find_element(By.CSS_SELECTOR, 'table.table-striped tr:nth-child(7) td').text

            writer.writerow([title, price, availability, rating, upc, price_excl_tax, price_incl_tax, tax, number_of_reviews])

            driver.back()

        try:
            next_button = driver.find_element(By.CSS_SELECTOR, 'li.next a')
            next_button.click()
            time.sleep(2)  
        except:
            print("No more pages to scrape.")
            break


driver.quit()
