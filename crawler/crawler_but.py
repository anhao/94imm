#!/usr/bin/python3

from bs4 import BeautifulSoup
import threading,pymysql,time,requests,os,urllib3,re
requests.packages.urllib3.disable_warnings()

class Spider():
    page_url_list = []
    img_url_list = []
    rlock = threading.RLock()
    s=requests.session()

    def __init__(self,page_number=10,img_path='imgdir',thread_number=5,type='meitui',type_id=1):
        self.spider_url = 'https://beauty.coding.ee/'
        self.page_number = int(page_number)
        self.img_path = img_path
        self.thread_num = thread_number
        self.type_id = type_id
        self.type=type

    def get_url(self):
        db = pymysql.connect("127.0.0.1", "root", "fendou2009", "silumz")
        cursor = db.cursor()
        for i in range(1, self.page_number+1):
            if i == 1:
                page = requests.get(self.spider_url + self.type, verify=False).text

            data = {
                "categorySlug": self.type,
                "currentPage": i
            }
            page = requests.post(self.spider_url, data=data, verify=False).text
            soup = BeautifulSoup(page, "html.parser").find("div", class_="main").find_all("dt")
            for pages in soup:
                title = pages.find("img").get("alt")
                isExists = cursor.execute("SELECT title FROM images_page WHERE title =" + "'" + title + "'" + " limit 1;")
                if isExists != 0:
                    print("已采集："+title)
				else:
					page_url = pages.find("a").get("href")
					url = self.spider_url + page_url
					self.page_url_list.append(url)
        db.close()

    def get_img_url(self):
        db = pymysql.connect("127.0.0.1", "root", "fendou2009", "silumz")
        cursor = db.cursor()
        for page_url in self.page_url_list:
            tagidlist = []
            page = requests.get(page_url, verify=False).text
            soup = BeautifulSoup(page, "html.parser")
            img = soup.find("div", id="picbox").find("img").get("src")
            title=soup.find("div",class_="title").find("h2").text
            print("添加图片："+title)
            taglist = re.findall('<meta name="keywords" content="(.*?)" />', page)
            for tag in taglist:
                sqltag = "SELECT * FROM images_tag WHERE tag =" + "'" + tag + "'" + " limit 1;"
                isExiststag = cursor.execute(sqltag)
                if isExiststag == 0:
                    cursor.execute("INSERT INTO images_tag (tag) VALUES (%s)", tag)
                cursor.execute("SELECT id FROM images_tag WHERE tag =" + "'" + tag + "'")
                for id in cursor.fetchall():
                    tagidlist.append(id[0])
            p = (title, str(tagidlist), time.strftime('%Y-%m-%d', time.localtime(time.time())), self.type_id, "1")
            cursor.execute("INSERT INTO images_page (title,tagid,sendtime,typeid,firstimg) VALUES (%s,%s,%s,%s,%s)", p)
            pageid = cursor.lastrowid
            img_base_url = "/".join(img.split("/")[0:-1]) + "/"
            img_num = soup.find("div", id="page").text.split(" ")[-2]
            i = 1
            for i in range(1, int(img_num) + 1):
                url = img_base_url + str(i) + ".jpg"
                img_loc_path = self.img_path + "/".join(url.split("/")[-2:])
                if i == 1:
                    cursor.execute(
                        "UPDATE images_page SET firstimg = " + "'" + img_loc_path + "'" + " WHERE title=" + "'" + title + "'")
                i = i + 1
                imgp = pageid, img_loc_path
                cursor.execute("INSERT INTO images_image (pageid,imageurl) VALUES (%s,%s)", imgp)
                i = i + 1
                self.img_url_list.append(url)
        db.close()

    def down_img(self,imgsrc):
        path = imgsrc.split("/")[-2] + "/" + imgsrc.split("/")[-1]
        isdata = os.path.exists("../" + self.img_path + imgsrc.split("/")[-2])
        if isdata == False:
            os.mkdir("../" + self.img_path + imgsrc.split("/")[-2])
        with open("../" + self.img_path + path, "wb")as f:
            print("下载图片："+self.img_path + path)
            f.write(requests.get(imgsrc, verify=False).content)

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
    for i in [{"page":1,"type":"meitui","type_id":2},{"page":1,"type":"xinggan","type_id":1},{"page":1,"type":"qingchun","type_id":3}]:
        spider = Spider(page_number=i.get("page"), img_path='/static/images/', thread_number=10,type=i.get("type"),type_id=i.get("type_id"))
        spider.get_url()
        spider.get_img_url()
        spider.run()
