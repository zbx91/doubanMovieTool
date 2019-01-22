import urllib.request
import ssl
import json
import ui


class getMovieInRankingList:
    
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



    # 从排行榜中获取电影数据
    # typeId 电影类型, movie_count 欲获取的该电影类型的数量, rating 电影的评分, vote_count 电影的评价人数
    def getUrlDataInRankingList(self, typeId, movie_count, rating, vote_count):
        context = ssl._create_unverified_context() #ssl
        f = urllib.request.urlopen('https://movie.douban.com/j/chart/top_list?type=' + str(typeId) + '&interval_id=100:90&action=unwatched&start=0&limit=' + str(movie_count), context=context)
        response=f.read()
        jsonData = json.loads(response) #转化为json数据

        list = []
        for subData in jsonData: #依次对每部电影进行操作
            if((float(subData['rating'][0]) >= float(rating)) and (float(subData['vote_count']) >= float(vote_count))):
                subList = []
                subList.append(subData['title'])
                subList.append(subData['rating'][0])
                subList.append(subData['rank'])
                subList.append(subData['vote_count'])
                list.append(subList)

        return list


