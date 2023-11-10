from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
browser = webdriver.Chrome()

def myparse():
    method = mid_form.find_element(By.XPATH, '//span[contains(@class, "chkRTK")]').text
    name = mid_form.find_element(By.XPATH, '//span[contains(@class, "frTTIz")]').text
    description = mid_form.find_elements(By.XPATH, "//div[@class='sc-dmovaM jttrbn']//p")
    # 获取endpoint名称
    endpoint_name = f'{method}:{name}'
    endpoint_description = ''
    if description:
    #获取endpoint描述文本
        endpoint_description = description[0].text
        print("endpoint_name值为"+endpoint_name)
    #获取除参数以外的元素（headerparam，X-rapidapi_key）
    extra_info = mid_form.find_elements(By.XPATH, '//div[@class="ant-collapse ant-collapse-icon-position-start"]/div')
    required_para = {}
    optional_para = {}
    if len(extra_info) > 1:
        for parameter in extra_info[0:]:
            # 除了Header Parameter， 先获取他们的Title，在parse 中间的部分
            parameter_type_elements = parameter.find_elements(By.XPATH, "//div[@class='ant-collapse-header']/span")
            texts = [element.text for element in parameter_type_elements]
            # 打印每个元素的文本内容
            for parameter_type in texts:
                print("输出的值为"+parameter_type)
            if parameter_type != 'Request Body':
                v_name = []
                v_type = []
                v_caution = []
                #无
                for variable in parameter.find_elements(By.XPATH, ".//div[@class='sc-gCkVGe hlHRNw']"):
                      name = variable.find_element(By.XPATH, ".//label[@class='name']")
                      my_type = variable.find_element(By.XPATH, ".//div[@class='type']")
                      caution = variable.find_element(By.XPATH, ".//div[@class='description']")
                      v_name.append(name.text)
                      v_type.append(my_type.text)
                      v_caution.append(caution.text)
                if parameter_type == 'Optional Parameters':
                     optional_para = {'参数名': v_name, '参数类型': v_type, '参数注意事项': v_caution}
                else:
                      required_para = {'参数名': v_name, '参数类型': v_type, '参数注意事项': v_caution}
            else:
                continue
    return endpoint_name, endpoint_description, required_para, optional_para
