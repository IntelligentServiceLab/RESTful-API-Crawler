from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

browser = webdriver.Chrome()
browser.get('https://rapidapi.com/categories')

# 获取所有的API类型的link
base_url = "https://rapidapi.com/category/"
categories = []

# driver_path = 'C:/Users/李文/AppData/Local/Google/Chrome/Application/chromedriver.exe'
# browser = webdriver.Chrome(executable_path=driver_path)

WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@class='ItemCard']")))
kinds = browser.find_elements(By.XPATH, "//div[@class='ItemCard']")
for category in kinds:
    category_name_element = category.find_element(By.XPATH, ".//span[@class='CategoryName Text body1 bold']")
    category_name = category_name_element.text.strip()
    category_href = base_url + category.find_element(By.XPATH, './a').get_attribute('href').split('/')[-1]

    category_info = {"name": category_name, "href": category_href}
    categories.append(category_info)

for category in categories[0:]:
    name_category = category["name"]
    if name_category == "Artificial Intelligence/Machine Learning":
        name_category = name_category.replace("/", "_")
    link = category["href"]
    browser.get(link)
    flag = 1

    df = pd.DataFrame(columns=['API名称', 'API链接', 'API描述', 'API Popularity', 'API Latency', 'API Service Level'])
    i = 0
    while flag != 0:
        if i > 40:
            try:
                WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@class='ItemCard']")))
                ItemCards = browser.find_elements(by=By.XPATH, value="//div[@class='ItemCard']")
            except Exception as e:
                break
        else:
            WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@class='ItemCard']")))
            ItemCards = browser.find_elements(by=By.XPATH, value="//div[@class='ItemCard']")

        a_elements = browser.find_elements(By.XPATH, '//div[@class="ItemCard"]/a')
        div_elements = browser.find_elements(By.XPATH, '//div[@class="body1 bold ApiName"]')
        p_elements = browser.find_elements(By.XPATH, '//div[@class="CardContent"]/p')
        API_hrefs = [element.get_attribute('href') for element in a_elements]
        names = [element.text for element in div_elements]
        descriptions = [element.text for element in p_elements]

        Popularity = []
        Latency = []
        Service_Level = []

        for element in ItemCards:  # 获取每一个API的方框，提取基本信息
            # 获取Popularity、Latency、Rating信息。注意可能不存在
            extra = element.find_elements(by=By.XPATH, value=".//div[@class='caption']")
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
                WebDriverWait(browser, 20).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//*[@id='category-search']/ul/li[position() = last() - 1]")))
                next_page = browser.find_elements(by=By.XPATH,
                                                  value="//*[@id='category-search']/ul/li[position() = last() - 1]")
            except Exception as e:
                i = 0
        else:
            WebDriverWait(browser, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='category-search']/ul/li[position() = last() - 1]")))
            next_page = browser.find_elements(by=By.XPATH,
                                              value="//*[@id='category-search']/ul/li[position() = last() - 1]")
        flip = ''
        if next_page:
            flip = next_page[0].get_dom_attribute('class')

        if (flip != 'r-page-item disabled') & (flip != ''):
            i += 1
            next_page[0].click()
        else:
            flag = 0

    print(f"./Basic_Mine/{name_category}.xlsx")
    excel_writer = pd.ExcelWriter(f"./Basic_Mine/{name_category}.xlsx", engine='xlsxwriter')
    df.to_excel(excel_writer, index=False)
    excel_writer._save()
    browser.back()

browser.quit()
