
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import font
from getMovieInRankingList import *
from PIL import Image, ImageTk
import threading
import os
import ssl
ssl._create_default_https_context = ssl._create_unverified_context #关闭SSL证书验证





def thread_it(func, *args):
    '''
    将函数打包进线程
    '''
    # 创建
    t = threading.Thread(target=func, args=args)
    # 守护
    t.setDaemon(True)
    # 启动
    t.start()


def handlerAdaptor(fun, **kwds):
    '''事件处理函数的适配器，相当于中介，那个event是从那里来的呢，我也纳闷，这也许就是python的伟大之处吧'''
    return lambda event, fun=fun, kwds=kwds: fun(event, **kwds)



def save_img(img_url, file_name, file_path):
    """
    下载指定url的图片，并保存运行目录下的img文件夹
    :param img_url: 图片地址
    :param file_name: 图片名字
    :param file_path: 存储目录
    :return:
    """
    #保存图片到磁盘文件夹 file_path中，默认为当前脚本运行目录下的img文件夹
    try:
        #判断文件夹是否已经存在
        if not os.path.exists(file_path):
            print('文件夹',file_path,'不存在，重新建立')
            os.makedirs(file_path)
        #获得图片后缀
        file_suffix = os.path.splitext(img_url)[1]
        #拼接图片名（包含路径）
        filename = '{}{}{}{}'.format(file_path,os.sep,file_name,file_suffix)

        #判断文件是否已经存在
        if not os.path.exists(filename):
            print('文件', filename, '不存在，重新建立')
            # 下载图片，并保存到文件夹中
            urllib.request.urlretrieve(img_url, filename=filename)
        return filename

    except IOError as e:
        print('下载图片操作失败',e)
    except Exception as e:
        print('错误:',e)



def resize(w_box, h_box, pil_image):
    """
    等比例缩放图片,并且限制在指定方框内
    :param w_box,h_box: 指定方框的宽度和高度
    :param pil_image: 原始图片
    :return:
    """

    f1 = 1.0 * w_box / pil_image.size[0]  # 1.0 forces float division in Python2
    f2 = 1.0 * h_box / pil_image.size[1]
    factor = min([f1, f2])
    # print(f1, f2, factor) # test
    # use best down-sizing filter
    width = int(pil_image.size[0] * factor)
    height = int(pil_image.size[1] * factor)
    return pil_image.resize((width, height), Image.ANTIALIAS)



