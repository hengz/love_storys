import itchat
import time
import datetime
import requests
import re
import os
from lxml import etree
from selenium import webdriver

love_word_path = "love_word.txt"
pic_path = os.getcwd() + '\\img\\'

def crawl_love_words():
    print("正在抓取情话...")
    browser = webdriver.PhantomJS()
    url = "http://www.binzz.com/yulu2/3588.html"
    browser.get(url)
    html = browser.page_source
    Selector = etree.HTML(html)
    love_words_xpath_str = "//div[@id='content']/p/text()"
    love_words = Selector.xpath(love_words_xpath_str)
    for i in love_words:
        word = i.strip("\n\t\u3000\u3000").strip()
        with open(love_word_path, "a") as file:
            file.write(word + "\n")
    print("情话抓取完成")

def crawl_love_image():
    print("正在抓取我爱你图片...")
    for i in range(1, 22):
        url = "http://tieba.baidu.com/p/3108805355?pn={}".format(i)
        response = requests.get(url)
        html = response.text
        pattern = re.compile(r'<div.*?class="d_post_content j_d_post_content.*?">.*?<img class="BDE_Image" src="(.*?)".*?>.*?</div>', re.S)
        image_url = re.findall(pattern, html)
        for j, data in enumerate(image_url):
            pics = requests.get(data)
            mkdir(pic_path)
            fq = open(pic_path + '\\' + str(i) + "_" + str(j) + '.jpg', 'wb')  # 下载图片，并保存和命名
            fq.write(pics.content)
            fq.close()
    print("图片抓取完成")

def mkdir(path):
    folder = os.path.exists(path)

    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print("---  new folder...  ---")
        print("---  OK  ---")
    else:
        print("正在保存图片中...")

def send_news():

    # 计算相恋天数
    inLoveDate = datetime.datetime(2017, 11, 11) # 相恋的时间
    todayDate = datetime.datetime.today()
    inLoveDays = (todayDate - inLoveDate).days

    # 获取情话
    file_path = os.getcwd() + '\\' + love_word_path
    with open(file_path) as file:
        love_word = file.readlines()[43].split('：')[1]

    itchat.auto_login(hotReload=True) # 热启动，不需要多次扫码登录
    my_friend = itchat.search_friends(name=u'can')
    girlfriend = my_friend[0]["UserName"]
    print(girlfriend)
    message = """
    亲爱的{}:

    早上好，今天是你和 恒 相恋的第 {} 天~

    今天他想对你说的话是：

    {}

    最后也是最重要的！
    """.format("灿", str(inLoveDays), love_word)
    itchat.send(message, toUserName=girlfriend)

    files = os.listdir(pic_path)
    file = files[42]
    love_image_file = pic_path + file
    try:
        itchat.send_image(love_image_file, toUserName=girlfriend)
    except Exception as e:
        print(e)

def main():
    with open(love_word_path, 'r') as file:
        if file.read():
            print("exit")
        else:
            crawl_Love_words()

    pic_path = os.getcwd() + '\img'
    foler = os.path.exists(pic_path)

    if not foler:
        crawl_love_image()
    else:
        print("情话图片已存在")
    send_news()

if __name__ == '__main__':
    while True:
        curr_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        love_time = curr_time.split(" ")[1]
        if love_time == "23:57:00":
            main()
            time.sleep(60)
        else:
            print("爱你的每一天都是如此美妙，现在时间：" + love_time)