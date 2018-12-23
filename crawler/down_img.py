from bs4 import BeautifulSoup
import threading,pymysql,time,requests,os,urllib3,re
requests.packages.urllib3.disable_warnings()
spider_url = 'http://www.moyunso.com/meinv/list_1_'
page_url_list=[]
img_url_list=[]
img_path='/static/images/'
type_id=1

def img_url():
    for i in range(1,46):
        img_path="/imgbqbvi/"
        imgurl="https://beauty.coding.ee/img"+img_path+str(i)+".jpg"
        down_img(imgurl)

def down_img(imgsrc):
    path = imgsrc.split("/")[-2]
    isdata = os.path.exists(".." + img_path + path)
    if isdata == False:
        os.makedirs(".." + img_path + path)
    with open(".." + img_path + path + "/" + imgsrc.split("/")[-1], "wb")as f:
        f.write(requests.get(imgsrc, verify=False).content)
        print(".." + img_path + path + "/" + imgsrc.split("/")[-1]+"下载完成")

img_url()