directory_path = 'D:/李文/Documents/Python/draft/rapid/Basic_Mine'
file = pd.read_excel('./example.xlsx', engine='openpyxl')
# 这里是所有种类API的文件
for filename in file['File Paths'][33:]:
    cannotEndpoion_failures = 0
    antilimitIP = 0
    # 将某一类的API文件读入，获取其中API的链接以供爬取
    df = pd.read_excel(filename)
    # 存储一类API所有的Endpoints，所以在文件loop定义
    # try:
    result = pd.DataFrame(
        columns=['API名称', 'API链接', 'API_Host', 'Endpoint名称', 'Endpoint描述', 'Endpoint种类', 'Endpoint必须参数','Endpoint可选参数'])
    # 对于每一个API，获取他的href开始爬取
    for i, api_link in enumerate(df['API链接']):
        antilimitIP += 1
        if antilimitIP == 250:
            time.sleep(250)
            antilimitIP = 0
        print(api_link)
        if cannotEndpoion_failures==5:
            print("Endpoint连续五次空值，结束该种类")
            break
        retry_count = 0
        flag = 0
        while retry_count<=5 and flag==0:
            try:
                if not api_link.startswith('https://rapidapi.com/'):
                    df.at[i, 'API链接'] = 'https://rapidapi.com' + api_link
                API_name = df.at[i, 'API名称']
                # 对于每一个API要先等待渲染，然后找到左侧和中间的根元素
                browser.get(df.at[i, 'API链接'])
                # 要注意，可能有些API已失效 比如Science/disaster-science/（https://rapidapi.com/disaster-science-disaster-science-default/api/disaster-science/）
                try:
                    WebDriverWait(browser, 10).until(
                        EC.frame_to_be_available_and_switch_to_it(
                            (By.XPATH, '//div[@class="flexContainer dirColumn TabContent"]/iframe')))
                except Exception as e:
                    flag=1
                    print("API not found 跳过")
                    continue
                Explor = browser.find_elements(By.XPATH, "//div[@class='css-1qfe40h']")
                # print(login)
                print(Explor)
                # 出现登录信息跳过该页面
                # if len(login) != 0 or len(Explor) != 0:
                if len(Explor) != 0:
                    api_data = {
                        'API名称': API_name,
                        'API链接': df.at[i, 'API链接'],
                        'API_Host': 'Require login',
                        'Endpoint名称': 'Require login',
                        'Endpoint描述': 'Require login',
                        'Endpoint种类': 'Require login',
                        'Endpoint必须参数': 'Require login',
                        'Endpoint可选参数': 'Require login',
                    }
                    df_new_api = pd.DataFrame.from_dict(api_data, orient='index')
                    df_new_api = df_new_api.transpose()
                    result = pd.concat([result, df_new_api], ignore_index=True)
                    flag = 1
                    print("出现登录界面或Explorer 跳过")
                    continue
                left_endpoints = []
                #获取所有leftendpoint，如果为空则跳过
                try:
                    WebDriverWait(browser, 20).until(EC.presence_of_all_elements_located((By.XPATH,'//div[@class="ant-spin-container"]')))
                    # login = browser.find_elements(By.XPATH, "//div[@class='ant-spin ant-spin-spinning']")
                    left_endpoints = browser.find_elements(By.XPATH,'//div[@class="ant-collapse ant-collapse-icon-position-start endpoints-list-collapse"]/div')
                    print(len(left_endpoints))
                    if len(left_endpoints) == 0:
                        print("Endpoint为空 跳过")
                        cannotEndpoion_failures += 1
                        flag=1
                        continue
                #超时跳过
                except TimeoutException:
                    flag = 1
                    print("Endpoint超时 跳过")
                    continue
                #爬取header中的host
                WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//form[@class="ant-form ant-form-horizontal sc-irmnWS AIKVv"]')))
                mid_form = browser.find_element(By.XPATH,
                                                '//form[@class="ant-form ant-form-horizontal sc-irmnWS AIKVv"]')
                API_host = mid_form.find_element(By.XPATH,
                                                 '//input[@id="x-rapidapi-host"]').get_dom_attribute('value')
                #遍历所有endpoint
                for endpoints in left_endpoints:
                    result_data = myparse()
                    Endpoint_category, Endpoint_name, Endpoint_description = '', '', ''
                    Required_para, Optional_para = {}, {}
                    if 'sc-eWhHU' not in endpoints.get_dom_attribute('class'):
                        if endpoints.get_dom_attribute('class') == 'ant-collapse-item endpoints-panel':
                            endpoints.click()
                        Endpoint_category = endpoints.find_element(By.XPATH,
                                                                   './/span[@class="group-name"]').text
                        # 从这里开始就要提取元素了  首先是API名字（点开页面后选取）、API类型（filename）、Endpoint的类型
                        # 等待Title下拉栏子元素可以被点击
                        try:
                            WebDriverWait(endpoints, 30).until(
                                EC.element_to_be_clickable(
                                    (By.XPATH,
                                     './/div[@class="ant-collapse-content-box"]/div')))
                        except Exception as e:
                            print("An exception occurred:", str(e))
                            # browser.quit()
                            # time.sleep(5)  # Wait for a while before restarting
                            # browser = webdriver.Chrome()
                            # break
                        for endpoint in endpoints.find_elements(By.XPATH, './/div[@class="ant-collapse-content-box"]/div'):
                            endpoint.click()
                            WebDriverWait(browser, 10).until(
                                EC.presence_of_element_located(
                                    (By.XPATH,
                                     '//form[@class="ant-form ant-form-horizontal sc-irmnWS AIKVv"]')))
                            Endpoint_name, Endpoint_description, Required_para, Optional_para = myparse()
                            api_data = {
                                'API名称': API_name,
                                'API链接': df.at[i, 'API链接'],
                                'API_Host': API_host,
                                'Endpoint名称': Endpoint_name,
                                'Endpoint描述': Endpoint_description,
                                'Endpoint种类': Endpoint_category,
                                'Endpoint必须参数': [Required_para],
                                'Endpoint可选参数': [Optional_para],
                            }
                            df_new_api = pd.DataFrame.from_dict(api_data, orient='index')
                            df_new_api = df_new_api.transpose()
                            result = pd.concat([result, df_new_api], ignore_index=True)
                    else:
                        endpoints.click()
                        WebDriverWait(browser, 10).until(
                            EC.presence_of_element_located(
                                (By.XPATH,
                                 '//form[@class="ant-form ant-form-horizontal sc-irmnWS AIKVv"]')))
                        Endpoint_name, Endpoint_description, Required_para, Optional_para = myparse()
                        api_data = {
                            'API名称': API_name,
                            'API链接': df.at[i, 'API链接'],
                            'API_Host': API_host,
                            'Endpoint名称': Endpoint_name,
                            'Endpoint描述': Endpoint_description,
                            'Endpoint种类': Endpoint_category,
                            'Endpoint必须参数': [Required_para],
                            'Endpoint可选参数': [Optional_para],
                        }
                        df_new_api = pd.DataFrame.from_dict(api_data, orient='index')
                        df_new_api = df_new_api.transpose()
                        result = pd.concat([result, df_new_api], ignore_index=True)
                    result.to_excel(f"./Detail_Mine/{filename.split('/')[-1].split('.')[0]}.xlsx", index=False)
                    print(f"./Detail_Mine/{filename.split('/')[-1].split('.')[0]}.xlsx")
                flag = 1
                print("成功获取")
                cannotEndpoion_failures = 0
                break
            except Exception as e:
                print("报错"+str(e))
                print(f"重试API {api_link} ({retry_count}/5)")
                retry_count +=1
                time.sleep(5)
    break
    # except Exception as e:
browser.quit()

