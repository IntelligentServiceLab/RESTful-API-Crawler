import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import configparser

class APIScraper:
    def __init__(self, config_file='config.ini'):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

        # Access values using the section and key
        self.category_url = self.config['URL']['CategoryURL']
        self.category_card_selector = self.config['Selector']['CategoryCard']
        self.category_name_selector = self.config['Selector']['CategoryName']
        self.api_card_selector = self.config['Selector']['APICard']
        self.api_href_selector = self.config['Selector']['APIHref']
        self.api_name_selector = self.config['Selector']['APIName']
        self.api_description_selector = self.config['Selector']['APIDescription']
        self.api_extra_selector = self.config['Selector']['APIExtra']
        self.next_page_selector = self.config['Selector']['NextPage']

    def initialize_browser(self):
        return webdriver.Chrome()

    def cleanup_browser(self, browser):
        browser.quit()

    def get_categories(self, browser, url):
        browser.get(url)
        base_url = "https://rapidapi.com/category/"

        WebDriverWait(browser, 20).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, self.category_card_selector)))
        kinds = browser.find_elements(By.CSS_SELECTOR, self.category_card_selector)

        categories = []

        for category in kinds:
            category_name_element = category.find_element(
                By.CSS_SELECTOR, self.category_name_selector)
            category_name = category_name_element.text.strip()
            category_href = base_url + \
                            category.find_element(
                                By.CSS_SELECTOR, 'a').get_attribute('href').split('/')[-1]

            category_info = {"name": category_name, "href": category_href}
            categories.append(category_info)

        return categories

    def scrape_api_data(self, browser, category):
        name_category = category["name"].replace("/", "_")
        link = category["href"]
        browser.get(link)
        flag = 1

        df = pd.DataFrame(columns=['API名称', 'API链接', 'API描述',
                                   'API Popularity', 'API Latency', 'API Service Level'])
        i = 0

        while flag != 0:
            if i > 40:
                try:
                    WebDriverWait(browser, 20).until(EC.presence_of_element_located(
                        (By.CSS_SELECTOR, self.api_card_selector)))
                    ItemCards = browser.find_elements(
                        by=By.CSS_SELECTOR, value=self.api_card_selector)
                except Exception as e:
                    break
            else:
                WebDriverWait(browser, 20).until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, self.api_card_selector)))
                ItemCards = browser.find_elements(
                    by=By.CSS_SELECTOR, value=self.api_card_selector)

            a_elements = browser.find_elements(
                By.CSS_SELECTOR, self.api_href_selector)
            div_elements = browser.find_elements(
                By.CSS_SELECTOR, self.api_name_selector)
            p_elements = browser.find_elements(
                By.CSS_SELECTOR, self.api_description_selector)
            API_hrefs = [element.get_attribute('href') for element in a_elements]
            names = [element.text for element in div_elements]
            descriptions = [element.text for element in p_elements]

            Popularity = []
            Latency = []
            Service_Level = []

            for element in ItemCards:
                extra = element.find_elements(
                    By.CSS_SELECTOR, value=self.api_extra_selector)
                if extra:
                    Popularity.append(extra[0].text)
                    Latency.append(extra[1].text)
                    Service_Level.append(extra[2].text)
                else:
                    Popularity.append("")
                    Latency.append("")
                    Service_Level.append("")

            api_data = {
                'API名称': names,
                'API链接': API_hrefs,
                'API描述': descriptions,
                'API Popularity': Popularity,
                'API Latency': Latency,
                'API Service Level': Service_Level
            }

            df_new_api = pd.DataFrame.from_dict(api_data)
            df = pd.concat([df, df_new_api], ignore_index=True)

            next_page = []
            if i == 0:
                try:
                    WebDriverWait(browser, 20).until(EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, self.next_page_selector)))
                    next_page = browser.find_elements(
                        by=By.CSS_SELECTOR, value=self.next_page_selector)
                except Exception as e:
                    i = 0
            else:
                WebDriverWait(browser, 20).until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, self.next_page_selector)))
                next_page = browser.find_elements(
                    by=By.CSS_SELECTOR, value=self.next_page_selector)
            flip = ''
            if next_page:
                flip = next_page[0].get_dom_attribute('class')

            if (flip != 'r-page-item disabled') and (flip != ''):
                i += 1
                next_page[0].click()
            else:
                flag = 0

        return df, name_category

if __name__ == '__main__':
    scraper = APIScraper()
    browser = scraper.initialize_browser()
    url = scraper.category_url

    try:
        categories = scraper.get_categories(browser, url)

        for category in categories:
            df, name_category = scraper.scrape_api_data(browser, category)
            csv_path = f"./Results/Basic/{name_category}.csv"
            os.makedirs(os.path.dirname(csv_path), exist_ok=True)
            print(f"./Basic_Mine/{name_category}.csv")
            df.to_csv(csv_path, index=False)
            browser.back()

    finally:
        scraper.cleanup_browser(browser)
