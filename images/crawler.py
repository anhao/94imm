from bs4 import BeautifulSoup
import threading,pymysql,time,requests,os,urllib3
requests.packages.urllib3.disable_warnings()

class Spider():
    # 定义全局页面url列表
    page_url_list = []
    # 定义具体各表情图片url列表
    img_url_list = []
    # 定义rlock进程锁
    rlock = threading.RLock()

    def __init__(self,page_number=10,img_path='imgdir',thread_number=5):
        """
        :param page_number: 抓去多少个页面，默认10
        :param img_dir: 定义图片目录
        :param thread_number:默认5个线程
        """
        self.spider_url = 'https://fenmimi.com/page/'
        self.page_number = int(page_number)
        self.img_path = img_path
        self.thread_num = thread_number

    def get_url(self):
        """
        创建image目录和生产pageurl列表
        :return:
        """
        for i in range(1,self.page_number+1):
            page = requests.get(self.spider_url + str(i), verify=False).text
            soup = BeautifulSoup(page, "html.parser").find_all("div", class_="post-list-item")
            for pages in soup:
                page_url=pages.find("div",class_="item-title").find("a").get("href")
                print("添加链接："+page_url)
                self.page_url_list.append(page_url)

    def get_img_url(self):
        db = pymysql.connect("127.0.0.1", "root", "fendou2009", "silumz")
        cursor = db.cursor()
        tagidlist=[]
        taglist=[]
        print(self.page_url_list)
        for page_url in self.page_url_list:
            page = requests.get(page_url, verify=False).text
            title= BeautifulSoup(page, "html.parser").find("h1",class_="post-title").text
            p = (title, "1", time.strftime('%Y-%m-%d', time.localtime(time.time())), "1", "1")
            cursor.execute("INSERT INTO images_page (title,tagid,sendtime,typeid,firstimg) VALUES (%s,%s,%s,%s,%s)", p)
            soup = BeautifulSoup(page, "html.parser").find_all("div", class_="post-content")
            for img_arr in soup:
                for tags in img_arr.find_all("p", class_="post-tags"):
                    for tag_a in tags.find_all("a"):
                        tag = tag_a.text
                        taglist.append(tag)
                        sqltag = "SELECT * FROM images_tag WHERE tag =" + "'" + tag + "'" + " limit 1;"
                        isExiststag = cursor.execute(sqltag)
                        if isExiststag != 1:
                            cursor.execute("INSERT INTO images_tag (tag) VALUES (%s)", tag)
                        cursor.execute("SELECT id FROM images_tag WHERE tag =" + "'" + tag + "'")
                        for id in cursor.fetchall():
                            tagidlist.append(id[0])
                cursor.execute(
                    "UPDATE images_page SET tagid = " + "'" + str(tagidlist) + "'" + " WHERE title=" + "'" + title + "'")
                cursor.execute("SELECT * FROM images_page WHERE title =" + "'" + title + "'" + " limit 1;")
                plist = cursor.fetchall()
                for pid in plist:
                    pageid = pid[0]
                imgs = img_arr.find_all("img")
                is_cover=1
                for img in imgs:
                    imgsrc = img.get("src")
                    self.img_url_list.append(imgsrc)
                    path = imgsrc.split("/")[-2] + "/" + imgsrc.split("/")[-1]
                    imgp = pageid, self.img_path + path
                    cursor.execute("INSERT INTO images_image (pageid,imageurl) VALUES (%s,%s)", imgp)
                    if is_cover==1:
                        cursor.execute("UPDATE images_page SET firstimg = " + "'" +self.img_path + path + "'" + " WHERE title=" + "'" + title + "'")
                    is_cover += 1
        db.close()


    def down_img(self):
        Spider.rlock.acquire()
        for imgsrc in self.img_url_list:
            path = imgsrc.split("/")[-2] + "/" + imgsrc.split("/")[-1]
            isdata = os.path.exists("../"+self.img_path + imgsrc.split("/")[-2])
            if isdata == False:
                os.mkdir("../"+self.img_path + imgsrc.split("/")[-2])
            with open("../"+self.img_path + path, "wb")as f:
                print("下载图片："+self.img_path + path)
                f.write(requests.get(imgsrc, verify=False).content)
        Spider.rlock.release()


    def run(self):
        # 启动thread_num个进程来爬去具体的img url 链接
        # for th in range(self.thread_num):
        #     add_pic_t = threading.Thread(target=self.get_img_url)
        #     add_pic_t.start()

        # 启动thread_num个来下载图片
        for img_th in range(self.thread_num):
            download_t = threading.Thread(target=self.down_img)
            download_t.start()


if __name__ == '__main__':
    spider = Spider(page_number=590, img_path='/static/images/', thread_number=10)
    spider.get_url()
    spider.get_img_url()
    spider.run()