# -*- coding: utf-8 -*-
import requests, re, json
from bs4 import BeautifulSoup


# 获取211学校，返回字典
def get_211():
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0',
        'Host': 'www.eol.cn'
    }
    url = 'http://www.eol.cn/html/g/gxmd/211.shtml'
    response = requests.get(url=url, headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')

    regions = []  # 存储地区
    for item in soup.find_all(name="div", class_="zf_main tong_lm"):
        r = re.search('> ([\u4E00-\u9FA5]+).+?([0-9]+)所', item.h1.text)
        regions.extend([r.group(1)] * int(r.group(2)))

    schools = {}
    for item in soup.find_all(name="div", attrs={'class': "zk_ad_475 left"}):
        for school in item.find_all(name="td", align="center", bgcolor="#FFFFFF"):
            try:
                school_link = school.find(name="a").get('href')
                school_num = re.search('school(\d+)\.htm', school_link).group(1)
                school_name = school.a.span.text
                schools[school_name] = {"id": int(school_num)}
            except:
                continue
        item = item.find_next_sibling()
        for school in item.find_all(name="td", align="center", bgcolor="#FFFFFF"):
            try:
                school_link = school.find(name="a").get('href')
                school_num = re.search('school(\d+)\.htm', school_link).group(1)
                school_name = school.a.span.text
                schools[school_name] = {"id": int(school_num)}
            except:
                continue

    for region, school in zip(regions, schools):
        schools[school]["region"] = region

    return schools


# 根据学校代码，查询分数线，返回字典
def get_score(id):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0',
        'Host': "static-data.eol.cn"
    }
    url_begin = 'https://static-data.eol.cn/www/2.0/schoolprovinceindex/'
    school_id = "/" + str(id)
    url_end = '/50/1/1.json'  # 重庆/理科/第一页
    school_dict = {}
    for i in range(5):  # 2014-2018年
        url = url_begin + str(2014 + i) + school_id + url_end
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            school = {}
            response_dict = json.loads(response.text)
            school["max"] = response_dict["data"]["item"][0]["max"]
            school["min"] = response_dict["data"]["item"][0]["min"]
            school["average"] = response_dict["data"]["item"][0]["average"]
            school["local_batch_name"] = response_dict["data"]["item"][0]["local_batch_name"]
            school_dict[str(2014 + i) + "score"] = school
    return school_dict


if __name__ == '__main__':
    schools = get_211()
    for i, (key, value) in enumerate(schools.items()):
        school = get_score(value["id"])
        schools[key].update(school)
    print(schools)
    with open("schools.json", "w", encoding="utf-8") as file_object:
        json.dump(schools, file_object, ensure_ascii=False)
        print("写入文件完成...")