class uiObject:

    def __init__(self):
        self.jsonData = ""
        self.jsonData_keyword = ""


    def show_GUI_movie_detail(self):
        '''
        显示 影片详情 界面GUI
        '''
        self.label_img['state'] = tkinter.NORMAL
        self.label_movie_name['state'] = tkinter.NORMAL
        self.label_movie_rating['state'] = tkinter.NORMAL
        self.label_movie_time['state'] = tkinter.NORMAL
        self.label_movie_type['state'] = tkinter.NORMAL
        self.label_movie_actor['state'] = tkinter.NORMAL


    def hidden_GUI_movie_detail(self):
        '''
        显示 影片详情 界面GUI
        '''
        self.label_img['state'] = tkinter.DISABLED
        self.label_movie_name['state'] = tkinter.DISABLED
        self.label_movie_rating['state'] = tkinter.DISABLED
        self.label_movie_time['state'] = tkinter.DISABLED
        self.label_movie_type['state'] = tkinter.DISABLED
        self.label_movie_actor['state'] = tkinter.DISABLED



    def show_movie_data_in_rating(self, event):
        '''
        显示某个被选择的电影的详情信息
        '''

        # self.hidden_GUI_movie_detail()
        item = self.treeview.selection()
        if(item):
            item_text = self.treeview.item(item, "values")
            movieName = item_text[0] # 输出电影名
            for movie in self.jsonData:
                if(movie['title'] == movieName):
                    img_url = movie['cover_url']
                    movie_name = movie['title']
                    file_name = save_img(img_url, movie_name, 'img') #下载网络图片
                    self.show_movie_img(file_name)
                    self.label_movie_name.config(text=movie['title'])
                    string_actors = "、".join(movie['actors'])
                    self.label_movie_actor.config(text=string_actors)
                    self.label_movie_rating.config(text=str(movie['rating'][0]) + '分 ' + str(movie['vote_count']) + '人评价')
                    self.label_movie_time.config(text=movie['release_date'])
                    self.label_movie_type.config(text=movie['types'])
                    break

        # self.show_GUI_movie_detail()





    def show_movie_data_in_keyword(self, event):
        '''
        显示某个被选择的电影的详情信息
        '''

        # self.hidden_GUI_movie_detail()
        item = self.treeview_keyword.selection()
        if(item):
            item_text = self.treeview_keyword.item(item, "values")
            movieName = item_text[0] # 输出电影名
            for movie in self.jsonData_keyword:
                if(movie['title'] == movieName):
                    img_url = movie['cover_url']
                    movie_name = movie['title']
                    file_name = save_img(img_url, movie_name, 'img') #下载网络图片
                    self.show_movie_img(file_name)
                    self.label_movie_name.config(text=movie['title'])
                    string_actors = "、".join(movie['actors'])
                    self.label_movie_actor.config(text=string_actors)
                    self.label_movie_rating.config(text=str(movie['rating'][0]) + '分 ' + str(movie['vote_count']) + '人评价')
                    self.label_movie_time.config(text=movie['release_date'])
                    self.label_movie_type.config(text=movie['types'])
                    break

        # self.show_GUI_movie_detail()





    def show_movie_img(self, file_name):
        '''
        更新图片GUI
        :param file_name: 图片路径
        :return:
        '''
        img_open = Image.open(file_name) #读取本地图片
        pil_image_resized = resize(160, 250, img_open) #等比例缩放本地图片
        img = ImageTk.PhotoImage(pil_image_resized) #读入图片
        self.label_img.config(image=img, width = pil_image_resized.size[0], height = pil_image_resized.size[1])
        self.label_img.image = img


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



    def clear_tree(self, tree):
        '''
        清空表格
        '''
        x = tree.get_children()
        for item in x:
            tree.delete(item)

    def add_tree(self,list, tree):
        '''
        新增数据到表格
        '''
        i = 0
        for subList in list:
            tree.insert('', 'end', values=subList)
            i = i + 1
        tree.grid()


    def searh_movie_in_rating(self):
        """
        从排行榜中搜索符合条件的影片信息
        """

        # 按钮设置为灰色状态
        self.clear_tree(self.treeview)  # 清空表格
        self.B_0['state'] = tkinter.DISABLED
        self.C_type['state'] = tkinter.DISABLED
        self.T_count['state'] = tkinter.DISABLED
        self.T_rating['state'] = tkinter.DISABLED
        self.T_vote['state'] = tkinter.DISABLED
        self.B_0['text'] = '正在查询'
        self.jsonData = ""


        jsonMovieData = json.loads(movieData)
        for subMovieData in jsonMovieData:
            if(subMovieData['title'] == self.C_type.get()):

                movieObject = getMovieInRankingList() #创建对象
                list,jsonData = movieObject.get_url_data_in_ranking_list(subMovieData['type'], self.T_count.get(), self.T_rating.get(), self.T_vote.get())  # 返回符合条件的电影信息
                self.jsonData = jsonData
                self.add_tree(list, self.treeview) # 将数据添加到tree中
                break

        # 按钮设置为正常状态
        self.B_0['state'] = tkinter.NORMAL
        self.C_type['state'] = 'readonly'
        self.T_count['state'] = tkinter.NORMAL
        self.T_rating['state'] = tkinter.NORMAL
        self.T_vote['state'] = tkinter.NORMAL
        self.B_0['text'] = '查询影片'




    def searh_movie_in_keyword(self):
        """
        从关键字中搜索符合条件的影片信息
        """
        # 按钮设置为灰色状态
        self.clear_tree(self.treeview_keyword)  # 清空表格
        self.B_0_keyword['state'] = tkinter.DISABLED
        self.T_vote_keyword['state'] = tkinter.DISABLED
        self.B_0_keyword['text'] = '正在查询'
        self.jsonData_keyword = ""




        movieObject = getMovieInRankingList(); #创建对象
        list,jsonData_keyword = movieObject.get_url_data_in_keyWord(self.T_vote_keyword.get())
        self.jsonData_keyword = jsonData_keyword
        self.add_tree(list, self.treeview_keyword) # 将数据添加到tree中



        # 按钮设置为正常状态
        self.B_0_keyword['state'] = tkinter.NORMAL
        self.T_vote_keyword['state'] = tkinter.NORMAL
        self.B_0_keyword['text'] = '查询影片'


    def ui_process(self):
        """
        Ui主程序
        :param
        :return:
        """
        root = Tk()
        self.root = root
        # 设置窗口位置
        root.title("豆瓣")
        self.center_window(root, 1000, 560)
        root.resizable(0, 0)  # 框体大小可调性，分别表示x,y方向的可变性


        # 从排行榜 电影搜索布局开始
        # 容器控件
        labelframe = LabelFrame(root, width=660, height=270, text="从排行榜搜索电影")
        labelframe.place(x=5, y=5)
        self.labelframe = labelframe

        # 电影类型
        L_typeId = Label(labelframe, text='电影类型')
        L_typeId.place(x=0, y=10)
        self.L_typeId = L_typeId

        #下拉列表框
        comvalue = StringVar()
        C_type = ttk.Combobox(labelframe, width=5, textvariable=comvalue, state='readonly')
        # 将影片类型输入到下拉列表框中
        jsonMovieData = json.loads(movieData) #json数据
        movieList = []
        for subMovieData in jsonMovieData: #对每一种类的电影题材进行操作
            movieList.append(subMovieData['title'])
        C_type["values"] = movieList #初始化
        C_type.current(0)  # 选择第一个
        C_type.place(x=65, y=8)
        self.C_type = C_type


        # 欲获取的电影数量
        L_count = Label(labelframe, text='获取数量=')
        L_count.place(x=150, y=10)
        self.L_count = L_count

        # 文本框
        T_count = Entry(labelframe, width=5)
        T_count.delete(0, END)
        T_count.insert(0, '500')
        T_count.place(x=220, y=7)
        self.T_count = T_count


        # 评分
        L_rating = Label(labelframe, text='影片评分>')
        L_rating.place(x=280, y=10)
        self.L_rating = L_rating

        # 文本框
        T_rating = Entry(labelframe, width=5)
        T_rating.delete(0, END)
        T_rating.insert(0, '8.5')
        T_rating.place(x=350, y=7)
        self.T_rating = T_rating

        # 评价人数
        L_vote = Label(labelframe, text='评价人数>')
        L_vote.place(x=410, y=10)
        self.L_vote = L_vote

        # 文本框
        T_vote = Entry(labelframe, width=7)
        T_vote.delete(0, END)
        T_vote.insert(0, '200000')
        T_vote.place(x=480, y=7)
        self.T_vote = T_vote



        # 查询按钮
        #lambda表示绑定的函数需要带参数，请勿删除lambda，否则会出现异常
        #thread_it表示新开启一个线程执行这个函数，防止GUI界面假死无响应
        B_0 = Button(labelframe, text="查询影片")
        B_0.place(x=580, y=10)
        self.B_0 = B_0



        # 框架布局，承载多个控件
        frame_root = Frame(labelframe, width=400)
        frame_l = Frame(frame_root)
        frame_r = Frame(frame_root)
        self.frame_root = frame_root
        self.frame_l = frame_l
        self.frame_r = frame_r


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



        #垂直滚动条
        vbar = ttk.Scrollbar(frame_r, command=treeview.yview)
        treeview.configure(yscrollcommand=vbar.set)

        treeview.pack()
        self.treeview = treeview
        vbar.pack(side=RIGHT, fill=Y)
        self.vbar = vbar

        # 框架的位置布局
        frame_l.grid(row=0, column=0, sticky=NSEW)
        frame_r.grid(row=0, column=1, sticky=NS)
        frame_root.place(x=5, y=40)
        # 从排行榜 电影搜索布局结束










        # 输入关键字 电影搜索布局开始
        # 容器控件
        labelframe_keyword = LabelFrame(root, width=660, height=270, text="从关键字搜索电影")
        labelframe_keyword.place(x=5, y=280)
        self.labelframe_keyword = labelframe_keyword


        # 评价人数
        L_vote_keyword = Label(labelframe_keyword, text='请输入影片名称')
        L_vote_keyword.place(x=0, y=10)
        #L_vote_keyword.grid(row=0,column=0)
        self.L_vote_keyword = L_vote_keyword

        # 文本框
        T_vote_keyword = Entry(labelframe_keyword, width=50)
        T_vote_keyword.delete(0, END)
        T_vote_keyword.insert(0, '我不是药神')
        T_vote_keyword.place(x=100, y=7)
        self.T_vote_keyword = T_vote_keyword


        # 查询按钮
        #lambda表示绑定的函数需要带参数，请勿删除lambda，否则会出现异常
        #thread_it表示新开启一个线程执行这个函数，防止GUI界面假死无响应
        B_0_keyword = Button(labelframe_keyword, text="查询影片")
        B_0_keyword.place(x=580, y=10)
        self.B_0_keyword = B_0_keyword


        # 框架布局，承载多个控件
        frame_root_keyword = Frame(labelframe_keyword, width=400)
        frame_l_keyword = Frame(frame_root_keyword)
        frame_r_keyword = Frame(frame_root_keyword)
        self.frame_root_keyword = frame_root_keyword
        self.frame_l_keyword = frame_l_keyword
        self.frame_r_keyword = frame_r_keyword


        # 表格
        columns_keyword = ("影片名字", "影片评分", "影片类型", "评价人数")
        treeview_keyword = ttk.Treeview(frame_l_keyword, height=10, show="headings", columns=columns_keyword)

        treeview_keyword.column("影片名字", width=210, anchor='center')  # 表示列,不显示
        treeview_keyword.column("影片评分", width=210, anchor='center')
        treeview_keyword.column("影片类型", width=100, anchor='center')
        treeview_keyword.column("评价人数", width=100, anchor='center')

        treeview_keyword.heading("影片名字", text="影片名字")  # 显示表头
        treeview_keyword.heading("影片评分", text="影片评分")
        treeview_keyword.heading("影片类型", text="影片类型")
        treeview_keyword.heading("评价人数", text="评价人数")


        #垂直滚动条
        vbar_keyword = ttk.Scrollbar(frame_r_keyword, command=treeview_keyword.yview)
        treeview_keyword.configure(yscrollcommand=vbar_keyword.set)

        treeview_keyword.pack()
        self.treeview_keyword = treeview_keyword
        vbar_keyword.pack(side=RIGHT, fill=Y)
        self.vbar_keyword = vbar_keyword

        # 框架的位置布局
        frame_l_keyword.grid(row=0, column=0, sticky=NSEW)
        frame_r_keyword.grid(row=0, column=1, sticky=NS)
        frame_root_keyword.place(x=5, y=40)
        # 输入关键字 电影搜索布局结束










        # 电影详情布局开始
        # 容器控件
        labelframe_movie_detail = LabelFrame(root, text="影片详情")
        labelframe_movie_detail.place(x=670, y=5)
        self.labelframe_movie_detail = labelframe_movie_detail


        # 框架布局，承载多个控件
        frame_left_movie_detail = Frame(labelframe_movie_detail, width=160,height=250)
        frame_left_movie_detail.grid(row=0, column=0)
        self.frame_left_movie_detail = frame_left_movie_detail


        frame_right_movie_detail = Frame(labelframe_movie_detail, width=160,height=250)
        frame_right_movie_detail.grid(row=0, column=1)
        self.frame_right_movie_detail = frame_right_movie_detail


        #影片图片
        label_img = Label(frame_left_movie_detail, text="", anchor=N)
        label_img.place(x=0,y=0) #布局
        self.label_img = label_img

        #影片名字
        ft = font.Font(size=15, weight=font.BOLD)
        label_movie_name = Label(frame_right_movie_detail, text="影片名字", fg='#FF0000', font=ft,anchor=NW)
        label_movie_name.place(x=0, y=0)
        self.label_movie_name = label_movie_name

        #影片评分
        ft_rating = font.Font(weight=font.BOLD)
        label_movie_rating = Label(frame_right_movie_detail, text="影片评价", fg='#7F00FF', font=ft_rating, anchor=NW)
        label_movie_rating.place(x=0, y=30)
        self.label_movie_rating = label_movie_rating

        #影片年代
        ft_time = font.Font(weight=font.BOLD)
        label_movie_time = Label(frame_right_movie_detail, text="影片日期", fg='#666600', font=ft_time, anchor=NW)
        label_movie_time.place(x=0, y=60)
        self.label_movie_time = label_movie_time

        #影片类型
        ft_type = font.Font(weight=font.BOLD)
        label_movie_type = Label(frame_right_movie_detail, text="影片类型", fg='#330033', font=ft_type, anchor=NW)
        label_movie_type.place(x=0, y=90)
        self.label_movie_type = label_movie_type

        #影片演员
        label_movie_actor = Label(frame_right_movie_detail, text="影片演员", wraplength=135, justify = 'left', anchor=NW)
        label_movie_actor.place(x=0, y=120)
        self.label_movie_actor = label_movie_actor
        # 电影详情布局结束




        #绑定事件
        treeview.bind('<<TreeviewSelect>>', self.show_movie_data_in_rating)  # 表格绑定选择事件
        B_0.configure(command=lambda:thread_it(self.searh_movie_in_rating)) #按钮绑定单击事件
        treeview_keyword.bind('<<TreeviewSelect>>', self.show_movie_data_in_keyword)  # 表格绑定选择事件
        B_0_keyword.configure(command=lambda:thread_it(self.searh_movie_in_keyword)) #按钮绑定单击事件


        root.mainloop()