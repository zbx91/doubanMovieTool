import urllib.request
import ssl
import json
import requests


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
    def __init__(self, typeId, movie_count, rating, vote_count):
        self.typeId = typeId
        self.movie_count = movie_count
        self.rating = rating
        self.vote_count = vote_count

    # 从排行榜中获取电影数据
    def getUrlDataInRankingList(self):
        context = ssl._create_unverified_context() #ssl
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
                      "Cookie":"bid=GOT4pCp9nDo; douban-fav-remind=1; ll=\"118281\"; _vwo_uuid_v2=D66FD66C128357F50256AF7D1640C2C4E|cfa1775f07bb9e7b103867cca686f90f; ct=y; push_noty_num=0; push_doumail_num=0; __utmv=30149280.17530; ps=y; dbcl2=\"175306983:IdbYxDP86ig\"; gr_user_id=114cc107-0ac5-4673-b200-31dd9a75055f; __yadk_uid=XB4UiG1j51gcqU0eP9Kixoh7Md13Iuh3; ck=C2_e; __utmc=30149280; __utmc=223695111; __utmz=223695111.1548048334.17.5.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utma=30149280.1293355995.1546000996.1548232182.1548236480.32; __utmz=30149280.1548236480.32.16.utmcsr=sec.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/a; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1548236776%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DamwH-XLMWrZif3MaPJ9II4CtZIM6A0xUPdB8UQKMadjqHZApcjKbViUzRtAqqYVRHkXKXw9YmL7INCYr3D4ONa%26wd%3D%26eqid%3Daafd0df100043c14000000065c4557c7%22%5D; _pk_id.100001.4cf6=a5fe3116fc29e5fa.1546939070.23.1548236776.1548232454.; __utma=223695111.1446768112.1546939070.1548232182.1548236776.21"}
        url = 'https://movie.douban.com/j/chart/top_list?type=' + str(self.typeId) + '&interval_id=100:90&action=unwatched&start=0&limit=' + str(self.movie_count)
        req = urllib.request.Request(url=url, headers=headers)
        f = urllib.request.urlopen(req, context=context)
        response=f.read()
        jsonData = json.loads(response) #转化为json数据

        list = []
        for subData in jsonData: #依次对每部电影进行操作
            if((float(subData['rating'][0]) >= float(self.rating)) and (float(subData['vote_count']) >= float(self.vote_count))):
                subList = []
                subList.append(subData['title'])
                subList.append(subData['rating'][0])
                subList.append(subData['rank'])
                subList.append(subData['vote_count'])
                list.append(subList)

        return list,jsonData


