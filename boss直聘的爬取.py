from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from pyecharts.render.engine import render_notebook
from pyecharts.charts import Bar
from pyecharts.charts import Scatter
from pyecharts import options as opts
import time
import random
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import re
import json

# 获取城市编号
with open(r'C:\Users\ikun\Desktop\1.txt', 'r', encoding='utf-8') as file:
    # 解析JSON字符串为Python字典
    json_content = file.read()
    data = json.loads(json_content)
data = data['zpData']["siteGroup"]
city_code_map = {}

for item in data:
    # 取出cityList
    city_list = item['cityList']

    # 遍历cityList中的每个城市
    for city in city_list:
        # 取出code和name
        code = city['code']
        name = city['name']

        # 打印code和name，或者做其他处理
        print(f"Code: {code}, Name: {name}")
        city_code_map[name] = code

for name, code in city_code_map.items():
    print(f"Name: {name}, Code: {code}")

#保存
with open('city_code_map.json', 'w', encoding='utf-8') as file:
    json.dump(city_code_map, file, ensure_ascii=False, indent=4)

#获得boss直聘公司信息
List1 = list()
List2 = list()
List3 = list()
ZheJiang = ["湖州", "台州", "杭州", "嘉兴",'宁波','舟山','衢州','金华','丽水','温州','绍兴']  # 这里列出你想要取的键
Place= {zj:city_code_map[zj] for zj in ZheJiang if zj in city_code_map}  # 使用列表推导式取值

print(Place)
for place,number in Place.items():
    for i in range(1, 9):
        # 创建浏览器驱动
        # 设置Edge驱动路径
        service = EdgeService(executable_path='C:/Program Files (x86)/Microsoft/Edge/Application/msedgedriver.exe')

        # 设置浏览器选项
        options = webdriver.EdgeOptions()
        options.add_argument("disable-blink-features=AutomationControlled")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0")

        # 创建浏览器对象
        driver = webdriver.Edge(service=service, options=options)



        window_width = random.randint(800, 1200)
        window_height = random.randint(600, 1000)
        driver.set_window_size(window_width, window_height)

        # 打开网页
        driver.get("https://www.zhipin.com/gongsi/_zzz_c{}/?page={}&ka=page-{}".format(number , i, i))

        # 等待动态内容加载完成
        wait = WebDriverWait(driver, 10)
        dynamic_content = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@id='wrap']")))
        # 模拟滚动和随机延迟
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(2, 5))
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(random.uniform(2, 5))

        # 随机移动鼠标
        action = ActionChains(driver)
        action.move_by_offset(random.randint(0, 500), random.randint(0, 500)).perform()
        time.sleep(random.uniform(1, 3))
        # 获取整个 HTML 文档
        html_content = driver.page_source

        # 获取 ::before 后面的内容
        before_content = html_content.split("::before")[-1]


        #beautifulsoup解析
        Soup = BeautifulSoup(before_content)
        scop = Soup.find('div', class_="company-tab-box company-list")
        GONGSI = scop.find_all('h4')
        zhiwei = scop.find_all('p')
        shuxing = scop.find_all('span')
        print(GONGSI)
        print('-' * 60)
        print(zhiwei)
        List1.append(GONGSI)
        List2.append(zhiwei)
        List3.append(shuxing)
    # 关闭浏览器
    driver.quit()

    #爬取的结果是一个由beautifulsoup组成的列表，为了继续提取信息转为txt并保存
    # 读取爬取的列表内容并移入output.txt
    with open('output.txt', 'w', encoding='utf-8') as file:
        for item in range(len(List2)):
            file.write(str(List2[item]))

    #初步获取职位信息(List1)
    with open('output.txt','r',encoding='utf-8') as file:
        file1=BeautifulSoup(file,'html.parser')
        zhiwei=file1.find_all('u',class_="h")


    #初步获取薪资信息(List1)

    import re
        #定义re的匹配模式
    pattern = r'(\d+-\d+K)'
        #定义一个获取薪资的函数
    def get_money(filename):
        #初始化
        salaries=[]
        with open(filename, 'r',encoding='utf-8') as file:
        #逐行读取文本
            for line in file:
                #re匹配
                matches = re.findall(pattern, line)
                #加入列表
                salaries.extend(matches)
            return salaries
    filename = "output.txt"
    moneys = get_money(filename)


        #初始化
    position2 = []
    Salary2 = []
    result2 = []
    kind2 = []
    # 对职位信息进一步提取
    for zhi in range(len(zhiwei)):
        position1 = zhiwei[zhi].text
        position2.append(position1)
    # 对薪资进一步提取
    for money in range(len(moneys)):
        Salary1 = moneys[money]
        Salary2.append(Salary1)
    #对公司进一步提取（List2）
    for i in range(len(List1)):
        a = str(List1[i])
        pattern = "<h4>(.*?)</h4>"
        result1 = re.findall(pattern, a)
        result2.append(result1)

    for i in range(len(List3)):
        b = str(List3[i])
        patterns = "<span>(.*?)</span>"
        kind1 = re.findall(patterns, b)
        kind2.append(kind1)

    for sublist in kind2:
        if '...' in sublist:
            sublist.remove('...')

    all_rows = []  # 创建一个空列表来收集所有的字典

    for sublist in kind2:
        # 使用列表推导式来创建包含每对公司属性的字典列表，同时确保不会超出索引范围
        rows = [{'属性1': sublist[i], '属性2': sublist[i + 1]} for i in range(0, len(sublist) - 1, 2) if
                i + 1 < len(sublist)]

        # 将这个子列表的字典列表添加到总列表中
        all_rows.extend(rows)

        # 使用收集到的所有字典列表创建最终的DataFrame
    kind = pd.DataFrame(all_rows)

    #创建公司列
    gongsi=pd.DataFrame(result2)
    conpany = gongsi.stack()
    conpany = conpany.reset_index(drop=True)
    conpany=pd.Series(conpany,name='conpany')
    #创建职位列
    position=pd.Series(position2,name='position')
    #创建薪资列
    Salary=pd.Series(Salary2,name='Salary')
    #组合成表格存入CSV
    df = pd.concat([conpany,position,Salary],axis=1)#.to_csv('boss直聘.csv')


    # 处理空值
    Salary = Salary.fillna('0 0')

    #创建函数用于读取数字
    def get_averageSalary(salary):
        # 匹配数字
        numbers = re.findall(r'\d+', salary)
        #如果没有两个数字就返回None
        if len(numbers) != 2:
            return None
        # 将字符串转换为整数
        num1, num2 = int(numbers[0]), int(numbers[1])
        # 计算均值
        return (num1 + num2) / 2


    mid_Salary = []
    #遍历薪资列取出数字并且计算均值
    for q in range(0, len(Salary)):

        avrage_salary = get_averageSalary(Salary[q])
        if avrage_salary is not None:  # 确保计算得到的平均薪资不是 None
            mid_Salary.append(avrage_salary)
    mid_Salary = pd.Series(mid_Salary, name='avg_salary')

    #整合进最后的Dataframe
    boss = pd.concat([conpany,position,Salary,mid_Salary],axis=1)#.to_csv('data//{}.csv'.format(place))


    max_len = max(len(boss), len(kind))
    boss = pd.concat([boss, pd.DataFrame(index=range(max_len - len(boss)))]).reset_index(drop=True)
    kind = pd.concat([kind, pd.DataFrame(index=range(max_len - len(kind)))]).reset_index(drop=True)
    # 现在 df_boss 和 df_kind 有相同的行数，可以直接使用 concat 结合
    df_combined= pd.concat([boss, kind], axis=1)
    print(df_combined)
    df_combined.to_csv('data//{}.csv'.format(place))


    #data = data.drop(columns=data.columns[0])
    #print(data.columns)
    #data = data.dropna()
    #def extract_salary_range(salary_str):
    #    min_max = salary_str.split('-')
    #    min_salary = int(min_max[0].replace('K', '') or min_max[0]) * (1000 if 'K' in min_max[0] else 1)
    #    max_salary = int(min_max[1].replace('K', '') or min_max[1]) * (1000 if 'K' in min_max[1] else 1)
    #    return pd.Series({'最小值': min_salary, '最大值': max_salary})
    #data = data.join(data['Salary'].apply(extract_salary_range))
    #data['最大值'] = data['最大值'] / 1000
    #data['最大值'] = data['最大值'].round().astype(int)
    #data = data.drop(columns=['position', 'Salary'])
    #cities = pd.Series(['------'] * len(data))
    #data.insert(0, '城市', cities)
    #data=data.to_csv('data//{}.csv'.format(place))

