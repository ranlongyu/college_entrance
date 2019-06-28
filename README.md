# 重庆高考录取分数爬取

- get_data.py 里面包含了主要的爬虫代码

先爬取211大学名单，再根据这份名单爬取每所大学的分数线，存到schools.json里。

分数线链接分析：

https://static-data.eol.cn/www/2.0/schoolprovinceindex/2017/119/50/2/1.json
2017：年份
119：重庆大学
50：重庆
1：理科，2：文科
1：第一页

- analysis.py 对爬取的分数线进行分析存储到 score.csv 中