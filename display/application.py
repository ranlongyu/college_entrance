import tkinter
from tkinter import ttk  # 导入内部包
import json

def main_window():
    window = tkinter.Tk()
    window.title('211高校列表')
    window.geometry('400x400')

    with open("schools.json", 'r') as file_object:
        schools = json.load(file_object)
    schools_name = []
    for key, school in schools.items():
        schools_name.append(key)

    var1 = tkinter.StringVar()
    var1.set(schools_name)  # 为变量设置值
    # 创建Listbox
    lb = tkinter.Listbox(window, listvariable=var1, height=20)  # 将var1的值赋给Listbox
    lb.pack()

    def print_score():
        value = lb.get(lb.curselection())  # 获取当前选中的文本
        all_score = schools[value]['all_score_list']
        display(all_score, value)

    b1 = tkinter.Button(window, text='点击查看分数', width=15,
                   height=2, command=print_score)
    b1.pack()

    # 显示主窗口
    window.mainloop()

def display(score_list, value):
    win = tkinter.Tk()
    win.title(value)
    win.geometry('400x300')

    tree = ttk.Treeview(win, show='headings')  # 表格
    tree["columns"] = ("年份", "最高", "平均", "最低")  # 设置表有三列
    tree.column("年份", width=100, anchor='center')  # 对三列分别设置参数
    tree.column("最高", width=100, anchor='center')
    tree.column("平均", width=100, anchor='center')
    tree.column("最低", width=100, anchor='center')

    tree.heading("年份", text="年份")  # 显示表头
    tree.heading("最高", text="最高")  # 显示表头
    tree.heading("平均", text="平均")
    tree.heading("最低", text="最低")

    for list in score_list:
        tree.insert("", 'end', values=list)  # 插入数据

    tree.pack()

    win.mainloop()

main_window()