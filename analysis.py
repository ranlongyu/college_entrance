import json, csv

if __name__ == '__main__':
    with open("schools.json", 'r') as file_object:
        schools_dict = json.load(file_object)

    all_lines = []
    for key, school in schools_dict.items():
        one_line = []
        one_line.append(key)  # 学校
        one_line.append(school["region"])  # 地区
        for i in range(5):  # 遍历5年的分数线
            name = str(2014 + i) + "score"
            if school.get(name):
                d = school.get(name)
                one_line.append(d["max"] if d["max"] != "--" else "")
                one_line.append(d["min"] if d["min"] != "--" else "")
                one_line.append(d["average"] if d["average"] != "--" else "")
            else:
                one_line.append("")
                one_line.append("")
                one_line.append("")
        all_lines.append(one_line)

    # 注意newline
    with open("score.csv", "w", encoding='utf8', newline="") as datacsv:
        # dialect为打开csv文件的方式，默认是excel，delimiter="\t"参数指写入的时候的分隔符
        csvwriter = csv.writer(datacsv, dialect=("excel"))
        for line in all_lines:
            csvwriter.writerow(line)
