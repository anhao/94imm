from bs4 import BeautifulSoup
import threading,pymysql,time,requests,os,urllib3
requests.packages.urllib3.disable_warnings()

class Spider():
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/65.0.3325.181 Safari/537.36',
        'Referer': "https://www.mzitu.com"
    }
    page_url_list = []
    img_url_list = []
    rlock = threading.RLock()
    s=requests.session()

    def __init__(self,page_number=10,img_path='imgdir',thread_number=5):
        self.spider_url = 'https://www.mzitu.com/xinggan/page/'
        self.page_number = int(page_number)
        self.img_path = img_path
        self.thread_num = thread_number

    def get_url(self):
        for i in range(1, self.page_number + 1):
            # print(requests.get(baseurl+str(i)).text)
            page_base_url = BeautifulSoup(self.s.get(self.spider_url+ str(i)).text, "html.parser").find("div",
                                                                                            class_="postlist").find_all(
                "li")
            for page_url in page_base_url:
                url = page_url.find("a").get("href")
                self.page_url_list.append(url)
            i = i + 1

    def get_img_url(self):
        db = pymysql.connect("192.168.1.67", "silumz", "123456", "silumz")
        cursor = db.cursor()
        for img_base_url in self.page_url_list:
            tagidlist = []
            img_soup = BeautifulSoup(self.s.get(img_base_url).text, "html.parser")
            img_num = img_soup.find("div", class_="pagenavi").text.split("…")[-1][0:-5]
            img_url = img_soup.find("div", class_="main-image").find("img").get("src").split("/")[0:-1]
            img_surl = "/".join(img_url)
            title = img_soup.find("h2", class_="main-title").text
            isExists = cursor.execute("SELECT * FROM images_page WHERE title =" + "'" + title + "'" + " limit 1;")
            tag_list = img_soup.find("div", class_="main-tags").find("a").text
            if isExists == 1:
                print("已存在")
            else:
                for tag in tag_list:
                    sqltag = "SELECT * FROM images_tag WHERE tag =" + "'" + tag + "'" + " limit 1;"
                    isExiststag = cursor.execute(sqltag)
                    if isExiststag != 1:
                        cursor.execute("INSERT INTO images_tag (tag) VALUES (%s)", tag)
                    cursor.execute("SELECT id FROM images_tag WHERE tag =" + "'" + tag + "'")
                    for id in cursor.fetchall():
                        tagidlist.append(id[0])
                p = (title, str(tagidlist), time.strftime('%Y-%m-%d', time.localtime(time.time())), "1", "1")
                cursor.execute("INSERT INTO images_page (title,tagid,sendtime,typeid,firstimg) VALUES (%s,%s,%s,%s,%s)",
                               p)
                pageid = cursor.lastrowid
                i = 1
                for i in range(1, int(img_num)):
                    temp_url = img_soup.find("div", class_="main-image").find("img").get("src").split("/")
                    path = temp_url[-1][0:3]
                    new_url = img_surl + "/" + path + str("%02d" % i) + ".jpg"
                    img_src = temp_url[-3] + "/" + temp_url[-2] + "/" + temp_url[-1]
                    imgp = pageid, self.img_path + img_src
                    cursor.execute("INSERT INTO images_image (pageid,imageurl) VALUES (%s,%s)", imgp)
                    if i == 1:
                        cursor.execute(
                            "UPDATE images_page SET firstimg = " + "'" + self.img_path + img_src + "'" + " WHERE title=" + "'" + title + "'")
                    self.img_url_list.append(new_url)
                    i = i + 1
        db.close()

    def down_img(self,imgsrc):
        path = imgsrc.split("/")[-3] + "/" + imgsrc.split("/")[-2]
        isdata = os.path.exists("../" + self.img_path + path)
        if isdata == False:
            os.makedirs("../" + self.img_path + path)
        with open("../" + self.img_path + path + "/" + imgsrc.split("/")[-1], "wb")as f:
            print("下载图片：" + self.img_path + path)
            f.write(requests.get(imgsrc, headers=self.headers, verify=False).content)

    def down_url(self):
        while True:
            Spider.rlock.acquire()
            if len(Spider.img_url_list) == 0:
                Spider.rlock.release()
                break
            else:
                img_url = Spider.img_url_list.pop()
                Spider.rlock.release()
                try:
                    self.down_img(img_url)
                except Exception as e:
                    pass


    def run(self):
        # 启动thread_num个进程来爬去具体的img url 链接
        # for th in range(self.thread_num):
        #     add_pic_t = threading.Thread(target=self.get_img_url)
        #     add_pic_t.start()

        # 启动thread_num个来下载图片
        for img_th in range(self.thread_num):
            download_t = threading.Thread(target=self.down_url)
            download_t.start()


if __name__ == '__main__':
    spider = Spider(page_number=1, img_path='/static/images/', thread_number=10)
    spider.get_url()
    spider.get_img_url()
    spider.run()