from uiObject import uiObject
from selenium import webdriver

# main入口
if __name__ == '__main__':


    # 使用selenium和phantomjs抓取js动态渲染的界面数据
    # selenium:Web自动化程序工具,安装方式pip install selenium==2.48.0
    # 注意selenium必须安装2.x版本,否则报错,新版selenium已经放弃phantomjs
    # phantomjs:一款无界面的浏览器内核，下载方式http://phantomjs.org/download.html
    # 此方式优点:可爬取js动态渲染后的数据,缺点:速度较低,效率一般

    url = "https://movie.douban.com/subject_search?search_text=%E9%80%9F%E5%BA%A6%E4%B8%8E%E6%BF%80%E6%83%85&cat=1002"
    driver = webdriver.PhantomJS(executable_path='phantomjs-2.1.1-macosx/bin/phantomjs') #里面的路径即为phantomjs.exe的路径
    driver.get(url) #get方式获取返回数据

    dr = driver.find_elements_by_xpath("//div[@class='item-root']") # 获取class为item-root的DIV(因为有多个结果)
    for son in dr:
        url = son.find_elements_by_xpath(".//a") #获取第一个a标签的url(因为有多个结果)
        if (url): print(url[0].get_attribute("href"))

        img_url = url[0].find_elements_by_xpath(".//img") #获取影片海报图片地址
        if (img_url): print(img_url[0].get_attribute("src"))

        title = son.find_elements_by_xpath(".//div[@class='title']") #获取标题
        if (title): print(title[0].text)

        rating = son.find_elements_by_xpath(".//span[@class='rating_nums']") #获取评分
        if(rating):print(rating[0].text)

        vote = son.find_elements_by_xpath(".//span[@class='pl']") #获取数量
        if(vote):print(vote[0].text)

        type = son.find_elements_by_xpath(".//div[@class='meta abstract']") #获取类型
        if(type):print(type[0].text)

        actors = son.find_elements_by_xpath(".//div[@class='meta abstract_2']") #获取演员
        if(actors):print(actors[0].text)

        print('\n\n')


    ui = uiObject()
    ui.ui_process()