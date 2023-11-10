from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
browser = webdriver.Chrome()
directory_path = '/rapid/Basic_Mine'
file = pd.read_excel('./example.xlsx', engine='openpyxl')
for filename in file['File Paths'][35:]:
    cannotEndpoion_failures = 0
    antilimitIP = 0
    # 将某一类的API文件读入，获取其中API的链接以供爬取
    df = pd.read_excel(filename)
    result = pd.DataFrame(columns=['API链接','Update_Time','Author'])
    # 对于每一个API，获取他的href开始爬取
    for i, api_link in enumerate(df['API链接']):
        if cannotEndpoion_failures==3:
            print("连续三次找不到，结束该种类")
            break
        #防止IP锁定
        antilimitIP += 1
        if antilimitIP == 250:
            time.sleep(250)
            antilimitIP = 0
        print(api_link)
        try:
            browser.get(api_link)
            element = browser.find_element(By.XPATH, './/div[@class="About"]')
            element_text = element.text
            split_text = element_text.split("|")
            #作者信息
            split_text[0] = split_text[0].replace("By", "");
            #更新时间
            split_text[1] = split_text[1].replace("Updated ","");
            api_data = {
                'API链接': api_link,
                'Update_Time': split_text[1],
                'Author': split_text[0]
            }
            api_data_df = pd.DataFrame(api_data, index=[0])
            api_data_df.to_csv('./ExtraInfo.csv', mode='a', index=False, header=False)
            cannotEndpoion_failures = 0
        except Exception as e:
            print("报错" + str(e))
            cannotEndpoion_failures += 1
            continue
    # break
    # except Exception as e:
browser.quit()

