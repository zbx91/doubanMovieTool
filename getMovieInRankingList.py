import urllib.request
import urllib.parse
import ssl
import json
from selenium import webdriver


movieData = ' [' \
            '{"title":"纪录片", "type":"1", "interval_id":"100:90"}, ' \
            ' {"title":"传记", "type":"2", "interval_id":"100:90"}, ' \
            ' {"title":"犯罪", "type":"3", "interval_id":"100:90"}, ' \
            ' {"title":"历史", "type":"4", "interval_id":"100:90"}, ' \
            ' {"title":"动作", "type":"5", "interval_id":"100:90"}, ' \
            ' {"title":"情色", "type":"6", "interval_id":"100:90"}, ' \
            ' {"title":"歌舞", "type":"7", "interval_id":"100:90"}, ' \
            ' {"title":"儿童", "type":"8", "interval_id":"100:90"}, ' \
            ' {"title":"悬疑", "type":"10", "interval_id":"100:90"}, ' \
            ' {"title":"剧情", "type":"11", "interval_id":"100:90"}, ' \
            ' {"title":"灾难", "type":"12", "interval_id":"100:90"}, ' \
            ' {"title":"爱情", "type":"13", "interval_id":"100:90"}, ' \
            ' {"title":"音乐", "type":"14", "interval_id":"100:90"}, ' \
            ' {"title":"冒险", "type":"15", "interval_id":"100:90"}, ' \
            ' {"title":"奇幻", "type":"16", "interval_id":"100:90"}, ' \
            ' {"title":"科幻", "type":"17", "interval_id":"100:90"}, ' \
            ' {"title":"运动", "type":"18", "interval_id":"100:90"}, ' \
            ' {"title":"惊悚", "type":"19", "interval_id":"100:90"}, ' \
            ' {"title":"恐怖", "type":"20", "interval_id":"100:90"}, ' \
            ' {"title":"战争", "type":"22", "interval_id":"100:90"}, ' \
            ' {"title":"短片", "type":"23", "interval_id":"100:90"}, ' \
            ' {"title":"喜剧", "type":"24", "interval_id":"100:90"}, ' \
            ' {"title":"动画", "type":"25", "interval_id":"100:90"}, ' \
            ' {"title":"同性", "type":"26", "interval_id":"100:90"}, ' \
            ' {"title":"西部", "type":"27", "interval_id":"100:90"}, ' \
            ' {"title":"家庭", "type":"28", "interval_id":"100:90"}, ' \
            ' {"title":"武侠", "type":"29", "interval_id":"100:90"}, ' \
            ' {"title":"古装", "type":"30", "interval_id":"100:90"}, ' \
            ' {"title":"黑色电影", "type":"31", "interval_id":"100:90"}' \
            ']'


