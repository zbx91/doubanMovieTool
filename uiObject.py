
import tkinter
from tkinter import *
from tkinter import ttk
from getMovieInRankingList import *
import threading

class uiObject:

    def xxxx(self, event):
        if(hasattr(self, 'jsonData')):
            print(self.jsonData)
        else:
            print('no')



    def thread_it(self, func, *args):
        '''
        将函数打包进线程
        '''
        # 创建
        t = threading.Thread(target=func, args=args)
        # 守护
        t.setDaemon(True)
        # 启动
        t.start()

    def center_window(self, root, w, h):
        """
        窗口居于屏幕中央
        :param root: root
        :param w: 窗口宽度
        :param h: 窗口高度
        :return:
        """
        # 获取屏幕 宽、高
        ws = root.winfo_screenwidth()
        hs = root.winfo_screenheight()

        # 计算 x, y 位置
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)

        root.geometry('%dx%d+%d+%d' % (w, h, x, y))



    def clearTree(self, tree):
        '''
        清空表格
        '''
        x = tree.get_children()
        for item in x:
            tree.delete(item)

    def addTree(self, tree,list):
        '''
        新增数据到表格
        '''
        i = 0
        for subList in list:
            tree.insert('', 'end', values=subList)
            i = i + 1
        tree.grid()


    def searhMovieInRating(self, tree, B_0, typeName, count, rating, vote):
        """
        从排行榜中搜索符合条件的影片信息
        :param root: root
        :param w: 窗口宽度
        :param h: 窗口高度
        :return:
        """

        # 按钮设置为灰色状态
        B_0['state'] = tkinter.DISABLED
        B_0['text'] = '正在查询'
        self.jsonData = ""



        jsonMovieData = json.loads(movieData)
        for subMovieData in jsonMovieData:
            if(subMovieData['title'] == typeName):
                self.clearTree(tree)  # 清空表格
                movieObject = getMovieInRankingList(subMovieData['type'], count, rating, vote); #创建对象
                list,jsonData = movieObject.getUrlDataInRankingList()  # 返回符合条件的电影信息
                self.jsonData = jsonData
                self.addTree(tree, list) # 将数据添加到tree中
                break

        # 按钮设置为正常状态
        B_0['state'] = tkinter.NORMAL
        B_0['text'] = '查询影片'




    def ui_process(self):
        """
        Ui主程序
        :param
        :return:
        """
        root = Tk()

        # 设置窗口位置
        root.title("豆瓣")
        self.center_window(root, 650, 250)

        # 电影类型
        L_typeId = Label(root, text='电影类型')
        L_typeId.place(x=0, y=10)

        #下拉列表框
        comvalue = StringVar()
        C_type = ttk.Combobox(root, width=5, textvariable=comvalue, state='readonly')
        # 将影片类型输入到下拉列表框中
        jsonMovieData = json.loads(movieData) #json数据
        movieList = []
        for subMovieData in jsonMovieData: #对每一种类的电影题材进行操作
            movieList.append(subMovieData['title'])
        C_type["values"] = movieList #初始化
        C_type.current(0)  # 选择第一个
        C_type.place(x=65, y=10)


        # 欲获取的电影数量
        L_count = Label(root, text='获取数量=')
        L_count.place(x=150, y=10)

        # 文本框
        T_count = Entry(root, width=5)
        T_count.delete(0, END)
        T_count.insert(0, '500')
        T_count.place(x=220, y=10)


        # 评分
        L_rating = Label(root, text='影片评分>')
        L_rating.place(x=280, y=10)

        # 文本框
        T_rating = Entry(root, width=5)
        T_rating.delete(0, END)
        T_rating.insert(0, '8.5')
        T_rating.place(x=350, y=10)

        # 评价人数
        L_vote = Label(root, text='评价人数>')
        L_vote.place(x=410, y=10)

        # 文本框
        T_vote = Entry(root, width=7)
        T_vote.delete(0, END)
        T_vote.insert(0, '200000')
        T_vote.place(x=480, y=10)



        # 查询按钮
        #lambda表示绑定的函数需要带参数，请勿删除lambda，否则会出现异常
        #thread_it表示新开启一个线程执行这个函数，防止GUI界面假死无响应
        B_0 = Button(root, text="查询影片")
        B_0.place(x=580, y=10)



        # 框架布局，承载多个控件
        frame_root = Frame(root, width=400)
        frame_l = Frame(frame_root)
        frame_r = Frame(frame_root)

        # 表格
        columns = ("影片名字", "影片评分", "同类排名", "评价人数")
        treeview = ttk.Treeview(frame_l, height=10, show="headings", columns=columns)

        treeview.column("影片名字", width=210, anchor='center')  # 表示列,不显示
        treeview.column("影片评分", width=210, anchor='center')
        treeview.column("同类排名", width=100, anchor='center')
        treeview.column("评价人数", width=100, anchor='center')

        treeview.heading("影片名字", text="影片名字")  # 显示表头
        treeview.heading("影片评分", text="影片评分")
        treeview.heading("同类排名", text="同类排名")
        treeview.heading("评价人数", text="评价人数")

        treeview.bind('<Button-1>', self.xxxx) #绑定鼠标左键事件

        #垂直滚动条
        vbar = ttk.Scrollbar(frame_r, command=treeview.yview)
        treeview.configure(yscrollcommand=vbar.set)

        treeview.pack()
        vbar.pack(side=RIGHT, fill=Y)

        # 框架的位置布局
        frame_l.grid(row=0, column=0, sticky=NSEW)
        frame_r.grid(row=0, column=1, sticky=NS)
        frame_root.place(x=5, y=40)

        B_0.configure(command=lambda : self.thread_it(self.searhMovieInRating, treeview, B_0, C_type.get(), T_count.get(), T_rating.get(), T_vote.get()))


        mainloop()