import pandas as pd
import os
# 假设你的CSV文件都存放在一个名为'data_folder'的文件夹中
data_folder = 'data'
# 创建一个空列表来存放带有地区名的数据框
all_name = []
# 遍历文件夹中的所有CSV文件
for filename in os.listdir(data_folder):
    # 读取CSV文件到数据框中
    df = pd.read_csv(os.path.join(data_folder, filename))
    # 提取地区名（这里假设文件名包含了地区名，例如'Beijing.csv'）
    region_name = filename.split('.')[0]
    # 为数据框增加一列地区名
    df['region'] = region_name
    # 将带有地区名的数据框添加到列表中
    all_name.append(df)
    # 使用pd.concat从上到下合并所有的数据框
combined_df = pd.concat(all_name, ignore_index=True)
# 保存合并后的数据框到CSV文件
combined_df.to_csv(r'data//combined_data.csv', index=False)

data = pd.read_csv(r'C:\Users\ikun\PycharmProjects\pythonProject\爬虫\data\combined_data.csv', encoding='GBK')
data = data.dropna()


def extract_salary_range(salary_str):
    min_max = str(salary_str).split('-')
    min_salary = int(min_max[0].replace('K', '') or min_max[0]) * (1000 if 'K' in min_max[0] else 1)
    max_salary = int(min_max[1].replace('K', '') or min_max[1]) * (1000 if 'K' in min_max[1] else 1)
    return pd.Series({'最小值': min_salary, '最大值': max_salary})


data = data.join(data['Salary'].apply(extract_salary_range))
data['最大值'] = data['最大值'] / 1000
data['最大值'] = data['最大值'].round().astype(int)
data_last = data.drop(columns=['position', 'Salary']).to_csv(
    r'C:\Users\ikun\PycharmProjects\pythonProject\爬虫\data\lastdata')
#可视化
#y_axis = boss.avg_salary
#x_axis = boss.position
#bar = Bar()
#bar.add_xaxis(list(x_axis))
#bar.add_yaxis("薪资", list(y_axis))
## 设置全局配置项（如标题）
#bar.set_global_opts(title_opts=opts.TitleOpts(title="薪资区间分布柱状图"))
## 在 Jupyter Notebook 中渲染图表
#bar.render_notebook()  # 在Jupyter Notebook中渲染图表
#bar.render('output.html')