class getMovieInRankingList:
    

    # typeId 电影类型, movie_count 欲获取的该电影类型的数量, rating 电影的评分, vote_count 电影的评价人数
    def __init__(self):
        pass

    # 从排行榜中获取电影数据
    def get_url_data_in_ranking_list(self, typeId, movie_count, rating, vote_count):
        context = ssl._create_unverified_context() #ssl
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
                   # "Cookie":"bid=GOT4pCp9nDo; douban-fav-remind=1; ll=\"118281\"; _vwo_uuid_v2=D66FD66C128357F50256AF7D1640C2C4E|cfa1775f07bb9e7b103867cca686f90f; ct=y; push_noty_num=0; push_doumail_num=0; __utmv=30149280.17530; ps=y; gr_user_id=114cc107-0ac5-4673-b200-31dd9a75055f; __yadk_uid=XB4UiG1j51gcqU0eP9Kixoh7Md13Iuh3; __utmz=30149280.1548260586.36.17.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmz=223695111.1548260586.24.6.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmc=30149280; __utmc=223695111; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1548695792%2C%22https%3A%2F%2Fwww.douban.com%2Fsearch%3Fq%3D%25E9%2580%259F%25E5%25BA%25A6%25E4%25B8%258E%25E6%25BF%2580%25E6%2583%2585%22%5D; _pk_ses.100001.4cf6=*; ap_v=0,6.0; __utma=30149280.1293355995.1546000996.1548664862.1548696797.44; __utmb=30149280.0.10.1548696797; __utma=223695111.1446768112.1546939070.1548664862.1548696797.29; __utmb=223695111.0.10.1548696797; dbcl2=\"175306983:wFDRFDTa1iY\"; ck=qgH3; _pk_id.100001.4cf6=a5fe3116fc29e5fa.1546939070.41.1548698529.1548666571."
                  }
        url = 'https://movie.douban.com/j/chart/top_list?type=' + str(typeId) + '&interval_id=100:90&action=unwatched&start=0&limit=' + str(movie_count)
        req = urllib.request.Request(url=url, headers=headers)
        f = urllib.request.urlopen(req, context=context)
        response=f.read()
        jsonData = json.loads(response) #将json转为python对象

        list = []
        for subData in jsonData: #依次对每部电影进行操作
            if((float(subData['rating'][0]) >= float(rating)) and (float(subData['vote_count']) >= float(vote_count))):
                subList = []
                subList.append(subData['title'])
                subList.append(subData['rating'][0])
                subList.append(subData['rank'])
                subList.append(subData['vote_count'])
                list.append(subList)

        return list,jsonData



    # 从关键字获取电影数据
    def get_url_data_in_keyWord(self,key_word):

        # 使用selenium和phantomjs抓取js动态渲染的界面数据
        # selenium:Web自动化程序工具,安装方式pip install selenium==2.48.0
        # 注意selenium必须安装2.x版本,否则报错,新版selenium已经放弃phantomjs
        # phantomjs:一款无界面的浏览器内核，下载方式http://phantomjs.org/download.html
        # 此方式优点:可爬取js动态渲染后的数据,缺点:速度较低,效率一般

        service_args = []
        service_args.append('--load-images=no') # 关闭图片加载
        service_args.append('--disk-cache=yes') # 开启缓存
        service_args.append('--ignore-ssl-errors=true') # 忽略https错误
        driver = webdriver.PhantomJS(executable_path='phantomjs-2.1.1-macosx/bin/phantomjs', service_args=service_args)  # 里面的路径即为phantomjs.exe的路径
        driver.get('https://movie.douban.com/subject_search?search_text=' + urllib.parse.quote(key_word) + '&cat=1002')  # get方式获取返回数据

        dr = driver.find_elements_by_xpath("//div[@class='item-root']")  # 获取class为item-root的DIV(因为有多个结果)
        jsonData = []
        list = []
        for son in dr:
            movieData = {'rating': ['', 'null'], 'cover_url': '', 'types': '', 'title': '', 'url': '', 'release_date': '', 'vote_count': '', 'actors': ''}
            subList = ['','','','']

            url_element = son.find_elements_by_xpath(".//a")  # 获取第一个a标签的url(因为有多个结果)
            if (url_element):
                movieData['url'] = (url_element[0].get_attribute("href"))

            img_url_element = url_element[0].find_elements_by_xpath(".//img")  # 获取影片海报图片地址
            if (img_url_element):
                movieData['cover_url'] = (img_url_element[0].get_attribute("src"))

            title_element = son.find_elements_by_xpath(".//div[@class='title']")  # 获取标题
            if (title_element):
                temp_title = (title_element[0].text)
                movieData['title'] = (temp_title.split('('))[0]
                movieData['release_date'] = temp_title[temp_title.find('(')+1:temp_title.find(')')]
                subList[0] = movieData['title']

            rating_element = son.find_elements_by_xpath(".//span[@class='rating_nums']")  # 获取评分
            if (rating_element):
                movieData['rating'][0] = (rating_element[0].text)
                subList[1] = movieData['rating'][0]

            vote_element = son.find_elements_by_xpath(".//span[@class='pl']")  # 获取数量
            if (vote_element):
                movieData['vote_count'] = (vote_element[0].text).replace('(','').replace(')','').replace('人评价','')
                subList[3] = movieData['vote_count']

            type_element = son.find_elements_by_xpath(".//div[@class='meta abstract']")  # 获取类型
            if (type_element):
                movieData['types'] = (type_element[0].text)
                subList[2] = movieData['types']

            actors_element = son.find_elements_by_xpath(".//div[@class='meta abstract_2']")  # 获取演员
            if (actors_element):
                movieData['actors'] = (actors_element[0].text)

            jsonData.append(movieData)
            list.append(subList)


        driver.quit()
        return list,jsonData





