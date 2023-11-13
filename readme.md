# 目录

1. **[数据集简介](#1-数据集简介)**  
2. **[软件包说明](#2-软件包说明)**  
3. **[代码使用说明](#3-代码使用说明)**  
 - **[项目结构](#项目结构)**  
 - **[核心代码](#核心代码)**  
 - **[结果保存](#结果保存)**  
4. **[数据集字段说明](#4-数据集字段说明)**  
5. **[API调用及组合示例](5-API调用及组合示例)**  

## 1-数据集简介

 所有数据均是使用爬虫从[Rapid API Hub](https://rapidapi.com/hub)中获取的。网站中的 API 帮助开发者快速编写代码并使用更广泛的 API 进行开发。爬取这些数据可以帮助研究者用于数据挖掘和信息提取，以发现隐藏的模式、关系和知识，进行服务组合以及服务推荐等深入探索。

 获取的数据集文件以所属种类命名，一共包含 49 个种类的 API，例如（Email，Sport），每个 API 包含一个或多个 Endpoint。Basic 文件中保存了描述 API 的基本信息，例如 API 名称，API 链接，流行度，服务水平等。Detail 文件中保存了该种类 API 对应的 Endpoint 信息，如 Endpoint 名称，可选参数，必选参数等。

![屏幕截图 2023-11-08 213652](./RESTful-API-Crawler/Static/index.png)

## 2-软件包说明

 **表格中包含了该程序所使用的软件包名称、版本号(requirements.txt)。**

| 软件包   | 版本号 |
| :------- | ------ |
| pandas   | 2.0.3  |
| selenium | 4.14.0 |

## 3-代码使用说明

### 项目结构

### ![image-20231113200858258](C:\Users\李文\AppData\Roaming\Typora\typora-user-images\image-20231113200858258.png)



### 核心代码

`Basic_API_Info.py`是爬取基本信息的 Python 文件。

`Detail.py`是爬取各 API 中具体信息的 Python 文件。

### 结果保存

Basic 文件夹中保存 API 基本信息，例如 API 名称，API 连接，流行度，服务水平等。

Detail 文件夹中保存 API 中各个 Endpoint 具体信息，Endpoint 名称，可选参数，必选参数等。

## 4-数据集字段说明

**Basic 文件字段说明**

| 字段名            | 说明                          | 示例                                                         |
| ----------------- | ----------------------------- | ------------------------------------------------------------ |
| API 名称          | API 名称                      | NetDetective                                                 |
| API 链接          | API 网络地址                  | https://rapidapi.com/tomwimmenhove/api/netdetective/         |
| Update_Time       | API 更新时间                  | 9 months ago                                                 |
| Author            | API 作者                      | Eduard Kleiner                                               |
| API描述           | 对API功能和使用范围的基本描述 | Optimize your website effortlessly with SEOOptimizeAPI - the powerful tool that provides valuable insights and automates repetitive tasks. With SEOOptimizeAPI, you can take the guesswork out of website optimization. The API utilizes advanced algorithms and technologies to provide in-depth insights into your website's performance and help you identify areas for improvement. And with its easy-to-use API endpoints, you can automate repetitive tasks and save time and effort. |
| API Popularity    | API 受欢迎度                  | 9.5                                                          |
| API Latency       | API 使用延迟                  | 1,399 ms                                                     |
| API Service Level | API 服务水平                  | 100%                                                         |

**Detail 文件字段说明**

| 字段名            | 说明                               | 示例                                                         |
| ----------------- | ---------------------------------- | ------------------------------------------------------------ |
| API 名称          | API 名称                           | SEO Automations                                              |
| API 链接          | API 网络地址                       | https://rapidapi.com/BigFoxMedia/api/seo-automations/        |
| API_Host          | API 名称与rapidapi.com的拼接字符串 | seo-automations.p.rapidapi.com                               |
| Endpoint 名称     | Endpoint 名称                      | GET:Extract Sitemap XML as JSON                              |
| Endpoint 描述     | Endpoint 的功能描述                | Are you looking for an API that can quickly and easily download and parse sitemap.xml files into JSON format? Look no further! Our API allows you to make a simple GET request, passing in the URL of a sitemap.xml file as a parameter. The API will handle the rest, downloading th... |
| Endpoint 种类     | Endpoint 所属类别                  | Tier 2 APIs ( Fast )                                         |
| Endpoint 必须参数 | Endpoint 使用时的必选参数          | [{'参数名': ['your-api-key', 'shortcode'], '参数类型': ['STRING', 'STRING'], '参数注意事项': ['Your APIKey provided by Workable', 'Retrieve detailed job information, including the job description. The shortcode is a unique identifier for each jobs and can be seen by invoking "/jobs"']}] |
| Endpoint 可选参数 | Endpoint 使用时的可选参数          | [{'参数名': ['address', 'lng', 'lat', 'note'], '参数类型': ['STRING', 'STRING', 'STRING', 'STRING'], '参数注意事项': ['An optional human readable address string where the QR Code will be attached', 'An optional longitude of where the QR Code will be attached', 'An optional latitude of where the QR Code will be attached', 'An optional note']}] |



## 5-API调用及组合示例

