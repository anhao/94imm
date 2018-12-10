from bs4 import BeautifulSoup
import requests,pymysql,time,os,threading

def getUrl():
    imgpath = "../static/images/"
    sqlpath="/static/images/"
    db = pymysql.connect("127.0.0.1", "root", "fendou2009", "silumz")
    cursor = db.cursor()
    for i in range(1,589):
        page=requests.get("https://fenmimi.com/page/"+str(i)+"/").text
        soup=BeautifulSoup(page,"html.parser").find_all("div",class_="post-list-item")
        # print(BeautifulSoup(page,"html.parser"))
        for itme in soup:
            taglist = []
            tagidlist = []
            title=itme.find("div",class_="item-title").text
            cover_arr=itme.find("div",class_="item-thumb bg-deepgrey")["style"]
            cover=cover_arr[cover_arr.find("url(")+4:cover_arr.find(");")]
            sql = "SELECT * FROM images_page WHERE title =" + "'"+title+ "'"+ " limit 1;"
            isExists = cursor.execute(sql)
            if isExists== 1:
                print("已采集")
            else:
                link=itme.find("div",class_="item-title").find("a").get("href")
                imgpage=requests.get(link).text
                imgsoup=BeautifulSoup(imgpage,"html.parser").find_all("div",class_="post-content")
                for img_arr in imgsoup:
                    for tags in img_arr.find_all("p",class_="post-tags"):

                        for tag_a in tags.find_all("a"):
                            tag = tag_a.text
                            taglist.append(tag)
                            sqltag = "SELECT * FROM images_tag WHERE tag ="+ "'"+tag+ "'"+ " limit 1;"
                            isExiststag = cursor.execute(sqltag)
                            if isExiststag !=1:
                                cursor.execute("INSERT INTO images_tag (tag) VALUES (%s)", tag)
                            cursor.execute("SELECT id FROM images_tag WHERE tag =" + "'"+tag+ "'")
                            for id in cursor.fetchall():
                                tagidlist.append(id[0])

                    p = (title, str(tagidlist),time.strftime('%Y-%m-%d',time.localtime(time.time())),"1","1")
                    cursor.execute("INSERT INTO images_page (title,tagid,sendtime,typeid,firstimg) VALUES (%s,%s,%s,%s,%s)", p)
                    cursor.execute("SELECT * FROM images_page WHERE title =" + "'"+title+ "'"+ " limit 1;")
                    plist=cursor.fetchall()
                    for pid in plist:
                        pageid=pid[0]
                    imgs=img_arr.find_all("img")
                    for img in imgs:
                        imgsrc=img.get("src")
                        path=imgsrc.split("/")[-2]+"/"+imgsrc.split("/")[-1]
                        if imgsrc==cover:
                            imgp = pageid, sqlpath + path, True
                            cursor.execute("INSERT INTO images_image (pageid,imageurl,is_cover) VALUES (%s,%s,%s)", imgp)
                            cursor.execute(
                                "SELECT id FROM images_image WHERE imageurl =" + "'" + sqlpath+path + "'" + " limit 1;")
                            for covers in cursor.fetchall():
                                coverid = covers[0]
                                print(covers[0])
                                cursor.execute("UPDATE images_page SET firstimg = " + str(coverid) + " WHERE title=" + "'"+title+ "'")
                        else:
                            imgp = pageid, sqlpath + path, False
                            cursor.execute("INSERT INTO images_image (pageid,imageurl,is_cover) VALUES (%s,%s,%s)", imgp)
                        isdata=os.path.exists(imgpath+imgsrc.split("/")[-2])
                        if isdata==False:
                            os.mkdir(imgpath+imgsrc.split("/")[-2])
                        with open(imgpath+path,"wb")as f:
                            f.write(requests.get(imgsrc).content)



    db.close()
                # for tag in tagsoup:
                #     print(tag.text)
            # print(itme)

getUrl()